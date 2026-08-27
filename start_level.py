import os
import sys
import time
import signal
import subprocess
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEVELS_DIR = os.path.join(BASE_DIR, "levels")

def get_level_scripts(level_num):
    """Return list of (script_name, working_dir) for the given level."""
    level_dir = os.path.join(LEVELS_DIR, f"level{level_num}")
    if not os.path.isdir(level_dir):
        raise FileNotFoundError(f"Level directory {level_dir} not found")

    if level_num == 1:
        return [
            ("internal_target.py", level_dir),
            ("app.py", level_dir)
        ]
    elif level_num == 2:
        return [
            ("internal_target.py", level_dir),
            ("rebind_dns.py", level_dir),
            ("app.py", level_dir)
        ]
    else:
        raise ValueError(f"Unsupported level number: {level_num}")

def main():
    parser = argparse.ArgumentParser(description="SSRF Lab launcher")
    parser.add_argument("-l", "--level", type=int, required=True, help="Level number to run")
    args = parser.parse_args()
    level = args.level

    try:
        scripts = get_level_scripts(level)
    except (FileNotFoundError, ValueError) as e:
        print(f"[!] {e}")
        sys.exit(1)

    processes = []
    def cleanup():
        print("\n[*] Stopping all processes...")
        for p in processes:
            try:
                p.terminate()
            except:
                pass
        time.sleep(0.5)
        for p in processes:
            if p.poll() is None:
                try:
                    p.kill()
                except:
                    pass
        sys.exit(0)

    signal.signal(signal.SIGINT, lambda sig, frame: cleanup())
    signal.signal(signal.SIGTERM, lambda sig, frame: cleanup())

    for script, cwd in scripts:
        cmd = [sys.executable, script]
        print(f"[*] Starting {script} in {cwd}")
        p = subprocess.Popen(cmd, cwd=cwd, stdout=None, stderr=None)
        processes.append(p)

    print(f"\n[+] Level {level} is running.")
    print(f"    Access: http://127.0.0.1:5050/level{level}")
    print("    Press Ctrl+C to stop all services.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
