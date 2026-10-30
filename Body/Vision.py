import cv2
import os
import pyautogui

BASE_DIR = os.path.dirname(__file__)
LOG_PATH = os.path.join(BASE_DIR, '..', 'Logs')


def CaptureScreen():
    try:
        print("[ JARVIS ]: Capturing screen...")
        path = os.path.join(LOG_PATH, 'screen.jpg')

        img = pyautogui.screenshot()
        img.save(path)

        return path

    except Exception as e:
        print(f"[VISION ERROR] Screen capture failed: {e}")
        return None


def CaptureWebcam():
    print("[ JARVIS ]: Activating camera...")

    for index in range(3):  # try multiple cameras
        cam = cv2.VideoCapture(index)

        if cam.isOpened():
            ret, frame = cam.read()

            if ret:
                path = os.path.join(LOG_PATH, 'camera.jpg')
                cv2.imwrite(path, frame)

                cam.release()
                cv2.destroyAllWindows()

                print("[ JARVIS ]: Camera frame captured.")
                return path

            cam.release()

    print("[VISION ERROR] No working camera found.")
    return None