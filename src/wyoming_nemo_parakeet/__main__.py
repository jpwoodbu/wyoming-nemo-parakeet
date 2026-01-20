import argparse
import asyncio
from functools import partial
import logging

# Set the root logging level to ERROR so suppress noisy third party loggers,
# which also log messages during import.
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s",
)

from nemo.utils import logging as nemo_logging
# NeMo logging has very noisy WARNING messages, even at import time.
nemo_logging.setLevel(logging.ERROR)
from nemo.collections import asr
from wyoming import server as wyoming_server

from wyoming_nemo_parakeet import handler


_LOGGER = logging.getLogger(__package__)


async def start(uri: str, use_xpu: bool) -> None:
    # The handler seems to get re-created for every request, so we need to do
    # the expensive work of loading the model ahead and time and pass it in.
    _LOGGER.info("Loading model...")
    model = asr.models.ASRModel.from_pretrained(
        model_name=f"{handler.REPO_ID}/{handler.MODEL_ID}"
    )
    # The return type for the function call above seems to be set
    # incorrectly.
    if use_xpu:
        _LOGGER.info("Configuring model to use Intel GPU")
        model = model.to("xpu")  # type: ignore
    _LOGGER.info("Model loaded")

    model_lock = asyncio.Lock()
    server = wyoming_server.AsyncServer.from_uri(uri)
    await server.run(partial(handler.ParakeetEventHandler, model, model_lock))


def main() -> None:
    # Since this package is the entrypoint for this app, it gets to use INFO
    # logging.
    _LOGGER.setLevel(logging.INFO)
    # Workaround for NeMo changing its logger's level at call time! Don't do
    # that!
    nemo_logging._logger.setLevel = lambda verbosity_level: None  # type: ignore

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

    try:
        asyncio.run(start(args.uri, args.use_xpu))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
