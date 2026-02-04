import smbus
import time

TCA_ADDR = 0x70
SHT_ADDR = 0x44
CHANNEL = 0  # Kanal am Multiplexer

bus = smbus.SMBus(1)

def select_channel(ch):
    bus.write_byte(TCA_ADDR, 1 << ch)
    time.sleep(0.01)

def read():
    select_channel(CHANNEL)

    bus.write_i2c_block_data(SHT_ADDR, 0x2C, [0x06])
    time.sleep(0.02)
    data = bus.read_i2c_block_data(SHT_ADDR, 0x00, 6)

    raw_temp = (data[0] << 8) | data[1]
    raw_hum  = (data[3] << 8) | data[4]

    temp = -45 + (175 * raw_temp / 65535)
    hum  = 100 * raw_hum / 65535

    return {
        "temperature": round(temp, 2),
        "humidity": round(hum, 2)
    }