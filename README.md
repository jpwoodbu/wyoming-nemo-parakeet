# Wyoming Parakeet

A Wyoming protocol server for NVIDIA Parakeet.

**IMPORTANT:** This project is transitioning from running Parakeet on the [NeMo framework](https://github.com/NVIDIA-NeMo/NeMo) to running on [onnx-asr](https://github.com/istupakov/onnx-asr).

**NOTE:** This project is also transitioning from primarily targetting execution on Intel GPUs to primarily targetting execution on CPUs with asperational support for Intel GPUs (and perhaps other GPUs too).

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

To see flags, run:
```sh
$ python -m wyoming_nemo_parakeet --help
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
