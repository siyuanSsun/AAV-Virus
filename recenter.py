import mrcfile as mf
import numpy as np
import argparse
import math
import sys
import warnings
from pyrelion.metadata import MetaData
from matrix import rotMatrix


class Recenter():
  def __init__(self, starfile, mask, dmap, l, angpix):
    '''
    Initialization of rencenter

    Args: \n
    starfile: .star file that stores the spatial infomation of a particle. \n
    mstack: .mrcs stack of 2D image of particles, identified in .star file. \n
    mask: .mrc reversion mask that used during projection. \n
    dmap: .mrc density map after reconstruction. \n
    l: integer that decide the size of box clipped.

    '''

    # Print out the input information
    print("The input details are:")
    print("Path of star file: {0}".format(starfile))
    print("Path of 3D mask: {0}".format(mask))
    print("Path of density map: {0}".format(dmap))
    print("Image size: {0}\n".format(l))
    print("Pixel size: {0}\n".format(angpix))
    
    assert (starfile and  mask and dmap and l and angpix), "Lack of arguments.\n"
    
    self.imagesize = l
    self.starfile = starfile
    self.mask = mask
    self.dmap = dmap
    self.angpix = angpix

    

  def main(self):
    self.cm = self.findCenterMass(self.mask, self.dmap)
    self.processMeta(self.starfile, self.imagesize, self.angpix)


  
  def findCenterMass(self, maskpath, dmappath):
    '''
    Find the center of mass of region of interet given the mask and density map.

    Args: \n
    maskpath: path of mask, voxel with value 1 stands for area of interet. \n
    dmappath: path of reconstruction model. \n
    
    '''

    print("Finding the center of mask of area of interest.")

    with warnings.catch_warnings(record=True) as w:
      print("Opening mask {0}".format(maskpath))
      with mf.open(maskpath, permissive=True) as mask:
        mdata = mask.data
    
      print("Opening density map {0}".format(dmappath))
      with mf.open(dmappath, permissive=True) as dmap:
          ddata = dmap.data
    
    # refernce here to calculate center of mass of a given 3D array
    # https://stackoverflow.com/questions/29356825/python-calculate-center-of-mass
    print("Calculating center of mass: ")
    arg = np.argwhere(mdata > 0.5)
    nrow = arg.shape[0]
    metadata = np.append(arg, ddata[arg[:,0], arg[:,1], arg[:,2]].reshape(nrow,1), axis=1)
    cm = np.average(metadata[:,:3], axis=0, weights=metadata[:,3])

    print(cm)
    print("After approximation: ")
    print(np.around(cm))
    return cm

  

  def processMeta(self, starfile, l, angpix):
    '''
    Read and process the stack data of mrc images. This is the key part of recentering.
    In this part, only starfile needs to be modified, then following clip in RELION.
    Actually, only translation and defocus value need to be modified.

    Args: \n
    starfile: the starfile storing the information; \n
    l: image size of 2D images
    '''
    meta = MetaData(starfile)
    submeta = MetaData()
    subparticle = []
    for particle in meta:

      rot = particle.rlnAngleRot
      psi = particle.rlnAnglePsi
      tilt = particle.rlnAngleTilt 


      rotM = rotMatrix(rot, tilt, psi, radians=False)
      
      cm = -int(l/2) + self.cm
      cm[0] += particle.rlnOriginX
      cm[1] += particle.rlnOriginY

      coord = np.dot(rotM, cm)

      x_d, x_i = math.modf(coord[0])
      y_d, y_i = math.modf(coord[1])
      z = coord[2]
      
      # Modify CTF defocus value
      particle.rlnDefocusU += z * angpix
      particle.rlnDefocusV += z * angpix

      # Set up the coordinate value
      particle.rlnCoordinateX = x_i + int(l/2)
      particle.rlnCoordinateY = y_i + int(l/2)

      # Set up origin value
      particle.rlnOriginX = x_d
      particle.rlnOriginY = y_d

      subparticle.append(particle)
    
    submeta.addData(subparticle)
    submeta.write("sub_" + starfile)
  
  


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="""recenter.py is a script to clip and recenter the region of 
                                                    interest from a stack of 2D cryo-em projection images.""")
  parser.add_argument("-m", "--mask", help="3D density mask of region of interest.")
  parser.add_argument("-l", "--length", type=int, help="The size of clipped box.")
  parser.add_argument("-s", "--star", help="Star file that stores the infomation of 2D images.")
  parser.add_argument("-d", "--dmap", help="Density map of 3D reconstruction model.")
  parser.add_argument("-a", "--angpix", help="Pixel size of 2D image.")

  args = parser.parse_args()

  my = Recenter(args.star, args.mask, args.dmap, args.length, args.angpix)
  my.main()