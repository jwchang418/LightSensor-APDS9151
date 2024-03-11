# RGB Light sensor ADPS-9151 and reapberry pi pico
A digital proximity and RGB sensor called ADPS-9151 is easily to use for detecting ambient light values which contain ir, green, blue and red light.

## Installing
This project adopts MicroPython as the programming language, hence we have to setup the MicroPython on the raspberry pi pico. At raspberry pi's official webside [here](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html), we can find the explain of setup in detail.

## Pin Connection
| raspberry pi pico w | | APDS-9151 |
| :--- | :---: |---: |
| GP16 | -> | SDA |
| GP17 | -> | SCL |
| 3V3 | -> | VCC |
| Gnd | -> | Gnd |

## Thonny
We use Thonny as development enviroment which can be downloaded at [here](https://thonny.org/)

## Code
Save the code as main.py into the raspberry pi pico w.

## license
Licensed under creative commons attribution CC BY-NC-SA