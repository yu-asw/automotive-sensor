#!/usr/bin/env python3
"""Exercise ARM64 demo binaries under user-mode QEMU; not a D3 boot test."""
import argparse
from pathlib import Path
import re
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('qemu', type=Path)
parser.add_argument('root', type=Path, help='Extracted rootfs directory')
parser.add_argument('logs', type=Path, help='New output directory')
args = parser.parse_args()
qemu, root = args.qemu.resolve(), args.root.resolve()
args.logs.mkdir(parents=True, exist_ok=False)
common = [str(qemu), '-L', str(root)]
for value in ('LD_LIBRARY_PATH=/opt/ros/humble/lib:/usr/lib:/lib',
              'AMENT_PREFIX_PATH=/opt/ros/humble', 'ROS_DISTRO=humble',
              'ROS_VERSION=2', 'RMW_IMPLEMENTATION=rmw_fastrtps_cpp',
              'ROS_LOCALHOST_ONLY=1', 'ROS_DOMAIN_ID=97'):
    common += ['-E', value]
processes = []
files = []
try:
    for node in ('listener', 'talker'):
        executable = root / 'opt/ros/humble/lib/demo_nodes_cpp' / node
        if not executable.is_file():
            raise SystemExit('Missing executable: ' + str(executable))
        log = (args.logs / (node + '.log')).open('w')
        files.append(log)
        processes.append(subprocess.Popen(common + [str(executable)], stdout=log, stderr=subprocess.STDOUT))
    deadline = time.monotonic() + 25
    while time.monotonic() < deadline:
        if any(p.poll() is not None for p in processes):
            raise SystemExit('A demo process exited early; inspect logs.')
        received = (args.logs / 'listener.log').read_text(errors='replace')
        if len(re.findall(r'I heard:', received)) >= 3:
            print('PASS: listener received at least 3 messages from ARM64 talker under QEMU')
            break
        time.sleep(0.5)
    else:
        raise SystemExit('No confirmed message exchange within 25 seconds; inspect logs.')
finally:
    for p in processes:
        if p.poll() is None:
            p.terminate()
    for p in processes:
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
    for f in files:
        f.close()
