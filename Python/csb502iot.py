import smbus
import time

bus = smbus.SMBus(1)
# I2C Address of max11603
address_adc = 0x6D
#i2c address of pca9554 digital io
address_gpio = 0x27
#i2c address of pwm bank 0
#address of bank one is bank0 address +1
address_pwm = 0x60

#setup byte and config byte for adc
setup_adc = 0xB4
config_adc = 0x61

#pwm setup
mode2_reg = 0x01
mode2_blink = 0x20
mode2_invert = 0x10
mode2_totem = 0x04
ledout_reg = 0x08
ledout_off = 0x0
ledout_on = 0x1
ledout_individual_only = 0x2
ledout_individual_and_group = 0x3
pwm_reg_base = 0x02 #pwm_reg = pwm_reg_base + pwm_pin 
mode2_value = 0;
mode1_reg = 0	
mode1_sleep_value = 0x11
mode1_wake_value = 0x1


#gpio setup
config_reg = 0x3
config_input = 0x1
config_output = 0x0
input_reg = 0x0
output_reg = 0x1
invert_reg = 0x2
inverted = 1


#send setup byte to adc
def analogSetup():
	bus.write_byte(address_adc,setup_adc)

# Read analog value from Pin
def analogRead(pin):
	pin = config_adc | pin << 1
        number = bus.read_byte_data(address_adc,pin)
        #time.sleep(.1)
        return number

def gpioConfigInput(pin):
        config_value = bus.read_byte_data(address_gpio, config_reg)
        config_value = config_value | 1 << pin
        bus.write_byte_data(address_gpio, config_reg, config_value)

def pwmWake(bank):
	bus.write_byte_data(address_pwm + bank, mode1_reg, mode1_wake_value)
	
#setup pin as pwm output on one of two pca9632 chips
#we will use open drain because some lines may be driven as outputs by gpio 
#and there is a built in pullup on the pca9554 gpio expander
#we will use non_inverted even though groveLED module is active high so that we know when LED is off it will always be HiZ
def pwmSetup(pin):
	pwm_bank = pin >> 2
	pwm_pin = 0x3 & pin
	#make sure gpio chip is not driving pin (set to input)
	gpioConfigInput(pin)
	pwmWake(pwm_bank)
	#set ledout bits
	ledout_value = bus.read_byte_data(address_pwm + pwm_bank, ledout_reg) 
	ledout_value = (ledout_value & ~(0x3 << (pwm_pin << 1))) | (ledout_individual_only << (pwm_pin << 1))
	bus.write_byte_data(address_pwm + pwm_bank, ledout_reg, ledout_value)
	#set mode register
	bus.write_byte_data(address_pwm + pwm_bank, mode2_reg, mode2_value)	

def pwmHiZ(pin):
	pwm_bank = pin >> 2
        pwm_pin = 0x3 & pin
	pwmWake(pwm_bank)
	#set mode register
	bus.write_byte_data(address_pwm + pwm_bank, mode2_reg, mode2_value)
	#set ledout bits to ledout_off
	ledout_value = bus.read_byte_data(address_pwm + pwm_bank, ledout_reg)
        ledout_value = (ledout_value & ~(0x3 << (pwm_pin << 1))) | (ledout_off << (pwm_pin << 1))   
	bus.write_byte_data(address_pwm + pwm_bank, ledout_reg, ledout_value)	

#set individual pwm value we use the inverted value instead of hardware inversion for safety with two drivers.
def pwmSetValue(pin, value):
        pwm_bank = pin >> 2
        pwm_pin = 0x3 & pin
	pwm_reg = pwm_reg_base + pwm_pin
	value = 255 - value  #reverse so higher is brighter
	bus.write_byte_data(address_pwm + pwm_bank ,pwm_reg, value)

def gpioConfigOutput(pin):
	#make sure pin is not driven by pwm controller
	pwmHiZ(pin)
	config_value = bus.read_byte_data(address_gpio, config_reg)
        config_value = config_value & ~(1 << pin)
        bus.write_byte_data(address_gpio, config_reg, config_value)
def gpioGet(pin):
	return (bus.read_byte_data(address_gpio, input_reg) >> pin) & 1 

def gpioSet(pin, value):
	output_value = (bus.read_byte_data(address_gpio, output_reg) & ~(1 <<pin)) | ((value & 1) << pin)
	bus.write_byte_data(address_gpio, output_reg, output_value)

def gpioInvertInput(pin):
	invert_value = bus.read_byte_data(address_gpio, invert_reg) | (inverted << pin)
	bus.write_byte_data(address_gpio, invert_reg, invert_value)

def gpioUnInvertInput(pin):
        invert_value = bus.read_byte_data(address_gpio, invert_reg) & ~(inverted << pin)
        bus.write_byte_data(address_gpio, invert_reg, invert_value)

