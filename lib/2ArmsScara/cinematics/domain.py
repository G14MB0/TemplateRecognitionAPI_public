import numpy as np
import matplotlib.pyplot as plt

# Constants for the robot arms
L1, L2, L3, L4, L5, L6 = 160, 160, 160, 160, 0, 180
alpha = 0  # Base orientation angle, adjust as per your robot's configuration


def is_concave_configuration(xa, ya, xb, yb, xc, yc):
    """
    Determina se la configurazione è concava basandosi sulla posizione dei giunti e dell'effettore finale.
    """
    # # Calcolo dei vettori braccio 1 (A-C) e braccio 2 (B-C)
    # vector_ac = np.array([xc - xa, yc - ya])
    # vector_bc = np.array([xc - xb, yc - yb])

    # # Calcolo del prodotto vettoriale tra i due vettori
    # cross_product = np.cross(vector_ac, vector_bc)

    # # Calcolo dell'angolo tra i due vettori
    # angle = np.arccos(np.dot(vector_ac, vector_bc) / (np.linalg.norm(vector_ac) * np.linalg.norm(vector_bc)))

    # Se l'angolo è maggiore di 180 gradi (in radianti), la configurazione è concava
    # Vettori braccio 1 (A-C) e braccio 2 (B-C)
    u = np.array([xc - xa, yc - ya])  # Vettore AC
    v = np.array([xc - xb, yc - yb])  # Vettore BC

    # Calcolo del prodotto vettoriale usando la formula data
    cross_product_result = (u[0] * v[1]) - (u[1] * v[0])

    # Se il risultato è negativo, la configurazione è concava
    return cross_product_result < 0


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


    psi = np.arctan2(yb-ya, xb-xa)
    h = np.sqrt((yb-ya)**2 + (xb-xa)**2)
    Phi = np.arccos(h/(2*L4)) + psi
    Phi2 = np.pi - (Phi - 2*psi)

    xc = xa + L4 * np.cos(Phi)
    yc = ya + L4 * np.sin(Phi)
    
    # if is_concave_configuration(xa, ya, xb, yb, xc, yc):
    #     raise ValueError()

    # Posizione del secondo giunto
    xd = xc + L5 * np.cos(Phi2)
    yd = yc + L5 * np.sin(Phi2)

    return xa, ya, xb, yb, xc, yc, xd, yd, Phi, Phi2

# Initialize arrays to store positions
xa_list, ya_list, xb_list, yb_list, xc_list, yc_list = [], [], [], [], [], []

# Iterate over a range of angles for q1 and q2 to calculate the domain
q1_range = np.linspace(-180, 180, 360)  # degrees
q2_range = np.linspace(-180, 180, 360)  # degrees

for q1 in q1_range:
    for q2 in q2_range:
        try:
            xa, ya, xb, yb, xc, yc, xd, yd, Phi, Phi2 = calculate_joint_positions(q1, q2, alpha)
            if yc < 0:
                continue
            xa_list.append(xa)
            ya_list.append(ya)
            xb_list.append(xb)
            yb_list.append(yb)
            xc_list.append(xc)
            yc_list.append(yc)
        except:
            pass

# Plot the calculated positions to visualize the domain
plt.figure(figsize=(10, 10))
plt.scatter(xc_list, yc_list, s=1)  # Plot end-effector positions
plt.title('Domain of Possible Movements for the SCARA Robot')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.axis('equal')
plt.grid(True)
plt.show()



index = 45785
# Creazione del plot
fig, ax = plt.subplots()
ax.plot([-L6/2, xa_list[index], xc_list[index]], [0, ya_list[index], yc_list[index]], 'o-', lw=2, markersize=10)
ax.plot([L6/2, xb_list[index], xc_list[index]], [0, yb_list[index], yc_list[index]], 'o-', lw=2, markersize=10)
ax.plot([0 - L6/2, 0 + L6/2], [0, 0], 'k--')  # Linea per indicare L6
ax.plot([xc_list[index], xc_list[index] - L5*np.cos(Phi2)], [yc_list[index], yc_list[index] + L5*np.sin(Phi2)], 'k--')  # Linea per indicare L6

print(xa_list[index], ya_list[index], xb_list[index], yb_list[index], xc_list[index], yc_list[index])
print(is_concave_configuration(xa_list[index], ya_list[index], xb_list[index], yb_list[index], xc_list[index], yc_list[index]))

# Impostazioni per il plot
# ax.set_xlim(-1.5, 1.5)
# ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid(True)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Robot SCARA a doppio braccio')

plt.show()