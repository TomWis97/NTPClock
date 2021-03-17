from miniconfigparser import MiniConfigParser
from ntpclock import NTPClock

def main():
    config = MiniConfigParser()
    ntpclock = NTPClock(config)
    ntpclock.bootup()
