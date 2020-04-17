#I utilize numpy to manage matix, mapplotlib to ilustrate the charges
import numpy as np
import matplotlib.pyplot as plt
import math
#I use the next lines to establish the interface size and style
plt.style.use("default")
fig, ax = plt.subplots(figsize=(6,6))

# numberOfPlaneCharges is used to stablish the number of charges between the range of a magnetic plane

resp = 0
Charges = []
ChargesPlane = []
ChargeRange = []
ChargeLocation = [] 
planeNumber = 0
X = []
Y = []
N = []
Ex = 0
Ey = 0
grid_min = 0
grid_max = 0
Ex_unit = 0
Ey_unit = 0

# the purpose of this funcion is to obtain the angles of every matix slot relative to the charge. it uses arctan(slope) to get the angle 
def Angle(x_,y_,N_):
    angles = []
    for _ in range(N_):
        angles.append([])
    for fila in range(N_):
        for columna in range(N_):
            if x_[fila][columna] == 0:
                if y_[fila][columna] != 0:
                    if y_[fila][columna] > 0:
                        angles[fila].append(np.pi/2)
                    else:
                        angles[fila].append(-np.pi/2)
                else:
                    angles[fila].append(0)
            elif x_[fila][columna] < 0:
                angles[fila].append(np.arctan(y_[fila][columna]/x_[fila][columna])+np.pi)
            else:
                angles[fila].append(np.arctan(y_[fila][columna]/x_[fila][columna]))
    return angles   
#this funcion generates the cartesian plane
def GenerateSpace(ChargeNumber):
    global N
    global grid_min
    global grid_max
    #declare two variables to store minimum, Maximum cartesian coordinate
    vM = 0
    vm = ChargeLocation[0][0]
    #compares the coordinates to get the minimum or Maximum eather on "x" or "y"
    for i in ChargeLocation:
        if (i[0] > vM) or (i[1] > vM):
            if i[1] > i[0]:
                vM = i[1]
            else:
                vM = i[0] 
        if (i[0] < vm) or (i[1] < vm):
            if i[1] < i[0]:
                vm = i[1]
            else:
                vm = i[0] 
    #sets the minimum and maximum of the grid +- space so it aint so tight to the charge both for a simple charge or combinated
    if resp == 1:
        N = 10
        grid_min = vm - float(math.ceil(N/(10/(len(Charges)))))
        grid_max = vM + float(math.ceil(N/(10/(len(Charges)))))
        print(len(Charges))
        print(float(math.ceil(N/10/(len(Charges)))))
    else:
        N = 25
        """grid_min = vm - float(math.ceil(N/(len(Charges)/numberOfPlaneCharges)))*0.3
        grid_max = vM + float(math.ceil(N/(len(Charges)/numberOfPlaneCharges)))*0.3 """
        grid_min = vm -abs(vM)
        grid_max = vM +abs(vm)
    #creates the cartesian coordinates both for "x" and "y"
    x = np.linspace(grid_min,grid_max,N)
    y = np.linspace(grid_min,grid_max,N)
    #creates the cartesian plane with multiple levels for both "x" and "y"
    return(np.meshgrid(x,y))
def Graph(X,Y,Ex_unit,Ey_unit,_q,q,grid_min,grid_max):
    #decides wether the charge is negative or positive and the size
    color =""
    if q < 0:
        color ='blue'
    else:
        color ='red'
    if resp == 1:
        size = 500
    else:
        size = 100
    #graphs the vectors and charges
    ax.quiver(X,Y,Ex_unit,Ey_unit)
    ax.scatter(_q[0],_q[1],c=color ,s=size)
    ax.axis([grid_min,grid_max,grid_min,grid_max])
    ax.set_aspect('equal','box')
#this funcion ask for the puntual charges and their location and puts them in their respective variables 
def ChargesGenerator(ChargeNumber):
    global Charges
    global ChargeLocation
    for _ in range(ChargeNumber): 
        ChargeInfo = input("put the Charges and their location like: -2E-6,1,-1: ")
        CL = ChargeInfo.split(",")
        Charges.append(float(CL[0]))
        ChargeLocation.append([int(CL[1]), int(CL[2])])
#this fuction does the calculations for the puncutal charges
def Puntual(): 
    global ChargeNumber, X,Y, Ex, Ey, Ex_unit, Ey_unit
    global Ex
    global Ey  
    
    angles = []
    #ask the number of charges you would like so the may the program repeat as many times as needed
    ChargeNumber = int(input("how many charges wolud you like (int): "))
    ChargesGenerator(ChargeNumber)
    
    X,Y = GenerateSpace(ChargeNumber)
    

    K = 9E9
 
    for i in range(ChargeNumber):
        # makes the cartesian plane relative to the charge
        XNew = X-ChargeLocation[i][0]
        YNew = Y-ChargeLocation[i][1]
        #gets the angle relative to the charge
        angles = Angle(XNew,YNew,N)
        #gets the distance to every point relative to the charge
        R = XNew**2+YNew**2
        #makes the sum of forces using the coulomb equation
        Ex += K*(Charges[i]/R)*np.cos(angles)
        Ey += K*(Charges[i]/R)*np.sin(angles)
    #gets the magnitude
    mags = np.sqrt(Ex**2+Ey**2)
    #gets the unit vectors
    Ex_unit = Ex/mags
    Ey_unit = Ey/mags

#this funcion ask for the plane charges and their location and puts them in their respective variables
def ChargesGeneratorPlane(planeNumber):
    global Charges
    global ChargeRange
    for i in range(planeNumber): 
        ChargeInfoPlane = input("put the planes Charge and their location like: -2E-6,1,-1,-1,-1: ")
        CP = ChargeInfoPlane.split(",")
        ChargesPlane.append(float(CP[0]))
        ChargeRange.append([float(CP[1]), float(CP[2]), float(CP[3]), float(CP[4])])
    #for every plane ads charges between the range of the plane
    for i in range(planeNumber):
        numeratorSlope = ChargeRange[i][3]-ChargeRange[i][1]
        denominatorSlope = ChargeRange[i][2]-ChargeRange[i][0]
        numberOfPlaneCharges = int(math.sqrt((denominatorSlope)**2+(numeratorSlope)**2)*25)
        #checks whats the beginning of the planes
        if ChargeRange[i][0] < ChargeRange[i][2]:
            dsx = ChargeRange[i][0]
        else:
            dsx = ChargeRange[i][2]

        if ChargeRange[i][1] < ChargeRange[i][3]:
            dsy = ChargeRange[i][1]
        else:
            dsy = ChargeRange[i][3]
        #checks if the plane is vertical because the slope will be infinite
        if (denominatorSlope) != 0:
            slope = numeratorSlope/denominatorSlope
            d = abs(ChargeRange[i][2]-ChargeRange[i][0])/numberOfPlaneCharges
            ds = dsx
        else:
            ds = dsy
            d = abs(ChargeRange[i][3]-ChargeRange[i][1])/numberOfPlaneCharges
            
        
        for _ in range(numberOfPlaneCharges):
            if (denominatorSlope) != 0:
                linealEcuation = slope*ds -slope*ChargeRange[i][0] + (ChargeRange[i][1])
                xp = ds
                yp = linealEcuation
            else:
                xp = dsx
                yp = ds
            #ads the charges
            Charges.append(ChargesPlane[i])
            ChargeLocation.append([xp, yp])
            ds += d
#this fuction does the calculations for the puncutal charges          
def Plane(): 
    global planeNumber, X,Y, Ex, Ey, Ex_unit, Ey_unit
    global Ex
    global Ey    
    angles = []
    #ask the number of planes you would like so the may the program repeat as many times as needed
    planeNumber = int(input("how many planes wolud you like (int): "))
    ChargesGeneratorPlane(planeNumber)
    X,Y = GenerateSpace(planeNumber)
    
    K = 9E9

    for i in range(len(Charges)):
        # makes the cartesian plane relative to the charge
        XNew = X-ChargeLocation[i][0]
        YNew = Y-ChargeLocation[i][1]
        #gets the angle relative to the charge
        angles = Angle(XNew,YNew,N)
        #gets the distance to every point relative to the charge
        R = XNew**2+YNew**2
        #makes the sum of forces using the coulomb equation
        Ex += K*(Charges[i]/R)*np.cos(angles)
        Ey += K*(Charges[i]/R)*np.sin(angles)
    #gets the magnitude
    mags = np.sqrt(Ex**2+Ey**2)
    #gets the unit vectors
    Ex_unit = Ex/mags
    Ey_unit = Ey/mags

def Main():
    global resp
    resp = int(input("would you like to simulate: \n 1. Puntual Charges \n 2. Plane Charges \n 3. Both \n"))
    if resp == 1:
        Puntual()
    elif resp == 2:
        Plane()
    elif resp == 3:
        Puntual()
        Plane()

    for i in range(len(Charges)):
        Graph(X,Y,Ex_unit,Ey_unit,ChargeLocation[i],Charges[i],grid_min,grid_max)

Main()
plt.show() 