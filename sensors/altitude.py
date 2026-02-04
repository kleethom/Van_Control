import time
import board
import busio
import adafruit_bmp3xx
import smbus


TCA_ADDR = 0x70
CHANNEL = 2  # Multiplexer-Kanal

# Standard-Luftdruck auf Meereshöhe in hPa
SEA_LEVEL_PRESSURE = 1013.25

# SMBus für I2C
bus = smbus.SMBus(1)

def select_channel(ch):
    bus.write_byte(TCA_ADDR, 1 << ch)
    time.sleep(0.01)  # Kurze Verzögerung nach Kanalwechsel

# I2C für Adafruit-Bibliothek
i2c = busio.I2C(board.SCL, board.SDA)

# BMP-Sensor
bmp = None

def init_sensor():
    global bmp
    select_channel(CHANNEL)
    bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    bmp.sea_level_pressure = SEA_LEVEL_PRESSURE

def read():
    global bmp
    if bmp is None:
        init_sensor()
    select_channel(CHANNEL)
    pressure = bmp.pressure      # hPa
    altitude = bmp.altitude      # Meter
    return {
        "pressure": round(pressure, 2),
        "altitude": round(altitude, 2)
    }