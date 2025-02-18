// Assignment 12 
//Edwin Cervantes

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <mpi.h>

int main(int argc, char** argv) {
    int rank, size;
    long N = 100000; // 10^5
    //long N = 10000000; // 10^7
    //long N = 1000000000; // 10^9
   
    long local_N;
    long local_count = 0, global_count = 0;
    double x, y;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    srand(time(NULL) + rank); // Seed the random number generator

    local_N = N / size;
    // Start timer

    double start = MPI_Wtime();
    
    for (long i = 0; i < local_N; i++) {
        x = (double)rand() / RAND_MAX;
        y = (double)rand() / RAND_MAX;
        if (x*x + y*y <= 1.0) {
            local_count++;
        } }

    MPI_Reduce(&local_count, &global_count, 1, MPI_LONG, MPI_SUM, 0, MPI_COMM_WORLD);

    // End timer

    double end = MPI_Wtime();

  if (rank == 0) {
        double pi_estimate = 4.0 * global_count / N;
        printf("Estimated value of pi: %f\n", pi_estimate);
        printf("Error: %f\n", fabs(pi_estimate - M_PI));
        printf("Elapsed time: %f seconds\n", end - start);
    }
    MPI_Finalize();
    return 0; }