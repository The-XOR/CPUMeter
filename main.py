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
pwm.freq(150000) # 150 kilocicli, mica na pezza a fiori!
# i valori trovati con "Taratura"
min_pwm=20500
max_pwm = 59500
last_received = time.time() # timeout comunicazione

def set_pwm(duty):
    retro.value(0 if duty < min_pwm else 1)
    if duty < min_pwm:
        duty = min_pwm
    pwm.duty_u16(duty)

def getvalue():    
    buf = bytearray(1)
    if poller.poll(50):          
        if sys.stdin.readinto(buf):
            if 0 <= buf[0] <= 100:
                return buf[0]     # 0–255 integer
    return None

# <<<<<<<<<<<<<<<<<<<<<<<< LUP >>>>>>>>>>>>>>>>>>>>>>>>>>
set_pwm(0)
print("Start!")
try:
    while True:
        cpu_load = getvalue()
        if cpu_load != None:
            print("Carico CPU =", cpu_load)            
            cpu_load = int(cpu_load * (max_pwm-min_pwm) / 100) + min_pwm            
            set_pwm(cpu_load)
            last_received = time.time()

        if time.time() - last_received > 10: # almeno 1 dato ogni 10 secondi, altrimenti spegni (doll combing)
            set_pwm(0)
        time.sleep(0.05)

except Exception as e:
    print("*** L'eccezione: ", e.value)
    set_pwm(0)
    
finally:
    set_pwm(0)
    pwm.deinit()    
    print("Qui abbiamo finito.")
