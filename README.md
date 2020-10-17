# Evoluciones-Sensibles
Código fuente del proyecto de Evoluciones Sensibles de Lucía Rosselot, Diseño UC 2020.


## Recursos Importantes

* *Getting started with MicroPython on the ESP32*: https://docs.micropython.org/en/latest/esp32/tutorial/intro.html

* *Controlling NeoPixels*: https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html

* *_thread in ESP32*: https://docs.pycom.io/firmwareapi/micropython/_thread/#app

* *Python threads*: https://www.youtube.com/watch?v=IEEhzQoKtQU

* *HC-SR04 Sensor Driver in Mipropython*: https://github.com/rsc1975/micropython-hcsr04

* *ESP32 firmware*: https://micropython.org/download/esp32/


## Comandos útiles

* esptool.py -p /dev/ttyUSB0 erase_flash

* esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 firmware/esp32-idf3-20200902-v1.13.bin

* ampy --port /dev/ttyUSB0 ls

* cu -l /dev/ttyUSB0 -s 115200
    ~.


## To Do

* Conocer bien el rango de fade de pwm en los leds
