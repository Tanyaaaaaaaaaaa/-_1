#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <fstream>
#include <cblas.h>
#include <algorithm>

const int MatrixSize = 4096;
const double TotalOps = 2.0 * MatrixSize * MatrixSize * MatrixSize; // 2n^3 операций

// Генерация случайной матрицы
void generate_matrix(std::vector<double> &matrix)
{
    std::random_device rd;
    std::mt19937 generator(rd());
    std::uniform_real_distribution<> distribution(-1.0, 1.0);

    for (auto &element : matrix)
    {
        element = distribution(generator);
    }
}

// Наивное умножение матриц
void naive_mmul(const std::vector<double> &MatA, const std::vector<double> &MatB, std::vector<double> &MatC)
{
    for (int row = 0; row < MatrixSize; ++row)
    {
        for (int col = 0; col < MatrixSize; ++col)
        {
            double sum = 0.0;
            for (int k = 0; k < MatrixSize; ++k)
            {
                sum += MatA[row * MatrixSize + k] * MatB[k * MatrixSize + col];
            }
            MatC[row * MatrixSize + col] = sum;
        }
    }
}

// Оптимизированное умножение (блочный алгоритм)
void optimized_mmul(const std::vector<double> &MatA, const std::vector<double> &MatB, std::vector<double> &MatC)
{
    const int Block = 64;
    for (int i = 0; i < MatrixSize; i += Block)
    {
        for (int j = 0; j < MatrixSize; j += Block)
        {
            for (int k = 0; k < MatrixSize; k += Block)
            {
                for (int ii = i; ii < std::min(i + Block, MatrixSize); ++ii)
                {
                    for (int kk = k; kk < std::min(k + Block, MatrixSize); ++kk)
                    {
                        double valA = MatA[ii * MatrixSize + kk];
                        for (int jj = j; jj < std::min(j + Block, MatrixSize); ++jj)
                        {
                            MatC[ii * MatrixSize + jj] += valA * MatB[kk * MatrixSize + jj];
                        }
                    }
                }
            }
        }
    }
}

// Запуск теста и вывод результатов
void benchmark(const std::vector<double> &MatA, const std::vector<double> &MatB,
               const std::string &method_name,
               void (*id7951572 (*multiply))(const std::vector<double> &, const std::vector<double> &, std::vector<double> &))
{
    std::vector<double> MatResult(MatrixSize * MatrixSize, 0.0);
    auto start_time = std::chrono::high_resolution_clock::now();
    multiply(MatA, MatB, MatResult);
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;
    double gflops = (TotalOps / elapsed.count()) * 1e-9;
    std::cout << method_name << ": " << gflops << " GFLOPS (time: " << elapsed.count() << "s)\n";
}

int main()
{
    std::cout << "Москат Татьяна Михайловна 090304-РПИа-о24" << std::endl;
    
    std::vector<double> MatrixA(MatrixSize * MatrixSize);
    std::vector<double> MatrixB(MatrixSize * MatrixSize);
    
    // Загрузка или генерация матриц
    std::ifstream input_file("matrices.bin", std::ios::binary);
    if (input_file)
    {
        input_file.read(reinterpret_cast<char *>(MatrixA.data()), MatrixA.size() * sizeof(double));
        input_file.read(reinterpret_cast<char *>(MatrixB.data()), MatrixB.size() * sizeof(double));
        input_file.close();
        std::cout << "Matrices loaded from file\n";
    }
    else
    {
        generate_matrix(MatrixA);
        generate_matrix(MatrixB);
        std::ofstream output_file("matrices.bin", std::ios::binary);
        output_file.write(reinterpret_cast<const char *>(MatrixA.data()), MatrixA.size() * sizeof(double));
        output_file.write(reinterpret_cast<const char *>(MatrixB.data()), MatrixB.size() * sizeof(double));
        output_file.close();
        std::cout << "New random matrices generated\n";
    }
    
    // Тестирование методов
    benchmark(MatrixA, MatrixB, "Naive multiplication", naive_mmul);
    benchmark(MatrixA, MatrixB, "Optimized multiplication",optimized_mmul);

    // Тест BLAS
    benchmark(MatrixA, MatrixB, "BLAS dgemm", [](const auto &A, const auto &B, auto &C)
             { cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                           MatrixSize, MatrixSize, MatrixSize, 1.0, A.data(), MatrixSize, B.data(), MatrixSize, 0.0, C.data(), MatrixSize); });
    
    return 0;
}
