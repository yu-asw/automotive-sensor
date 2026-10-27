#!/usr/bin/env python3
"""Reuse TOPST's packager in an isolated staging tree; never flash a device."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('rootfs', type=Path, help='Completed ROS 2 ext4 in the new deploy directory')
parser.add_argument('output', type=Path, help='New staging/output directory (must not exist)')
args = parser.parse_args()
work = Path.home() / 'd3-g-yocto'
deploy = work / 'build/d3-g-topst-ros2/tmp/deploy/images/d3-g-topst-main'
rootfs = args.rootfs.resolve(strict=True)
if rootfs.parent != deploy.resolve() or not rootfs.name.startswith('yu-ros2-image'):
    raise SystemExit('Rootfs must be the new ROS 2 image, not the original build.')
inputs = {
    'ca72_bl3.rom': deploy / 'ca72_bl3.rom',
    'tc-boot-d3-g-topst-main.img': deploy / 'tc-boot-d3-g-topst-main.img',
    'tcc8050-topst-d3-g.dtb': deploy / 'tcc8050-topst-d3-g.dtb',
    'telechips-topst-image-d3-g-topst-main.ext4': rootfs,
}
for path in inputs.values():
    if not path.is_file():
        raise SystemExit('Missing packaging input: ' + str(path))
# Reject oversized inputs before invoking the vendor packager.
for line in (work / 'tools/partition.single.list.d3').read_text().splitlines():
    match = re.fullmatch(r'([^:]+):(\d+)([KMG])@(.+)', line.strip())
    if not match:
        raise SystemExit('Unsupported partition entry: ' + line)
    partition, size, unit, filename = match.groups()
    source = inputs.get(Path(filename).name)
    if source is None:
        raise SystemExit('Unknown partition input: ' + filename)
    capacity = int(size) * 1024 ** {'K': 1, 'M': 2, 'G': 3}[unit]
    if source.stat().st_size > capacity:
        raise SystemExit('Image exceeds partition capacity: ' + partition)
output = args.output.resolve()
output.mkdir(parents=True, exist_ok=False)
# The vendor script locates an SDK root by the .repo directory. This marker
# belongs only to the packaging sandbox; no repo commands are executed here.
(output / '.repo').mkdir()
(output / 'tools').mkdir()
(output / 'tools/fwdn_d3').symlink_to(work / 'tools/fwdn_d3', target_is_directory=True)
shutil.copy2(work / 'tools/partition.single.list.d3', output / 'tools/partition.single.list.d3')
shutil.copy2(work / 'tools/stitch-fai-d3.sh', output / 'stitch-fai-d3.sh')
staged = output / 'build/d3-g-topst-main/tmp/deploy/images/d3-g-topst-main'
staged.mkdir(parents=True)
metadata = {}
for name, source in inputs.items():
    source = source.resolve(strict=True)
    (staged / name).symlink_to(source)
    digest = hashlib.sha256()
    with source.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(chunk)
    metadata[name] = {'source': str(source), 'sha256': digest.hexdigest()}
(output / 'inputs.json').write_text(json.dumps(metadata, indent=2) + '\n')
with (output / 'packaging.log').open('w') as log:
    subprocess.run(['bash', './stitch-fai-d3.sh', '-f', 'yu_ros2_d3g'], cwd=output,
                   stdout=log, stderr=subprocess.STDOUT, check=True)
archive = output / 'yu_ros2_d3g.fwdn.zip'
with zipfile.ZipFile(archive) as z:
    bad = z.testzip()
    if bad:
        raise SystemExit('ZIP CRC check failed: ' + bad)
    required = {'yu_ros2_d3g.fai', 'fwdn', 'fwdn.sh', 'fwdn.bat'}
    if not required.issubset(z.namelist()):
        raise SystemExit('Missing required FWDN package members')
print('PASS: FWDN archive CRC and required members:', archive)
print('No device was flashed; hardware validation remains pending.')
