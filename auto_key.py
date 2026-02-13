#!/usr/bin/env python3
"""
auto_key.py

Random keyboard input generator restricted to keys that perform actions in Minecraft.

Usage examples:
  Simulation (safe):
    python3 auto_key.py --simulate --mode minecraft --count 50 --interval 0.05 --delay 1

  Real (sends events):
    python3 auto_key.py --mode minecraft --interval 0.1

Defaults to `minecraft` mode which only uses keys mapped to Minecraft actions.
Use `--mode all` to allow all printable characters (not recommended for Minecraft).

Press `Esc` to stop when running in real mode. Press Ctrl-C to stop simulation.
"""

import argparse
import random
import string
import time
import threading
import sys

stop_flag = threading.Event()


def minecraft_keyset():
    # Keys that map to common Minecraft actions
    # movement: w a s d
    # jump: space
    # sneak/sprint: shift, ctrl
    # inventory/open: e
    # drop: q
    # hotbar: 1-9
    # swap hands: f
    keys = ["w", "a", "s", "d", "space", "shift", "ctrl", "e", "q", "f"]
    keys += [str(i) for i in range(1, 10)]
    return keys


def all_keyset():
    return list(string.ascii_letters + string.digits + string.punctuation + " \t\n")


def press_and_release(controller, key_name, duration):
    from pynput.keyboard import Key

    special = {
        "space": Key.space,
        "shift": Key.shift,
        "ctrl": Key.ctrl,
        "enter": Key.enter,
        "tab": Key.tab,
        "esc": Key.esc,
    }

    key_obj = special.get(key_name, None)
    try:
        if key_obj is not None:
            controller.press(key_obj)
            time.sleep(duration)
            controller.release(key_obj)
        else:
            # assume single-character string for letters and digits
            controller.press(key_name)
            time.sleep(duration)
            controller.release(key_name)
    except Exception:
        # swallow exceptions from controller (e.g., if blocked by Wayland)
        pass


def simulate_behavior(key_list, interval, count=None):
    i = 0
    try:
        while (count is None or i < count) and not stop_flag.is_set():
            key = random.choice(key_list)
            dur = random.uniform(0.03, max(interval, 0.15))
            print(f"[PRESS] {key} for {dur:.2f}s", end="\r", flush=True)
            time.sleep(interval)
            i += 1
    except KeyboardInterrupt:
        stop_flag.set()


def real_behavior(interval, key_list):
    try:
        from pynput.keyboard import Controller, Listener, Key
    except Exception as e:
        print("Failed to import pynput or initialize controller:", e, file=sys.stderr)
        print("On Wayland or locked-down systems synthetic input may be blocked.")
        sys.exit(1)

    controller = Controller()

    def on_press(key):
        try:
            if key == Key.esc:
                stop_flag.set()
                return False
        except Exception:
            pass

    t = threading.Thread(target=_real_typing_thread, args=(controller, key_list, interval), daemon=True)
    t.start()

    with Listener(on_press=on_press) as listener:
        listener.join()


def _real_typing_thread(controller, key_list, interval):
    while not stop_flag.is_set():
        key = random.choice(key_list)
        # Press duration random so some actions are taps, some are holds
        dur = random.uniform(0.05, 0.4)
        press_and_release(controller, key, dur)
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="Random keyboard input (Minecraft-only by default)")
    parser.add_argument("--simulate", action="store_true", help="Print actions instead of sending real key events")
    parser.add_argument("--mode", choices=["minecraft", "all"], default="minecraft", help="Key selection mode (default: minecraft)")
    parser.add_argument("--interval", type=float, default=0.12, help="Seconds between actions")
    parser.add_argument("--count", type=int, default=None, help="Number of actions (simulate mode only)")
    parser.add_argument("--delay", type=float, default=5.0, help="Initial delay before starting")
    args = parser.parse_args()

    print(f"Mode: {args.mode} | {'SIMULATION' if args.simulate else 'REAL'} | Delay: {args.delay}s")
    print("Move focus to Minecraft window now, or cancel. Esc stops real mode. Ctrl-C stops simulation.")
    time.sleep(args.delay)

    key_list = minecraft_keyset() if args.mode == "minecraft" else all_keyset()

    if args.simulate:
        simulate_behavior(key_list, args.interval, count=args.count)
        print("\nSimulation finished.")
        return

    real_behavior(args.interval, key_list)
    print("Stopped.")


if __name__ == "__main__":
    main()
