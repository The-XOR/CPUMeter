from machine import Pin, PWM
import sys
import uselect
import time
import micropython

# Inizializzazione oggetti vari
pwm_pin = Pin(15) # PIN PWM: 15
pwm = PWM(pwm_pin)
retro = Pin(8, Pin.OUT) # Retroill. pin 8
poller = uselect.poll()
poller.register(sys.stdin, uselect.POLLIN)
pwm.freq(150000) # 150 kHz (basteranno? famo de si....)

# i valori trovati con "Taratura"
min_pwm=20500
max_pwm = 59500

# Breve spiegazione der Duty cycle:
# On RP2040 with MicroPython, duty is a 16-bit value: 0–65535
# 0 = 0% on-time, 65535 = 100% on-time
# Esempio:50% duty = pwm.duty_u16(32768)

def set_pwm(duty):
    print("duty",duty)
    pwm.duty_u16(duty)

def set_load(duty):
    cpu_load = int(duty * (max_pwm-min_pwm) / 100) + min_pwm
    set_pwm(cpu_load)

set_pwm(min_pwm)

print("Retroilluminazione spenta")
retro.value(0)
time.sleep(5)
retro.value(1)
print("Retroilluminazione accesa")

try:
    while True:
        print("Carico CPU = 0")
        set_load(0)
        time.sleep(5)
        
        print("Carico CPU = 50")
        set_load(50)
        time.sleep(5)
        
        print("Carico CPU = 100")
        set_load(100)
        time.sleep(5)
        
        
except Exception as e:
    print("L'eccezione: ", e.value)
    set_load(0)
    
finally:
    retro.value(0)
    set_load(0)
    pwm.deinit()    
    print("Fine.")

