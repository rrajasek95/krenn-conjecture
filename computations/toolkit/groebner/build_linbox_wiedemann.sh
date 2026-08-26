#!/bin/zsh
set -euo pipefail

repo_root=${0:A:h:h:h:h}
prefix="$repo_root/computations/toolkit/vendor/prefix-x86"
source_file="$repo_root/computations/toolkit/groebner/linbox_parallel_wiedemann.cpp"
output_file="$repo_root/computations/toolkit/groebner/linbox_parallel_wiedemann"

export PKG_CONFIG_PATH="$prefix/lib/pkgconfig"
cflags="$(pkg-config --cflags linbox)"
libs="$(pkg-config --libs linbox)"
clang++ -arch x86_64 -std=c++17 -O3 -DNDEBUG ${=cflags} \
  -UDISABLE_COMMENTATOR -Xpreprocessor -fopenmp \
  -I/usr/local/opt/libomp/include "$source_file" -o "$output_file" \
  ${=libs} -L/usr/local/opt/libomp/lib -lomp -framework Accelerate
file "$output_file"
