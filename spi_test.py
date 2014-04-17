import spidev
import thread
import time
import os
import OSC
import math

spi = spidev.SpiDev()
spi.open(0, 0)
exit = 0

client = OSC.OSCClient()
client.connect(('127.0.0.1', 9002))

try:
    client.send(OSC.OSCMessage("/address", 1))
except:
    print "not connected"
    pass

deadzone = 55

def distance_with_deadzone(x, y):
    d = math.sqrt((x-1023)**2 + (y-1023)**2)
    if d > (deadzone * 2):
        return d
    else:
        return 0

def get_hip(y):
    if (y > 1023 + deadzone):
        return ((y - 1023) / (1023.0 + deadzone) * 4000)
    return 0

def get_lop(y):
    if (y < 1023 - deadzone):
        return (y / (1023.0 - deadzone) * 4000)
    return 4000

def get_pwm(x):
    return (x/2048.0)*100

def spithread():
    print "Starting SPI Thread"
    while True:
        try:
            resp = spi.xfer2([1, 2, 3, 4])
            xpos = (resp[0] << 8) + resp[1]
            ypos = (resp[2] << 8) + resp[3]
            print "XPos: %s, YPos: %s\n" % (xpos, ypos)
            #client.send(OSC.OSCMessage("/hip1", get_hip(ypos)))
            #client.send(OSC.OSCMessage("/lop1", get_lop(ypos)))
            #client.send(OSC.OSCMessage("/volume1", distance_with_deadzone(xpos, ypos)))
            #client.send(OSC.OSCMessage("/pwm1", get_pwm(xpos)))
            #print "hip: %s, lop: %s, volume: %s, pwm: %s" % (get_hip(ypos), \
                                                             #get_lop(ypos), \
                                                             #distance_with_deadzone(xpos, ypos), \
                                                             #get_pwm(xpos))
            time.sleep(0.001)
        except:
            time.sleep(0.001)
        if exit:
            thread.exit()

try:
    thread.start_new_thread(spithread, ())
except:
    print "failed"
    
exit = raw_input("Press Enter to exit\n")
exit = 1
time.sleep(1)
