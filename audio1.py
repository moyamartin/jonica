import pyaudio
import math
import numpy as np
from scipy.linalg import norm
from scipy.fftpack import fft, ifft

CHUNK = 8192
RATE = 48000

c = 343.2
d = 0.2

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16, 
                channels = 2, 
                rate = RATE, 
                input = True,
                frames_per_buffer = CHUNK)

while True:
    data = np.fromstring(stream.read(CHUNK), dtype = np.int16)
    CHL = fft(data[::2])
    CHR = fft(data[1::2])
    aux = (CHL*np.conj(CHR))/(norm(CHL)*norm(CHR))
    fase = ifft(aux)
    index = np.argmax(fase)
    if index < (fase.size/2):
        delay = (index)
        theta = (180.0/np.pi)*math.acos((c*delay)/(RATE*d)) 
    else:
        delay = (fase.size-index)
        theta = 180.0 - (180.0/np.pi)*math.acos((c*delay)/(RATE*d))
    print(theta)


stream.stop_stream()
stream.close()
p.terminate()