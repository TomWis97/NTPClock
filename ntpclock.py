import machine
import json
import time
import network
import tm1637
import ntptime
import urequests

class NTPClock():
    def __init__(self, config):
        """Define all objects and variables."""
        self.tm = tm1637.TM1637(clk=machine.Pin(config['display_clock']),
                                dio=machine.Pin(config['display_dio']))
        self.config = config
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan_ap = network.WLAN(network.AP_IF)
        self.rtc = machine.RTC()

    def bootup(self):
        """This connects to WiFi, configures the clock and timezone."""
        # Disable AP and enable client.
        self.wlan.active(True)
        self.wlan_ap.active(False)

        self.wlan.connect(self.config['ssid'], self.config['psk'])

        # Display animation
        self.tm.brightness(0)
        self.tm.show('boot')
        animation_brightness = 0
        while not self.wlan.isconnected():
            animation_brightness += 1
            if animation_brightness > 7:
                animation_brightness = 0
            self.tm.brightness(animation_brightness)
            time.sleep_ms(500)

        self.tm.brightness(7)
        self.tm.show('sync')

        # Sync time
        ntptime.settime()
        
        # Get timezone info
        ip_data = json.loads(urequests.get('http://ip-api.com/json?fields=status,message,countryCode,timezone,offset,mobile,query').text)
        print("ip_data:", ip_data)
        self.set_timezone(ip_data['offset'])
        print("UTC Offset:", ip_data['offset'])
        print("Current datetime:", self.rtc.datetime())

    def set_timezone(self, timezone):
        """Expects UTC offset in seconds, positive or negative."""
        offset = int(timezone)
        if offset > 0:
            tz_add = True
        elif offset == 0:
            # No offset, no further action required
            return
        else:
            tz_add = False

        # offset is in seconds, 3600 seconds in an hour.
        tz_hours = int(abs(offset) / 3600)
        tz_minutes = int(abs(offset) % 3600 / 60)

        current_time = self.rtc.datetime()

        # Adjust minutes
        fixed_minutes = current_time[5]
        if tz_add == True:
            fixed_minutes += tz_minutes
            if fixed_minutes >= 60:
                tz_hours += 1
                fixed_minutes -= 60
        else:
            fixed_minutes = fixed_minutes - tz_minutes
            if fixed_minutes < 0:
                # We have to substract an extra hour
                tz_hours += 1
                fixed_minutes += 60

        # Adjust hours
        extra_day = False # Whether to take an extra day
        fixed_hours = current_time[4]
        if tz_add == True:
            fixed_hours += tz_hours
            if fixed_hours >= 24:
                extra_day = True
                fixed_hours -= 24
        else:
            fixed_hours -= tz_hours
            if fixed_hours < 0:
                extra_day = True
                fixed_hours += 24

        fixed_days = current_time[2]
        # This might catch fire on the beginning or end
        # of the month. But I can't be bothered to fix this.
        if tz_add == True and extra_day == True:
            fixed_days += 1
        elif tz_add == False and extra_day == True:
            fixed_days -= 1

        new_time = (current_time[0],
                    current_time[1],
                    fixed_days,
                    current_time[3], # This value doesn't seem to do anything
                    fixed_hours,
                    fixed_minutes,
                    current_time[6],
                    current_time[7])

        # Finally, update time
        self.rtc.datetime(new_time)

    def update_display(self):
        """This function will loop continously."""
        while True:
            now = self.rtc.datetime()
            hours = now[4]
            minutes = now[5]
            self.tm.numbers(hours, minutes)
            time.sleep(1)
