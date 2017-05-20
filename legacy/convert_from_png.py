#!/usr/bin/python3
import png, array

def clamp(val,minVal,maxVal):
  if val < minVal:
    return minVal
  if val > maxVal:
    return maxVal
  return val

# http://www.equasys.de/colorconversion.html
def YCbCrToRGB(y,cb,cr):
  #y -= 16
  cb -= 128
  cr -= 128
  #return (
  #  int(1.164*float(y) + 1.596*float(cr)),
  #  int(1.164*float(y) - 0.392*float(cb) - 0.813*float(cr)),
  #  int(1.164*float(y) + 2.017*float(cb))
  #)
  return (
    clamp(int(float(y) + 1.4*float(cr)),0,255),
    clamp(int(float(y) - 0.343*float(cb) - 0.711*float(cr)),0,255),
    clamp(int(float(y) + 1.765*float(cb)),0,255)
  )

reader = png.Reader(filename="cam1_000_1.png")
(width, height, pixels, metadata) = reader.read()
writer = png.Writer(width=int(width/2), height=height, interlace=0)
print(width, height)
print(metadata)
## Format: u01 y0 v01 y1
## https://www.fourcc.org/pixel-format/yuv-uyvy/
rows = list(pixels)
newrows = []
for r in rows:
  i = 0
  newrow = array.array('B')
  while i < len(r):
    u = r[i]
    y0 = r[i+3]
    v = r[i+6]
    y1 = r[i+9]
    #print(u,y0,v,y1)
    (r0,g0,b0) = YCbCrToRGB(y0,u,v)
    (r1,g1,b1) = YCbCrToRGB(y1,u,v)
    #print(r0,g0,b0,r1,g1,b1)
    newrow.fromlist([r0,g0,b0,r1,g1,b1])
    i += 12 # 3 bytes/pixel * 4 pixel/macropixel
  newrows.append(newrow)
f = open("newfile.png", "wb")
writer.write(f, newrows)
f.close()
