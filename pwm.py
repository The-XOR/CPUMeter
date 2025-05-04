from machine import Pin, PWM
import sys
import uselect
import time
import micropython

# Inizializzazione oggetti vari
pwm_pin = Pin(15) # PIN PWM: 15
pwm = PWM(pwm_pin)
retro = Pin(8, Pin.OUT)
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

def getvalue():
    global poller
    buf = bytearray(1)
    if poller.poll(50):          # wait up to 100 ms
        n = sys.stdin.readinto(buf)
        if n:                     # n==1 if a byte was read
            if 0 <= buf[0] <= 100:
                return buf[0]            # 0–255 integer
    return None

set_pwm(min_pwm)
retro.value(0) # retroilluminazione spena

try:
    while True:
        cpu_load = getvalue()
        if cpu_load != None:
            cpu_load = int(cpu_load * (max_pwm-min_pwm) / 100) + min_pwm
            set_pwm(cpu_load)
            retro.value(1) # accende retroilluminazione per segnalare che il programma è in esecuzione

        time.sleep(0.05)
        
except Exception as e:
    print("L'eccezione: ", e.value)
    set_pwm(min_pwm)
    
finally:
    retro.value(0)
    pwm.deinit()    
    print("Fine.")
