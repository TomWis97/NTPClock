from miniconfigparser import MiniConfigParser
from ntpclock import NTPClock
import machine
import time

def main():
    config = MiniConfigParser()
    print("SSID:", config['ssid'])
    print("PSK:", config['psk'])
    ntpclock = NTPClock(config)
    ntpclock.bootup()
    try:
        ntpclock.update_display()
    except:
        # Reboot when something goes wrong.
        ntpclock.display_err()
        time.sleep(5)
        machine.reset()

main()
