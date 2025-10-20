# GAME_CONSOLE

Kratak opis: projekat ručne konzole (Arduino joystick + RetroPie).

## Sadržaj
- `ardino_kontroler.py` – Python skripta (uinput/evdev)
- `arduino_read.ino` – Arduino kod
- `systemd.txt` – servis za automatsko pokretanje
- `udev.txt` – udev pravilo za /dev/uinput
- `dokumentacija.pdf` – izveštaj

## Kako pokrenuti
1. Udev pravilo: `sudo cp udev.txt /etc/udev/rules.d/99-uinput.rules`  
   `sudo udevadm control --reload-rules && sudo modprobe uinput`
2. Servis: `sudo cp systemd.txt /etc/systemd/system/arduino-input.service`  
   `sudo systemctl daemon-reload && sudo systemctl enable --now arduino-input.service`

## Video
Biće naknadno: [*(YouTube link)*.](https://youtube.com/shorts/HdgQtF8e0pU)
