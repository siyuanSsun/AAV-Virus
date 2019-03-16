#!/usr/bin/python
#-*- coding: utf-8 -*-
####################################################################################
#  author: Siyuan Sun
#  e-mail: thusiyuansun@gmail.com
#  version: 0.0
#  detail: new file
#
#  @Brief: This is a simple python script to cut the 3-fold face out of aav virus --
#  an icosahedral shape virus.
#####################################################################################


import mrcfile as mf
import numpy as np
import warnings

filename = '../Reference_000_A_Final_Mask_02.mrc'
center = np.array([190, 190, 190])

# 3-fold, 5-fold and 2 fold normalized vector
''' 
axisList = []
axisList.append((2, np.array[1, 0, 0]))
axisList.append((5, np.array[0.8506508, 0, -0.5257311]))
axisList.append((3, np.array[0.9341724, 0.3568221, 0]))
'''

# Vertex normalize dirction vector of a 3-fold face
p1 = np.array([0.5257311, 0, 0.8506508])
p2 = np.array([0.8506508, 0.5257311, 0])
p3 = np.array([0.8506508, -0.5257311, 0])

a = 0.8506508
b = 0.5257311

# Vertex normalized direction vector of a 5-fold face

l = -1.0e-8
def isValid(p):
  '''
  To validate whether a vector p, is in the region surrounded by 3-fold face

  args: p,  3d numpy array vector
  '''
  vec = p - center
  x = vec[2]/a
  y = (vec[0]*b + vec[1]*a - x*b*b)/(2*a*b)
  z = (vec[0]*b - vec[1]*a - x*b*b)/(2*a*b)
  # print(x, y, z)
  return x >= l and y >= l and z >= l


# Open the mrcfile and obtain its data and voxel information
with warnings.catch_warnings(record=True) as w:
  print("Loading MRC File......")
  with mf.open(filename, mode='r+', permissive=True) as aav:
    data = aav.data
    voxel_size = aav.voxel_size
    nx, ny, nz = aav.data.shape
  
  print("MRC File Loaded Successfully")


# Create a new mrcfile and do the cutting-face task
with mf.new('aav_face_mask.mrc', overwrite=True) as aav_cut:
  print("Prepare Cutting Face......")
  for x in range(nx):
    for y in range(ny):
      for z in range(nz):
        if(data[x,y,z] != 0):
          if not isValid(np.array([x, y, z])):
            data[x,y,z] = 0
    if x % 5 == 0:
      print("%{:.0f} Percent Data Processed .....".format(100*(x+1)/nx))
  print("Cutting is Done")
  aav_cut.set_data(data)
  aav_cut.voxel_size = voxel_size
  print("Finished")



