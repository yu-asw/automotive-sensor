#!/usr/bin/env python3
"""Static acceptance checks on a completed Yocto image, not a board boot test."""
from pathlib import Path
import argparse
import hashlib
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('manifest', type=Path)
parser.add_argument('rootfs', type=Path)
args = parser.parse_args()
packages = {line.split()[0] for line in args.manifest.read_text().splitlines() if line.strip()}
required = {'ros-workspace', 'ros-environment', 'demo-nodes-cpp', 'ros2cli', 'ros2run',
            'ros2node', 'ros2topic', 'ros2param', 'ros2interface', 'ros2launch',
            'rmw-fastrtps-cpp', 'v4l2-camera', 'v4l-utils', 'usbutils'}
missing = required - packages
if missing:
    raise SystemExit('Missing packages: ' + ', '.join(sorted(missing)))
print('PASS: required packages in manifest')
for name in ('local_setup.sh', 'bin/ros2', 'lib/demo_nodes_cpp/talker',
             'lib/demo_nodes_cpp/listener', 'lib/v4l2_camera/v4l2_camera_node'):
    path = '/opt/ros/humble/' + name
    result = subprocess.run(['debugfs', '-R', 'stat ' + path, str(args.rootfs)],
                            text=True, capture_output=True, check=True)
    if 'Inode:' not in result.stdout:
        raise SystemExit('Missing rootfs file: ' + path + '\n' + result.stderr)
    print('PASS:', path)
with tempfile.TemporaryDirectory() as directory:
    executable = Path(directory) / 'talker.elf'
    subprocess.run(['debugfs', '-R', f'dump /opt/ros/humble/lib/demo_nodes_cpp/talker {executable}',
                    str(args.rootfs)], check=True, capture_output=True)
    header = subprocess.check_output(['readelf', '-h', str(executable)], text=True)
    if 'AArch64' not in header:
        raise SystemExit('Talker is not an AArch64 executable')
    print('PASS: talker ELF machine AArch64')
for path in (args.manifest, args.rootfs):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
    print(digest.hexdigest(), path)
print('Static checks only. Hardware boot, DDS transport, and camera capture remain untested.')
