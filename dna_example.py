
import rerun as rr

from math import tau
import numpy as np
from rerun.utilities import build_color_spiral
from rerun.utilities import bounce_lerp

rr.init("rerun_example_dna_abacus") #gives an id to the entire process

rr.spawn() #makes viewer show up
rr.set_time("stable_time", duration=0)

pointCt = 100
pts1, clrs1 = build_color_spiral(pointCt)
pts2, clrs2 = build_color_spiral(pointCt, angular_offset = tau*0.5)

rr.log("dna/structure/left", rr.Points3D(pts1, colors=clrs1, radii = 0.08)) #log makes it actually show up
rr.log("dna/structure/right", rr.Points3D(pts2, colors=clrs2, radii=0.5))

rr.log(
    "dna/structure/scaffolding",
    rr.LineStrips3D(np.stack((pts1,pts2), axis=1), colors=[128,128,128])#rgb colors, axis controls how lines connect
)

offsets = np.random.rand(pointCt) #generate a set of 100 random numbers


#TIME
timeOffset = np.random.rand(pointCt)

for i in range(400):
    time = i*0.01
    rr.set_time("stable_time", duration=time)

    #BEADS
    times = np.repeat(time, pointCt) + timeOffset
    beads = [bounce_lerp(pts1[n],pts2[n],times[n]) for n in range(pointCt)]
    colors = [[int(bounce_lerp(80,230,times[n]*2))] for n in range(pointCt)]
    rr.log(
        "dna/structure/scaffolding/beads",
        rr.Points3D(beads,radii=0.06, colors=np.repeat(colors, 3, axis=-1)),
    )

    #EVERYTHING ELSE
    rr.log(
        "dna/structure",
        rr.Transform3D(rotation=rr.RotationAxisAngle(axis=[0,0,1], radians=time / 4.0*tau))
    )