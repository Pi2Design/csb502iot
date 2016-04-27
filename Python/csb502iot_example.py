import time
import csb502iot

#Sensor connected to A0 Port
sensor = 0              # AIN0 sig1
#sensor = 1              # AIN0 sig2
#sensor = 2              # AIN1 sig1
#sensor = 3              # AIN1 sig2
#sensor = 4              # AIN2 sig1
#sensor = 5              # AIN2 sig2
#sensor = 6              # AIN3 sig1
#sensor = 7              # AIN3 sig2

#blue LED connected to DIO0 Port
#led = 0              # DIO3 sig1
#led = 1              # DIO3 sig2
#led = 2              # DIO2 sig1
#led = 3              # DIO2 sig2
#led = 4              # DIO1 sig1
#led = 5              # DIO1 sig2
blueled = 6              # DIO0 sig1
#led = 7              # DIO0 sig2

#red LED connected to DIO3 Port
redled = 0              # DIO3 sig1
#led = 1              # DIO3 sig2
#led = 2              # DIO2 sig1
#led = 3              # DIO2 sig2
#led = 4              # DIO1 sig1
#led = 5              # DIO1 sig2
#led = 6              # DIO0 sig1
#led = 7              # DIO0 sig2

#button connected to DIO1 port
#button = 0		# DIO3 sig1
#button = 1              # DIO3 sig2
#button = 2              # DIO2 sig1
#button = 3              # DIO2 sig2
button = 4              # DIO1 sig1
#button = 5              # DIO1 sig2
#button = 6              # DIO0 sig1
#button = 7              # DIO0 sig2





csb502iot.analogSetup()
csb502iot.pwmSetup(blueled)
csb502iot.gpioConfigOutput(redled)
csb502iot.gpioConfigInput(button)
csb502iot.gpioInvertInput(button)
csb502iot.gpioUnInvertInput(button)

while True:
    try:
        sensor_value = csb502iot.analogRead(sensor)
	csb502iot.pwmSetValue(blueled, sensor_value)
        print ("sensor_value =", sensor_value)
        #time.sleep(.5)
	csb502iot.gpioSet(redled, csb502iot.gpioGet(button))

    except IOError:
        print ("Error")

