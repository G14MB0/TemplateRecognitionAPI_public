import numpy as np
import matplotlib.pyplot as plt


# Definizione delle lunghezze dei bracci (esempio)
L1, L2, L3, L4, L5, L6 = 0.7, 0.7, 1.2, 1.2, 0, 0.8


yMin = np.sqrt((L4-L2)**2 - (L6/2)**2)


# Definizione dei parametri di orientamento (esempio)
alpha = 0  # Cambia questo in base alle specifiche del tuo robot

# Test della cinematica inversa con posizione e orientamento dell'effettore finale
xd, yd, phi2 = +1.12, -1.05, 0  # Sostituisci con i valori desiderati

radius1 = np.sqrt((xd+L6/2)**2 + yd**2)
radius2 = np.sqrt((xd-L6/2)**2 + yd**2)

if radius1 >= L2+L4 or radius2 >= L1+L3:
    raise ValueError("out of domain")



# Funzioni per calcolare le variabili intermedie e i valori dei giunti
def calculate_intermediate_vars(xd, yd, phi2):
    # Calcola xc, yc basandosi su xd, yd, e phi2
    xc = xd - L5 * np.cos(np.radians(phi2))
    yc = yd - L5 * np.sin(np.radians(phi2))

    # Calcola k1, k2
    k1 = np.sqrt((xc + L6/2)**2 + yc**2)
    k2 = np.sqrt((xc - L6/2)**2 + yc**2)
    
    return xc, yc, k1, k2

def inverse_kinematics(xd, yd, phi2):
    # Calcola le variabili intermedie
    xc, yc, k1, k2 = calculate_intermediate_vars(xd, yd, phi2)
    # Calcola ξ1, ξ2
    xi1 = np.arctan2(yc, xc + L6/2)
    xi2 = np.arctan2(yc, xc - L6/2)
    
    # print("\n",(L2**2 + k1**2 - L4**2), (2 * L1 * k2), "\n")
    # Calcola γ1, γ2
    gamma1 = np.arccos((L2**2 + k1**2 - L4**2) / (2 * L1 * k1))
    gamma2 = np.arccos((L2**2 + k2**2 - L4**2) / (2 * L1 * k2))
    
    # Calcola q1, q2
    q1 = np.degrees(xi1 + gamma1)
    q2 = np.degrees(xi2 - gamma2)
    
    # Calcola q3
    q3 = alpha - phi2
    
    return q1, q2, q3


q1, q2, q3 = inverse_kinematics(xd, yd, phi2)

print(q1, q2, q3)  # Output dei valori dei giunti
# Funzione per calcolare la posizione dei giunti e dell'effettore finale
def calculate_joint_positions(q1, q2, q3):
    # Convertire angoli in radianti
    q1_rad = np.radians(q1)
    q2_rad = np.radians(q2)

    # Calcolo delle posizioni dei giunti
    # Posizione del primo giunto
    xb = L1 * np.cos(q2_rad) + L6/2
    yb = L1 * np.sin(q2_rad)

    xa = L2 * np.cos(q1_rad) - L6/2
    ya = L2 * np.sin(q1_rad)

    print(f"A, B: {xa},{ya},  {xb},{yb}")

    psi = np.arctan2(yb-ya, xb-xa)
    h = np.sqrt((yb-ya)**2 + (xb-xa)**2)
    Phi = np.arccos(h/(2*L4)) + psi
    Phi2 = np.pi - (Phi - 2*psi)
    print(psi, h, Phi, Phi2)


    xc = xa + L4 * np.cos(Phi)
    yc = ya + L4 * np.sin(Phi)
    print(xc, yc)

    # Posizione del secondo giunto
    xd = xc + L5 * np.cos(Phi2)
    yd = yc + L5 * np.sin(Phi2)

    
    return xa, ya, xb, yb, xc, yc, xd, yd, Phi, Phi2


def verify_and_adjust_angles(xd_desired, yd_desired, phi2):
    # Calculate initial joint angles using inverse kinematics
    q1, q2, q3 = inverse_kinematics(xd_desired, yd_desired, phi2)
    
    # Use forward kinematics to calculate the end-effector position from these angles
    xa, ya, xb, yb, xc, yc, xd, yd, Phi, Phi2 = calculate_joint_positions(q1, q2, q3)
    
    # Define a tolerance for comparing desired and calculated positions
    tolerance = 0.5  # Adjust based on your system's precision requirements
    
    # Check if the calculated position matches the desired position within tolerance
    if (abs(xd - xd_desired) <= tolerance and
        abs(yd - yd_desired) <= tolerance):
        print("FISRT")
        # If it matches, return the original angles
        return xa, ya, xb, yb, xc, yc, xd, yd, Phi, Phi2
    else:
        raise ValueError("Error in forward kinematic")

# # Calcola la posizione dei giunti e dell'effettore finale
xa, ya, xb, yb, xc, yc, xd, yd, Phi, Phi2 = verify_and_adjust_angles(xd, yd, phi2)


# Creazione del plot
fig, ax = plt.subplots()
ax.plot([-L6/2, xa, xc], [0, ya, yc], 'o-', lw=2, markersize=10)
ax.plot([L6/2, xb, xc], [0, yb, yc], 'o-', lw=2, markersize=10)
ax.plot([0 - L6/2, 0 + L6/2], [0, 0], 'k--')  # Linea per indicare L6
ax.plot([xc, xc - L5*np.cos(Phi2)], [yc, yc + L5*np.sin(Phi2)], 'k--')  # Linea per indicare L6

# Impostazioni per il plot
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid(True)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Robot SCARA a doppio braccio')

plt.show()
