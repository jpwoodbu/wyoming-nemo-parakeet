# Wyoming NeMo Parakeet

A Wyoming protocol server for NVIDIA NeMo Parakeet that runs on Intel GPUs.

## Setup

**IMPORTANT**: The `requirements.txt` file must be processed first when installing dependencies. Those dependencies come from the **PyTorch** repo and provide the Intel XPU specific versions.

From the project root:
```sh
$ python3 -m venv .venv
$ pip install -r requirements.txt
$ pip install .
```

## Running the server

From the `src` directory:
```sh
$ python -m wyoming_nemo_parakeet
```
