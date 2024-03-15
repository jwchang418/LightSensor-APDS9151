import time
import apds

ls = apds.APDS()
ls.set_mode()

while True:
    print('ir = {}'.format(ls.get_ls_data_ir()),end='\t')
    print('green = {}'.format(ls.get_ls_data_green()),end='\t')
    print('blue = {}'.format(ls.get_ls_data_blue()),end='\t')
    print('red = {}'.format(ls.get_ls_data_red()))
    time.sleep(0.1)
