#!/usr/bin/env python
import argparse,logging,subprocess
import os,shutil
from typing import Dict

logger = logging.getLogger(__name__)

DEFAULT_KOKKOS_VERSION="3.7.02"

cuda_arch = [
   "Kokkos_ARCH_VOLTA70",
   "Kokkos_ARCH_AMPERE80",
]



def main():
   """ build kokkos. """
   logging_format = "%(asctime)s %(levelname)s:%(name)s:%(message)s"
   logging_datefmt = "%Y-%m-%d %H:%M:%S"
   logging_level = logging.INFO
   
   parser = argparse.ArgumentParser(description="")
   parser.add_argument("-t","--target",help="target path for installation; note that the kokkos tag and architecture will be appended",required=True)

   parser.add_argument("--kokkos-repo",help="git url for kokkos",default="https://github.com/kokkos/kokkos.git")
   parser.add_argument("--kokkos-tag",help="git url for kokkos",default=DEFAULT_KOKKOS_VERSION)

   parser.add_argument("--kokkos-kernels-repo",help="git url for kokkos",default="https://github.com/kokkos/kokkos-kernels.git")
   parser.add_argument("--kokkos-kernels-tag",help="git url for kokkos",default=DEFAULT_KOKKOS_VERSION,type=str)

   parser.add_argument("--kokkos-tools-repo",help="git url for kokkos",default="https://github.com/kokkos/kokkos-tools.git")
   parser.add_argument("--kokkos-tools-tag",help="git url for kokkos",default="",type=str)

   parser.add_argument("-a","--arch",help="target architecture, e.g.: Kokkos_ARCH_SKX, Kokkos_ARCH_VEGA908, Kokkos_ARCH_AMPERE80",required=True)
   parser.add_argument("-c","--cstd",help="target c++ standard, e.g.: 17, 20, ...",default="17")
   parser.add_argument("-b","--setup-script",help="the setup script to run before building software",required=True)
   parser.add_argument("-r","--build-type",help="the cmake build type, e.g.: DEBUG, Release, RelWithDebInfo ",default="RelWithDebInfo")


   parser.add_argument("--shared-libs", default=False, action="store_true", help="Build shared libraries")

   parser.add_argument("--debug", default=False, action="store_true", help="Set Logger to DEBUG")
   parser.add_argument("--error", default=False, action="store_true", help="Set Logger to ERROR")
   parser.add_argument("--warning", default=False, action="store_true", help="Set Logger to ERROR")
   parser.add_argument("--logfilename" ,default=None,help="if set, logging information will go to file")
   args = parser.parse_args()

   if args.debug and not args.error and not args.warning:
      logging_level = logging.DEBUG
   elif not args.debug and args.error and not args.warning:
      logging_level = logging.ERROR
   elif not args.debug and not args.error and args.warning:
      logging_level = logging.WARNING

   logging.basicConfig(level=logging_level,
                       format=logging_format,
                       datefmt=logging_datefmt,
                       filename=args.logfilename)

   initial_path = os.getcwd()

   shared_libs = "Off"
   if args.shared_libs:
      shared_libs = "On"
   
   # create working directory
   base_install_path = os.path.join(args.target,"kokkos-" + args.kokkos_tag,args.arch)
   prepare_target(base_install_path)
   os.chdir(base_install_path)

   # clone kokkos
   cmake_opts = {
      "Kokkos_ENABLE_CUDA": "On",
      args.arch: "On",
      "CMAKE_CXX_STANDARD": args.cstd,
      "CMAKE_POSITION_INDEPENDENT_CODE": "On",
      "BUILD_SHARED_LIBS": shared_libs,
      "CMAKE_CXX_EXTENSIONS": "On",
      "CMAKE_BUILD_TYPE": args.build_type,
   }
   if args.arch in cuda_arch:
      cmake_opts["Kokkos_ENABLE_CUDA_LAMBDA"] = "On"
      cmake_opts["Kokkos_ENABLE_CUDA_CONSTEXPR"] = "On"
   git_clone(args.kokkos_repo,args.kokkos_tag)
   cmake_build_and_install(base_install_path,
                           args.kokkos_repo,
                           args.setup_script,
                           **cmake_opts
                           )

   # clone kokkos-kernels
   git_clone(args.kokkos_kernels_repo,args.kokkos_kernels_tag)
   cmake_opts = {
      "CMAKE_POSITION_INDEPENDENT_CODE": "On",
      "CMAKE_BUILD_TYPE": args.build_type,
      "CMAKE_CXX_STANDARD": args.cstd,
      "BUILD_SHARED_LIBS": shared_libs,
   }
   # if args.arch in cuda_arch:
   #    cmake_opts["CUDA_TOOLKIT_ROOT_DIR"] = "$CUDA_HOME"
   cmake_build_and_install(base_install_path,
                           args.kokkos_kernels_repo,
                           args.setup_script,
                           **cmake_opts
                           )

   # clone kokkos-tools
   git_clone(args.kokkos_tools_repo,args.kokkos_tools_tag)

   shutil.copyfile(args.setup_script,os.path.join(base_install_path,"setup.sh"))

   os.chdir(initial_path)

def cmake_build_and_install(install_path: str, repo_url: str, setup_script: str, **kwargs: Dict[str, str]):
   repo_name = get_repo_name(repo_url)
   repo_path = os.path.join(install_path, repo_name)
   build_path = os.path.join(repo_path, "build")
   install_dir = os.path.join(repo_path, "install")

   # Prepare the cmake command
   cmake_command = ["cmake", "-S", repo_path, "-B", build_path, "-DCMAKE_INSTALL_PREFIX=" + install_dir]

   # Add kwargs as flags
   for key, value in kwargs.items():
      cmake_command.append(f"-D{key}={value}")

   # Join the cmake command into a single string
   cmake_cmd_str = " ".join(cmake_command)

   # Construct the full command to source the setup script and run the cmake command
   full_cmd = f"source {setup_script} {install_path} && {cmake_cmd_str} && make -j -C {build_path} install"

   # Run the command
   completed = subprocess.run(full_cmd, shell=True, 
                              cwd=repo_path, check=True,
                              stdout=open(f"{repo_name}_cmake_stdout.txt","w"),
                              stderr=open(f"{repo_name}_cmake_stderr.txt","w"))
   if completed.returncode != 0:
      logger.error("cmake for %s returned non-zero value: %d",repo_name,completed.returncode)


def prepare_target(target: str):
   os.makedirs(target,exist_ok=True)

def git_clone(repo_url: str,tag: str = "") -> subprocess.CompletedProcess:
   cmd = ["git","clone"]
   if len(tag) > 0:
      cmd += ["--depth","1", "--branch",tag]
   cmd += [repo_url]

   # dump stdout and stderr to a file that uses the repo name as a base
   repo_name = get_repo_name(repo_url)
   # write stdout
   fout = open(repo_name + "_git_stdout.txt",'w')
   # write stderr
   ferr = open(repo_name + "_git_stderr.txt",'w')

   completed = subprocess.run(cmd,stdout=fout,stderr=ferr)
   if completed.returncode != 0:
      logger.error("git clone returned non-zero value: %d",completed.returncode)
   
   return completed

def get_repo_name(repo_url: str) -> str:
   return repo_url.split("/")[-1].replace(".git", "")

if __name__ == "__main__":
   main()