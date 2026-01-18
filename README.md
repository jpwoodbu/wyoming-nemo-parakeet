# Wyoming NeMo Parakeet

A Wyoming protocol server for NVIDIA NeMo Parakeet that runs on Intel GPUs.

## Setup

Follow the [Software Prerequisite](https://docs.pytorch.org/docs/stable/notes/get_start_xpu.html#software-prerequisite) instructions for using PyTorch on Intel GPUs before proceeding to install Python dependencies.

**IMPORTANT**: The `requirements.txt` file must be processed first when installing dependencies. Those dependencies come from the **PyTorch** repo and provide the Intel XPU specific versions.

From the project root:
```sh
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
$ pip install .
```

## Running the server

From the `src` directory:
```sh
$ python -m wyoming_nemo_parakeet
```

## Roadmap
* Make running on Intel GPUs optional
* Add application logging
* Add flags for things like where to store the model, what address and port to listen on, etc.
* Reduce or eliminate the **very** noisy NeMo logging
* Make a `DockerFile` which builds a container with all the dependencies needed to work on Intel GPUs
