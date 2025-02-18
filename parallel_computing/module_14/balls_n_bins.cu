#include <thrust/device_vector.h>
#include <thrust/host_vector.h>
#include <thrust/generate.h>
#include <thrust/sort.h> 
#include <thrust/count.h>
#include <thrust/reduce.h>
#include <cstdlib>
#include <cstdio>

struct rand_functor
{
    const int bins;
    rand_functor(int _bins) : bins(_bins) {}
    __host__ __device__
    int operator()() const {
        return rand() % bins;
    }
};

int main(void) {
    for (int n = 2; n <= (1 << 20); n *= 2) {
        thrust::host_vector<int> hv(n);
        thrust::generate(hv.begin(), hv.end(), rand_functor(n));
        thrust::device_vector<int> dv = hv;
        thrust::sort(dv.begin(), dv.end());
        thrust::device_vector<int> bin_counts(n, 0);
        for (int i = 0; i < n; ++i) {
            bin_counts[dv[i]] += 1;
        }

        int max_bin_size = thrust::reduce(bin_counts.begin(), bin_counts.end(), 0, thrust::maximum<int>());

        printf("Max bin capacity for N = %d bins is %d",  n, max_bin_size);
    }

    return 0;
}