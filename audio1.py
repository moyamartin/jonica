import pyaudio
import math
import numpy as np
from scipy.linalg import norm
from scipy.fftpack import fft, ifft
import RPi.GPIO as GPIO
import time




# Configurar servo
DC0 = 4.5
DC180 = 10.5
FServo = 50
##################
DCNeutral = (DC180+DC0)/2
m = (DC180-DC0)/180.0
h = DC0
##################
UMBRAL = 5.0

# Obtener el DC a partir del angulo
def set_angle(angle):
	global m
	global h
	return (m*angle + h)

GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.OUT)
pwm = GPIO.PWM(24,FServo)
# Servo en el canal 24
pwm.start(DCNeutral)
# Servo comienza en posicion central 
theta_sa = 90.0 #angulo actual del servo referido al sistema de referencia absoluto
theta_sf = 0.0

# Parametros de la interfaz de audio
CHUNK = 8192    # Leo buffers de 8192 samples
RATE = 48000    # Frecuencia de muestreo 48 KHz
Fs = 48000.0
# Parametros del sistema fisico
c = 343.2       # Velocidad del sonido
d = 0.2         # Distancia entre microfonos

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16, 
                channels = 2, 
                rate = RATE, 
                input = True,
                frames_per_buffer = CHUNK)

# Bucle infinito
while True:
    # Obtengo un frame (2*8192 muestras = 16384 samples)
    data = np.fromstring(stream.read(CHUNK), dtype = np.int16)
    # Separo en canal izquiero y derecho, y les calculo su FFT              
    CHL = fft(data[::2])                                                    
    CHR = fft(data[1::2])
    # Calculo GCC
    aux = (CHL*np.conj(CHR))/(norm(CHL)*norm(CHR))                      
    # Inversa
    fase = ifft(aux)
    # Obtengo el indice en el cual se encuentra el maximo                                                        
    index = np.argmax(fase)
    print("####################")

    # Observo si el indice esta en la primera o segunda mitad para corregir el delay obtenido (GCC simetrica)                                   
    if index < (fase.size/2):                                               
        delay = (index)
        # angulo medido por los microfonos
        theta_m = (180.0/np.pi)*np.arccos((c*delay)/(Fs*d)) 
    else:
        delay = (fase.size-index)
        # angulo medido por los microfonos
        theta_m = 180.0 - (180.0/np.pi)*np.arccos((c*delay)/(Fs*d) )   
    if np.isnan(theta_m):
        print ("Ignorado")
    elif (theta_m > 180.0):
        print ("Theta > 180")
    else:
        print("Indice: ", index)
        print("Angulo Estimado: %.2f" % theta_m)
         # Calculo el angulo final del servo (donde debe ir) a partir del angulo actual y del medido por los mics
        theta_sf = theta_m + theta_sa - 90
         # Obtengo el dCycle para el servo a partir del angulo
        if(np.abs(theta_sf-theta_sa) < UMBRAL ):
            print("Umbral chico, no muevo el servo")
        else:
            setpoint = set_angle(theta_sf)                                     
            if (setpoint < 0.0 and setpoint > 100.0):
                print("DC invalido")
            else:
                print("Setpoint dCycle: %.2f" % setpoint)
                #Cambio el dCycle del servo
                pwm.ChangeDutyCycle(setpoint)                                 
        
    # Actualizo el valor de angulo actual para la proxima iteracion
    theta_sa = theta_sf                                                


pwm.stop()
GPIO.cleanup()
stream.stop_stream()
stream.close()
p.terminate()