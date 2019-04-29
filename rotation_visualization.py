import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import torch

def readData(filename, num):
  count = 0
  matrixAll = []
  with open(filename) as file:
    while(True):
      line = file.readline()

      # End of line, exit
      if not line:
        break
      
      if count == num:
        break

      # Obtain the R matrix 
      if line.startswith('R matrix'):
        matrix = []
        for i in range(3):
          line = file.readline()
          splited = line.split()
          matrix.append(float(splited[0]))
          matrix.append(float(splited[1]))
          matrix.append(float(splited[2]))
        matrixAll.append(matrix)
        count += 1
  
  return np.array(matrixAll)

def display(data):
  p = np.array([0.0, 1.0, 1.0]).reshape(3,1)
  x = []
  y = []
  z = []
  for rot in data:
    rot = rot.reshape(3,3)
    after_rot = np.dot(rot, p)
    x.append(after_rot[0][0])
    y.append(after_rot[1][0])
    z.append(after_rot[2][0])
  fig = plt.figure().add_subplot(111, projection='3d')
  fig.scatter(x, y, z, c='r', marker='o')
  plt.show()




filename = '/home/sunsy/I1_FULL_LOG'

data = readData(filename, 59)
display(data)




