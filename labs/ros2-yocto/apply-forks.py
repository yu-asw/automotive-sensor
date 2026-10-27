#!/usr/bin/env python3
"""Select pinned personal forks only while both D3 build servers are stopped."""
from pathlib import Path
import fcntl
import json
import subprocess
import xml.etree.ElementTree as ET

work = Path.home() / 'd3-g-yocto'
lockdata = json.loads(Path(__file__).with_name('forks.json').read_text())
locks = []
for build in ('d3-g-topst-main', 'd3-g-topst-ros2'):
    lockpath = work / 'build' / build / 'bitbake.lock'
    if lockpath.exists():
        f = lockpath.open('r+')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('Stop the active BitBake server before selecting forks: ' + build)
        locks.append(f)

def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args], text=True).strip()

manifest = ET.Element('manifest')
ET.SubElement(manifest, 'remote', name='hulryung', fetch='https://github.com/hulryung')
for path, item in lockdata.items():
    ET.SubElement(manifest, 'extend-project', name=Path(path).name,
                  path=path, remote='hulryung', revision=item['revision'],
                  upstream='refs/heads/' + item['branch'], **{'dest-branch': item['branch']})
ET.indent(manifest)
output = work / '.repo/local_manifests/yu-ros2-forks.xml'
output.parent.mkdir(parents=True, exist_ok=True)
content = ET.tostring(manifest, encoding='unicode') + '\n'
if output.exists() and output.read_text() != content:
    raise SystemExit('Existing local manifest differs; inspect before overwriting: ' + str(output))

# Validate every target before changing any checkout.
for path, item in lockdata.items():
    repo = work / path
    if git(repo, 'status', '--porcelain', '--untracked-files=no'):
        raise SystemExit('Tracked local edits must be preserved manually: ' + str(repo))
    if git(repo, 'rev-parse', 'HEAD') not in (item['base'], item['revision']):
        raise SystemExit('Unexpected source revision; inspect first: ' + str(repo))
    if 'hulryung' in git(repo, 'remote').splitlines():
        if git(repo, 'remote', 'get-url', 'hulryung') != item['url']:
            raise SystemExit('Existing hulryung remote has a different URL: ' + str(repo))

for path, item in lockdata.items():
    repo = work / path
    if 'hulryung' not in git(repo, 'remote').splitlines():
        git(repo, 'remote', 'add', 'hulryung', item['url'])
    git(repo, 'fetch', '--no-tags', 'hulryung', item['revision'])
    git(repo, 'checkout', '--detach', item['revision'])
    print(path, git(repo, 'rev-parse', 'HEAD'))

output.write_text(content)
print('Pinned personal forks in', output)
