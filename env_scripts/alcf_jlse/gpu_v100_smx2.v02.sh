
if [ "$#" -ne 1 ]; then
   echo must pass base path to script
   exit -1
fi

BASEPATH=$1
echo using BASEPATH=$BASEPATH

module load cmake/3.23.2 gcc/11.1.0
module swap cuda cuda/11.8.0

export INSTPATH=install
export KOKKOS_HOME=$BASEPATH/kokkos/$INSTPATH
export KOKKOSKERNELS_HOME=$BASEPATH/kokkos-kernels/$INSTPATH
export CMAKE_PREFIX_PATH=$KOKKOS_HOME/lib64/cmake/Kokkos:$KOKKOSKERNELS_HOME/lib64/cmake/KokkosKernels
export LD_LIBRARY_PATH=$KOKKOS_HOME/lib:$LD_LIBRARY_PATH
export PATH=$KOKKOS_HOME/bin:$PATH
