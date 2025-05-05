from machine import Pin, PWM
import sys
import uselect
import time
import micropython

# Breve spiegazione der Duty cycle:
# On RP2040 with MicroPython, duty is a 16-bit value: 0–65535
# 0 = 0% on-time, 65535 = 100% on-time
# Esempio:50% duty = pwm.duty_u16(32768)

# Inizializzazione oggetti vari
micropython.kbd_intr(-1) # Senza di cus, il byte 0x03 viene interpretato come 'break' e il programma crescia 
pwm_pin = Pin(15) # PIN PWM: 15
pwm = PWM(pwm_pin)
retro = Pin(8, Pin.OUT)
poller = uselect.poll()
poller.register(sys.stdin, uselect.POLLIN)
pwm.freq(100000) # 100 kHz (basteranno? famo de si....)
min_pwm = 6144  # corrisponde, secondo certosina misurazione a spanne, a 0 RPM
max_pwm = 63488 # sempre rigorosamente a spanne, fondo scala RPM
last_received = time.time() # timeout comunicazione

def set_pwm(duty):
    global pwm, retro
    retro.value(0 if duty < min_pwm else 1)
    pwm.duty_u16(65535-duty)

def getvalue():
    global poller
    buf = bytearray(1)
    if poller.poll(50):          
        if sys.stdin.readinto(buf):
            if 0 <= buf[0] <= 100:
                return buf[0]     # 0–255 integer
    return None

# <<<<<<<<<<<<<<<<<<<<<<<< LUP >>>>>>>>>>>>>>>>>>>>>>>>>>
set_pwm(0)
try:
    while True:
        cpu_load = getvalue()
        if cpu_load != None:
            cpu_load = int(cpu_load * (max_pwm-min_pwm) / 100) + min_pwm            
            set_pwm(cpu_load)
            last_received = time.time()

        if time.time() - last_received > 10: # almeno 1 dato ogni 10 secondi!
            set_pwm(0)
        time.sleep(0.05)

except Exception as e:
    print("*** L'eccezione: ", e.value)
    set_pwm(0)
    
finally:
    set_pwm(0)
    pwm.deinit()    
    print("Qui abbiamo finito.")
