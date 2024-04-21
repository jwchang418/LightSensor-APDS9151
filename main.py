import time
import apds

ls = apds.APDS()
ls.enable_light_sensor()
ls.set_rgb_mode()

while True:
    r, g, b = ls.get_rgb_value()
    ir = ls.get_ir_value()
    print('ir = {}'.format(ir),end='\t')
    print('green = {}'.format(r),end='\t')
    print('blue = {}'.format(g),end='\t')
    print('red = {}'.format(b))
    time.sleep(0.1)
