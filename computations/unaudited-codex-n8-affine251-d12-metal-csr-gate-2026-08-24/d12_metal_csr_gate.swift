import CryptoKit
import Darwin
import Foundation
import Metal

let headerBytes = 112
let primePlus: UInt32 = 1_073_741_827
let primeMinus: UInt32 = 1_073_741_789
let mask30: UInt64 = (1 << 30) - 1

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

func bytes<T>(of values: [T]) -> Data {
    values.withUnsafeBytes { Data($0) }
}

func sha256(_ data: Data) -> String {
    SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
}

func seconds(_ start: ContinuousClock.Instant, _ end: ContinuousClock.Instant) -> Double {
    let duration = start.duration(to: end)
    return Double(duration.components.seconds) + Double(duration.components.attoseconds) / 1.0e18
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

func residue(_ coefficient: Int32, _ prime: UInt32) -> UInt32 {
    if coefficient >= 0 { return UInt32(coefficient) }
    return prime - UInt32(-Int64(coefficient))
}

func regularVector(count: Int, prime: UInt32) -> [UInt32] {
    (0..<count).map { index in
        var value = UInt64(index) &+ 0x9e3779b97f4a7c15
        value = (value ^ (value >> 30)) &* 0xbf58476d1ce4e5b9
        value = (value ^ (value >> 27)) &* 0x94d049bb133111eb
        value ^= value >> 31
        return UInt32(value % UInt64(prime))
    }
}

func referenceSpMV(rowOffsets: [UInt32], columnIndices: [UInt32], coefficients: [Int32],
                   vector: [UInt32], prime: UInt32) -> [UInt32] {
    var output = [UInt32](repeating: 0, count: rowOffsets.count - 1)
    for row in output.indices {
        var sum: UInt64 = 0
        for edge in Int(rowOffsets[row])..<Int(rowOffsets[row + 1]) {
            let value = UInt64(residue(coefficients[edge], prime))
            sum += (value * UInt64(vector[Int(columnIndices[edge])])) % UInt64(prime)
            if sum >= UInt64(prime) { sum -= UInt64(prime) }
        }
        output[row] = UInt32(sum)
    }
    return output
}

func optimizedSpMV(rowOffsets: [UInt32], columnIndices: [UInt32], values: [UInt32],
                   vector: [UInt32], prime: UInt32, kind: UInt32,
                   repetitions: Int) -> [UInt32] {
    var output = [UInt32](repeating: 0, count: rowOffsets.count - 1)
    for _ in 0..<repetitions {
        for row in output.indices {
            var sum: UInt32 = 0
            for edge in Int(rowOffsets[row])..<Int(rowOffsets[row + 1]) {
                let term = productMod(values[edge], vector[Int(columnIndices[edge])], kind)
                sum &+= term
                if sum >= prime { sum &-= prime }
            }
            output[row] = sum
        }
    }
    return output
}

func makeBuffer<T>(_ device: MTLDevice, _ values: [T]) -> MTLBuffer {
    values.withUnsafeBytes { raw in
        guard let base = raw.baseAddress,
              let buffer = device.makeBuffer(bytes: base, length: raw.count, options: .storageModeShared) else {
            fail("Metal buffer allocation failed")
        }
        return buffer
    }
}

struct Parameters {
    var rows: UInt32
    var primeKind: UInt32
}

let inputPath = argument("--input")
let shaderPath = argument("--shader")
let sourcePath = argument("--source")
let outputPath = argument("--output")
let outputDirectory = argument("--output-dir")
let repetitions = Int(argument("--repetitions")) ?? 0
require(repetitions > 0 && repetitions <= 4096, "bad repetition count")

let clock = ContinuousClock()
let programStart = clock.now
let input = try! Data(contentsOf: URL(fileURLWithPath: inputPath), options: .mappedIfSafe)
require(input.count >= headerBytes, "short CSR interface")
require(String(data: input[0..<13], encoding: .ascii) == "D12CSRSLICEV1", "bad CSR magic")
require(u32(input, 16) == 1, "bad CSR version")
require(u32(input, 20) == primePlus, "bad CSR source prime")
let rows = Int(u32(input, 24))
let columns = Int(u32(input, 28))
let nnz = Int(u64(input, 32))
require(rows > 0 && columns > 0 && nnz > 0 && nnz < Int(UInt32.max), "bad CSR dimensions")
let payloadExpected = input[80..<112].map { String(format: "%02x", $0) }.joined()
let payload = input[headerBytes...]
require(sha256(Data(payload)) == payloadExpected, "CSR payload SHA-256 mismatch")
let expectedBytes = headerBytes + 4 * (rows + 1) + 4 * nnz + 4 * nnz
require(input.count == expectedBytes, "CSR byte length mismatch")

var cursor = headerBytes
var rowOffsets = [UInt32](repeating: 0, count: rows + 1)
rowOffsets.withUnsafeMutableBytes { input.copyBytes(to: $0, from: cursor..<(cursor + $0.count)) }
cursor += 4 * (rows + 1)
var columnIndices = [UInt32](repeating: 0, count: nnz)
columnIndices.withUnsafeMutableBytes { input.copyBytes(to: $0, from: cursor..<(cursor + $0.count)) }
cursor += 4 * nnz
var coefficients = [Int32](repeating: 0, count: nnz)
coefficients.withUnsafeMutableBytes { input.copyBytes(to: $0, from: cursor..<(cursor + $0.count)) }
require(rowOffsets[0] == 0 && rowOffsets[rows] == UInt32(nnz), "bad CSR endpoints")
require(zip(rowOffsets, rowOffsets.dropFirst()).allSatisfy { $0 <= $1 }, "nonmonotone CSR offsets")
require(columnIndices.allSatisfy { $0 < UInt32(columns) }, "CSR column out of range")
require(coefficients.allSatisfy { $0 != 0 && abs(Int64($0)) <= 1440 }, "CSR coefficient bound")

let shaderSource = try! String(contentsOfFile: shaderPath, encoding: .utf8)
let swiftSource = try! Data(contentsOf: URL(fileURLWithPath: sourcePath))
let executable = try! Data(contentsOf: URL(fileURLWithPath: CommandLine.arguments[0]))
let pipelineStart = clock.now
guard let device = MTLCreateSystemDefaultDevice() else { fail("no Metal device") }
guard let queue = device.makeCommandQueue() else { fail("Metal command queue") }
let library: MTLLibrary
do {
    library = try device.makeLibrary(source: shaderSource, options: nil)
} catch {
    fail("Metal shader compilation: \(error)")
}
guard let function = library.makeFunction(name: "csr_pairing") else { fail("Metal function missing") }
let pipeline: MTLComputePipelineState
do {
    pipeline = try device.makeComputePipelineState(function: function)
} catch {
    fail("Metal pipeline creation: \(error)")
}
let rowBuffer = makeBuffer(device, rowOffsets)
let columnBuffer = makeBuffer(device, columnIndices)
let pipelineEnd = clock.now

try! FileManager.default.createDirectory(atPath: outputDirectory,
                                         withIntermediateDirectories: true)
var cases = [[String: Any]]()
var aggregateCPU = 0.0
var aggregateMetal = seconds(pipelineStart, pipelineEnd)
var byteHostileRejected = true

for (kind, prime) in [(UInt32(0), primePlus), (UInt32(1), primeMinus)] {
    let values = coefficients.map { residue($0, prime) }
    for mode in ["regular", "max_residue"] {
        let vector = mode == "regular" ? regularVector(count: columns, prime: prime)
                                       : [UInt32](repeating: prime - 1, count: columns)
        let referenceStart = clock.now
        let reference = referenceSpMV(rowOffsets: rowOffsets, columnIndices: columnIndices,
                                      coefficients: coefficients, vector: vector, prime: prime)
        let referenceEnd = clock.now
        let cpuStart = clock.now
        let cpu = optimizedSpMV(rowOffsets: rowOffsets, columnIndices: columnIndices,
                                values: values, vector: vector, prime: prime, kind: kind,
                                repetitions: repetitions)
        let cpuEnd = clock.now
        require(cpu == reference, "optimized CPU/reference mismatch for \(prime)/\(mode)")

        let metalStart = clock.now
        let valuesBuffer = makeBuffer(device, values)
        let vectorBuffer = makeBuffer(device, vector)
        let outputBuffer = device.makeBuffer(length: rows * 4, options: .storageModeShared)!
        guard let commandBuffer = queue.makeCommandBuffer(),
              let encoder = commandBuffer.makeComputeCommandEncoder() else {
            fail("Metal command encoding")
        }
        encoder.setComputePipelineState(pipeline)
        encoder.setBuffer(rowBuffer, offset: 0, index: 0)
        encoder.setBuffer(columnBuffer, offset: 0, index: 1)
        encoder.setBuffer(valuesBuffer, offset: 0, index: 2)
        encoder.setBuffer(vectorBuffer, offset: 0, index: 3)
        encoder.setBuffer(outputBuffer, offset: 0, index: 4)
        var parameters = Parameters(rows: UInt32(rows), primeKind: kind)
        encoder.setBytes(&parameters, length: MemoryLayout<Parameters>.stride, index: 5)
        let width = min(256, pipeline.maxTotalThreadsPerThreadgroup)
        let grid = MTLSize(width: rows, height: 1, depth: 1)
        let group = MTLSize(width: width, height: 1, depth: 1)
        for _ in 0..<repetitions {
            encoder.dispatchThreads(grid, threadsPerThreadgroup: group)
        }
        encoder.endEncoding()
        commandBuffer.commit()
        commandBuffer.waitUntilCompleted()
        require(commandBuffer.status == .completed && commandBuffer.error == nil,
                "Metal command failed for \(prime)/\(mode)")
        let metal = Array(UnsafeBufferPointer(
            start: outputBuffer.contents().bindMemory(to: UInt32.self, capacity: rows),
            count: rows))
        let metalEnd = clock.now
        require(metal == reference, "Metal/reference mismatch for \(prime)/\(mode)")

        let cpuData = bytes(of: cpu)
        let metalData = bytes(of: metal)
        require(cpuData == metalData, "CPU/Metal byte mismatch for \(prime)/\(mode)")
        var hostile = metalData
        hostile[0] ^= 1
        byteHostileRejected = byteHostileRejected && hostile != cpuData
        let stem = "p\(prime)_\(mode)"
        try! cpuData.write(to: URL(fileURLWithPath: outputDirectory + "/cpu_" + stem + ".bin"),
                           options: .atomic)
        try! metalData.write(to: URL(fileURLWithPath: outputDirectory + "/metal_" + stem + ".bin"),
                             options: .atomic)

        let cpuSeconds = seconds(cpuStart, cpuEnd)
        let metalSeconds = seconds(metalStart, metalEnd)
        let gpuSeconds = commandBuffer.gpuEndTime > commandBuffer.gpuStartTime
            ? commandBuffer.gpuEndTime - commandBuffer.gpuStartTime : 0.0
        aggregateCPU += cpuSeconds
        aggregateMetal += metalSeconds
        cases.append([
            "prime": Int(prime),
            "mode": mode,
            "reference_single_seconds": seconds(referenceStart, referenceEnd),
            "cpu_optimized_seconds": cpuSeconds,
            "metal_end_to_end_seconds": metalSeconds,
            "metal_gpu_seconds": gpuSeconds,
            "warm_end_to_end_speedup": cpuSeconds / metalSeconds,
            "output_sha256": sha256(cpuData),
            "byte_exact_equal": true,
            "nonzero_outputs": reference.reduce(0) { $0 + ($1 == 0 ? 0 : 1) },
        ])
    }
}

require(byteHostileRejected, "byte comparator hostile was accepted")
var usage = rusage()
getrusage(RUSAGE_SELF, &usage)
let minimumWarm = cases.map { $0["warm_end_to_end_speedup"] as! Double }.min()!
let aggregateSpeedup = aggregateCPU / aggregateMetal
let promoted = aggregateSpeedup >= 3.0 && minimumWarm >= 3.0
let result: [String: Any] = [
    "status": promoted ? "PASS_METAL_CSR_PROMOTION_GATE" : "PASS_METAL_CSR_EXACT_NO_LAUNCH",
    "schema": "KRENN_AFFINE251_D12_METAL_CSR_GATE_V1",
    "device": device.name,
    "rows": rows,
    "columns": columns,
    "nnz": nnz,
    "repetitions": repetitions,
    "shader_sha256": sha256(Data(shaderSource.utf8)),
    "swift_source_sha256": sha256(swiftSource),
    "binary_sha256": sha256(executable),
    "input_sha256": sha256(input),
    "pipeline_setup_seconds": seconds(pipelineStart, pipelineEnd),
    "aggregate_cpu_optimized_seconds": aggregateCPU,
    "aggregate_metal_cold_end_to_end_seconds": aggregateMetal,
    "aggregate_cold_end_to_end_speedup": aggregateSpeedup,
    "minimum_warm_end_to_end_speedup": minimumWarm,
    "promotion_threshold": 3.0,
    "promoted": promoted,
    "byte_comparator_hostile_rejected": byteHostileRejected,
    "peak_rss_bytes": Int64(usage.ru_maxrss),
    "cases": cases,
    "scope": "Bounded persisted-vector CSR pairing/SpMV only; no closure, rank, membership, or higher-degree run.",
    "total_program_seconds": seconds(programStart, clock.now),
]
let json = try! JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted, .sortedKeys])
let destination = URL(fileURLWithPath: outputPath)
try! json.write(to: destination, options: .atomic)
print(String(data: json, encoding: .utf8)!)
