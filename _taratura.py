from machine import Pin, PWM
import sys
import uselect
import time
import micropython

# Inizializzazione oggetti vari
pwm_pin = Pin(15) # PIN PWM: 15
pwm = PWM(pwm_pin)

# **** COLLEGARE UN PULSANTONE TRA PIN 8 E MASSA: AD OGNI PRESSIONE VIENE INCREMENTATO IL VALORE DI PIVUEMME ****
cambio = Pin(8, Pin.IN, Pin.PULL_UP)
poller = uselect.poll()
poller.register(sys.stdin, uselect.POLLIN)
pwm.freq(150000) # 150 kilocicli, mica na pezza a fiori!

# Breve spiegazione der Duty cycle:
# On RP2040 with MicroPython, duty is a 16-bit value: 0–65535
# 0 = 0% on-time, 65535 = 100% on-time
# Esempio:50% duty = pwm.duty_u16(32768)

min_pwm=20000
max_pwm = 61000

cur_pwm=min_pwm
step_pwm=1000
pwm.duty_u16(min_pwm)

try:
    while True:
        if cambio.value() == 0:
            cur_pwm=cur_pwm+step_pwm
            if cur_pwm > max_pwm:
                cur_pwm=min_pwm
            print("Current: ",cur_pwm)
            pwm.duty_u16(cur_pwm)
            while cambio.value() == 0:
                pass
        else:
            time.sleep(0.1)
        
        
except Exception as e:
    print("L'eccezione: ", e.value)
    
    
finally:
    pwm.deinit()    
    print("Fine.")
