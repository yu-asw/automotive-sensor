#!/usr/bin/env bash
set -e
cd "$HOME/d3-g-yocto"
# Keep the known-good tar before /usr/bin when BitBake creates tmp/hosttools.
export PATH="$HOME/yocto-tools/tar-1.34/bin:$PATH"
export TEMPLATECONF="$PWD/poky/meta-topst/template/d3-g-topst-main"
source poky/oe-init-build-env build/d3-g-topst-ros2 >/dev/null
if [ "$#" -eq 0 ]; then set -- yu-ros2-image; fi
exec bitbake "$@"
