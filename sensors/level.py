import time
import board
import busio
import adafruit_bno055
import smbus

TCA_ADDR = 0x70
CHANNEL = 3

bus = smbus.SMBus(1)

def select_channel(ch):
    bus.write_byte(TCA_ADDR, 1 << ch)
    time.sleep(0.01)

i2c = busio.I2C(board.SCL, board.SDA)

sensor = None

def init_sensor():
    global sensor
    select_channel(CHANNEL)
#    sensor = adafruit_bno055.BNO055_I2C(i2c)
    sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x28)

def read():
    global sensor
    if sensor is None:
        init_sensor()
        # Sensor braucht kurz, um bereit zu sein
        time.sleep(0.05)  # 50ms, evtl auf 0.1s erhöhen

    # Kanal sicherstellen
    select_channel(CHANNEL)

    euler = sensor.euler

    if euler is None:
        return {"tilt_x": 0.0, "tilt_y": 0.0}

    _, roll, pitch = euler
    return {"tilt_x": round(roll,2), "tilt_y": round(pitch,2)}