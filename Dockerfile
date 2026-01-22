FROM python:3.13-slim

WORKDIR /app

# Create and activate virtual environment
RUN python -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

RUN pip install --upgrade pip && \
    pip install .

# Set up a cache directory for models that is writable by any user
ENV XDG_CACHE_HOME=/models
RUN mkdir -p /models && chmod 1777 /models

ENTRYPOINT ["python", "-m", "wyoming_parakeet"]
