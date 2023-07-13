import librosa
import soundfile as sf


def load_wav(file_path, offset=0.0, duration=None, sr=None, mono=True):
    audio, sampling_rate = librosa.core.load(
        file_path,
        offset=offset,
        duration=duration,
        sr=sr,
        mono=mono,
    )
    return audio, sampling_rate


def save_wav(file_path, audio, sampling_rate, subtype="PCM_24"):
    sf.write(
        file=file_path,
        data=audio,
        samplerate=sampling_rate,
        subtype=subtype,
    )
    print(f"wav chunk saved at {file_path}")
