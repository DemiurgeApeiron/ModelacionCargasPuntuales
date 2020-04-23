import numpy as np
import matplotlib.pyplot as plt

plt.style.use("default")

def Angulo(X_, Y_, N_):
    alpha = []
    for fil in range(N_):
        alpha.append([])
        for col in range(N_):
            if X_[fil][col] == 0:
                if Y_[fil][col] > 0:
                    alpha[fil].append(np.pi/2)
                else:
                    alpha[fil].append(-np.pi/2)
            elif X_[fil][col] < 0:
                alpha[fil].append(np.arctan(Y_[fil][col]/X_[fil][col])+np.pi)
            else:
                alpha[fil].append(np.arctan(Y_[fil][col]/X_[fil][col]))
    return alpha

def Color(carga):
    if carga > 0:
        color = 'red'
    else:
        color = 'black'
    return color

def getField(X, Y, q, q_loc):
    eps_0 = 8.8542e-12
    k_e = 1/(4*np.pi*eps_0)
    X_new = X-q_loc[0]
    Y_new = Y-q_loc[1]
    Alpha = Angulo(X_new, Y_new, N)
    r_2 = X_new**2+Y_new**2

    Ex1 = k_e*(q/r_2)*np.cos(Alpha)
    Ey1 = k_e*(q/r_2)*np.sin(Alpha)

    return Ex1, Ey1

Ex = 0
Ey = 0

N = 25
gridMax = 5
gridMin = -5

x = np.linspace(gridMin, gridMax, N)
y = np.linspace(gridMin, gridMax, N)

X, Y = np.meshgrid(x, y)

pInicial = -4
pFinal = -pInicial
q = 2
q_loc_x = np.linspace(pInicial, pFinal, (pFinal-pInicial)*25)
q_loc_y = 2

pInicial2 = -2
pFinal2 = -4
q2 = -2
q_loc_y2 = np.linspace(pInicial2, pFinal2, -(pFinal2-pInicial2)*25)
q_loc_x2 = 0

q3 = -400
q_loc_x3 = 0
q_loc_y3 = 0.05
q4 = 400
q_loc_y4 = q_loc_y3-0.1

for i in q_loc_x:
    Ex_, Ey_ = getField(X, Y, q,[i,q_loc_y])
    Ex += Ex_
    Ey += Ey_
for i in q_loc_y2:
    Ex_, Ey_ = getField(X, Y, q2,[q_loc_x2,i])
    Ex += Ex_
    Ey += Ey_
Ex_, Ey_ = getField(X, Y, q3,[q_loc_x3,q_loc_y3])
Ex += Ex_
Ey += Ey_
Ex_, Ey_ = getField(X, Y, q4,[q_loc_x3,q_loc_y4])
Ex += Ex_
Ey += Ey_

mags = np.sqrt(Ex**2+Ey**2)

Ex_unit = Ex/mags
Ey_unit = Ey/mags

fig, ax = plt.subplots(figsize=(7,7))
ax.quiver(X,Y,Ex_unit,Ey_unit)
for i in q_loc_x:
    ax.scatter(i,q_loc_y,c=Color(q),s=500)
for i in q_loc_y2:
    ax.scatter(q_loc_x2,i,c=Color(q2),s=500)
ax.scatter(q_loc_x3,q_loc_y3,c=Color(q3),s=500)
ax.scatter(q_loc_x3,q_loc_y4,c=Color(q4),s=500)
ax.axis([gridMin, gridMax,gridMin,gridMax])
ax.set_aspect('equal','box')
plt.title("Malaria")
plt.xlabel("Cargas")
plt.tight_layout()
plt.grid(True)
plt.show()

