

BASEPATH=$1
if [ "$#" -ne 1 ]; then
   BASEPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
fi
echo using BASEPATH=$BASEPATH

module load cmake/3.27.2 gcc/12.2.0
module swap cuda cuda/12.3.0

export INSTPATH=install
export KOKKOS_HOME=$BASEPATH/kokkos/$INSTPATH
export KOKKOSKERNELS_HOME=$BASEPATH/kokkos-kernels/$INSTPATH
export CMAKE_PREFIX_PATH=$KOKKOS_HOME/lib64/cmake/Kokkos:$KOKKOSKERNELS_HOME/lib64/cmake/KokkosKernels
export LD_LIBRARY_PATH=$KOKKOS_HOME/lib:$LD_LIBRARY_PATH
export PATH=$KOKKOS_HOME/bin:$PATH
