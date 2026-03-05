import rerun as rr
import math
import numpy as np
import av
import numpy.typing as npt
from scipy.spatial.transform import Rotation as rot
import pyrealsense2 as rs

class fakeData:
    def __init__(self):
        rr.init("rerun_fake_data_test")
        serverGRPC = rr.serve_grpc()

if __name__ == "__main__":
    fakeData()
