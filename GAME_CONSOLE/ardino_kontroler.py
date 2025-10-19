#!/usr/bin/env python3
import time
import sys
from collections import defaultdict

import serial
from evdev import UInput, ecodes as e

# ==== Podesi serijski port i baudrate po potrebi ====
SER_PORT = "/dev/ttyACM0" # npr. /dev/ttyUSB0 ili /dev/ttyACM1
SER_BAUD = 9600

# Koliko dugo (sekundi) držati strelicu pritisnutom ako ne stigne novi JOY_* event
HOLD_TIMEOUT_S = 0.30

# Mapiranje Arduino tokena -> Linux KEY_ kodovi (tastatura)
TOKEN_TO_KEY = {
    "JOY_UP": e.KEY_UP,
    "JOY_DOWN": e.KEY_DOWN,
    "JOY_LEFT": e.KEY_LEFT,
    "JOY_RIGHT": e.KEY_RIGHT,
    "JOY_PRESS": e.KEY_ENTER, # klik na štapić (SW) = Enter

    # Dugmad A–F (mijenjaj po želji u skladu sa tvojim RetroPie mappingom)
    "BTN_A": e.KEY_Z,
    "BTN_B": e.KEY_X,
    "BTN_C": e.KEY_A,
    "BTN_D": e.KEY_S,
    "BTN_E": e.KEY_Q,
    "BTN_F": e.KEY_W,
}

# Koji tokeni su "drživi" (hold) umjesto kratkog tapanja
HOLDABLE_TOKENS = {"JOY_UP", "JOY_DOWN", "JOY_LEFT", "JOY_RIGHT", "BTN_E"}

def make_keyboard():
    capabilities = {
        e.EV_KEY: list(set(TOKEN_TO_KEY.values()))
    }
    ui = UInput(capabilities, name="Arduino2RetroPie Virtual Keyboard", bustype=0x03)
    return ui

def main():
    # Otvori serijski
    try:
        ser = serial.Serial(SER_PORT, SER_BAUD, timeout=0.1)
    except Exception as ex:
        print(f"[ERR] Ne mogu otvoriti {SER_PORT}: {ex}", file=sys.stderr)
        sys.exit(1)

    ui = make_keyboard()

    # Stanje dugmeta za hold (strelice)
    held_keys = set() # skup evdev key code-ova koji su trenutno “držani”
    last_seen = defaultdict(lambda: 0.0) # token -> vrijeme zadnjeg prijema

    print("[INFO] Spremno. Čitam sa Arduina i šaljem uinput događaje…")
    try:
        while True:
            # 1) U čitanju serijskog, pokupi jednu liniju
            line = ser.readline()
            if line:
                try:
                    token = line.decode("utf-8", errors="ignore").strip()
                except UnicodeDecodeError:
                    token = ""

                if token in TOKEN_TO_KEY:
                    keycode = TOKEN_TO_KEY[token]

                    if token in HOLDABLE_TOKENS:
                        # Držive komande (strelice): pritisni kad stigne prva,
                        # osvježavaj timestamp na svaki novi event,
                        # a u watchdog-u ispuštaj kad istekne timeout.
                        last_seen[token] = time.monotonic()
                        if keycode not in held_keys:
                            ui.write(e.EV_KEY, keycode, 1) # press
                            ui.syn()
                            held_keys.add(keycode)
                    else:
                        # Ostala dugmad: kratki tap (press + release)
                        ui.write(e.EV_KEY, keycode, 1)
                        ui.syn()
                        # vrlo kratak tap
                        time.sleep(0.02)
                        ui.write(e.EV_KEY, keycode, 0)
                        ui.syn()
                # (nepoznate linije ignorišemo)
            
            # 2) Watchdog za strelice: otpusti ako je prošao timeout bez novog eventa
            now = time.monotonic()
            for tok in list(HOLDABLE_TOKENS):
                key = TOKEN_TO_KEY[tok]
                if key in held_keys:
                    if (now - last_seen[tok]) > HOLD_TIMEOUT_S:
                        ui.write(e.EV_KEY, key, 0) # release
                        ui.syn()
                        held_keys.remove(key)

            # kratko spavaj da CPU ne divlja
            time.sleep(0.005)

    except KeyboardInterrupt:
        print("\n[INFO] Gasim…")
    finally:
        # Pobrini se da su svi “held” tasteri pušteni
        for key in list(held_keys):
            ui.write(e.EV_KEY, key, 0)
        ui.syn()
        ui.close()
        ser.close()

if __name__ == "__main__":
    main()
