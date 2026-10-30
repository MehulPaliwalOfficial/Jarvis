import speech_recognition as sr
import whisper
import warnings
import os
import uuid

warnings.filterwarnings("ignore")

print("[ JARVIS ]: Loading Real-Time Acoustic Neural Interface...")

model = whisper.load_model("small")
recognizer = sr.Recognizer()

recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.6
recognizer.energy_threshold = 300


def Listen():
    try:
        with sr.Microphone() as source:
            print("\n[ JARVIS ]: Calibrating audio environment...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            print("[ JARVIS ]: Listening...")
            audio = recognizer.listen(source, phrase_time_limit=6)

        # ✅ SAFE TEMP FILE (no locking issues)
        temp_filename = os.path.join(
            os.environ.get("TEMP", "."),
            f"jarvis_{uuid.uuid4().hex}.wav"
        )

        with open(temp_filename, "wb") as f:
            f.write(audio.get_wav_data())

        print("[ JARVIS ]: Processing speech stream...")

        result = model.transcribe(
            temp_filename,
            task="transcribe",
            language=None,
            fp16=False
        )

        # cleanup immediately after use
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        text = result.get("text", "").strip().lower()

        if not text:
            return ""

        print(f"➜ Recognized: {text}")
        return text

    except sr.WaitTimeoutError:
        return ""

    except Exception as e:
        print(f"[ JARVIS ERROR ]: {e}")
        return ""


def MicExecution():
    return Listen()


if __name__ == "__main__":
    print("=== Jarvis Acoustic Core Online ===")

    while True:
        cmd = MicExecution()
        if cmd:
            print(f"[ INPUT ]: {cmd}")