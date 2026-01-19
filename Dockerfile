# The Intel GPU deps document that they require Ubuntu 25.04.
FROM ubuntu:plucky

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository -y ppa:kobuk-team/intel-graphics && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3.13-dev \
        python3-pip \
        python3-venv \
        libze-intel-gpu1 \
        libze1 \
        intel-metrics-discovery \
        intel-opencl-icd \
        clinfo \
        intel-gsc \
        libze-dev \
        intel-ocloc \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3.13 -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install .

# Set up a cache directory for models that is writable by any user
ENV XDG_CACHE_HOME=/models
RUN mkdir -p /models && chmod 1777 /models

ENTRYPOINT ["python", "-m", "wyoming_nemo_parakeet"]
