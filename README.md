# kokkos_tools
A place for my Kokkos build scripts for various systems and apps

The `build_kokkos.py` has a command line interface so use `-h` to get a hopefully explanatory dump.

# JLSE Notes

I used this to build multiple kokkos versions for each architecture.

## Skylake 8180

``` bash
/gpfs/jlse-fs0/projects/datascience/parton/conda/2022-03/bin/python build_kokkos.py -t /projects/datascience/parton/kokkos/ -a Kokkos_ARCH_SKX -b /home/jchilders/git/my_kokkos_tools/env_scripts/alcf_jlse/skylake_8180.v02.sh -r Release
```

## NVidia V100
```bash
gpfs/jlse-fs0/projects/datascience/parton/conda/2022-03/bin/python build_kokkos.py -t /projects/datascience/parton/kokkos -a Kokkos_ARCH_VOLTA70 -b /home/jchilders/git/my_kokkos_tools/env_scripts/alcf_jlse/gpu_v100_smx2.v02.sh -r Release
```

## NVidia A100
```bash
/gpfs/jlse-fs0/projects/datascience/parton/conda/2022-03/bin/python build_kokkos.py -t /projects/datascience/parton/kokkos/ -a Kokkos_ARCH_AMPERE80 -b /home/jchilders/git/my_kokkos_tools/env_scripts/alcf_jlse/gpu_a100.v02.sh -r Release
```

## AMD MI250
```bash
/gpfs/jlse-fs0/projects/datascience/parton/conda/2022-03/bin/python build_kokkos.py -t /projects/datascience/parton/kokkos/ -a Kokkos_ARCH_VEGA90A -b /home/jchilders/git/my_kokkos_tools/env_scripts/alcf_jlse/gpu_amd_mi250.v01.sh -r Release
```