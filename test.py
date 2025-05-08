from machine import Pin, PWM
import sys
import uselect
import time
import micropython

# Inizializzazione oggetti vari
pwm_pin = Pin(15) # PIN PWM: 15
pwm = PWM(pwm_pin)
retro = Pin(14, Pin.OUT) # Retroill. pin 14
poller = uselect.poll()
poller.register(sys.stdin, uselect.POLLIN)
pwm.freq(100000) # 100 kHz (basteranno? famo de si....)
min_pwm = 6144  # corrisponde, a spanne, a 0 RPM
max_pwm = 63488 # corrisponde, a spanne, a fondo scala RPM
micropython.kbd_intr(-1) # Senza di cus, il byte 0x03 viene interpretato come 'break' e il programma crescia 

# Breve spiegazione der Duty cycle:
# On RP2040 with MicroPython, duty is a 16-bit value: 0–65535
# 0 = 0% on-time, 65535 = 100% on-time
# Esempio:50% duty = pwm.duty_u16(32768)

def set_pwm(duty):
    global pwm
    pwm.duty_u16(65535-duty)

set_pwm(min_pwm)

try:
    while True:
        print("On")
        retro.value(1)
        cpu_load = 0
        cpu_load = int(cpu_load * (max_pwm-min_pwm) / 100) + min_pwm
        set_pwm(cpu_load)
        time.sleep(1)
        retro.value(0)
        print("Off")
        time.sleep(1)
        
except Exception as e:
    print("L'eccezione: ", e.value)
    set_pwm(min_pwm)
    
finally:
    retro.value(0)
    pwm.deinit()    
    print("Fine.")
