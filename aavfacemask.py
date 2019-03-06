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
import warning

filename = 'aav.mrc'
center = np.array([177.08, 177.08, 177.08])

# Vertex normalize dirction vector of a 3-fold face
a = np.array([0.8506508, 0, -0.5257311])
b = np.array([0.8506508, 0,  0.5257311])
c = np.array([0.5257311, -0.8506508, 0])

def isValid(p):
  vec = p - center

# Open the mrcfile and obtain its data and voxel information
with warnings.catch_warnings(record=True) as w:
  with mf.open(filename, mode='r+', permissive=True) as aav:
    data = aav.data
    voxel_size = aav.voxel_size
    nx, ny, nz = aav.data.shape


axisList = []
axisList.append((2, np.array[1, 0, 0]))
axisList.append((5, np.array[0.8506508, 0, -0.5257311]))
axisList.append((3, np.array[0.9341724, 0.3568221, 0]))




# Vertex normalized direction vector of a 5-fold face
