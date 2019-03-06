#!/usr/bin/python
#-*- coding: utf-8 -*-

############################################################################
#  author: Siyuan Sun
#  e-mail: thusiyuansun@gmail.com
#  version: 0.0
#  details: new file
#
#  @brief  Visualize the symmetry operation of a certain point in real space
#  For example, can a combination of several symmetry operations cover the 
#  whole parts of a symmetry element ? Visualization is always the best test.
#############################################################################


import numpy as np
try:
  import mrcfile as mf
except:
  print("Have you installed mrcfile package? \nTry 'pip install mrcfile' in your commandline.")

class symmetry():
  def __init__(self, sym='I1'):
    '''
    Initialize symmetry class

    args: sym: symmetry symbols, for example, C1, D1, I1 etc, here we focus on I1 symmetry firstly
               (reference: https://en.wikipedia.org/wiki/Schoenflies_notation)
          
    '''
    #TODO
    self.sym = sym
    self.symSwitcher = {}
    self.init()
    pass

  def init(self):
  '''
  Initialize symmetry axis in a list, axis format in (n, np.array(3))

  '''
    self.axis = []
    self.axis.append((2, np.array[1, 0, 0]))
    self.axis.append((5, np.array[0.8506508, 0, -0.5257311]))
    self.axis.append((3, np.array[0.9341724, 0.3568221, 0]))

  def display(self, display=True):
    '''
    Display symmetry operation in real space in a gif demo

    '''
    #TODO
    pass

  def getSymOperation(self):
    '''
    Get all the symmetry operation according to the symmetry symbol
    '''
    self.symOpList = []
    for axis in self.axis:
      radians = 2*np.pi/axis[0]
      vector = axis[1]
      # Do some transform operations here
      rotationMatrix = ""
      self.symOpList.append(rotationMatrix)

    pass

  def fillOperation(self):
