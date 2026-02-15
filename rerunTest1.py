
import rerun as rr

from math import tau
import numpy as np
import av
import numpy.typing as npt
from scipy.spatial.transform import Rotation as rot
import pyrealsense2 as rs

#VIDEO SETTINGS - laptop webcam
input_container = av.open("/dev/video0", format="v4l2")
istr = input_container.streams.video[0]
fps = 30
duration_s = 4
width = istr.width
height = istr.height
codec = rr.VideoCodec.H264

formats = {rr.VideoCodec.H265: "hevc", rr.VideoCodec.H264: "h264"}
encoders = {rr.VideoCodec.H265: "libx265", rr.VideoCodec.H264: "libx264"}

#VIDEO SETTINGS - actual cameras


#VIDEO PIPELINE SETTINGS
av.logging.set_level(av.logging.VERBOSE)
container = av.open("/dev/null", "w", format=formats[codec])
stream = container.add_stream(encoders[codec], rate=fps)
assert isinstance(stream, av.video.stream.VideoStream)
stream.width = width
stream.height = height
stream.pix_fmt = "yuv420p"
stream.max_b_frames = 0

#VIEWER SETTINGS
rr.init("rerun_robot_test") 
rr.spawn()
rr.set_time("stable_time", duration=0)

#CAMERAS
camloc = [[0, 0.25, 0.5], [0.25, 0, 0.5], [0, -0.25, 0.5], [-0.25, 0.0, 0.5]]
camrot = [0,270,180,90]
for c in range(4):
    quat = rot.from_euler('xz', [-90,camrot[c]], degrees=True).as_quat()
    rr.log(
        f"bot/cam{c+1}",
        rr.Pinhole(
            width=width, 
            height=height, 
            focal_length=width/2,
            image_plane_distance=0.2
        ),
        rr.Transform3D(
            translation=camloc[c],
            quaternion = quat
        ),
        static=True,
    )
    rr.log(f"bot/cam{c+1}", rr.VideoStream(codec=codec), static=True)

#VIEWER    
for f in input_container.decode(video=0):
    f.pict_type = av.video.frame.PictureType.NONE

    for packet in stream.encode(f):
        if packet.pts is None:
            continue
        rr.set_time("stable_time", duration=float(packet.pts * packet.time_base))

        for c in range(4):
            rr.log(f"bot/cam{c+1}", rr.VideoStream.from_fields(sample=bytes(packet)))

    #EVERYTHING ELSE
    rr.log(
        "bot/main",
        rr.Cylinders3D(lengths=0.5, radii=0.3, colors=[128,128,200], fill_mode=3, centers=(0,0,0.25))
    )
    #PANEL DETECTIONS AND OTHER BOTS
    rr.log(
        "otherbot/main",
        rr.Cylinders3D(lengths=0.5, radii=0.3, colors=[128,128,200], fill_mode=1, centers=(1,2,0.25))
    )
    panloc = [[0, 0.25, 0.5], [0.25, 0, 0.5], [0, -0.25, 0.5], [-0.25, 0.0, 0.5]]
    panrot = [0,270,180,90]
    quat = rot.from_euler('xz', [-90,camrot[c]], degrees=True).as_quat()
    rr.log(
        "panels",
        rr.Boxes3D(
            centers=[[2, 0, 0], [-2, 0, 0], [0, 0, 2]],
            half_sizes=[[0.25, 0.1, 0.1], [1.0, 1.0, 0.5], [2.0, 0.5, 1.0]],
            quaternions=quat,
            radii=0.02,
            colors=[[200,128,128], [200,128,128], [200,128,128]],
            fill_mode=1,
            labels=["pan1", "pan2", "pan3"],
        ),
    )




#TIME
for i in range(400):
    time = i*0.01
    rr.set_time("stable_time", duration=time)