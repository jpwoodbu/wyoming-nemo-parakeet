import argparse
import asyncio
from functools import partial
import logging

from nemo.collections import asr
from wyoming import server as wyoming_server

from wyoming_nemo_parakeet import handler


_LOGGER = logging.getLogger(__name__)


async def start() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--uri",
        default="tcp://0.0.0.0:10300",
        help="URI the Wyoming server should listen on",
    )
    parser.add_argument(
        "--use_xpu", action="store_true", help="Run model on Intel GPU"
    )
    args = parser.parse_args()

    # The handler seems to get re-created for every request, so we need to do
    # the expensive work of loading the model ahead and time and pass it in.
    model = asr.models.ASRModel.from_pretrained(
        model_name=f"{handler.REPO_ID}/{handler.MODEL_ID}"
    )
    # The return type for the function call above seems to be set
    # incorrectly.
    if args.use_xpu:
        _LOGGER.info("Loading model onto Intel GPU")
        model = model.to("xpu")  # type: ignore
    _LOGGER.info("model loaded")

    model_lock = asyncio.Lock()
    server = wyoming_server.AsyncServer.from_uri(args.uri)
    await server.run(partial(handler.ParakeetEventHandler, model, model_lock))


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
