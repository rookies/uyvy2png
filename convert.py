#!/usr/bin/python3
import png, array, struct

######################################################################
## Configuration Start                                              ##
######################################################################
# Image size:
width = 640
height = 480

# Input & Output file:
inputFile = "out.yuv"
outputFile = "newfile.png"

# Byte order in input file:
# For uyvy: (see https://www.fourcc.org/pixel-format/yuv-uyvy/)
def mapper(b1,b2,b3,b4): return (b1,b2,b3,b4)
# For yuyv:
#def mapper(b1,b2,b3,b4): return (b2,b1,b4,b3)
# For yvyu: (see https://www.fourcc.org/pixel-format/yuv-yvyu/)
#def mapper(b1,b2,b3,b4): return (b4,b1,b2,b3)
######################################################################
## Configuration End                                                ##
######################################################################

## Helper function, applies a lower and upper limit to the given    ##
## value and returns it back.                                       ##
def clamp(val,minVal,maxVal):
  if val < minVal:
    return minVal
  if val > maxVal:
    return maxVal
  return val

## Helper function, converts the given full-range YCbCr tuple to a  ##
## RGB tuple and returns it back.                                   ##
## Based on: http://www.equasys.de/colorconversion.html             ##
def YCbCrToRGB(y,cb,cr):
  cb -= 128
  cr -= 128
  return (
    clamp(int(float(y) + 1.403*float(cr)),0,255),
    clamp(int(float(y) - 0.344*float(cb) - 0.714*float(cr)),0,255),
    clamp(int(float(y) + 1.770*float(cb)),0,255)
  )

## Read the input file and check the size:                          ##
print("Reading from %s, assuming image size: %dx%d" % (inputFile, width, height))
with open(inputFile, "rb") as f:
  data = f.read()
size = len(data)
print("Input file size: %d bytes" % size)
assert(size == width*height*2)
assert(size % 4 == 0)
## Create the pixel rows for the output file:                       ##
newrows = []
newrow = None
i = 0
while i < size:
  # Create new row, if necessary:
  if i % (2*width) == 0:
    if newrow is not None:
      newrows.append(newrow)
    newrow = array.array('B')
  # Unpack a macropixel:
  (b1,b2,b3,b4) = struct.unpack_from("4B", data, i)
  # Reorder bytes according to configuration:
  (u,y1,v,y2) = mapper(b1,b2,b3,b4)
  # Convert both pixels to RGB:
  (r1,g1,b1) = YCbCrToRGB(y1,u,v)
  (r2,g2,b2) = YCbCrToRGB(y2,u,v)
  # Append the pixels to the row:
  newrow.fromlist([r1,g1,b1,r2,g2,b2])
  # Move to the next macropixel:
  i += 4
newrows.append(newrow)
## Write to the output file:                                        ##
with open(outputFile, "wb") as f:
  writer = png.Writer(width=width, height=height, interlace=0)
  writer.write(f, newrows)
