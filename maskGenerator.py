#!/usr/bin/python
#-*- coding: utf-8 -*-
####################################################################################
#  author: Siyuan Sun
#  e-mail: thusiyuansun@gmail.com
#  version: 0.0
#  detail: new file
#
#  @Brief: Mask generator for high symmetry virus of their outside shell, 
#  especially those with high signal capsids but low signal internal genome.
#####################################################################################

import numpy as np
try: 
  import mrcfile as mf
except:
  print("MODULE IMPORT ERROR: HAVE YOU INSTALLED 'mrcfile' PACKAGE?\nTRY: pip install mrcfile")



class mask():
  def __init__(self, filename, threshold=1.0, r=0):
    '''
    Initialize the mask class
    Args: filename: name of input file
        threshold: the value you choose from Chimera viewer
        r: scattering radius for each pixel

    '''
    self.filename = filename
    self.threshold = threshold
    self.r = r
    self.initModel()

  def initModel(self):
    '''
    Open and store the mrc model, store the model in a private value
    '''
    with mf.open(self.filename, mode='r+', permissive=True) as model:
      self.model_data = model.data
      self.nx, self.ny, self.nz = model.data.shape

  def showData(self):
    # TODO something with self.model.data
    # TODO visualization
    pass



  def search(self):
    '''
    Given the threshold, search function will find the most valid internal pixel postion

    Return: the smallest valid radius
    '''
    radius = 0
    #TODO
    self.radius = radius
    pass

  def generateMask(self):
    '''
    Generate the outside shell mask of the given virus

    Output: the mask of input filename
    '''
    tmp_data = (self.model_data >= self.threshold) * 1
    data = np.array(tmp_data, dtype=np.int8)
    for pos in np.argwhere(tmp_data == 1):
      for r in range(1, self.r+1):
        loc = self.scatter(pos, r)
        data[loc[:,0], loc[:,[1]], loc[:,2]] = 1
      
    
    with mf.new(self.filename + '.mask.mrc', overwrite=True) as nmask:
      nmask.set_data(data)
      print("Mask Generated")
    



  def scatter(self, p, step):
    '''
    Scatter the pixel in (i, j, k) into surrounding postion

    Return: surrounding pixels position list
    '''
    pos = []
    for x in range(3):
      for y in range(3):
        for z in range(3):
          if x == 1 and y == 1  and z == 1:
            continue
          else:
            if p[0]+(x-2)*step < 0 or p[1]+(y-2)*step < 0 or p[2]+(z-2)*step < 0:
              continue
            else:
              pos.append([p[0]+(x-1)*step, p[1]+(y-1)*step, p[2]+(z-1)*step])
    return np.array(pos)




# if main, show a demo mask generated
if __name__ == "__main__":
  demo = mask("../piezo_subtract.mrc", threshold=0.013, r=6)
  demo.generateMask()
  