#!/bin/bash
set -eux

mkcd() { mkdir "$@" && cd "${!#}"; }

cd $(dirname ${BASH_SOURCE})

# Following debian/rules
mkcd -p build
cmake .. \
    -DCMAKE_INSTALL_PREFIX=${PWD}/install \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_ASSIMP_SAMPLES=OFF \
    -DASSIMP_BUILD_TESTS=OFF \
    -DBUILD_DOCS=OFF \
    -DCMAKE_DEBUG_POSTFIX='' \
    -DASSIMP_ENABLE_BOOST_WORKAROUND=OFF

# Takes a few min to compile and link shared lib.
make -j install

cd install
mkdir -p lib/python3.10/site-packages
cp -r ../../port/PyAssimp/pyassimp lib/python3.10/site-packages/
# # Use symlink if hacking.
# rm -rf lib/python3.10/site-packages/*
# ln -sr ../../port/PyAssimp/pyassimp lib/python3.10/site-packages/
# echo "Bailing early to hack directly."; exit 0

# Generate tarball.
# WARNING: Debian version of shared lib is ~13MB for Focal, ~8MB for Jammy.
# However, this one is ~180MB. Dunno why, but don't really care.
tar cfz ../assimp-5.0.1_ds0-1.tar.gz ./
