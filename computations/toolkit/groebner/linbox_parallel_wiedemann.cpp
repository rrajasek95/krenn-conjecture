#include <linbox/linbox-config.h>

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <vector>

#include <omp.h>

#include <givaro/modular.h>
#include <givaro/gfq.h>
#include <linbox/blackbox/blackbox-interface.h>
#include <linbox/solutions/methods.h>
#include <linbox/solutions/solve.h>
#include <linbox/util/commentator.h>
#include <linbox/vector/blas-vector.h>
#include <linbox/vector/vector-domain.h>

namespace {

struct CSR {
    std::size_t rows = 0;
    std::size_t columns = 0;
    std::vector<std::uint64_t> starts;
    std::vector<std::uint32_t> indices;
    std::vector<std::uint32_t> values;
};

CSR read_sms(const std::string& path, std::uint32_t prime) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open " + path);
    char kind = 0;
    CSR matrix;
    if (!(input >> matrix.rows >> matrix.columns >> kind) || kind != 'M')
        throw std::runtime_error("bad SMS header in " + path);
    matrix.starts.assign(matrix.rows + 1, 0);
    struct Entry { std::uint32_t row, column, value; };
    std::vector<Entry> entries;
    std::uint64_t raw_row = 0, raw_column = 0;
    long long raw_value = 0;
    std::uint32_t previous_row = 0, previous_column = 0;
    bool first = true, terminated = false;
    while (input >> raw_row >> raw_column >> raw_value) {
        if (raw_row == 0 && raw_column == 0 && raw_value == 0) {
            terminated = true;
            break;
        }
        if (raw_row == 0 || raw_row > matrix.rows ||
            raw_column == 0 || raw_column > matrix.columns)
            throw std::runtime_error("SMS coordinate out of range in " + path);
        std::uint32_t row = static_cast<std::uint32_t>(raw_row - 1);
        std::uint32_t column = static_cast<std::uint32_t>(raw_column - 1);
        if (!first && (row < previous_row ||
                       (row == previous_row && column <= previous_column)))
            throw std::runtime_error("SMS entries not strictly row-major in " + path);
        first = false;
        previous_row = row;
        previous_column = column;
        long long reduced = raw_value % static_cast<long long>(prime);
        if (reduced < 0) reduced += prime;
        if (reduced == 0) throw std::runtime_error("stored zero modulo prime in " + path);
        entries.push_back({row, column, static_cast<std::uint32_t>(reduced)});
        matrix.starts[row + 1]++;
    }
    if (!terminated) throw std::runtime_error("missing SMS terminator in " + path);
    std::string trailing;
    if (input >> trailing) throw std::runtime_error("trailing SMS data in " + path);
    for (std::size_t row = 0; row < matrix.rows; ++row)
        matrix.starts[row + 1] += matrix.starts[row];
    matrix.indices.resize(entries.size());
    matrix.values.resize(entries.size());
    std::vector<std::uint64_t> next = matrix.starts;
    for (const auto& entry : entries) {
        const auto position = next[entry.row]++;
        matrix.indices[position] = entry.column;
        matrix.values[position] = entry.value;
    }
    std::cerr << "loaded " << path << " shape=" << matrix.rows << "x"
              << matrix.columns << " nnz=" << entries.size() << "\n";
    return matrix;
}

template<class Field_>
class ParallelCSRBlackbox : public LinBox::BlackboxInterface {
public:
    using Field = Field_;
    using Element = typename Field::Element;

    ParallelCSRBlackbox(const Field& field, CSR forward, CSR transpose,
                        std::uint32_t prime)
        : field_(&field), forward_(std::move(forward)),
          transpose_(std::move(transpose)), prime_(prime) {
        if (forward_.rows != transpose_.columns ||
            forward_.columns != transpose_.rows)
            throw std::runtime_error("forward/transpose dimensions disagree");
    }

    template<class OtherField>
    ParallelCSRBlackbox(const ParallelCSRBlackbox<OtherField>& other,
                        const Field& field)
        : field_(&field), forward_(other.forward_),
          transpose_(other.transpose_), prime_(other.prime_) {}

    template<class NewField>
    struct rebind {
        using other = ParallelCSRBlackbox<NewField>;

        void operator()(other& target,
                        const ParallelCSRBlackbox& source) const {
            target.forward_ = source.forward_;
            target.transpose_ = source.transpose_;
            target.prime_ = source.prime_;
        }
    };

    const Field& field() const { return *field_; }
    std::size_t rowdim() const { return forward_.rows; }
    std::size_t coldim() const { return forward_.columns; }

    template<class OutVector, class InVector>
    OutVector& apply(OutVector& output, const InVector& input) const {
        multiply(forward_, output, input);
        return output;
    }

    template<class OutVector, class InVector>
    OutVector& applyTranspose(OutVector& output, const InVector& input) const {
        multiply(transpose_, output, input);
        return output;
    }

private:
    template<class> friend class ParallelCSRBlackbox;

    template<class OutVector, class InVector>
    void multiply(const CSR& matrix, OutVector& output,
                  const InVector& input) const {
        if (output.size() != matrix.rows || input.size() != matrix.columns)
            throw std::runtime_error("matvec dimension mismatch");
        if constexpr (std::is_same_v<Element, double>) {
#pragma omp parallel for schedule(static)
            for (std::int64_t signed_row = 0;
                 signed_row < static_cast<std::int64_t>(matrix.rows); ++signed_row) {
                const std::size_t row = static_cast<std::size_t>(signed_row);
                std::uint64_t accumulator = 0;
                for (std::uint64_t position = matrix.starts[row];
                     position < matrix.starts[row + 1]; ++position) {
                    long long signed_value = static_cast<long long>(
                        std::llround(input[matrix.indices[position]]));
                    signed_value %= static_cast<long long>(prime_);
                    if (signed_value < 0) signed_value += prime_;
                    accumulator += static_cast<std::uint64_t>(matrix.values[position]) *
                                   static_cast<std::uint64_t>(signed_value);
                    if (accumulator >= (UINT64_C(1) << 61)) accumulator %= prime_;
                }
                field().init(output[row],
                             static_cast<long long>(accumulator % prime_));
            }
        } else {
#pragma omp parallel for schedule(static)
            for (std::int64_t signed_row = 0;
                 signed_row < static_cast<std::int64_t>(matrix.rows); ++signed_row) {
                const std::size_t row = static_cast<std::size_t>(signed_row);
                Element accumulator, coefficient;
                field().init(accumulator, 0);
                for (std::uint64_t position = matrix.starts[row];
                     position < matrix.starts[row + 1]; ++position) {
                    field().init(coefficient,
                                 static_cast<long long>(matrix.values[position]));
                    field().axpyin(accumulator, coefficient,
                                   input[matrix.indices[position]]);
                }
                field().assign(output[row], accumulator);
            }
        }
    }

    const Field* field_;
    CSR forward_, transpose_;
    std::uint32_t prime_;
};

template<class Field, class Vector>
void read_rhs(const std::string& path, const Field& field, Vector& rhs,
              std::uint32_t prime) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open " + path);
    std::size_t rows = 0, columns = 0;
    char kind = 0;
    if (!(input >> rows >> columns >> kind) || rows != 1 ||
        columns != rhs.size() || kind != 'M')
        throw std::runtime_error("bad RHS SMS header");
    for (auto& value : rhs) field.init(value, 0);
    std::size_t row = 0, column = 0;
    long long raw = 0;
    bool terminated = false;
    while (input >> row >> column >> raw) {
        if (row == 0 && column == 0 && raw == 0) {
            terminated = true;
            break;
        }
        if (row != 1 || column == 0 || column > rhs.size())
            throw std::runtime_error("RHS coordinate out of range");
        field.init(rhs[column - 1], raw % static_cast<long long>(prime));
    }
    if (!terminated) throw std::runtime_error("missing RHS terminator");
}

template<class Field, class Vector>
void write_solution(const std::string& path, const Field& field,
                    const Vector& solution, std::uint32_t prime) {
    std::ofstream output(path);
    if (!output) throw std::runtime_error("cannot create " + path);
    output << "1 " << solution.size() << " M\n";
    for (std::size_t index = 0; index < solution.size(); ++index) {
        long long value = 0;
        field.convert(value, solution[index]);
        value %= prime;
        if (value < 0) value += prime;
        if (value != 0) {
            if (value > static_cast<long long>(prime / 2)) value -= prime;
            output << "1 " << index + 1 << " " << value << "\n";
        }
    }
    output << "0 0 0\n";
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 6 && argc != 7) {
        std::cerr << "usage: linbox_parallel_wiedemann MATRIX TRANSPOSE RHS OUTPUT PRIME"
                     " [benchmark-extension]\n";
        return 2;
    }
    try {
        const std::uint32_t prime = static_cast<std::uint32_t>(std::stoul(argv[5]));
        const bool benchmark_extension =
            argc == 7 && std::string(argv[6]) == "benchmark-extension";
        if (argc == 7 && !benchmark_extension)
            throw std::runtime_error("unknown optional mode");
        if (benchmark_extension) {
            using ExtensionField = Givaro::GFqDom<std::int64_t>;
            using ExtensionVector = LinBox::BlasVector<ExtensionField>;
            ExtensionField extension(prime, 2);
            auto forward = read_sms(argv[1], prime);
            auto transpose = read_sms(argv[2], prime);
            ParallelCSRBlackbox<ExtensionField> matrix(
                extension, std::move(forward), std::move(transpose), prime);
            ExtensionVector input(extension, matrix.coldim());
            ExtensionVector output(extension, matrix.rowdim());
            for (auto& value : input) extension.init(value, 1);
            const auto begin = std::chrono::steady_clock::now();
            for (int iteration = 0; iteration < 3; ++iteration)
                matrix.apply(output, input);
            const auto elapsed = std::chrono::duration<double>(
                std::chrono::steady_clock::now() - begin).count();
            std::cerr << "quadratic-extension matvec seconds=" << elapsed / 3
                      << " threads=" << omp_get_max_threads() << "\n";
            return 0;
        }
        using Field = Givaro::Modular<double>;
        using Vector = LinBox::BlasVector<Field>;
        Field field(static_cast<double>(prime));
        auto forward = read_sms(argv[1], prime);
        auto transpose = read_sms(argv[2], prime);
        ParallelCSRBlackbox<Field> matrix(field, std::move(forward),
                                          std::move(transpose), prime);
        Vector rhs(field, matrix.rowdim()), solution(field, matrix.coldim());
        read_rhs(argv[3], field, rhs, prime);

        Vector check(field, matrix.rowdim());
        auto begin = std::chrono::steady_clock::now();
        matrix.apply(check, solution);
        auto elapsed = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - begin).count();
        std::cerr << "parallel matvec benchmark seconds=" << elapsed
                  << " threads=" << omp_get_max_threads() << "\n";

        std::srand(1);
        srand48(1);
        LinBox::commentator().setMaxDetailLevel(-1);
        LinBox::commentator().setMaxDepth(-1);
        LinBox::commentator().setReportStream(std::cerr);
        LinBox::Method::Wiedemann method;
        method.trialsBeforeFailure = 3;
        method.checkResult = true;
        method.certifyInconsistency = true;
        const char* preconditioner = std::getenv(
            "LINBOX_WIEDEMANN_PRECONDITIONER");
        if (preconditioner != nullptr) {
            const std::string requested(preconditioner);
            if (requested == "sparse")
                method.preconditioner = LinBox::Preconditioner::Sparse;
            else if (requested == "butterfly")
                method.preconditioner = LinBox::Preconditioner::Butterfly;
            else if (requested != "none")
                throw std::runtime_error(
                    "LINBOX_WIEDEMANN_PRECONDITIONER must be none, sparse, "
                    "or butterfly");
            std::cerr << "Wiedemann preconditioner=" << requested << "\n";
        }
        LinBox::solve(solution, matrix, rhs, method);

        matrix.apply(check, solution);
        LinBox::VectorDomain<Field> domain(field);
        if (!domain.areEqual(check, rhs))
            throw std::runtime_error("LinBox returned a vector that fails A*x=b");
        write_solution(argv[4], field, solution, prime);
        std::cerr << "solution verified and written\n";
        return 0;
    } catch (const LinBox::LinboxError& error) {
        std::cerr << "LINBOX ERROR: " << error.what() << "\n";
        return 1;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << "\n";
        return 1;
    }
}
