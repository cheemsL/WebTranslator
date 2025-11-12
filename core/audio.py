import os
import tempfile
import pyttsx4


class Audio:
    def __init__(self):
        os.makedirs("./temp", exist_ok=True)
        self.engine = pyttsx4.init()

    def speak(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()

    def save(self, text: str, file_path: str) -> None:
        self.engine.save_to_file(text, file_path)
        self.engine.runAndWait()

    def to_audio(self, text: str) -> bytes:
        # 临时文件保存音频
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            temp_path = tmp.name

        self.save(text, temp_path)

        with open(temp_path, "rb") as f:
            wav_bytes = f.read()

        # 删除临时文件
        os.remove(temp_path)

        return wav_bytes