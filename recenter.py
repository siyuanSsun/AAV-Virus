from EMAN2 import EMData
import mrcfile as mf
import numpy as np
import argparse
import sys
import warnings

class Recenter():
  def __init__(self, starfile, mstack, mask, dmap, l):
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
    print("Path of stack file: {0}".format(mstack))
    print("Path of 3D mask: {0}".format(mask))
    print("Path of density map: {0}".format(dmap))
    print("Path of box size: {0}\n".format(l))

    self.nbox = l
    self.starfile = starfile
    self.mstack = mstack

    # Obtain the center of mass of region of interest
    self.cm = self.findCenterMass(mask, dmap)


  
  def findCenterMass(self, maskpath, dmappath):
    '''
    Find the center of mass of region of interet given the mask and density map.

    Args: \n
    maskpath: path of mask, voxel with value 1 stands for area of interet. \n
    dmappath: path of reconstruction model. \n
    
    '''

    p = EMData(maskpath)
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
    return np.around(cm)

  

  def processMeta(self, starfile, mstack):
    '''
    Read and process the stack data of mrc images. This is the key part of recentering.

    Args: \n
    starfile: the starfile storing the information; \n
    mstack: path of the stack file; \n
    
    '''
    pass

  
  
  def transformClip(self, rot, image):
    '''
    Clip box from a 2D cryo-em image.

    Args: \n
    rot: rotation matrix; \n
    image: the 2D cryo-em image; \n
    
    '''
    pass



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="""recenter.py is a script to clip and recenter the region of 
                                                    interest from a stack of 2D cryo-em projection images.""")
  parser.add_argument("-m", "--mask", help="3D density mask of region of interest.")
  parser.add_argument("-l", "--length", type=int, help="The size of clipped box.")
  parser.add_argument("-s", "--star", help="Star file that stores the infomation of 2D images.")
  parser.add_argument("-d", "--dmap", help="Density map of 3D reconstruction model.")
  parser.add_argument("-t", "--stack", help="Stack of 2D images.")

  args = parser.parse_args()

  task = Recenter(args.star, args.stack, args.mask, args.dmap, args.length)
  