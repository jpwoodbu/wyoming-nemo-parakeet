import os
BAZEL_DATA_FILES = os.environ.get('BAZEL_DATA_FILES', None)
if BAZEL_DATA_FILES:
    from python.runfiles import runfiles
    r = runfiles.Create()
    lib_dirs = {os.path.dirname(r.Rlocation(x)) for x in BAZEL_DATA_FILES.split(' ') if '.so' in x}
    os.environ['LD_LIBRARY_PATH'] = ':'.join(lib_dirs)
    del os.environ['BAZEL_DATA_FILES']
    import sys
    os.environ['PYTHONPATH'] = ':'.join(sys.path)
    os.execv(sys.executable, [sys.executable] + sys.argv)

import torch


if __name__ == '__main__':
    xpu = torch.xpu.is_available()
    print(f"XPU is available: {xpu}")
