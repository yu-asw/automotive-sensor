#!/usr/bin/env bash
# A persistent, logged build suitable for nohup on the VM.
set -uo pipefail
logdir="${1:?Usage: build-job.sh NEW_LOG_DIRECTORY}"
mkdir -p "$logdir"
if [ -e "$logdir/build.log" ]; then
    echo "Refusing to overwrite an existing build log" >&2
    exit 2
fi
date -Is > "$logdir/started.txt"
python3 - "$HOME/d3-g-yocto/run-build.sh" > "$logdir/build.log" 2>&1 <<'PYRUN'
import os
import signal
import sys
# Background shells can inherit ignored SIGINT; allow a clean BitBake stop.
signal.signal(signal.SIGINT, signal.SIG_DFL)
os.execv(sys.argv[1], [sys.argv[1], 'yu-ros2-image'])
PYRUN
result=$?
printf '%s\n' "$result" > "$logdir/exit-code.txt"
date -Is > "$logdir/finished.txt"
exit "$result"
