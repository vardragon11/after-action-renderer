import whisper

class VoiceToText:
    def __init__(self, model_size="base"):
        self.model_size = model_size
        try:
            self.model = whisper.load_model(model_size)
            print(f"[✅] Whisper model '{model_size}' loaded.")
        except Exception as e:
            print(f"[❌] Failed to load Whisper model: {e}")
            self.model = None

    def transcribe(self, audio_path: str) -> str:
        if not self.model:
            return "[Error] Whisper model not loaded."
        try:
            print(f"[🎧] Transcribing '{audio_path}'...")
            result = self.model.transcribe(audio_path)
            text = result["text"].strip()
            print("[✅] Transcription complete.")
            return text
        except Exception as e:
            print(f"[❌] Transcription failed: {e}")
            return ""
