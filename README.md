# Wyoming Parakeet

A Wyoming protocol server for NVIDIA Parakeet. This project is currently configured to only run on CPUs, not GPUs. As a reference, on my Ryzen 5500, most Home Assistant related commands, _e.g. "Turn off the light"_, are transcribed in about 200ms. I initially planned to have GPU support, but at this time, at least for me, the latency while running on the CPU is adequate.

## Setup without Docker

From the project root:
```sh
python3 -m venv .venv
. .venv/bin/activate
pip install .
```

### Running the server

```sh
. .venv/bin/activate
python -m wyoming_parakeet
```

To see flags, run:
```sh
python -m wyoming_parakeet --help
```

## Setup with Docker

Build the Docker image:
```sh
docker build . -t jpwoodbu/wyoming-parakeet
```

### Running the server

Modify the `docker-compose.yaml` file to suit your needs and system.

```sh
docker compose up -d
```
