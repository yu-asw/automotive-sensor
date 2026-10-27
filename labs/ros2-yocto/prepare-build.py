#!/usr/bin/env python3
"""Run on the existing D3 Yocto host. Preserve the original build directory."""
from pathlib import Path
import json
import shutil
import subprocess

work = Path.home() / 'd3-g-yocto'
base = work / 'build/d3-g-topst-main'
build = work / 'build/d3-g-topst-ros2'
ros = work / 'layers/meta-ros'
revision = '446dd9e3f26fe8a6594671b5b865872b4199f16c'
assert subprocess.check_output(['git', '-C', str(ros), 'rev-parse', 'HEAD'], text=True).strip() == revision
assert (Path.home() / 'yocto-tools/tar-1.34/bin/tar').is_file()
forks = json.loads(Path(__file__).with_name('forks.json').read_text())
for path, item in forks.items():
    actual = subprocess.check_output(['git', '-C', str(work / path), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != item['revision']:
        raise SystemExit('Run apply-forks.py first: ' + path)

if (build / 'conf').exists():
    raise SystemExit('Build configuration already exists; inspect it instead of overwriting.')
(build / 'conf').mkdir(parents=True)
for name in ('local.conf', 'bblayers.conf'):
    shutil.copy2(base / 'conf' / name, build / 'conf' / name)
with (build / 'conf/bblayers.conf').open('a') as f:
    f.write('\nBBLAYERS += " ' + ' '.join(str(p) for p in (
        ros / 'meta-ros-common', ros / 'meta-ros2', ros / 'meta-ros2-humble',
        work / 'layers/meta-yu-ros2')) + ' "\n')
(build / 'conf/auto.conf').write_text(f'''# Isolated ROS 2 test build; original configuration is unchanged.
DL_DIR = "{base}/downloads"
SSTATE_DIR = "{base}/sstate-cache"
BB_NUMBER_THREADS = "2"
PARALLEL_MAKE = "-j 2"
PARALLEL_MAKE:pn-rust-llvm-native = "-j 2"
# Preserve the BSP host tool chain; target zstd remains ROS-selected.
PREFERRED_VERSION_zstd-native = "1.5.2"
ROS_DISTRO = "humble"
# This classroom image does not use Fortran-dependent ROS packages.
ROS_WORLD_SKIP_GROUPS += "fortran"
BB_DISKMON_DIRS = "STOPTASKS,${{TMPDIR}},5G,100K HALT,${{TMPDIR}},1G,10K"
''')
print(build)
