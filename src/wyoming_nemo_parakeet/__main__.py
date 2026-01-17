import asyncio
from functools import partial
import logging

from nemo.collections import asr
from wyoming import server as wyoming_server

from wyoming_nemo_parakeet import handler


_LOGGER = logging.getLogger(__name__)


async def start() -> None:
    # The handler seems to get re-created for every request, so we need to do
    # the expensive work of loading the model ahead and time and pass it in.
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
