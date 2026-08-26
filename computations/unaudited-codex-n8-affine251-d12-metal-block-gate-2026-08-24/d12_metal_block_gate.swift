import CryptoKit
import Darwin
import Foundation
import Metal

let expectedMatrixSHA = "30ff854947b1b0f76ff01b07297b6aef8797ae44c0fca3b1b11ffae60e0d0439"
let expectedVectorSHA = "dd74d7392a005fb9c7726d9a0cc5c86e5b16d987bcb707d1c3a0f90e6e4d9e40"
let expectedCheckpointSHA = "761804372a3f7e12b1915dd2718f7f69ef00b799dc6f90cd083b2fa7d2fc3c88"
let primePlus: UInt32 = 1_073_741_827
let primeMinus: UInt32 = 1_073_741_789
let mask30: UInt64 = (1 << 30) - 1
let hardWallSeconds = 180.0
let stopSchedulingSeconds = 170.0
let hardRSSBytes: Int64 = 6 * 1024 * 1024 * 1024

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data("FAIL: \(message)\n".utf8))
    exit(2)
}

func require(_ condition: @autoclosure () -> Bool, _ message: String) {
    if !condition() { fail(message) }
}

func argument(_ name: String) -> String {
    let args = CommandLine.arguments
    guard let index = args.firstIndex(of: name), index + 1 < args.count else {
        fail("missing \(name)")
    }
    return args[index + 1]
}

func u32(_ data: Data, _ offset: Int) -> UInt32 {
    data.withUnsafeBytes { UInt32(littleEndian: $0.loadUnaligned(fromByteOffset: offset, as: UInt32.self)) }
}

func u64(_ data: Data, _ offset: Int) -> UInt64 {
    data.withUnsafeBytes { UInt64(littleEndian: $0.loadUnaligned(fromByteOffset: offset, as: UInt64.self)) }
}

func sha256(_ data: Data) -> String {
    SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
}

func sha256File(_ path: String) -> String {
    sha256(try! Data(contentsOf: URL(fileURLWithPath: path), options: .mappedIfSafe))
}

func sha256Array<T>(_ values: [T]) -> String {
    var hash = SHA256()
    values.withUnsafeBytes { hash.update(bufferPointer: $0) }
    return hash.finalize().map { String(format: "%02x", $0) }.joined()
}

func seconds(_ start: ContinuousClock.Instant, _ end: ContinuousClock.Instant) -> Double {
    let duration = start.duration(to: end)
    return Double(duration.components.seconds) + Double(duration.components.attoseconds) / 1.0e18
}

func loadArray<T>(_ data: Data, offset: Int, count: Int, as: T.Type) -> [T] {
    let byteCount = count * MemoryLayout<T>.stride
    require(offset >= 0 && byteCount >= 0 && offset + byteCount <= data.count,
            "matrix section outside file")
    return Array<T>(unsafeUninitializedCapacity: count) { buffer, initialized in
        let raw = UnsafeMutableRawBufferPointer(buffer)
        data.copyBytes(to: raw, from: offset..<(offset + byteCount))
        initialized = count
    }
}

@inline(__always)
func productMod(_ left: UInt32, _ right: UInt32, _ kind: UInt32) -> UInt32 {
    let product = UInt64(left) * UInt64(right)
    if kind == 0 {
        var reduced = Int64(product & mask30) - 3 * Int64(product >> 30)
        if reduced < 0 { reduced += Int64(primePlus) }
        if reduced < 0 { reduced += Int64(primePlus) }
        if reduced < 0 { reduced += Int64(primePlus) }
        if reduced >= Int64(primePlus) { reduced -= Int64(primePlus) }
        return UInt32(reduced)
    }
    var reduced = (product & mask30) + 35 * (product >> 30)
    reduced = (reduced & mask30) + 35 * (reduced >> 30)
    if reduced >= UInt64(primeMinus) { reduced -= UInt64(primeMinus) }
    if reduced >= UInt64(primeMinus) { reduced -= UInt64(primeMinus) }
    return UInt32(reduced)
}

@inline(__always)
func residue(_ coefficient: Int32, _ prime: UInt32) -> UInt32 {
    coefficient >= 0 ? UInt32(coefficient) : prime - UInt32(-Int64(coefficient))
}

struct CandidateRecord {
    let dense: UInt32
    let value: UInt32
    let row: Data
}

struct Matrix {
    let rows: Int
    let columns: Int
    let nnz: Int
    let inputSHA: String
    let cscPointers: [UInt32]
    let cscRows: [UInt32]
    let cscValues: [Int32]
    let csrPointers: [UInt32]
    let csrColumns: [UInt32]
    let csrValues: [Int32]
    let candidate: [CandidateRecord]
}

func loadMatrix(_ path: String) -> Matrix {
    let data = try! Data(contentsOf: URL(fileURLWithPath: path), options: .mappedIfSafe)
    let inputSHA = sha256(data)
    require(inputSHA == expectedMatrixSHA, "unfrozen matrix SHA-256")
    require(data.count >= 256, "short matrix")
    require(String(data: data[0..<11], encoding: .ascii) == "D12CSRCSCV1", "matrix magic")
    require(u32(data, 16) == 1 && u32(data, 20) == primePlus, "matrix version/prime")
    let rows = Int(u64(data, 24))
    let columns = Int(u64(data, 32))
    let nnz = Int(u64(data, 40))
    let candidateSupport = Int(u64(data, 48))
    let candidatePresent = Int(u64(data, 56))
    require((rows, columns, nnz) == (14_814_562, 222_676, 22_539_257), "matrix census")
    require(candidateSupport == 315 && candidatePresent == 315, "candidate census")
    require(u64(data, 64) == 478_445_989 && u64(data, 72) == 3_346_799,
            "source byte census")
    require(u64(data, 80) == 9_218_588_987_274_412_661 && u64(data, 96) == 635,
            "provider/round census")
    let sourceSHA = data[104..<136].map { String(format: "%02x", $0) }.joined()
    let checkpointSHA = data[136..<168].map { String(format: "%02x", $0) }.joined()
    require(sourceSHA == expectedVectorSHA && checkpointSHA == expectedCheckpointSHA,
            "source evidence pins")
    require(u64(data, 168) == 256 && u64(data, 232) == UInt64(data.count), "header/file bytes")
    let offsets = stride(from: 176, through: 224, by: 8).map { Int(u64(data, $0)) }
    require(offsets == offsets.sorted() && offsets[0] == 256, "matrix section offsets")
    let cscPointers = loadArray(data, offset: offsets[0], count: columns + 1, as: UInt32.self)
    let cscRows = loadArray(data, offset: offsets[1], count: nnz, as: UInt32.self)
    let cscValues = loadArray(data, offset: offsets[2], count: nnz, as: Int32.self)
    let csrPointers = loadArray(data, offset: offsets[3], count: rows + 1, as: UInt32.self)
    let csrColumns = loadArray(data, offset: offsets[4], count: nnz, as: UInt32.self)
    let csrValues = loadArray(data, offset: offsets[5], count: nnz, as: Int32.self)
    require(cscPointers.first == 0 && cscPointers.last == UInt32(nnz), "CSC endpoints")
    require(csrPointers.first == 0 && csrPointers.last == UInt32(nnz), "CSR endpoints")
    require(zip(cscPointers, cscPointers.dropFirst()).allSatisfy { $0 <= $1 }, "CSC pointers")
    require(zip(csrPointers, csrPointers.dropFirst()).allSatisfy { $0 <= $1 }, "CSR pointers")
    require(cscRows.allSatisfy { $0 < UInt32(rows) }, "CSC row index")
    require(csrColumns.allSatisfy { $0 < UInt32(columns) }, "CSR column index")
    require(cscValues.allSatisfy { $0 != 0 && abs(Int64($0)) <= 1440 }, "CSC coefficient")
    require(csrValues.allSatisfy { $0 != 0 && abs(Int64($0)) <= 1440 }, "CSR coefficient")
    var candidate = [CandidateRecord]()
    var previousRow: Data? = nil
    var denseSeen = Set<UInt32>()
    for index in 0..<candidateSupport {
        let base = offsets[6] + 24 * index
        let dense = u32(data, base)
        let value = u32(data, base + 4)
        require(dense < UInt32(rows) && value > 0 && value < primePlus, "candidate entry")
        require(data[base + 8] == 12 && data[base + 21..<base + 24].allSatisfy { $0 == 0 },
                "candidate provenance encoding")
        let row = Data(data[base + 9..<base + 21])
        require(previousRow == nil || previousRow!.lexicographicallyPrecedes(row),
                "candidate provenance order")
        require(denseSeen.insert(dense).inserted, "duplicate candidate dense row")
        previousRow = row
        candidate.append(CandidateRecord(dense: dense, value: value, row: row))
    }
    require(offsets[6] + 24 * candidateSupport == data.count, "candidate terminal offset")
    return Matrix(rows: rows, columns: columns, nnz: nnz, inputSHA: inputSHA,
                  cscPointers: cscPointers, cscRows: cscRows, cscValues: cscValues,
                  csrPointers: csrPointers, csrColumns: csrColumns, csrValues: csrValues,
                  candidate: candidate)
}

func regularVector(count: Int, prime: UInt32, tag: UInt64) -> [UInt32] {
    Array<UInt32>(unsafeUninitializedCapacity: count) { buffer, initialized in
        for index in 0..<count {
            let mixed = UInt64(index) &* 2_654_435_761 &+ tag
            buffer[index] = UInt32(mixed % UInt64(prime))
        }
        initialized = count
    }
}

func cpuBlock(pointers: [UInt32], indices: [UInt32], coefficients: [Int32],
              input: [UInt32], outputEntities: Int, width: Int,
              prime: UInt32, kind: UInt32) -> [UInt32] {
    var output = [UInt32](repeating: 0, count: outputEntities * width)
    for entity in 0..<outputEntities {
        for lane in 0..<width {
            var sum: UInt32 = 0
            for edge in Int(pointers[entity])..<Int(pointers[entity + 1]) {
                let term = productMod(residue(coefficients[edge], prime),
                                      input[Int(indices[edge]) * width + lane], kind)
                sum &+= term
                if sum >= prime { sum &-= prime }
            }
            output[entity * width + lane] = sum
        }
    }
    return output
}

func makeBuffer<T>(_ device: MTLDevice, _ values: [T]) -> MTLBuffer {
    values.withUnsafeBytes { raw in
        guard let base = raw.baseAddress,
              let buffer = device.makeBuffer(bytes: base, length: raw.count,
                                             options: .storageModeShared) else {
            fail("Metal buffer allocation failed for \(raw.count) bytes")
        }
        return buffer
    }
}

struct Parameters {
    var outputEntities: UInt32
    var width: UInt32
    var primeKind: UInt32
    var reserved: UInt32 = 0
}

struct ResidentMetalMatrix {
    let cscPointers: MTLBuffer
    let cscRows: MTLBuffer
    let cscValues: MTLBuffer
    let csrPointers: MTLBuffer
    let csrColumns: MTLBuffer
    let csrValues: MTLBuffer
}

func runGPU(queue: MTLCommandQueue, pipeline: MTLComputePipelineState,
            pointers: MTLBuffer, indices: MTLBuffer, coefficients: MTLBuffer,
            input: MTLBuffer, output: MTLBuffer, outputEntities: Int, width: Int,
            kind: UInt32) -> (Double, Double) {
    guard let command = queue.makeCommandBuffer(), let encoder = command.makeComputeCommandEncoder()
    else { fail("Metal command creation") }
    encoder.setComputePipelineState(pipeline)
    encoder.setBuffer(pointers, offset: 0, index: 0)
    encoder.setBuffer(indices, offset: 0, index: 1)
    encoder.setBuffer(coefficients, offset: 0, index: 2)
    encoder.setBuffer(input, offset: 0, index: 3)
    encoder.setBuffer(output, offset: 0, index: 4)
    var parameters = Parameters(outputEntities: UInt32(outputEntities), width: UInt32(width),
                                primeKind: kind)
    encoder.setBytes(&parameters, length: MemoryLayout<Parameters>.stride, index: 5)
    let count = outputEntities * width
    let threads = min(256, pipeline.maxTotalThreadsPerThreadgroup)
    encoder.dispatchThreads(MTLSize(width: count, height: 1, depth: 1),
                            threadsPerThreadgroup: MTLSize(width: threads, height: 1, depth: 1))
    encoder.endEncoding()
    let clock = ContinuousClock()
    let start = clock.now
    command.commit()
    command.waitUntilCompleted()
    let end = clock.now
    require(command.status == .completed && command.error == nil, "Metal command failed")
    let gpu = command.gpuEndTime > command.gpuStartTime
        ? command.gpuEndTime - command.gpuStartTime : 0.0
    return (seconds(start, end), gpu)
}

func byteEqual<T>(_ cpu: [T], _ metal: MTLBuffer) -> Bool {
    cpu.withUnsafeBytes { raw in
        memcmp(raw.baseAddress!, metal.contents(), raw.count) == 0
    }
}

func benchmarkCase(device: MTLDevice, queue: MTLCommandQueue,
                   pipeline: MTLComputePipelineState,
                   pointers: [UInt32], indices: [UInt32], coefficients: [Int32],
                   metalPointers: MTLBuffer, metalIndices: MTLBuffer,
                   metalCoefficients: MTLBuffer,
                   inputEntities: Int, outputEntities: Int,
                   direction: String, width: Int, kind: UInt32,
                   prime: UInt32, mode: String) -> [String: Any] {
    autoreleasepool {
        let clock = ContinuousClock()
        let inputBuildStart = clock.now
        let count = inputEntities * width
        let tag = UInt64(direction == "A" ? 0xA251 : 0xA7251)
            &+ UInt64(width * 131) &+ UInt64(prime)
        let input = mode == "regular"
            ? regularVector(count: count, prime: prime, tag: tag)
            : [UInt32](repeating: prime - 1, count: count)
        let inputBuildSeconds = seconds(inputBuildStart, clock.now)
        let allocationStart = clock.now
        let inputBuffer = makeBuffer(device, input)
        guard let outputBuffer = device.makeBuffer(length: outputEntities * width * 4,
                                                   options: .storageModeShared) else {
            fail("Metal output allocation failed")
        }
        let uploadAllocationSeconds = seconds(allocationStart, clock.now)
        _ = runGPU(queue: queue, pipeline: pipeline, pointers: metalPointers,
                   indices: metalIndices, coefficients: metalCoefficients,
                   input: inputBuffer, output: outputBuffer,
                   outputEntities: outputEntities, width: width, kind: kind)
        let cpuStart = clock.now
        let cpu = cpuBlock(pointers: pointers, indices: indices,
                           coefficients: coefficients, input: input,
                           outputEntities: outputEntities, width: width,
                           prime: prime, kind: kind)
        let cpuSeconds = seconds(cpuStart, clock.now)
        let (metalSeconds, gpuSeconds) = runGPU(
            queue: queue, pipeline: pipeline, pointers: metalPointers,
            indices: metalIndices, coefficients: metalCoefficients,
            input: inputBuffer, output: outputBuffer,
            outputEntities: outputEntities, width: width, kind: kind)
        let exact = byteEqual(cpu, outputBuffer)
        require(exact, "CPU/Metal byte mismatch \(direction)/\(width)/\(prime)/\(mode)")
        var hostile = cpu
        hostile[hostile.count - 1] ^= 1
        require(!byteEqual(hostile, outputBuffer), "byte hostile accepted")
        let speedup = cpuSeconds / metalSeconds
        return [
            "direction": direction,
            "width": width,
            "prime": Int(prime),
            "mode": mode,
            "input_values": count,
            "output_values": outputEntities * width,
            "input_build_seconds": inputBuildSeconds,
            "input_upload_output_allocation_seconds": uploadAllocationSeconds,
            "cpu_operator_seconds": cpuSeconds,
            "metal_warm_end_to_end_seconds": metalSeconds,
            "metal_gpu_seconds": gpuSeconds,
            "warm_operator_speedup": speedup,
            "output_sha256": sha256Array(cpu),
            "byte_exact_equal": exact,
        ]
    }
}

let matrixPath = argument("--matrix")
let shaderPath = argument("--shader")
let sourcePath = argument("--source")
let outputPath = argument("--output")
let clock = ContinuousClock()
let programStart = clock.now
let buildStart = clock.now
let matrix = loadMatrix(matrixPath)
require(seconds(programStart, clock.now) < stopSchedulingSeconds, "stop scheduling after matrix load")
let shaderSource = try! String(contentsOfFile: shaderPath, encoding: .utf8)
let swiftSource = try! Data(contentsOf: URL(fileURLWithPath: sourcePath))
let executable = try! Data(contentsOf: URL(fileURLWithPath: CommandLine.arguments[0]))
guard let device = MTLCreateSystemDefaultDevice() else { fail("no Metal device") }
require(device.maxBufferLength >= matrix.rows * 16 * 4, "device buffer cap below width-16 row block")
guard let queue = device.makeCommandQueue() else { fail("Metal command queue") }
let library: MTLLibrary
do { library = try device.makeLibrary(source: shaderSource, options: nil) }
catch { fail("Metal shader compilation: \(error)") }
guard let function = library.makeFunction(name: "block_spmv") else { fail("Metal function") }
let pipeline: MTLComputePipelineState
do { pipeline = try device.makeComputePipelineState(function: function) }
catch { fail("Metal pipeline: \(error)") }
let resident = ResidentMetalMatrix(
    cscPointers: makeBuffer(device, matrix.cscPointers),
    cscRows: makeBuffer(device, matrix.cscRows),
    cscValues: makeBuffer(device, matrix.cscValues),
    csrPointers: makeBuffer(device, matrix.csrPointers),
    csrColumns: makeBuffer(device, matrix.csrColumns),
    csrValues: makeBuffer(device, matrix.csrValues))
let residentBuildSeconds = seconds(buildStart, clock.now)

// Exact current round-635 checkpoint candidate: A^T y must annihilate all exposed columns.
let candidateStart = clock.now
var candidateDense = [UInt32](repeating: 0, count: matrix.rows)
for record in matrix.candidate { candidateDense[Int(record.dense)] = record.value }
let candidateCPU = cpuBlock(pointers: matrix.cscPointers, indices: matrix.cscRows,
                            coefficients: matrix.cscValues, input: candidateDense,
                            outputEntities: matrix.columns, width: 1, prime: primePlus, kind: 0)
require(candidateCPU.allSatisfy { $0 == 0 }, "current candidate does not annihilate A")
let candidateInputBuffer = makeBuffer(device, candidateDense)
let candidateOutputBuffer = device.makeBuffer(length: matrix.columns * 4,
                                               options: .storageModeShared)!
_ = runGPU(queue: queue, pipeline: pipeline, pointers: resident.cscPointers,
           indices: resident.cscRows, coefficients: resident.cscValues,
           input: candidateInputBuffer, output: candidateOutputBuffer,
           outputEntities: matrix.columns, width: 1, kind: 0) // warm-up
let (candidateMetalSeconds, candidateGPUSeconds) = runGPU(
    queue: queue, pipeline: pipeline, pointers: resident.cscPointers,
    indices: resident.cscRows, coefficients: resident.cscValues,
    input: candidateInputBuffer, output: candidateOutputBuffer,
    outputEntities: matrix.columns, width: 1, kind: 0)
require(byteEqual(candidateCPU, candidateOutputBuffer), "candidate CPU/Metal byte mismatch")
let candidateSeconds = seconds(candidateStart, clock.now)

var cases = [[String: Any]]()
var blockMinimumSpeedup = Double.infinity
var allByteExact = true
for direction in ["A", "AT"] {
    let pointers = direction == "A" ? matrix.csrPointers : matrix.cscPointers
    let indices = direction == "A" ? matrix.csrColumns : matrix.cscRows
    let coefficients = direction == "A" ? matrix.csrValues : matrix.cscValues
    let metalPointers = direction == "A" ? resident.csrPointers : resident.cscPointers
    let metalIndices = direction == "A" ? resident.csrColumns : resident.cscRows
    let metalCoefficients = direction == "A" ? resident.csrValues : resident.cscValues
    let inputEntities = direction == "A" ? matrix.columns : matrix.rows
    let outputEntities = direction == "A" ? matrix.rows : matrix.columns
    // Largest-first permits released Metal allocations to be reused by smaller cases.
    for width in [16, 8, 1] {
        for (kind, prime) in [(UInt32(0), primePlus), (UInt32(1), primeMinus)] {
            for mode in ["regular", "max_residue"] {
                require(seconds(programStart, clock.now) < stopSchedulingSeconds,
                        "stop scheduling wall gate")
                let record = benchmarkCase(
                    device: device, queue: queue, pipeline: pipeline,
                    pointers: pointers, indices: indices, coefficients: coefficients,
                    metalPointers: metalPointers, metalIndices: metalIndices,
                    metalCoefficients: metalCoefficients,
                    inputEntities: inputEntities, outputEntities: outputEntities,
                    direction: direction, width: width, kind: kind, prime: prime, mode: mode)
                let speedup = record["warm_operator_speedup"] as! Double
                if width >= 8 { blockMinimumSpeedup = min(blockMinimumSpeedup, speedup) }
                allByteExact = allByteExact && (record["byte_exact_equal"] as! Bool)
                cases.append(record)
            }
        }
    }
}

var usage = rusage()
getrusage(RUSAGE_SELF, &usage)
let totalSeconds = seconds(programStart, clock.now)
let resourcePass = totalSeconds < hardWallSeconds && Int64(usage.ru_maxrss) < hardRSSBytes
let productionReady = allByteExact && resourcePass && blockMinimumSpeedup >= 3.0
let result: [String: Any] = [
    "status": productionReady ? "PASS_PRODUCTION_READY_EXACT_METAL_BLOCK_OPERATORS" :
                                "PASS_EXACT_METAL_BLOCK_OPERATORS_NOT_PRODUCTION_READY",
    "schema": "KRENN_AFFINE251_D12_ROUND635_METAL_BLOCK_GATE_V1",
    "matrix_sha256": matrix.inputSHA,
    "shader_sha256": sha256(Data(shaderSource.utf8)),
    "swift_source_sha256": sha256(swiftSource),
    "binary_sha256": sha256(executable),
    "device": device.name,
    "device_max_buffer_length": device.maxBufferLength,
    "rows": matrix.rows,
    "columns": matrix.columns,
    "nnz": matrix.nnz,
    "widths": [1, 8, 16],
    "primes": [Int(primePlus), Int(primeMinus)],
    "modes": ["regular", "max_residue"],
    "directions": ["A", "AT"],
    "cases": cases,
    "all_cpu_metal_byte_exact": allByteExact,
    "byte_flip_hostile_rejected": true,
    "block_width_8_16_minimum_warm_speedup": blockMinimumSpeedup,
    "production_ready_threshold": 3.0,
    "production_ready_for_future_block_operators": productionReady,
    "resident_matrix_pipeline_build_seconds": residentBuildSeconds,
    "candidate_annihilation": [
        "checkpoint_round": 635,
        "support": matrix.candidate.count,
        "dense_present": matrix.candidate.count,
        "prime": Int(primePlus),
        "nonzero_outputs": candidateCPU.reduce(0) { $0 + ($1 == 0 ? 0 : 1) },
        "output_sha256": sha256Array(candidateCPU),
        "metal_warm_end_to_end_seconds": candidateMetalSeconds,
        "metal_gpu_seconds": candidateGPUSeconds,
        "total_replay_seconds": candidateSeconds,
        "byte_exact_equal": true,
    ],
    "total_gate_seconds": totalSeconds,
    "peak_rss_bytes": Int64(usage.ru_maxrss),
    "hard_wall_seconds": hardWallSeconds,
    "hard_rss_bytes": hardRSSBytes,
    "resource_gate_pass": resourcePass,
    "scope": "Exact resident round-635 A/A^T block operators only; no closure, rank, Krylov, membership, or higher-degree launch.",
]
require(resourcePass,
        "resource gate failed total_seconds=\(totalSeconds) peak_rss_bytes=\(usage.ru_maxrss)")
let json = try! JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted, .sortedKeys])
try! json.write(to: URL(fileURLWithPath: outputPath), options: .atomic)
print(String(data: json, encoding: .utf8)!)
