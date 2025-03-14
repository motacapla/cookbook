import sys
import whisper
from pyannote.audio import Pipeline
from pyannote.audio import Audio

import secret

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=secret.HF_AUTH_TOKEN,
)

if len(sys.argv) > 1:
    audio_file = sys.argv[1]
else:
    print("Usage: python diarizer.py <audio_file>")
    exit()

diarization = pipeline(audio_file)

audio = Audio(sample_rate=16000, mono=True)

model = whisper.load_model("large-v3-turbo")

for segment, _, speaker in diarization.itertracks(yield_label=True):
    waveform, _ = audio.crop(audio_file, segment)
    text = model.transcribe(waveform.squeeze().numpy())["text"]
    print(f"[{segment.start:03.1f}s - {segment.end:03.1f}s] {speaker}: {text}")
