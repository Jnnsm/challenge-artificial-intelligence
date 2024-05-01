from torch import cuda

import whisper


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Whisper(metaclass=Singleton):
    def __init__(self):
        self.model: whisper.model = whisper.load_model(
            'medium', device="cuda:0" if cuda.is_available() else "cpu")

    def extract_text_from_audio(self, audio_path: str) -> str:
        return self.model.transcribe(audio_path, temperature=0, word_timestamps=False)['text']
