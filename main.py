import machine
import ustruct
import time

# APDS-9151's I2C address
APDS9151_ADDR = 0x52

# Registers
MAIN_CTRL_ADDR = 0x00
LS_GAIN_ADDR = 0x50
LS_DATA_IR_ADDR = 0x0A
LS_DATA_GREEN_ADDR = 0x0D
LS_DATA_BLUE_ADDR = 0x10
LS_DATA_RED_ADDR = 0x13

# Control bits in MAIN_CTRL
SAI_PS = 0x40
SAI_LS = 0x20
SW_RESET = 0x10
RGB_MODE = 0x04
LS_EN = 0x02
PS_EN = 0x01

# Gain value in LS_Gain
GAIN_1 = 0x00
GAIN_3 = 0x01
GAIN_6 = 0x02
GAIN_9 = 0x03
GAIN_18 = 0x04

# Set i2c pins and initialize
i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))

def init():
    data_byte = bytes([LS_EN | RGB_MODE])
    i2c.writeto_mem( APDS9151_ADDR, MAIN_CTRL_ADDR, data_byte)
    return


def set_gain(gain):
    '''
    LS GAIN RANGE has only 5 gain values
    000:Gain 1
    001:Gain 3 (defalt)
    010:Gain 6
    011:Gain 9
    100:Gain 18
    '''
    i2c.writeto_mem( APDS9151_ADDR, LS_GAIN_ADDR, bytes([gain]))
    

def read_data(reg_addr,data_len):
    return i2c.readfrom_mem( APDS9151_ADDR, reg_addr, data_len )


def get_ls_data_ir():
    data_bytes = read_data(LS_DATA_IR_ADDR,3)
    return ustruct.unpack_from("<h",data_bytes,0)[0]


def get_ls_data_green():
    data_bytes = read_data(LS_DATA_GREEN_ADDR,3)
    return ustruct.unpack_from("<h",data_bytes,0)[0]


def get_ls_data_blue():
    data_bytes = read_data(LS_DATA_BLUE_ADDR,3)
    return ustruct.unpack_from("<h",data_bytes,0)[0]


def get_ls_data_red():
    data_bytes = read_data(LS_DATA_RED_ADDR,3)
    return ustruct.unpack_from("<h",data_bytes,0)[0]


init()
set_gain(GAIN_3)
while True:
    print('ir = {}'.format(get_ls_data_ir()),end='\t')
    print('green = {}'.format(get_ls_data_green()),end='\t')
    print('blue = {}'.format(get_ls_data_blue()),end='\t')
    print('red = {}'.format(get_ls_data_red()))
    time.sleep(0.1)