"""Event handler for clients of the server."""
from typing import Optional

import asyncio
import logging
import os
import tempfile
import time
import wave

from wyoming import asr
from wyoming import audio
from wyoming import event
from wyoming import info
from wyoming import server


_LOGGER = logging.getLogger(__name__)


REPO_ID = "nvidia"
MODEL_ID = "parakeet-tdt-0.6b-v3"
_URL = f"https://huggingface.co/{REPO_ID}/{MODEL_ID}"

_INFO = info.Info(
    asr=[
        info.AsrProgram(
            name="Parakeet ASR",
            description="NeMo Parakeet transcription",
            attribution=info.Attribution(
                name="Jonathan Woodbury",
                url="https://github.com/jpwoodbu/wyoming-nemo-parakeet",
            ),
            installed=True,
            version="0.0.1",
            models=[
                info.AsrModel(
                    name=MODEL_ID,
                    description="NVIDIA Parakeet multilingual automatic speech recognition (ASR) model",
                    attribution=info.Attribution(
                        name=REPO_ID.title(),
                        url=_URL,
                    ),
                    installed=True,
                    # TODO(jpwoodbu) Fill out this list of languages.
                    languages=["en"],
                    version="v3",
                ),
            ]
        )
    ]
)


class ParakeetEventHandler(server.AsyncEventHandler):

    def __init__(
        self,
        model,
        model_lock: asyncio.Lock,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.info_event = _INFO.event()
        self.model = model
        self.model_lock = model_lock
        self._wav_dir = tempfile.TemporaryDirectory()
        self._wav_path = os.path.join(self._wav_dir.name, "speech.wav")
        self._wav_file: Optional[wave.Wave_write] = None

    async def handle_event(self, event: event.Event) -> bool:
        if audio.AudioChunk.is_type(event.type):
            chunk = audio.AudioChunk.from_event(event)

            if self._wav_file is None:
                self._wav_file = wave.open(self._wav_path, "wb")
                self._wav_file.setframerate(chunk.rate)
                self._wav_file.setsampwidth(chunk.width)
                self._wav_file.setnchannels(chunk.channels)

            self._wav_file.writeframes(chunk.audio)
            return True

        if audio.AudioStop.is_type(event.type):
            _LOGGER.debug("Audio stopped. Transcribing...")
            assert self._wav_file is not None

            self._wav_file.close()
            self._wav_file = None

            async with self.model_lock:
                start_time = time.perf_counter()
                result = self.model.transcribe(self._wav_path, verbose=False)
                end_time = time.perf_counter()
            text = result[0].text
            assert isinstance(text, str)
            inference_time = end_time - start_time
            _LOGGER.info(f"Transcribed in {inference_time:.3f}s: {text}")

            await self.write_event(asr.Transcript(text=text).event())
            _LOGGER.debug("Completed request")

            # Reset
            self._language = self._language

            return False

        if asr.Transcribe.is_type(event.type):
            transcribe = asr.Transcribe.from_event(event)
            if transcribe.language:
                self._language = transcribe.language
                _LOGGER.debug(
                    "Language set to %s but is ignored by this handler",
                    transcribe.language)
            return True

        if info.Describe.is_type(event.type):
            await self.write_event(self.info_event)
            _LOGGER.debug("Sent info")
            return True

        return True
