Similar to https://gist.github.com/EricCousineau-TRI/827bd669da73c76a0d793464bd46cb82#file-debian_source_trace_pyassimp-sh, but for 
Jammy.

```sh
sudoedit /etc/apt/sources.list
# Uncomment: deb-src http://us.archive.ubuntu.com/ubuntu/ jammy universe

mkcd() { mkdir "$@" && cd "${!#}"; }

sudo apt update
mkcd -p /tmp/assimp-src/jammy
apt-get source python3-pyassimp
# see patches applied (below)
cd assimp-5.2.2~ds0
deb_dir=${PWD}  # Record absdir
patch_dir=${deb_dir}/debian/patches

# Go to this repo.
cd .../assimp
git am ${patch_dir}/pyassimp.patch ${patch_dir}/pyassimp_faces.patch
```

```
dpkg-source: info: using patch list from debian/patches/series
dpkg-source: info: applying drop-stripped-sources.patch
dpkg-source: info: applying use-system-utf8cpp.patch
dpkg-source: info: applying use-system-stb_image.patch
dpkg-source: info: applying use-system-libdraco.patch
dpkg-source: info: applying use-system-minizip.patch
dpkg-source: info: applying pyassimp.patch
dpkg-source: info: applying pyassimp_faces.patch
dpkg-source: info: applying doxygen.patch
```
