import os


BAZEL_DATA_FILES = os.environ.get("BAZEL_DATA_FILES", None)


if BAZEL_DATA_FILES:
    from python.runfiles import runfiles

    r = runfiles.Create()
    lib_dirs = {
        os.path.dirname(r.Rlocation(x))
        for x in BAZEL_DATA_FILES.split(" ")
        if ".so" in x
    }
    os.environ["LD_LIBRARY_PATH"] = ":".join(lib_dirs)
    del os.environ["BAZEL_DATA_FILES"]
    import sys

    # Restart the Python process so that the dynamic linker to can see the
    # changes made to LD_LIBRARY_PATH.
    os.environ["PYTHONPATH"] = ":".join(sys.path)
    os.execv(sys.executable, [sys.executable] + sys.argv)


import asyncio
from functools import partial
import logging

from nemo.collections import asr
from wyoming import server as wyoming_server

from src.wyoming_nemo_parakeet import handler


_LOGGER = logging.getLogger(__name__)


async def start() -> None:
    # The handler seems to get re-created for every request, so we need to do
    # the expensive work of loading the model ahead of time and pass it in.
    model = asr.models.ASRModel.from_pretrained(
        model_name=f"{handler.REPO_ID}/{handler.MODEL_ID}"
    )
    # TODO(jpwoodbu) Make using an Intel GPU optional.
    # The return type for the function call above seems to be set
    # incorrectly.
    model = model.to("xpu")  # type: ignore
    model_lock = asyncio.Lock()
    _LOGGER.info("model loaded")
    # TODO(jpwoodbu) Make the uri a flag.
    server = wyoming_server.AsyncServer.from_uri("tcp://0.0.0.0:10300")
    await server.run(partial(handler.ParakeetEventHandler, model, model_lock))


def main() -> None:
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
