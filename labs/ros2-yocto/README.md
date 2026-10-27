# D3-G ROS 2 Yocto lab

These are **course-provided scripts**, not commands shipped by Telechips or Yocto.
They extend the D3-G image built in the previous class with ROS 2 Humble and a USB camera node.

Status: integration material under validation. Hardware boot and camera tests remain pending. Use an instructor-validated image for deployment.

## Prerequisites

Run these commands on the **Ubuntu build host**, not on the D3 board or a Windows/macOS terminal.

- An existing TOPST D3-G SDK at `~/d3-g-yocto`, using the previous lesson's pinned baseline.
- Existing `build/d3-g-topst-main/conf/local.conf` and `bblayers.conf`, with paths valid for your user.
- Git, Python 3.10+ and the previous lesson's Yocto host dependencies.
- The course host workaround at `~/yocto-tools/tar-1.34/bin/tar`. If it is absent, ask the instructor to prepare the host. These scripts do not replace system tar.
- Sufficient disk space for another build. The configuration stops new tasks below 5 GiB free and halts below 1 GiB.
- No active BitBake build/server while installing files or switching source revisions. Coordinate with the instructor on shared hosts.

The scripts currently require the SDK location above. They refuse unexpected source revisions or conflicting files. Do not delete those checks to force installation.

## 1. Download the complete lab

No GitHub login is required for this public repository:

```bash
cd ~
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/yu-asw/automotive-sensor.git automotive-sensor-labs
cd automotive-sensor-labs
git sparse-checkout set labs/ros2-yocto
git rev-parse HEAD
```

Save the displayed commit ID with your lab results. If that directory already exists, inspect it instead of cloning over it.

Alternatively, open https://github.com/yu-asw/automotive-sensor and choose **Code → Download ZIP**, extract it on the build host, and use its `labs/ros2-yocto` directory below.

## 2. Check and install the course files

From the downloaded repository root:

```bash
python3 labs/ros2-yocto/install-tools.py --check
python3 labs/ros2-yocto/install-tools.py
```

The installer copies the scripts and `meta-yu-ros2` layer into the SDK. It makes shell wrappers executable, preserves differing existing files by refusing to overwrite them, and does not launch a build.

## 3. Prepare meta-ros and the pinned forks

For a host that does not already contain `layers/meta-ros`:

```bash
cd ~/d3-g-yocto
mkdir -p layers
git clone --branch kirkstone https://github.com/ros/meta-ros.git layers/meta-ros
git -C layers/meta-ros checkout --detach \
  446dd9e3f26fe8a6594671b5b865872b4199f16c
python3 apply-forks.py
python3 prepare-build.py
```

If meta-ros already exists, check its revision and local edits with the instructor rather than recloning or discarding changes. `apply-forks.py` selects the pinned personal Poky and meta-openembedded fixes in `forks.json` and records a repo local manifest. It changes source checkouts, but leaves the previous image and build configuration intact.

`prepare-build.py` creates **`build/d3-g-topst-ros2`**. If that build configuration already exists, inspect/reuse it instead of running setup again. The old downloads and sstate cache are shared.

## 4. Run the build

```bash
cd ~/d3-g-yocto
./run-build.sh -n yu-ros2-image
./run-build.sh yu-ros2-image
```

`run-build.sh` selects the course tar PATH, sources `poky/oe-init-build-env` for the separate ROS build, and runs BitBake. The `-n` command is a dry run, not a compilation test. Check the final exit code and errors.

A persistent build can use a new log directory:

```bash
nohup ./build-job.sh "$HOME/yocto-logs/ros2-student-01" \
  > "$HOME/ros2-student-01-launch.log" 2>&1 &
```

Do not start this while another build is running. The log directory must be new. Inspect its `build.log`, then `exit-code.txt` after completion.

## 5. Verify before deploying

Output directory:

```text
~/d3-g-yocto/build/d3-g-topst-ros2/tmp/deploy/images/d3-g-topst-main/
```

Use `verify-image.py MANIFEST ROOTFS_EXT4` with the actual generated paths after a successful build. `package-fwdn.py ROOTFS_EXT4 NEW_OUTPUT_DIRECTORY` stages the new image separately. Both require their existing host dependencies. Neither command flashes a board.

Follow the previous class's board-specific FWDN procedure only after the instructor checks the archive. A successful build does not establish boot, DDS communication or camera capture.

## Files and scope

| File | Purpose |
|---|---|
| `install-tools.py` | Check and copy course tools into the existing SDK |
| `run-build.sh` | Select the ROS build environment and invoke BitBake |
| `build-job.sh` | Record a persistent build's log and exit status |
| `apply-forks.py`, `forks.json` | Select and record exact personal-fork source revisions |
| `prepare-build.py` | Create the separate ROS build configuration |
| `meta-yu-ros2/` | Image recipe and D3 OpenCV configuration |
| `verify-image.py` | Check packages and ARM64 executable in the image |
| `qemu-smoke.py` | Optional user-mode QEMU talker/listener check |
| `package-fwdn.py` | Package the new image using existing TOPST tools |

The repository does not include the vendor SDK, proprietary firmware, generated images or private network configuration. This retains the existing BSP's Kirkstone release. The [meta-ros Kirkstone branch](https://github.com/ros/meta-ros/tree/kirkstone) is unsupported. General source-location fixes live in [hulryung/poky](https://github.com/hulryung/poky) and [hulryung/meta-openembedded](https://github.com/hulryung/meta-openembedded).
