def dht11():
    serial.write_string("!1:TEMP:" + str(NPNBitKit.dht11_temp()) + "#")
    serial.write_string("!1:HUMI:" + str(NPNBitKit.dht11_hum()) + "#")
def LCD():
    NPNLCD.clear()
    NPNLCD.show_string("TEMP:" + str(NPNBitKit.dht11_temp()), 0, 0)
    NPNLCD.show_string("HUMI:" + str(NPNBitKit.dht11_hum()), 9, 0)
    NPNLCD.show_string("GAS:" + str(pins.analog_read_pin(AnalogPin.P2)), 0, 1)
def gas():
    if pins.analog_read_pin(AnalogPin.P2) >= 700:
        pins.digital_write_pin(DigitalPin.P6, 1)
        pins.digital_write_pin(DigitalPin.P7, 0)
    elif pins.analog_read_pin(AnalogPin.P2) >= 500:
        pins.digital_write_pin(DigitalPin.P6, 1)
        pins.digital_write_pin(DigitalPin.P7, 1)
    else:
        pins.digital_write_pin(DigitalPin.P6, 0)
        pins.digital_write_pin(DigitalPin.P7, 1)
    serial.write_string("!1:GAS:" + str(pins.analog_read_pin(AnalogPin.P2)) + "#")

def on_data_received():
    global cmd
    cmd = serial.read_until(serial.delimiters(Delimiters.HASH))
    if cmd == "0":
        pins.digital_write_pin(DigitalPin.P0, 0)
        pins.digital_write_pin(DigitalPin.P1, 0)
    elif cmd == "1":
        pins.digital_write_pin(DigitalPin.P0, 1)
        pins.digital_write_pin(DigitalPin.P1, 0)
    if cmd == "2":
        pins.digital_write_pin(DigitalPin.P10, 0)
    elif cmd == "3":
        pins.digital_write_pin(DigitalPin.P10, 1)
serial.on_data_received(serial.delimiters(Delimiters.HASH), on_data_received)

def door_bell():
    global counter_door
    if NPNBitKit.button_door_open(DigitalPin.P5):
        counter_door += 1
        if counter_door < 30:
            NPNBitKit.buzzer(DigitalPin.P4, True)
        else:
            NPNBitKit.buzzer(DigitalPin.P4, False)
    else:
        counter_door = 0
        NPNBitKit.buzzer(DigitalPin.P4, False, 0)
def timer_run():
    global value, time
    value += 1
    if time == 5:
        dht11()
        NPNLCD.clear()
        NPNLCD.show_string("Update", 0, 0)
    if time == 10:
        gas()
        time = 0
        NPNLCD.clear()
        NPNLCD.show_string("Update", 0, 0)
value = 0
cmd = ""
counter_door = 0
time = 0
serial.redirect_to_usb()
serial.set_baud_rate(BaudRate.BAUD_RATE115200)
led.enable(False)
time = 0
time_out = 0
counter_door = 0
NPNLCD.lcd_init()
NPNLCD.show_string("Xin chao", 0, 0)

def on_forever():
    NPNBitKit.dht11_read(DigitalPin.P3)
    timer_run()
    LCD()
    door_bell()
    basic.pause(1000)
basic.forever(on_forever)
