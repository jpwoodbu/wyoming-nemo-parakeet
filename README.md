# Wyoming NeMo Parakeet

A Wyoming protocol server for NVIDIA NeMo Parakeet that runs on Intel GPUs.

## Setup without Docker

Follow the [Software Prerequisite](https://docs.pytorch.org/docs/stable/notes/get_start_xpu.html#software-prerequisite) instructions for using PyTorch on Intel GPUs before proceeding to install Python dependencies.

**IMPORTANT**: The `requirements.txt` file must be processed first when installing dependencies. Those dependencies come from the **PyTorch** repo and provide the Intel XPU specific versions.

From the project root:
```sh
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
$ pip install .
```

### Running the server

```sh
$ . .venv/bin/activate
$ python -m wyoming_nemo_parakeet
```

## Setup with Docker

Build the Docker image:
```sh
$ docker build . -t jpwoodbu/wyoming-nemo-parakeet
```

Modify the `docker-compose.yaml` file to suit your needs and system. In particular, set the group ID under `group_add` to match your system's `render` group ID to facilitate GPU acceleration. To find it, run:
```sh
$ getent group render | cut -d: -f3
```

### Running the server

```sh
$ docker compose up -d
```

**NOTE:** It usually takes a minute or so before the server is ready to serve requests; more time if it's the first time it's run and it needs to download the model.

## Roadmap
* Make running on Intel GPUs optional
* Add application logging
* Add flags for things like where to store the model, what address and port to listen on, etc.
* Reduce or eliminate the **very** noisy NeMo logging
