# apds.py
# Copyright (c) 2024 by Jun-Wei Chang.
# All rights reserved.
# Released under creative commons attribution CC BY-NC-SA.

import machine
import ustruct

class APDS():
    # APDS-9151's I2C address
    APDS9151_ADDR = 0x52

    # Registers
    MAIN_CTRL_ADDR = 0x00
    LS_MEANS_RATE_ADDR = 0x04
    LS_GAIN_ADDR = 0x05
    PART_ID_ADDR = 0x06
    MAIN_STATUS_ADDR = 0x07
    PS_DARA_ADDR = 0x08
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

    # resoltion value and measurement rate values MEAS_RATE
    RES_20bit = 0x00
    RES_19bit = 0x10
    RES_18bit = 0x20 # default
    RES_17bit = 0x30
    RES_16bit = 0x40
    RES_13bit = 0x50
    M_RATE_25ms = 0x00
    M_RATE_50ms = 0x01
    M_RATE_100ms = 0x02 # default
    M_RATE_200ms = 0x03
    M_RATE_500s = 0x04
    M_RATE_1000s = 0x05
    M_RATE_2000ms = 0x06
    M_RATE_2000ms = 0x07

    # Gain value in LS_Gain
    GAIN_1 = 0x00
    GAIN_3 = 0x01 # default
    GAIN_6 = 0x02
    GAIN_9 = 0x03
    GAIN_18 = 0x04


    def __init__(self, i2c_addr = APDS9151_ADDR, i2c_id = 0, scl_pin = 17, sda_pin = 16):
        # Set i2c pins and initialize
        self.i2c = machine.I2C(i2c_id, scl=machine.Pin(scl_pin), sda=machine.Pin(sda_pin))
        self.i2c_addr = i2c_addr
        return

    # write data to register
    def __write_reg(self,reg_addr,set_data):
        self.i2c.writeto_mem( self.i2c_addr, reg_addr, set_data)


    def set_mode(self):
        data_byte=bytes([self.LS_EN | self.RGB_MODE])
        self.__write_reg(self.MAIN_CTRL_ADDR, data_byte)


    def set_ls_means_rate(self, resolution=RES_18bit, rate=M_RATE_100ms):
        data_byte=bytes([resolution | rate])
        self.__write_reg(self.LS_MEANS_RATE_ADDR, data_byte)


    '''
    @ parameters
    gain is the light sensor gain value in which
    LS GAIN RANGE has only 5 gain values
    000:Gain_1
    001:Gain_3 (defalt)
    010:Gain_6
    011:Gain_9
    100:Gain_18
    '''
    def set_gain(self,gain=GAIN_3):
        self.i2c.writeto_mem( self.i2c_addr, self.LS_GAIN_ADDR, bytes([gain]))


    # read data from registers
    def __read_reg(self,reg_addr,data_len):
        return self.i2c.readfrom_mem( self.i2c_addr, reg_addr, data_len )


    def get_mode(self):
        data_bytes = self.__read_reg(self.MAIN_CTRL_ADDR,1)
        return ustruct.unpack("B",data_bytes)[0]
    

    def get_ls_means_rate(self):
        data_bytes = self.__read_reg(self.LS_MEANS_RATE_ADDR,1)
        return ustruct.unpack("B",data_bytes)[0]


    def get_part_id(self):
        data_bytes = self.__read_reg(self.PART_ID_ADDR,1)
        data_uchar = ustruct.unpack("B",data_bytes)[0] 
        part_id = data_uchar >> 4
        revision_id = data_uchar & 0x0F
        return part_id, revision_id


    def get_main_status(self):
        data_bytes = self.__read_reg(self.MAIN_STATUS_ADDR,1)
        data_uchar = ustruct.unpack("B",data_bytes)[0]
        ps_data_status = data_uchar & 0x01
        ps_interrupt_status = (data_uchar >> 1) & 0x01
        ps_logic_signal_status= (data_uchar >> 2) & 0x01
        ls_data_status = (data_uchar >> 3) & 0x01
        ls_interrupts_status = (data_uchar >> 4) & 0x01
        power_on_status = (data_uchar >> 5) & 0x01
        return ps_data_status, \
               ps_interrupt_status, \
               ps_logic_signal_status, \
               ls_data_status, \
               ls_interrupts_status, \
               power_on_status


    def get_ps_data(self):
        data_bytes = self.__read_reg(self.LS_DATA_IR_ADDR,2)
        return ustruct.unpack("<H",data_bytes)[0]


    def get_ls_data_ir(self):
        data_bytes = self.__read_reg(self.LS_DATA_IR_ADDR,3)
        return ustruct.unpack("<L",data_bytes + b'\x00')[0]


    def get_ls_data_green(self):
        data_bytes = self.__read_reg(self.LS_DATA_GREEN_ADDR,3)
        return ustruct.unpack("<L",data_bytes + b'\x00')[0]


    def get_ls_data_blue(self):
        data_bytes = self.__read_reg(self.LS_DATA_BLUE_ADDR,3)
        return ustruct.unpack("<L",data_bytes + b'\x00')[0]


    def get_ls_data_red(self):
        data_bytes =self. __read_reg(self.LS_DATA_RED_ADDR,3)
        return ustruct.unpack("<L",data_bytes + b'\x00')[0]

