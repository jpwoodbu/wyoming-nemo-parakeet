import asyncio

from wyoming import server as wyoming_server

from wyoming_nemo_parakeet import handler


async def start() -> None:
    # TODO(jpwoodbu) Make the uri a flag.
    server = wyoming_server.AsyncServer.from_uri('tcp:/0.0.0.0:10300')
    await server.run()


def main() -> None:
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
