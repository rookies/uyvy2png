#!/bin/bash
avconv -f video4linux2 -i /dev/video0 -vcodec rawvideo -pix_fmt yuyv422 -vframes 1 out.yuv
