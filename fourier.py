import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
import sys
sys.setrecursionlimit(10000)
import joblib
import random
import pandas as pd

point_x=hoge #極座標の原点
point_y=hoge


img = cv2.imread('C:/Users/hoge')
pixel_y, pixel_x, _ = img.shape

r=[]
s=[]
x1=[]
y1=[]

for y in range(pixel_y-1,1,-1): #黒画素のみ(x1,y1)に格納
    for x in range(pixel_x):
        if img[y,x,2]==0 and img[y,x,1]==0 and img[y,x,0]==0:
            x1.append(x)
            y1.append(y)

keep_x=[]
keep_y=[]

keep_x.append(x1[0])
keep_y.append(y1[0])
img[y1[0],x1[0],2]=0
img[y1[0],x1[0],1]=255
img[y1[0],x1[0],0]=0

i=0
for k in range(len(x1)):
    min=10
    count=0
    for j in range(len(x1)):
        if img[y1[j],x1[j],1]==0:
            if abs(complex(x1[i],y1[i])-complex(x1[j],y1[j]))<min and abs(complex(x1[i],y1[i])-complex(x1[j],y1[j]))!=0:
                min=abs(complex(x1[i],y1[i])-complex(x1[j],y1[j]))
                count=j
    keep_x.append(x1[count])
    keep_y.append(y1[count])
    img[y1[count],x1[count],1]=255
    i=count


t_x=np.array(keep_x) 
t_y=np.array(keep_y) 


w=[] # 曲率CのP表現：wを求める
for j in range(len(keep_x)-1): #i+1を指定するにはlen(keep_x)-1
    if abs(complex(keep_x[j+1],keep_y[j+1])-complex(keep_x[j],keep_y[j]))!=0: #分母が０でないとき
        comp=complex(keep_x[j+1],keep_y[j+1])-complex(keep_x[j],keep_y[j])
        w.append(comp/abs(comp))

n=len(w)+1

c = []
for k in range(n):#cを求める　
    y = 0j
    for j in range(n-1):
        t = 2 * math.pi * j * k / n
        y += w[j]* math.e**(-1j * t)
    c.append(y/n)

c1=[]
c2=[]

for i in range((n//2)+1): #c^の作成
    c1.append(c[i])
for i in range((n//2)+1,len(c),1):
    c2.append(c[i])
      
count=len(c2)
c2.extend(c1) #c2=c^

w_N = []
N = 7# 解像度
for j in range(n-1): #w_Nの作成
    y = 0j
    for k in range((-1)*N, N+1, 1):
        b = 2 * math.pi * j * k / n
        y += c2[count+k] * math.e**(1j * b)
    w_N.append(y)

z_N=[]
for j in range(n): #z_Nの作成：再生曲線
    y=0j
    for r in range(j-1):
        y+=w_N[r]*abs(complex(keep_x[r+1],keep_y[r+1])-complex(keep_x[r],keep_y[r]))
    z_N.append(y+complex(keep_x[0],keep_y[0]))


q_x=[]
q_y=[]
for i in range(len(z_N)):
    q_x.append(z_N[i].real)
    q_y.append(z_N[i].imag)

plt.plot(q_x,q_y) 
plt.gca().invert_yaxis()
plt.xlim([0,500])
plt.ylim([800,0])
plt.show()
