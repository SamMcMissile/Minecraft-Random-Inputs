# Minecraft-Random-Inputs
I had a funny idea. I have know idea what I'm doing.

## auto_key.py

This repository includes `auto_key.py`, a small utility to generate random keyboard input.

- Default mode targets keys commonly used in Minecraft (movement, hotbar, inventory, drop, jump, etc.).
- It supports a safe simulation mode that prints actions instead of sending real key events.

Quick start:

```bash
pip install -r requirements.txt
# Simulation (safe): prints actions instead of sending keys
python3 auto_key.py --simulate --mode minecraft --count 200 --interval 0.08 --delay 2

# Real mode (send input) — use with caution, focus Minecraft window first
python3 auto_key.py --mode minecraft --interval 0.12 --delay 5
```

Stopping:
- Simulation: Ctrl-C
- Real mode: Press `Esc` to stop sending input

Notes:
- On Wayland, synthetic input may be blocked; the script will fail to send real events in that case.
- Use only on machines you control. Do not use automated input in contexts that violate terms of service.

Changes from initial version:

- Default startup delay is now **15 seconds** to give more time to focus the Minecraft window or cancel.
- `W`, `A`, `S`, `D` are now weighted to appear significantly more often (better for movement).
- Left and right mouse clicks are supported as actions (`mouse_left`, `mouse_right`) and will be used in Minecraft mode.
- Movement keys and mouse clicks may be held for up to **5 seconds** to simulate sustained movement or continuous actions.

Always test in simulation mode (`--simulate`) before enabling real input.

