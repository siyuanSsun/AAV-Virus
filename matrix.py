'''

This file generates rotation matrix from either euler angles or symmtery symbols.

Curretly only I1 symmetry supported.

'''

import numpy as np

def rotMatrix(rot, tilt, psi):
  
  rotM = np.zeros(9,)

  rotM[0] = np.cos(psi) * np.cos(tilt) * np.cos(rot) - np.sin(psi) * np.sin(rot)
  rotM[1] = np.cos(psi) * np.cos(tilt) * np.sin(rot) + np.sin(psi) * np.cos(rot)
  rotM[2] =-np.cos(psi) * np.sin(tilt)
  rotM[3] =-np.sin(psi) * np.cos(tilt) * np.cos(rot) - np.cos(psi) * np.sin(rot)
  rotM[4] =-np.sin(psi) * np.cos(tilt) * np.sin(rot) + np.cos(psi) * np.cos(rot)
  rotM[5] = np.sin(psi) * np.sin(tilt)
  rotM[6] = np.sin(tilt)* np.cos(rot)
  rotM[7] = np.sin(tilt)* np.sin(rot)
  rotM[8] = np.cos(tilt)

  return rotM.reshape(3,3)

def symMatrix(sym):

  return None