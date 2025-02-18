//transpose.cu
#include <stdio.h>
#include "gputimer.h"
// #include "utils.h"
#define NumSMPs 30 //Machine dependent see gpu_enum
#define M 8192 //problem size
#define ThreadsperBlock 1024
#define BlocksperGrid M/ThreadsperBlock

const int N= 1024;	// matrix size will be NxN

int compare_matrices(float *gpu, float *ref, int N)
{
        int result = 0;
        for(int j=0; j < N; j++)
        for(int i=0; i < N; i++)
                if (ref[i + j*N] != gpu[i + j*N])
                   {result = 1;}
        return result;
}

// fill a matrix with sequential numbers in the range 0..N-1
void fill_matrix(float *mat, int N)
{
        for(int j=0; j < N * N; j++)
                mat[j] = (float) j;
}


void 
transpose_CPU(float in[], float out[])
{
	for(int j=0; j < N; j++)
    	    for(int i=0; i < N; i++)
      		out[j + i*N] = in[i + j*N]; // implements flip out(j,i) = in(i,j)
}

// to be launched on a single thread
__global__ void 
transpose_serial(float in[], float out[])
{
	for(int j=0; j < N; j++)
		for(int i=0; i < N; i++)
			out[j + i*N] = in[i + j*N]; 
}

// to be launched with one thread per row of output matrix
__global__ void 
transpose_parallel_per_row(float in[], float out[])
{
	int i = threadIdx.x + blockDim.x * blockIdx.y;

	for(int j=0; j < N; j++)
		out[j + i*N] = in[i + j*N]; 
}

__global__ void 
transpose_parallel_per_element_tiled(float in[], float out[])
{
    int i = blockIdx.y * blockDim.y + threadIdx.y; // Row
    int j = blockIdx.x * blockDim.x + threadIdx.x; // Column

    if (i < N && j < N) {
        out[i + j*N] = in[j + i*N]; // Transpose
    }
}

__global__ void 
transpose_parallel_per_element_tiled_shared(float in[], float out[])
{
    // Global tiles
    __shared__ float tile[16][16]; // KxK shared memory tile

    int i = blockIdx.y * blockDim.y + threadIdx.y; // Row 
    int j = blockIdx.x * blockDim.x + threadIdx.x; // Column
    
// Load from global memory to shared memory
    if (i < N && j < N) {
        tile[threadIdx.y][threadIdx.x] = in[i* N + j];

    }

    // Write from shared memory to global memory
    if (i < N && j < N){
        out[j * N + i] = tile[threadIdx.y][threadIdx.x];
    }
}

int main(int argc, char **argv)
{
	int numbytes = N * N * sizeof(float);
	float *in = (float *) malloc(numbytes);
	float *out = (float *) malloc(numbytes);
	float *gold = (float *) malloc(numbytes);
	fill_matrix(in, N);
	transpose_CPU(in, gold);

	float *d_in, *d_out;

	cudaMalloc(&d_in, numbytes);
	cudaMalloc(&d_out, numbytes);
	cudaMemcpy(d_in, in, numbytes, cudaMemcpyHostToDevice);

	GpuTimer timer;
        timer.Start();
	transpose_serial<<<1,1>>>(d_in, d_out);
	timer.Stop();
        for (int i=0; i < N*N; ++i){out[i] = 0.0;}
        cudaMemcpy(out, d_out, numbytes, cudaMemcpyDeviceToHost);
	printf("transpose_serial: %g ms.\nVerifying ...%s\n", 
		   timer.Elapsed(), compare_matrices(out, gold, N) ? "Failed" : "Success");

   
        cudaMemcpy(d_out, d_in, numbytes, cudaMemcpyDeviceToDevice); //clean d_out
        timer.Start();
	transpose_parallel_per_row<<<1,N>>>(d_in, d_out);
	timer.Stop();
        for (int i=0; i < N*N; ++i){out[i] = 0.0;}  //clean out
	cudaMemcpy(out, d_out, numbytes, cudaMemcpyDeviceToHost);
	printf("transpose_parallel_per_row: %g ms.\nVerifying ...%s\n", 
		    timer.Elapsed(), compare_matrices(out, gold, N) ? "Failed" : "Success");

        cudaMemcpy(d_out, d_in, numbytes, cudaMemcpyDeviceToDevice); //clean d_out
        // Tiled versions
        const int K= 16;
        dim3 blocks_tiled(N/K,N/K);
	dim3 threads_tiled(K,K);
	timer.Start();
	transpose_parallel_per_element_tiled<<<blocks_tiled,threads_tiled>>>(d_in, d_out);
	timer.Stop();
        for (int i=0; i < N*N; ++i){out[i] = 0.0;}
	cudaMemcpy(out, d_out, numbytes, cudaMemcpyDeviceToHost);
	printf("transpose_parallel_per_element_tiled %dx%d: %g ms.\nVerifying ...%s\n", 
		   K, K, timer.Elapsed(), compare_matrices(out, gold, N) ? "Failed" : "Success");
        cudaMemcpy(d_out, d_in, numbytes, cudaMemcpyDeviceToDevice); //clean d_out
        dim3 blocks_tiled_sh(N/K,N/K);
	dim3 threads_tiled_sh(K,K);
        timer.Start();
	transpose_parallel_per_element_tiled_shared<<<blocks_tiled_sh,threads_tiled_sh>>>(d_in, d_out);
	timer.Stop();
        for (int i=0; i < N*N; ++i){out[i] = 0.0;}
	cudaMemcpy(out, d_out, numbytes, cudaMemcpyDeviceToHost);
	printf("transpose_parallel_per_element_tiled_shared %dx%d: %g ms.\nVerifying ...%s\n", 
		   K, K, timer.Elapsed(), compare_matrices(out, gold, N) ? "Failed" : "Success");

	cudaFree(d_in);
	cudaFree(d_out);
}

