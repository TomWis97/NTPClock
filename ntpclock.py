import machine
import tm1637

class NTPClock():
    def __init__(self, config):
        """Define all objects and variables."""
        self.tm = tm1637.TM1637(clk=machine.Pin(config['display_clock']),
                                dio=machine.Pin(config['display_dio']))
        self.config = config
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan_ap = network.WLAN(network.AP_IF)

    def bootup(self):
        """This connects to WiFi, configures the clock and timezone."""
        # Disable AP and enable client.
        self.wlan.active(True)
        self.wlan_ap.active(False)

        wlan.connect(config['ssid'], config['psk'])

        # Display animation
        self.tm.brightness(0)
        self.tm.show('boot')
        animation_brightness = 0
        while not wlan.isconnected():
            animation_brightness += 1
            if animation_brightness > 7:
                animation_brightness = 0
            tm.brightness(animation_brightness)

        self.tm.show('sync')
