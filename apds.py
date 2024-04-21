# apds.py
# Copyright (c) 2024 by Jun-Wei Chang.
# All rights reserved.
# Released under creative commons attribution CC BY-NC-SA.

import machine
import ustruct

class APDS():
    # APDS-9151's I2C address
    __APDS9151_ADDR = 0x52

    # Registers
    __MAIN_CTRL_ADDR = 0x00
    __PS_LED_ADDR = 0x01
    __PS_PULSES_ADDR = 0x02
    __PS_MEANS_RATE_ADDR = 0x03
    __LS_MEANS_RATE_ADDR = 0x04
    __LS_GAIN_ADDR = 0x05
    __PART_ID_ADDR = 0x06
    __MAIN_STATUS_ADDR = 0x07
    __PS_DARA_ADDR = 0x08
    __LS_DATA_IR_ADDR = 0x0A
    __LS_DATA_GREEN_ADDR = 0x0D
    __LS_DATA_BLUE_ADDR = 0x10
    __LS_DATA_RED_ADDR = 0x13

    # Data bits in MAIN_CTRL
    __SAI_PS = 0x40
    __SAI_LS = 0x20
    __SW_RESET = 0x10
    __RGB_MODE = 0x04
    __LS_EN = 0x02
    __PS_EN = 0x01

    # Data bits in PS_LED
    __FREQ_60K = 0x30
    __FREQ_70K = 0x40
    __FREQ_80K = 0x50
    __FREQ_90K = 0x60
    __FREQ_100K = 0x70
    __PULSE_CURRENT_2_5MA = 0x00
    __PULSE_CURRENT_5MA = 0x01
    __PULSE_CURRENT_10MA = 0x02
    __PULSE_CURRENT_25MA = 0x03
    __PULSE_CURRENT_50MA = 0x04
    __PULSE_CURRENT_75MA = 0x05
    __PULSE_CURRENT_100MA = 0x06
    __PULSE_CURRENT_125MA = 0x07
    
    # Resoltion value and measurement rate values in PS_MEAS_RATE
    __PS_RESOLUTION_8bit = 0x00
    __PS_RESOLUTION_9bit = 0x08
    __PS_RESOLUTION_10bit = 0x10
    __PS_RESOLUTION_11bit = 0x18
    __PS_MEASUREMENT_RATE_6_25ms = 0x01     
    __PS_MEASUREMENT_RATE_12_5ms = 0x02
    __PS_MEASUREMENT_RATE_25ms = 0x03
    __PS_MEASUREMENT_RATE_50ms = 0x04
    __PS_MEASUREMENT_RATE_100ms = 0x05
    __PS_MEASUREMENT_RATE_200ms = 0x06
    __PS_MEASUREMENT_RATE_400ms = 0x07

    # Resoltion value and measurement rate values in LS_MEAS_RATE
    __LS_RESOLUTION_20bit = 0x00
    __LS_RESOLUTION_19bit = 0x10
    __LS_RESOLUTION_18bit = 0x20 # default
    __LS_RESOLUTION_17bit = 0x30
    __LS_RESOLUTION_16bit = 0x40
    __LS_RESOLUTION_13bit = 0x50
    __LS_MEASUREMENT_RATE_25ms = 0x00
    __LS_MEASUREMENT_RATE_50ms = 0x01
    __LS_MEASUREMENT_RATE_100ms = 0x02 # default
    __LS_MEASUREMENT_RATE_200ms = 0x03
    __LS_MEASUREMENT_RATE_500s = 0x04
    __LS_MEASUREMENT_RATE_1000s = 0x05
    __LS_MEASUREMENT_RATE_2000ms = 0x06
    __LS_MEASUREMENT_RATE_2000ms = 0x07

    # Gain value in LS_Gain
    __GAIN_1 = 0x00
    __GAIN_3 = 0x01 # default
    __GAIN_6 = 0x02
    __GAIN_9 = 0x03
    __GAIN_18 = 0x04


    def __init__(self, i2c_addr = __APDS9151_ADDR, i2c_id = 0, scl_pin = 17, sda_pin = 16):
        # Set i2c pins and initialize
        self.i2c = machine.I2C(i2c_id, scl=machine.Pin(scl_pin), sda=machine.Pin(sda_pin))
        self.i2c_addr = i2c_addr
        return
    

    def set_rgb_mode(self):
        ps_en, ls_en, rgb_mode, sw_reset, sai_ls, sai_ps  = self.get_main_ctrl()
        rgb_mode = True
        self.set_main_ctrl( sai_ps = sai_ps, \
                            sai_ls = sai_ls, \
                            sw_reset = sw_reset, \
                            rgb_mode = rgb_mode, \
                            ls_en = ls_en, \
                            ps_en = ps_en )
        

    def set_ambient_light_mode(self):
        ps_en, ls_en, rgb_mode, sw_reset, sai_ls, sai_ps  = self.get_main_ctrl()
        rgb_mode = False
        self.set_main_ctrl( sai_ps = sai_ps, \
                            sai_ls = sai_ls, \
                            sw_reset = sw_reset, \
                            rgb_mode = rgb_mode, \
                            ls_en = ls_en, \
                            ps_en = ps_en )


    def enable_light_sensor(self):
        ps_en, ls_en, rgb_mode, sw_reset, sai_ls, sai_ps  = self.get_main_ctrl()
        ls_en = True
        self.set_main_ctrl( sai_ps = sai_ps, \
                            sai_ls = sai_ls, \
                            sw_reset = sw_reset, \
                            rgb_mode = rgb_mode, \
                            ls_en = ls_en, \
                            ps_en = ps_en )


    def disable_light_sensor(self):
        ps_en, ls_en, rgb_mode, sw_reset, sai_ls, sai_ps  = self.get_main_ctrl()
        ls_en = False
        self.set_main_ctrl( sai_ps = sai_ps, \
                            sai_ls = sai_ls, \
                            sw_reset = sw_reset, \
                            rgb_mode = rgb_mode, \
                            ls_en = ls_en, \
                            ps_en = ps_en )


    def enable_proximity_sensor(self):
        ps_en, ls_en, rgb_mode, sw_reset, sai_ls, sai_ps  = self.get_main_ctrl()
        ps_en = True
        self.set_main_ctrl( sai_ps = sai_ps, \
                            sai_ls = sai_ls, \
                            sw_reset = sw_reset, \
                            rgb_mode = rgb_mode, \
                            ls_en = ls_en, \
                            ps_en = ps_en )


    def disable_proximity_sensor(self):
        ps_en, ls_en, rgb_mode, sw_reset, sai_ls, sai_ps  = self.get_main_ctrl()
        ps_en = False
        self.set_main_ctrl( sai_ps = sai_ps, \
                            sai_ls = sai_ls, \
                            sw_reset = sw_reset, \
                            rgb_mode = rgb_mode, \
                            ls_en = ls_en, \
                            ps_en = ps_en )


    def get_als_value(self):
        return self.get_ls_data_green()
    

    def get_rgb_value(self):
        r = self.get_ls_data_red()
        g = self.get_ls_data_green()
        b = self.get_ls_data_blue()
        return r, g, b
    

    def get_ir_value(self):
        return self.get_ls_data_ir()


    def get_ps_value(self):
        return self.get_ps_data()
    

    # write data to register
    def __write_reg(self,reg_addr,set_data):
        self.i2c.writeto_mem( self.i2c_addr, reg_addr, set_data)

    '''
    __SAI_PS = 0x40
    __SAI_LS = 0x20
    __SW_RESET = 0x10
    __RGB_MODE = 0x04
    __LS_EN = 0x02
    __PS_EN = 0x01
    '''
    def set_main_ctrl(self, sai_ps = False, \
                            sai_ls = False, \
                            sw_reset = False, \
                            rgb_mode = False, \
                            ls_en = False, \
                            ps_en = False ):
        data = 0
        if sai_ps:
            data |= self.__SAI_PS
        if sai_ls:
            data |= self.__SAI_LS
        if sw_reset:
            data |= self.__SW_RESET
        if rgb_mode:
            data |= self.__RGB_MODE
        if ls_en:
            data |= self.__LS_EN
        if ps_en:
            data |= self.__PS_EN
        data_byte=bytes([data])
        self.__write_reg(self.__MAIN_CTRL_ADDR, data_byte)


    def set_ps_led(self,frequency = __FREQ_60K, current = __PULSE_CURRENT_100MA):
        data_byte=bytes([frequency | current])
        self.__write_reg(self.__PS_LED_ADDR, data_byte)


    def set_ps_pulses(self,pulses = 0x08):
        data_byte=bytes([pulses])
        self.__write_reg(self.__PS_PULSES_ADDR, data_byte)


    def set_ps_meas_rate(self,resolution = __PS_RESOLUTION_8bit, measurement_rate = __PS_MEASUREMENT_RATE_100ms):
        data_byte=bytes([resolution | measurement_rate])
        self.__write_reg(self.__PS_MEANS_RATE_ADDR, data_byte)


    def set_ls_means_rate(self, resolution = __LS_RESOLUTION_18bit, measurement_rate=__LS_MEASUREMENT_RATE_100ms):
        data_byte=bytes([resolution | measurement_rate])
        self.__write_reg(self.__LS_MEANS_RATE_ADDR, data_byte)


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
    def set_gain(self,gain=__GAIN_3):
        self.i2c.writeto_mem( self.i2c_addr, self.__LS_GAIN_ADDR, bytes([gain]))


    # read data from registers
    def __read_reg(self,reg_addr,data_len):
        return self.i2c.readfrom_mem( self.i2c_addr, reg_addr, data_len )


    def get_main_ctrl(self):
        data_bytes = self.__read_reg(self.__MAIN_CTRL_ADDR,1)
        data_uchar = ustruct.unpack("B",data_bytes)[0]
        ps_en = data_uchar & 0x01
        ls_en = (data_uchar >> 1) & 0x01
        rgb_mode = (data_uchar >> 2) & 0x01
        sw_reset = (data_uchar >> 4) & 0x01
        sai_ls = (data_uchar >> 5) & 0x01
        sai_ps = (data_uchar >> 6) & 0x01
        return ps_en, \
               ls_en, \
               rgb_mode, \
               sw_reset, \
               sai_ls, \
               sai_ps


    def get_ls_means_rate(self):
        data_bytes = self.__read_reg(self.__LS_MEANS_RATE_ADDR,1)
        return ustruct.unpack("B",data_bytes)[0]


    def get_part_id(self):
        data_bytes = self.__read_reg(self.__PART_ID_ADDR,1)
        data_uchar = ustruct.unpack("B",data_bytes)[0] 
        part_id = data_uchar >> 4
        revision_id = data_uchar & 0x0F
        return part_id, revision_id


    def get_main_status(self):
        data_bytes = self.__read_reg(self.__MAIN_STATUS_ADDR,1)
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
        data_bytes = self.__read_reg(self.__LS_DATA_IR_ADDR,2)
        return ustruct.unpack("<H",data_bytes)[0]


    def get_ls_data_ir(self):
        data_bytes = self.__read_reg(self.__LS_DATA_IR_ADDR,3)
        return ustruct.unpack("<L",data_bytes + b'\x00')[0]


    def get_ls_data_green(self):
        data_bytes = self.__read_reg(self.__LS_DATA_GREEN_ADDR,3)
        return ustruct.unpack("<L",data_bytes + b'\x00')[0]


    def get_ls_data_blue(self):
        data_bytes = self.__read_reg(self.__LS_DATA_BLUE_ADDR,3)
        return ustruct.unpack("<L",data_bytes + b'\x00')[0]


    def get_ls_data_red(self):
        data_bytes =self. __read_reg(self.__LS_DATA_RED_ADDR,3)
        return ustruct.unpack("<L",data_bytes + b'\x00')[0]
