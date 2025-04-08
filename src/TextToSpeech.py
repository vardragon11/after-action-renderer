from gtts import gTTS
from pydub import AudioSegment
import os

class TextToVoice:
    def __init__(self, text: str, filename_base="scenario"):
        self.text = text.strip()
        self.filename_base = filename_base
        self.mp3_file = f"{filename_base}.mp3"
        self.wav_file = f"{filename_base}.wav"

    def create_voice(self) -> bool:
        if not self.text:
            print("[❌] Empty text. Cannot generate voice.")
            return False

        try:
            # Generate speech
            tts = gTTS(self.text)
            tts.save(self.mp3_file)
            print(f"[✅] MP3 file saved as: {self.mp3_file}")

            # Convert to WAV
            AudioSegment.from_mp3(self.mp3_file).export(self.wav_file, format="wav")
            print(f"[✅] WAV file exported as: {self.wav_file}")
            return True

        except Exception as e:
            print(f"[❌] Failed to generate voice: {e}")
            return False

    def cleanup(self):
        # Optional: remove temporary MP3 if desired
        if os.path.exists(self.mp3_file):
            os.remove(self.mp3_file)
            print(f"[🧹] Removed temporary file: {self.mp3_file}")

tts = TextToVoice("This is a test scenario.")
if tts.create_voice():
    print("Voice synthesis complete.")
    # Optionally clean up
    #tts.cleanup()