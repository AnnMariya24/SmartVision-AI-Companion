import sys
import atexit
import subprocess
import threading

from flask import Flask, render_template, jsonify, request
from voice.voice_engine import VoiceEngine

# ---------------- INIT ---------------- #

app = Flask(__name__)
voice = VoiceEngine()

# 🔌 GLOBAL SYSTEM STATES
power_state = False
voice_process = None
vision_process = None
boot_process = None


# ---------------- PROCESS MANAGEMENT ---------------- #

def stop_process(proc, name):
    """Safely stop a running subprocess"""
    if proc and proc.poll() is None:
        print(f"🛑 Stopping {name}...")
        proc.terminate()
        proc.wait()


def cleanup_processes():
    """Kill all running SmartVision modules"""
    global voice_process, vision_process, boot_process

    print("\n🛑 Cleaning all SmartVision processes...")

    stop_process(voice_process, "Voice Assistant")
    stop_process(vision_process, "Walking Mode")
    stop_process(boot_process, "Boot")

    voice_process = None
    vision_process = None
    boot_process = None


atexit.register(cleanup_processes)


# ---------------- HELPER FUNCTIONS ---------------- #

def speak_async(text):
    """Speak without blocking Flask"""
    threading.Thread(target=voice.speak, args=(text,)).start()


def shutdown_server():
    """Stop Flask server"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with Werkzeug')
    func()


def check_power():
    """Prevent starting modes when power is OFF"""
    if not power_state:
        return False, jsonify({"status": "⚠️ Power is OFF"})
    return True, None


# ---------------- PAGE ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/onboarding")
def onboarding():
    return render_template("onboarding.html")

@app.route("/device")
def device():
    return render_template("device.html")

@app.route("/walking_page")
def walking_page():
    return render_template("walking.html")

@app.route("/companion_page")
def companion_page():
    return render_template("companion.html")


# ---------------- POWER BUTTON ---------------- #

@app.route("/power")
def power():
    global power_state, boot_process

    if not power_state:
        # 🔌 POWER ON
        power_state = True
        print("🔋 Power ON")

        boot_process = subprocess.Popen([sys.executable, "boot.py"])

        return jsonify({"status": "✅ System Powered ON"})

    else:
        # 🔌 POWER OFF
        print("🔋 Power OFF")

        power_state = False

        # Stop all modules
        cleanup_processes()

        # Play shutdown sound/voice
        subprocess.Popen([sys.executable, "shutdown.py"])

        # Stop Flask server
        shutdown_server()

        return jsonify({"status": "❌ System Powered OFF"})


# ---------------- COMPANION MODE ---------------- #

@app.route("/start_voice")
def start_voice():
    global voice_process

    ok, resp = check_power()
    if not ok:
        return resp

    # Prevent duplicate launch
    if voice_process and voice_process.poll() is None:
        return jsonify({"status": "🤖 Companion already running"})

    print("🎙️ Starting Companion Mode...")
    voice_process = subprocess.Popen([sys.executable, "voice_mode.py"])

    return jsonify({"status": "🤖 Companion Mode Started"})


# ---------------- WALKING MODE ---------------- #

@app.route("/start_detection")
def start_detection():
    global vision_process

    ok, resp = check_power()
    if not ok:
        return resp

    # Prevent duplicate launch
    if vision_process and vision_process.poll() is None:
        return jsonify({"status": "🚶 Walking mode already running"})

    print("👁️ Starting Walking Mode...")
    vision_process = subprocess.Popen([sys.executable, "walking_mode.py"])

    return jsonify({"status": "🚶 Walking Mode Started"})


# ---------------- RUN SERVER ---------------- #

if __name__ == "__main__":
    try:
        print("🌐 SmartVision Web Controller Started")
        app.run(debug=True, use_reloader=False)
    except KeyboardInterrupt:
        cleanup_processes()
        print("👋 SmartVision stopped")
