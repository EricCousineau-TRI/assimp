#!/bin/bash
set -eux

# Applies Debian patches.

cd $(dirname ${BASH_SOURCE})

# Should use the following branch:
# 

patch_dir=./debian/patches
patch_relpaths=$(cat ${patch_dir}/series)
patch_files=()
for relpath in ${patch_relpaths}; do
    patch_file=${patch_dir}/${relpath}
    patch_files+=(${patch_file})
done

# git am struggles :( So just use patch.
git apply ${patch_files[@]}
git add -A :/
git commit -m "[hack] Apply Debian patches"
