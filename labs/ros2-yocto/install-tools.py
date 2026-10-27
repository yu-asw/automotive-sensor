#!/usr/bin/env python3
"""Install the course tools into an existing D3 SDK without replacing local edits."""
from pathlib import Path
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--workspace', type=Path, default=Path.home() / 'd3-g-yocto')
parser.add_argument('--check', action='store_true', help='Validate and list copies without writing')
args = parser.parse_args()
source = Path(__file__).resolve().parent
work = args.workspace.expanduser().resolve()
# The wrappers and configuration generator currently use this fixed SDK location.
if work != (Path.home() / 'd3-g-yocto').resolve():
    raise SystemExit('This version requires the SDK at ~/d3-g-yocto.')
for relative in ('poky/oe-init-build-env', 'build/d3-g-topst-main/conf/local.conf',
                 'build/d3-g-topst-main/conf/bblayers.conf'):
    if not (work / relative).is_file():
        raise SystemExit('Missing previous-lesson SDK file: ' + str(work / relative))
if not (Path.home() / 'yocto-tools/tar-1.34/bin/tar').is_file():
    raise SystemExit('Missing course host prerequisite: ~/yocto-tools/tar-1.34/bin/tar. Ask the instructor to prepare the build host.')
names = ('run-build.sh', 'build-job.sh', 'forks.json', 'apply-forks.py',
         'prepare-build.py', 'verify-image.py', 'qemu-smoke.py', 'package-fwdn.py')
pairs = [(source / n, work / n) for n in names]
pairs += [(p, work / 'layers/meta-yu-ros2' / p.relative_to(source / 'meta-yu-ros2'))
          for p in sorted((source / 'meta-yu-ros2').rglob('*')) if p.is_file()]
if not (source / 'meta-yu-ros2/conf/layer.conf').is_file():
    raise SystemExit('Download the complete labs/ros2-yocto directory, including meta-yu-ros2.')
# Validate the complete operation before copying anything.
for src, dst in pairs:
    if not src.is_file():
        raise SystemExit('Incomplete download: ' + str(src))
    if dst.is_symlink() or (dst.exists() and (not dst.is_file() or dst.read_bytes() != src.read_bytes())):
        raise SystemExit('Existing file differs. Preserve and review it before installing: ' + str(dst))
for src, dst in pairs:
    if not args.check:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(src, dst)
        if dst.suffix == '.sh':
            dst.chmod(dst.stat().st_mode | 0o100)
    print(('CHECK ' if args.check else 'READY ') + str(dst))
print('No build was started and no source revision was changed.')
