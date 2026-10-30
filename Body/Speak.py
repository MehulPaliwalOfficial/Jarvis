import asyncio
import edge_tts
import pygame
import os
import json
import tempfile

pygame.mixer.init()

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'Data', 'Config.json')


def Load_Vocal_Config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        return config.get("voice_profile", "en-GB-RyanNeural"), config.get("voice_speed", "+0%")
    except:
        return "en-GB-RyanNeural", "+0%"


async def _generate_audio(text, voice, rate, path):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(path)


def Speak(text: str):
    if not text:
        return

    voice, rate = Load_Vocal_Config()

    # Temporary file (no clutter, safer than fixed filename)
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    try:
        print(f"\n[ JARVIS ]: {text}\n")

        asyncio.run(_generate_audio(text, voice, rate, path))

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(20)

    finally:
        try:
            pygame.mixer.music.stop()
        except:
            pass

        if os.path.exists(path):
            os.remove(path)