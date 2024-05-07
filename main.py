import os
import subprocess
import signal
from config import UVICORN_PORT, STREAMLIT_PORT  # Import port configurations

# Global variables to store the subprocesses
backend_process = None
frontend_process = None

def start_backend():
    global backend_process
    backend_command = f"uvicorn app:app --reload --port {UVICORN_PORT}"
    backend_process = subprocess.Popen(backend_command, shell=True, cwd="backend")

def start_frontend():
    global frontend_process
    frontend_command = f"streamlit run main.py --server.port {STREAMLIT_PORT}"
    frontend_process = subprocess.Popen(frontend_command, shell=True, cwd="frontend")

def stop_processes():
    global backend_process, frontend_process
    if backend_process:
        backend_process.terminate()
    if frontend_process:
        frontend_process.terminate()

if __name__ == "__main__":
    try:
        start_backend()
        start_frontend()
        # Keep waiting for KeyboardInterrupt
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping subprocesses...")
        stop_processes()
