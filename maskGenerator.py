#!/usr/bin/python
#-*- coding: utf-8 -*-
####################################################################################
#  author: Siyuan Sun
#  e-mail: thusiyuansun@gmail.com
#  version: 0.0
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
      self.model = model

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

    Output the mask as filename
    '''
  


  def scatter(self, i, j, k, step):
    '''
    Scatter the pixel in (i, j, k) into surrounding postion

    Return: surrounding pos list
    '''
    pos = []
    for x in range(3):
      for y in range(3):
        for z in range(3):
          if x == 1 and y == 1  and z == 1:
            continue
          else:
            pos.append([i+(x-2)*step, j+(y-2)*step, k+(z-2)*step])

    return pos




# if main, show a demo mask generated
if __name__ == "__main__":
  demo = mask("demo.mrc")
  