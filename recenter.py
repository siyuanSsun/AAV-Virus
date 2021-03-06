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
    
    self.imagesize = int(l)
    self.starfile = starfile
    self.mask = mask
    self.dmap = dmap
    self.angpix = float(angpix)

    

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

    print("Reading star file ...")
    meta = MetaData(starfile)
    labels = meta.getLabels()
    print("Star file read successfully.")
    submeta = MetaData()
    subparticle = []

    print("Processing metadata ...")
    for particle in meta:

      subpart = particle.clone()

      rot = particle.rlnAngleRot
      psi = particle.rlnAnglePsi
      tilt = particle.rlnAngleTilt 


      rotM = rotMatrix(rot, tilt, psi, radians=False)
      
      cm = -int(l/2) + self.cm
      coord = np.dot(rotM, cm)
      coord[0] += particle.rlnOriginX
      coord[1] += particle.rlnOriginY


      x_d, x_i = math.modf(coord[0])
      y_d, y_i = math.modf(coord[1])
      z = coord[2]
      
      # Modify CTF defocus value

      subpart.rlnDefocusU = particle.rlnDefocusU + z * angpix
      subpart.rlnDefocusV = particle.rlnDefocusV + z * angpix

      # Set up the coordinate value
      subpart.rlnCoordinateX = particle.rlnCoordinateX - coord[0]
      subpart.rlnCoordinateY = particle.rlnCoordinateY - coord[1]

      # Set up origin value
      subpart.rlnOriginX = x_d
      subpart.rlnOriginY = y_d

      subparticle.append(subpart)
    
    print("Metadata process done.")
    submeta.addLabels(labels)
    submeta.addData(subparticle)
    submeta.write("sub_" + starfile)
  

def removedup(starfile):
    '''
    To remove the duplicated line from a starfile and save it as a copy

    Args:
    starfile: star file that contains particles info
    '''
    print("Reading star file ...")
    meta = MetaData(starfile)
    labels = meta.getLabels()
    print("Star file read successfully.")
    print("Before processing, {0} particles read.".format(meta.size()))
    submeta = MetaData()
    subparticle = []
    existed = {}
    print("Processing metadata ...")
    for particle in meta:
      pos = str(particle.rlnCoordinateX) + str(particle.rlnCoordinateY)
      existed[pos] = 0
    
    for particle in meta:
      pos = str(particle.rlnCoordinateX) + str(particle.rlnCoordinateY)
      existed[pos] += 1

      if existed[pos] == 1:
        subparticle.append(particle)
      
    print("After processing, {0} particles remained.".format(len(subparticle)))
    print("Metadata process done.")
    submeta.addLabels(labels)
    submeta.addData(subparticle)
    submeta.write(starfile.split('.')[0] + '_dupless.star')


def createRef(dmappath, maskpath):

  with warnings.catch_warnings(record=True) as w:
    print("Opening mask {0}".format(maskpath))
    with mf.open(maskpath, mode='r+', permissive=True) as mask:
      mdata = mask.data
    
    print("Opening density map {0}".format(dmappath))
    with mf.open(dmappath, mode='r+', permissive=True) as dmap:
        ddata = dmap.data
        voxel_size = dmap.voxel_size
    

  print("Creating reference map.....")
  with mf.new(dmappath + '_ref.mrc', overwrite=True) as ref:
    cord = np.argwhere(mdata < 0.2)
    data = ddata[:]
    print(data[cord[:,0], cord[:,1], cord[:,2]]) 
    data[cord[:,0], cord[:,1], cord[:,2]] = 0
    print(data)
    print(np.argwhere(data > 0))
    ref.set_data(data)
    ref.voxel_size = voxel_size
    print('Reference created')



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