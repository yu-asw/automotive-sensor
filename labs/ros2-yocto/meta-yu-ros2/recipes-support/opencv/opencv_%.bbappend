# Camera transport uses CPU image conversion. OE's OpenCL loader/headers
# collide with the TOPST PowerVR providers when both enter the same sysroot.
PACKAGECONFIG:remove:class-target = "opencl"
