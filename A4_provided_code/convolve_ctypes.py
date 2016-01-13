#Alexander Chatron-Michaud, 260611509
#!/usr/bin/python
import sys
import struct
import copy
import cProfile
import ctypes

clib = ctypes.cdll.LoadLibrary("libfast_filter.so")

# Reads a BMP image from disk into a convenient array format
def loadBMPImage( img_name ):
  img_data = []
  i=0
  img_in = open( img_name, 'rb' )
  byte = img_in.read(1)
  while byte != "":
      img_data.append(byte)
      byte = img_in.read(1)
  img_data = (ctypes.c_char * len(img_data))(*img_data)
  return img_data

# Read the filter information from command line and 
# set it up to be used on the image  
def parseFilterCmdArgs( cmd_args ):

  filter_width = int( cmd_args[3] )
  filter_weights = []
  filter_offsets = []

  for i in range(0,filter_width*filter_width):
    filter_weights.append( float(cmd_args[4+i] ))

  filter_weights = (ctypes.c_float * len(filter_weights))(*filter_weights)
  return ( filter_width, filter_weights )
   
  
# Write the output image to file  
def saveBMPImage( out_img_data, out_fname):
  img_out = open( out_fname, 'wb' )
  img_out.write( out_img_data )
  img_out.close()

# The main code starts here 
def main():
  img_data = loadBMPImage( sys.argv[1] )
  (filter_width, filter_weights) = parseFilterCmdArgs( sys.argv )
  out_img_data = []
  out_img_data = (ctypes.c_char * len(img_data))(*out_img_data)
  clib.doFiltering(img_data, filter_weights, filter_width, out_img_data)
  saveBMPImage( out_img_data, sys.argv[2])

if __name__ == "__main__":
  #cProfile.run('main()')
  main()
  print "Done!"
