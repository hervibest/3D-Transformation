from graphics import *
import numpy as np
from math import *
import sys


#Class ini untuk melakukan operasi terhadap titik 3 dimensi termasuk memproyeksikannya dalam bidang 2 dimensi
class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
    #Translation
    def translate(self, xTrans, yTrans, zTrans):
        matrix = np.array([
            [1,0,0,xTrans], 
            [0,1,0,yTrans], 
            [0,0,1,zTrans], 
            [0,0,0,1]
            ])
        vector = np.array([self.x, self.y, self.z,1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
    #Scaling
    def scale(self, Sc):
        matrix = np.array([
            [Sc, 0, 0, 0],
            [0, Sc, 0, 0],
            [0,0, Sc, 0],
            [0,0,0,1]
        ])
        vector = np.array([self.x, self.y, self.z, 1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
    #Shearing
    def Shear(self, Shx,Shy,Shz):
        Shxy = np.array([
            [1, 0, Shx, 0], 
            [0, 1, Shy, 0],
            [0, 0, 1, 0],
            [0,0,0,1]
            ])
        Shyz = np.array([
            [1,0,0,0],
            [0, Shy, 0,0],
            [0, Shz, 1,0],
            [0,0,0,1]
            ])
        Shxz = np.array([
            [Shx, 0, 0, 0],
            [0, 1, 0, 0],
            [Shz, 0, 1,0],
            [0,0,0,1]
            ])
        vector = np.array ([self.x, self.y, self.z, 1])
        if Shz == 0:
            result = Shxy.dot(vector)
        elif Shy == 0:
            result = Shxz.dot(vector)
        elif Shx == 0:
            result = Shyz.dot(vector)
        
        return Point3D(result[0], result[1], result[2])
    #Rotasi pada sumbu x
    def rotateX(self, angle):
        """ Merotasikan titik terhadap sumbu X sesuai sudut yang diinginkan (degrees) """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        matrix = np.array(
            [[1,0,0,0], 
            [0, cosa, -sina, 0], 
            [0,sina, cosa, 0], 
            [0,0,0,1]])
        vector = np.array([self.x, self.y, self.z,1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
    #Rotasi terhadap sumbu Y
    def rotateY(self, angle):
        """ Merotasikan titik terhadap sumbu Y sesuai sudut yang diinginkan (degrees) """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        matrix = np.array([
            [cosa,0,sina,0], 
            [0, 1, 0, 0], 
            [-sina,0, cosa, 0], 
            [0,0,0,1]
            ])
        vector = np.array([self.x, self.y, self.z,1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
    #Rotasi terhadap sumbu Z
    def rotateZ(self, angle):
        """ Merotasikan titik terhadap sumbu Z sesuai sudut yang diinginkan (degrees) """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        matrix = np.array([
            [cosa, -sina ,0,0], 
            [sina, cosa , 0, 0], 
            [0 ,0, 1, 0], 
            [0,0,0,1]
            ])
        vector = np.array([self.x, self.y, self.z,1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
    #Rotasi terhadap sumbu bebas (arbitrary)
    def rotateArbitraryAxis(self, point1, point2, angle):
        #Determining arbitrary axis
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
            miu = atan (yVect / sqrt(xVect **2 + zVect**2)) * 180 / pi
        step1 = self.translate(0 - point1[0], 0 - point1[1], 0 - point1[2])
        step2 = step1.rotateY(-beta)
        step3 = step2.rotateX(miu)
        step4 = step3.rotateZ(angle)
        step5 = step4.rotateX(-miu)
        step6 = step5.rotateY(beta)
        result = step6.translate(point1[0] - 0, point1[1] - 0, point1[2] - 0)

        return result
    
    #Proyeksi ke bidang 2 dimensi
    def project(self, width, height, fov, viewer_distance):
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + width / 2
        y = -self.y * factor + height / 2
        return Point3D(x, y, 1)

#Fungsi ini berfungsi untuk meminta input dari pengguna
def question():
    values = []
    #Program mendeteksi transformasi yang akan dilakukan dengan input dibawah
    operation =int(input(
        """Selamat datang! Transformasi apa yang ingin anda lakukan?
        0. Melihat ukuran asli balok
        1. Translation
        2. Scaling
        3. Shearing
        4. Rotation terhadap sumbu x, y, atau z
        5. Rotation terhadap sumbu bebas (arbirary)
        Hanya pilih angka 0 sampai 5!
        (Panduan: untuk melihat ukuran asli balok, tuliskan angka '0' tanpa tanda petik)
        Pilihan: """))
    #Ketika pengguna memasukan nilai diluar yang diterima, program akan dihentikan
    if operation > 5 or operation < 0:
        print("PILIHAN TIDAK TERSEDIA")
        sys.exit()
        
    #tidak dilakukan transformasi
    if operation == 0:
        values = [0]
    
    #Operasi 1 adalah translasi, bagian ini untuk memasukan nilai translasi
    elif operation == 1:
        xTrans = int(input("Digeser sejauh berapa satuan ke arah sumbu X?\nSatuan: "))
        yTrans = int(input("Digeser sejauh berapa satuan ke arah sumbu Y?\nSatuan: "))
        zTrans = int(input("Digeser sejauh berapa satuan ke arah sumbu Z?\nSatuan: "))
        values = [xTrans, yTrans, zTrans]
        
    #Operasi 2 adalah scaling, bagian ini untuk memasukan seberapa besar scaling akan dilakukan
    elif operation == 2:
        factor = float(input("Berapa faktor scaling yang diinginkan?\nFaktor: "))
        values = [factor]
        
    #Operasi 3 adalah Shear, bagian ini untuk memasukkan nilai shear
    elif operation == 3:
        xShear = float(input("Shearing ke arah sumbu X sebanyak berapa satuan?\nSatuan: "))
        yShear = float(input("Shearing ke arah sumbu Y sebanyak berapa satuan?\nSatuan: "))
        zShear = float(input("Shearing ke arah sumbu Z sebanyak berapa satuan?\nSatuan: "))
        if(xShear != 0 and yShear != 0 and zShear != 0):
            print("INPUT TIDAK SESUAI! Hanya isikan 2 bilangan non-zero")
            sys.exit()
        values = [xShear, yShear, zShear]

    #Operasi 4 adalah rotasi, bagian ini untuk memasukan sudut rotasi
    elif operation == 4:
        xRot = float(input("Rotasi terhadap sumbu X dengan sumbu putar sebesar? (dalam satuan degrees)\n"))
        yRot = float(input("Rotasi terhadap sumbu Y dengan sumbu putar sebesar? (dalam satuan degrees)\n"))
        zRot = float(input("Rotasi terhadap sumbu Z dengan sumbu putar sebesar? (dalam satuan degrees)\n"))
        values = [xRot, yRot, zRot] 
   
    #Operasi 5 adalah rotasi pada arbitrary axis, bagian ini untuk memasukan axis dan sudut rotasi
    elif operation == 5:
        x1, y1,z1 = input("Masukkan titik pertama dari sumbu arbitrary (Format: x y z, Contoh: jika titik P(1,2,3) maka dituliskan menjadi '1 2 3' tanpa tanda petik\nTitik: ").split()
        x2, y2,z2 = input("Masukkan titik kedua dari sumbu arbitrary (Format: x y z, Contoh: jika titik P(1,2,3) maka dituliskan menjadi '1 2 3' tanpa tanda petik\nTitik: ").split()
        angle = int(input("Berapa besar sumbu putar yang digunakan? (dalam satuan defrees)\nSudut: "))
        values = [[int(x1), int(y1), int(z1)], [int(x2), int(y2), int(z2)], [angle,0,0]]
    
    #Nilai ini bertujuan agar fungsi utama tahu operasi apa yang dilakukan dan besaran nilai transformasinya
    return operation, values


#Fungsi ini merupakan fungsi operasi utama dari program 
def main(operation, values, points):
    #Koordinat titik telah pre-assigned 
    p = 0
    # variabel ini menyimpan titik yang harus dihubungkan untuk membentuk sebuah permukaan pada balok
    # misal 0 1 2 3 artinya sisi pertama terbentuk dengan menghubungkan titik 0 1 2 dan 3
    # 0 1 2 3 tersebut merujuk kepada index pada array points
    faces = [[0,1,2,3],[1,5,6,2],[5,4,7,6],[4,0,3,7],[0,4,5,1],[3,2,6,7]]

    width, height = 1280, 720
    #Untuk menyimpan garis yang dibentuk:
    lines = []
    #Untuk menyimpan titik yang dilakukan transformasi:
    operatedPoints = []
    #Untuk menyimpan titik yang telah diproyeksi
    transformedPoints = []
    
    #tidak dilakukan apa apa
    if operation == 0:
        for i in range(len(points)):
            operatedPoints.append(points[i])
            
    #Melakukan translasi
    elif operation == 1:
        xTrans, yTrans, zTrans = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].translate(xTrans, yTrans, zTrans))
            
    #Melakukan scaling
    elif operation == 2:
        Sc = values[0]
        for i in range(len(points)):
            operatedPoints.append(points[i].scale(Sc))
            
    #Melakukan Shear
    elif operation == 3:
        xShear, yShear, zShear = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].Shear(xShear, yShear, zShear))
            
    #Melakukan Rotasi terhadap sumbu x y dan z
    elif operation == 4:
        angleX, angleY, angleZ = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].rotateX(angleX).rotateY(angleY).rotateZ(angleZ))

    #Melakukan rotasi terhadap arbitrary axis
    elif operation == 5:
        point1 = [values[0][0], values[0][1], values[0][2]]
        point2 = [values[1][0], values[1][1], values[1][2]]
        for i in range(len(points)):
            operatedPoints.append(points[i].rotateArbitraryAxis(point1, point2, values[2][0]))

    #Melakukan proyeksi koordinat yang telah di transformasi pada bidang 2 dimensi
    for i in range(len(operatedPoints)):
        transformedPoints.append(operatedPoints[i].project(width, height, 300, 5))

    win = GraphWin('3D Transformation', width, height)
    win.setBackground('black')
    

    #Menentukan nilai garis pembentuk balok
    for i in faces:
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y)))
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
        lines.append(Line(Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y), Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y)))
        lines.append(Line(Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
    #Menggambar garis pembentuk balok
    for i in lines:
        i.draw(win)
        i.setFill('white')

    #Menampilkan titik koordinat di x y z
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

#Nilai ini bertujuan agar fungsi utama tahu operasi apa yang dilakukan dan besaran nilai transformasinya
points = [Point3D(2,3,2),
            Point3D(4,3,2),
            Point3D(4,5,2),
            Point3D(2,5,2),
            Point3D(4,5,6),
            Point3D(6,5,6),
            Point3D(6,7,6),
            Point3D(4,7,6)]
op, val = question()
main(op, val, points)