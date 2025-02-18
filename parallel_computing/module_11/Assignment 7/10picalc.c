#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double f(double a)
{
    return (4.0 / (1.0 + a * a));
}

int main(int argc, char *argv[])
{
    int myid, numprocs, i;
    double PI25DT = 3.141592653589793238462643;
    double mypi, pi, h, sum, x;
    double startwtime, endwtime;
    int namelen;
    char processor_name[MPI_MAX_PROCESSOR_NAME];

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);
    MPI_Get_processor_name(processor_name, &namelen);

    // Write Results to file to be plotted using Python
    FILE *fp;
    if (myid == 0) {
        fp = fopen("pi_results.txt", "w");
        fprintf(fp, "Exponent\tIntervals\tError\t\t\tTime (sec)\n");
    }

    // Loop from 1-10 which will be used as the exponent
    for (int exp = 1; exp <= 10; exp++)
    {
        int n = pow(10, exp);
        if (myid == 0)
        {
            startwtime = MPI_Wtime();
        }

        MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

        h = 1.0 / (double)n;
        sum = 0.0;
        
        for (i = myid + 1; i <= n; i += numprocs)
        {
            x = h * ((double)i - 0.5);
            sum += f(x);
        }
        mypi = h * sum;

        MPI_Reduce(&mypi, &pi, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
        // Print info detailing exponent, interval, accuracy, time
        if (myid == 0)
        {
            double error = fabs(pi - PI25DT);
            endwtime = MPI_Wtime();
            double time_taken = endwtime - startwtime;

            fprintf(fp, "%d\t%d\t%.16f\t%f\n", exp, n, error, time_taken);

            printf("Exponent: %d, Intervals: %d, pi approx: %.16f, Error: %.16f, Time: %f sec\n",
                   exp, n, pi, error, time_taken);
        }
    }
    // Close plot file
    if (myid == 0)
    {
        fclose(fp);
        printf("Results written to pi_results.txt\n");
    }

    MPI_Finalize();
    return 0;
}