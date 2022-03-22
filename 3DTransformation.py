# Kelompok 6 :
# 1. Annisa Raihana Cahya Putri   (20/460540/TK/51129)
# 2. Auletta Khansa Pradiviasari  (20/456359/TK/50489)
# 3. Hervi Nur Rahmandien         (20/463601/TK/51593)
# 4. Rahmiyatul Hasanah YE        (20/460561/TK/51150)
# 5. Siti Malatania               (20/456380/TK/50510)

import numpy as np
import math
import sys
from graphics import *
from math import *

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def translation(self, xTr, yTr, zTr):
        trans = np.array([[1, 0, 0, xTr], 
                       [0, 1, 0, yTr], 
                       [0, 0, 1, zTr], 
                       [0, 0, 0, 1]])
        result = np.dot(trans, [self.x, self.y, self.z, 1])
        return Point3D(result[0], result[1], result[2])

    def scaling(self, Sx, Sy, Sz):
        sc = np.array([[Sx, 0, 0, 0],
                       [0, Sy, 0, 0],
                       [0, 0, Sz, 0],
                       [0, 0, 0, 1]])
        result = np.dot(sc, [self.x, self.y, self.z, 1])
        return Point3D(result[0], result[1], result[2])

    def shearing(self, shx, shy, shz):
        sh = [[0]*4]*4
        if shx == 0:
            sh = np.array([[1, 0, 0, 0],
                          [0, shy, 0, 0],
                          [0, shz, 1, 0],
                          [0, 0, 0, 1]])
                        
        elif shy == 0:
            sh = np.array([[shx, 0, 0, 0],
                           [0, 1, 0, 0],
                           [shz, 0, 1,0],
                           [0, 0, 0, 1]])
        elif shz == 0:
            sh = np.array([[1, 0, shx, 0], 
                           [0, 1, shy, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])

        result = np.dot(sh, [self.x, self.y, self.z, 1])
        return Point3D(result[0], result[1], result[2])

    def rotationX(self, angle):
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        rtX = np.array([[1, 0, 0, 0], 
                        [0, cosa, -sina, 0], 
                        [0, sina, cosa, 0], 
                        [0, 0, 0, 1]])
        result = np.dot(rtX, [self.x, self.y, self.z,1])
        return Point3D(result[0], result[1], result[2])

    def rotationY(self, angle):
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        rtY = np.array([[cosa, 0, sina, 0], 
                        [0, 1, 0, 0], 
                        [-sina, 0, cosa, 0], 
                        [0, 0, 0, 1]])
        result = np.dot(rtY, [self.x, self.y, self.z,1])
        return Point3D(result[0], result[1], result[2])

    def rotationZ(self, angle):
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        rtZ = np.array([[cosa, -sina, 0, 0], 
                        [sina, cosa, 0, 0], 
                        [0, 0, 1, 0], 
                        [0, 0, 0, 1]])
        result = np.dot(rtZ, [self.x, self.y, self.z,1])
        return Point3D(result[0], result[1], result[2])
    
    def rotateArbitraryAxis(self, point1, point2, angle):
        xVect = point2[0] - point1[0]
        yVect = point2[1] - point1[1]
        zVect = point2[2] - point1[2]
        beta, miu = 0,0

        if zVect == 0:
            if xVect > 0: 
                beta = 90
            else:
                beta = 270
        else:
            beta = atan(xVect/ zVect) * 180 / pi
        if xVect **2 + zVect**2 == 0:
            if yVect > 0:
                miu = 90
            else:
                miu = 270
        else:
            miu = atan(yVect / math.sqrt(xVect **2 + zVect**2)) * 180 / pi
            
        t1 = np.array([[1, 0, 0, 0 - point1[0]],
                       [0, 1, 0, 0 - point1[1]],
                       [0, 0, 1, 0 - point1[2]],
                       [0, 0, 0, 1]])
        
        rotY1 = np.array([[np.cos(-beta),   0, np.sin(-beta), 0],
                          [0,               1, 0,             0],
                          [-(np.sin(-beta)),0, np.cos(-beta), 0],
                          [0,               0, 0,             1]])
        
        rotX1 = np.array([[1, 0,            0,              0],
                          [0, np.cos(miu) , -(np.sin(miu)), 0],
                          [0, np.sin(miu) , np.cos(miu),    0], 
                          [0, 0,            0,              1]])
        
        rotZ = np.array([[np.cos(angle), -(np.sin(angle)), 0, 0],
                         [np.sin(angle), np.cos(angle),    0, 0],
                         [0,             0,                1, 0],
                         [0,             0,                0, 1]])
        
        rotX2 = np.array([[1, 0,            0,               0],
                          [0, np.cos(-miu), -(np.sin(-miu)), 0],
                          [0, np.sin(-miu), np.cos(-miu),    0], 
                          [0, 0,            0,               1]])
        
        rotY2 = np.array([[np.cos(beta),    0, np.sin(beta), 0],
                          [0,               1, 0,            0],
                          [-(np.sin(beta)), 0, np.cos(beta), 0],
                          [0,               0, 0,            1]])
        
        t2 = np.array([[1, 0, 0, point1[0] - 0],
                       [0, 1, 0, point1[1] - 0],
                       [0, 0, 1, point1[2] - 0],
                       [0, 0, 0, 1]])

        result = np.dot(t2,np.dot(rotY2,np.dot(rotX2,np.dot(rotZ,np.dot(rotX1, np.dot(rotY1,np.dot(t1,[self.x,self.y,self.z,1])))))))

        return Point3D(result[0],result[1],result[2])

    
    def project(self, width, height, fov, viewer_distance):
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + width / 2
        y = -self.y * factor + height / 2
        return Point3D(x, y, 1)

#Input user
def question():
    values = []

    operation =int(input(
        """Selamat datang! Transformasi apa yang ingin anda lakukan?
        0. Melihat ukuran asli balok
        1. Translation
        2. Scaling
        3. Shearing
        4. Rotasi terhadap sumbu x, y, atau z
        5. Rotasi terhadap sumbu bebas (arbirary)
        Hanya pilih angka 0 sampai 5!
        Pilihan: """))

    #Jika input diluar nilai yang ada program akan berhenti
    if operation > 5 or operation < 0:
        print("PILIHAN TIDAK TERSEDIA")
        sys.exit()
        
    #tidak dilakukan transformasi
    if operation == 0:
        values = [0]
    
    #Operasi 1 translation
    elif operation == 1:
        xTrans = int(input("Digeser sejauh berapa satuan ke arah sumbu X?\nSatuan: "))
        yTrans = int(input("Digeser sejauh berapa satuan ke arah sumbu Y?\nSatuan: "))
        zTrans = int(input("Digeser sejauh berapa satuan ke arah sumbu Z?\nSatuan: "))
        values = [xTrans, yTrans, zTrans]
        
    #Operasi 2 scaling
    elif operation == 2:
        xFactor = float(input("Berapa faktor scaling x yang diinginkan?\nFaktor: "))
        yFactor = float(input("Berapa faktor scaling y yang diinginkan?\nFaktor: "))
        zFactor = float(input("Berapa faktor scaling z yang diinginkan?\nFaktor: "))
        values = [xFactor, yFactor, zFactor]
        
    #Operasi 3 shearing
    elif operation == 3:
        print("3D shearing apa yang ingin anda lakukan : \n1. xy \n2. yz \n3. xz")
        shear = int(input("Pilih sesuai nomor \n"))
        if shear > 3 or shear < 1:
            print("PILIHAN TIDAK TERSEDIA")
            sys.exit
        
        if shear == 1:
            xShear = float(input("Berapa faktor Shear x yang diinginkan?\nFaktor x: "))
            yShear = float(input("Berapa faktor Shear y yang diinginkan?\nFaktor y: "))
            values = [xShear, yShear, 0]
        elif shear == 2:
            yShear = float(input("Berapa faktor Shear y yang diinginkan?\nFaktor y: "))
            zShear = float(input("Berapa faktor Shear z yang diinginkan?\nFaktor z: "))
            values = [0, yShear, zShear]
        elif shear == 3:
            xShear = float(input("Berapa faktor Shear x yang diinginkan?\nFaktor x: "))
            zShear = float(input("Berapa faktor Shear z yang diinginkan?\nFaktor z: "))
            values = [xShear, 0, zShear]

    #Operasi 4 rotasi
    elif operation == 4:
        xRot = float(input("Rotasi terhadap sumbu X dengan sumbu putar sebesar? (satuan degrees)\n"))
        yRot = float(input("Rotasi terhadap sumbu Y dengan sumbu putar sebesar? (satuan degrees)\n"))
        zRot = float(input("Rotasi terhadap sumbu Z dengan sumbu putar sebesar? (satuan degrees)\n"))
        values = [xRot, yRot, zRot] 
   
    #Operasi 5 rotasi terhadap sumbu bebas
    elif operation == 5:
        x1, y1,z1 = input("Masukkan titik pertama dari sumbu arbitrary (Format: x y z, Contoh: jika titik P(1,2,3) maka dituliskan menjadi '1 2 3' tanpa tanda petik\nTitik: ").split()
        x2, y2,z2 = input("Masukkan titik kedua dari sumbu arbitrary (Format: x y z, Contoh: jika titik P(1,2,3) maka dituliskan menjadi '1 2 3' tanpa tanda petik\nTitik: ").split()
        angle = int(input("Berapa besar sumbu putar yang digunakan? (dalam satuan defrees)\nSudut: "))
        values = [[int(x1), int(y1), int(z1)], [int(x2), int(y2), int(z2)], [angle,0,0]]
    
    #Nilai ini bertujuan agar fungsi utama tahu operasi apa yang dilakukan dan besaran nilai transformasinya
    return operation, values


#Main program
def main(operation, values, points):
    p = 0
    faces = [[0,1,2,3],[1,5,6,2],[5,4,7,6],[4,0,3,7],[0,4,5,1],[3,2,6,7]]
    width, height = 640, 480

    lines = []
    operatedPoints = []
    transformedPoints = []
    
    #tidak terjadi apa-apa
    if operation == 0:
        for i in range(len(points)):
            operatedPoints.append(points[i])
            
    #translasi
    elif operation == 1:
        xTrans, yTrans, zTrans = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].translation(xTrans, yTrans, zTrans))
            
    #scaling
    elif operation == 2:
        xFactor, yFactor, zFactor = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].scaling(xFactor, yFactor, zFactor))
            
    #shearing
    elif operation == 3:
        xShear, yShear, zShear = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].shearing(xShear, yShear, zShear))
            
    #rotasi sumbu xyz
    elif operation == 4:
        angleX, angleY, angleZ = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].rotationX(angleX).rotationY(angleY).rotationZ(angleZ))

    #rotasi sumbu bebas (arbitary axis)
    elif operation == 5:
        point1 = [values[0][0], values[0][1], values[0][2]]
        point2 = [values[1][0], values[1][1], values[1][2]]
        for i in range(len(points)):
            operatedPoints.append(points[i].rotateArbitraryAxis(point1, point2, values[2][0]))

    #Proyeksi koordinat hasil transformasi pada bidang 2D
    for i in range(len(operatedPoints)):
        transformedPoints.append(operatedPoints[i].project(width, height, 500, 10))

    win = GraphWin('3D Transformation', width, height)
    win.setBackground('black')

    #Nilai garis balok
    for i in faces:
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y)))
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
        lines.append(Line(Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y), Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y)))
        lines.append(Line(Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
    
    #Gambar garis balok
    for i in lines:
        i.draw(win)
        i.setFill('white')

    #Titik koordinat di xyz
    for i in range(len(transformedPoints)):
        p = Text(Point(transformedPoints[i].x, transformedPoints[i].y), "{:.2f}, {:.2f}, {:.2f}".format(operatedPoints[i].x, operatedPoints[i].y, operatedPoints[i].z))
        print("{:.2f}, {:.2f}, {:.2f}".format(operatedPoints[i].x, operatedPoints[i].y, operatedPoints[i].z))
        p.setSize(8)
        p.setTextColor('yellow')
        p.draw(win) 

    ask = int(input("Apakah anda ingin melanjutkan dengan transformasi lainnya?\nPilih 1 untuk melanjutkan, dan bilangan lainnya untuk berhenti.\nPilihan: "))
    if ask==1:
        op, val = question()
        win.close()
        main(op,val, operatedPoints)
    else:
        sys.exit()  
    win.getMouse()
    win.close()

#Titik Balok
points = [Point3D(-2,1,-2),
          Point3D(2,1,-2),
          Point3D(2,-1,-2),
          Point3D(-2,-1,-2),
          Point3D(-2,1,2),
          Point3D(2,1,2),
          Point3D(2,-1,2),
          Point3D(-2,-1,2)]

op, val = question()
main(op, val, points)
