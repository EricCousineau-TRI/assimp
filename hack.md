# Hacks for Ubuntu Jammy (22.04) and Bazel Consumption

Relates https://gist.github.com/EricCousineau-TRI/827bd669da73c76a0d793464bd46cb82#file-debian_source_trace_pyassimp-sh

Painful to reconcile differences in functionality between v5.0.1 (used for
Ubuntu Focal (20.04)) and v5.2.2 (used for Ubuntu Jammy (22.04)).

Just rebuild known working version (Debian-patched v5.0.1) for Jammy.

## Generate Patches and Commit

*Note*: This is only for *documentation purposes*. These patches already live
on this branch, in addition to other functionality changes.

```sh
git clone https://salsa.debian.org/debian/assimp
cd assimp
git checkout -b feature-v5.0.1-deb-patch-for-bazel debian/5.0.1_ds0-1
./hack_apply_debian_patches.sh
```

## Build Tarball

```sh
./hack_build_for_bazel.sh
```
