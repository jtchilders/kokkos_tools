
module load cmake/3.23.2 gcc/11.1.0

export CUDA_HOME=/soft/compilers/cuda/cuda-11.8.0

export INSTPATH=install_v100
export KOKKOS_HOME=/home/jchilders/git/kokkos/$INSTPATH
export KOKKOSKERNELS_HOME=/home/jchilders/git/kokkos-kernels/$INSTPATH
export CMAKE_PREFIX_PATH=$KOKKOS_HOME/lib64/cmake/Kokkos:$KOKKOSKERNELS_HOME/lib64/cmake/KokkosKernels
export LD_LIBRARY_PATH=$KOKKOS_HOME/lib:$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export PATH=$KOKKOS_HOME/bin:$CUDA_HOME/bin:$PATH

source $HOME/gdb-13.1/setup.sh