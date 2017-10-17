Flag_newValue = 0
UMBRAL_MIN = 5.0
UMBRAL_MAX = 30.0

Outliers_cnt = 0
Outlierts_MAX = 10

# Calculo el angulo final del servo (donde debe ir) a partir del angulo actual y del medido por los mics
theta_sf = theta_m + theta_sa - 90

if(np.abs(theta_sf-theta_sa) < UMBRAL_MIN ):
    print("Umbral chico, no muevo el servo")
elif (Flag_newValue == 0):          # Flag en 0, quiere decir que es una nueva medicion
    set_angle(theta_sf)             # Seteo el angulo calculado
    theta_sa = theta_sf
    Flag_newValue = 1               # Seteo el flag
else:
    # Si entro aca quiere decir que ya se realizo una medicion antes, tengo que ver si hay mucha diferencia en grados
    if(np.abs(theta_sf-theta_sa) > UMBRAL_MAX ):
        print("Posible Oulier, espero un poco...")
        i = i+1
        if(i == Outlierts_MAX):
            i = 0
            Flag_newValue = 0   # Al bajar el flag, en la proxima iteracion cae al statement elif anterior