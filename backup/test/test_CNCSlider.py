from Slider import *
import sys

velocity = sys.argv[1]
step = sys.argv[2]
direction = sys.argv[3]

slider = CNCSlider()
slider.move(velocity,direction,step)



