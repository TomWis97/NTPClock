from miniconfigparser import MiniConfigParser
from ntpclock import NTPClock

def main():
    config = MiniConfigParser()
    print("SSID:", config['ssid'])
    print("PSK:", config['psk'])
    ntpclock = NTPClock(config)
    ntpclock.bootup()
    ntpclock.update_display()

main()
