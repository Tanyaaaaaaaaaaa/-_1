#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <fstream>
#include <cblas.h>

const int N = 4096;
const double complexity = 2.0 * N * N * N; // 2n^3 operations

// Генерация случайной матрицы
void generate_matrix(std::vector<double> &mat)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(-1.0, 1.0);

    for (auto &val : mat)
    {
        val = dis(gen);
    }
}

// Наивное умножение матриц
void naive_mmul(const std::vector<double> &A, const std::vector<double> &B, std::vector<double> &C)
{
    for (int i = 0; i < N; ++i)
    {
        for (int j = 0; j < N; ++j)
        {
            double sum = 0.0;
            for (int k = 0; k < N; ++k)
            {
                sum += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = sum;
        }
    }
}

// Оптимизированное умножение (блочный алгоритм)
void optimized_mmul(const std::vector<double> &A, const std::vector<double> &B, std::vector<double> &C)
{
    const int block_size = 64;
    for (int i = 0; i < N; i += block_size)
    {
        for (int j = 0; j < N; j += block_size)
        {
            for (int k = 0; k < N; k += block_size)
            {
                for (int ii = i; ii < std::min(i + block_size, N); ++ii)
                {
                    for (int kk = k; kk < std::min(k + block_size, N); ++kk)
                    {
                        double a = A[ii * N + kk];
                        for (int jj = j; jj < std::min(j + block_size, N); ++jj)
                        {
                            C[ii * N + jj] += a * B[kk * N + jj];
                        }
                    }
                }
            }
        }
    }
}

// Запуск теста и вывод результатов
void run_test(const std::vector<double> &A, const std::vector<double> &B,
              const std::string &name,
              void (*mmul)(const std::vector<double> &, const std::vector<double> &, std::vector<double> &))
{
    std::vector<double> C(N * N, 0.0);
    auto start = std::chrono::high_resolution_clock::now();
    mmul(A, B, C);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    double gflops = (complexity / elapsed.count()) * 1e-9;
    std::cout << name << ": " << gflops << " GFLOPS (time: " << elapsed.count() << "s)\n";
}

int main()
{
    cout<<"Москат Татьяна Михайловна 090304-РПИа-о24"<<endl;
    std::vector<double> A(N * N);
    std::vector<double> B(N * N);
    // Загрузка или генерация матриц
    std::ifstream in_file("matrices.bin", std::ios::binary);
    if (in_file)
    {
        in_file.read(reinterpret_cast<char *>(A.data()), A.size() * sizeof(double));
        in_file.read(reinterpret_cast<char *>(B.data()), B.size() * sizeof(double));
        in_file.close();
        std::cout << "Matrices loaded from file\n";
    }
    else
    {
        generate_matrix(A);
        generate_matrix(B);
        std::ofstream out_file("matrices.bin", std::ios::binary);
        out_file.write(reinterpret_cast<const char *>(A.data()), A.size() * sizeof(double));
        out_file.write(reinterpret_cast<const char *>(B.data()), B.size() * sizeof(double));
        out_file.close();
        std::cout << "New random matrices generated\n";
    }
    // Тестирование методов
    run_test(A, B, "Naive multiplication", naive_mmul);
    run_test(A, B, "Optimized multiplication", optimized_mmul);

    run_test(A, B, "BLAS dgemm", [](const auto &A, const auto &B, auto &C)
             { cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                           N, N, N, 1.0, A.data(), N, B.data(), N, 0.0, C.data(), N); });
    return 0;
}
