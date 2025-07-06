import traceback
import adsk.core
import csv
import time

# System Settings
_APP = adsk.core.Application.get()
_UI  = _APP.userInterface
_PRODUCT = _APP.activeProduct


# User Settings
FOOTPRINT_NAME = "fusion-motion-analysis"
# CSV_PATH = "C:\\Users\\lynchpin\\repository\\terra-I\\resources\\joint_angles_20250630_233108.csv"
CSV_PATH = "C:\\Users\\lynchpin\\repository\\terra-I\\resources\\init.csv"
FPS = 60
DESIGN = _PRODUCT # Derived Classes: "CAM", "Design", "Drawing"


control_interval = 1/FPS
ROOT = DESIGN.rootComponent
with open(CSV_PATH, 'r') as f:
    reader = csv.reader(f)
    sequence = [row for row in reader]

# Main method
def run(_context: str):

    try:
        _UI.messageBox(f'"{FOOTPRINT_NAME} in progress...')
        
        ############  Defining and binding joints  ############
        for joint in ROOT.allJoints:
            if joint.name == "la-j1" : la_j1 = joint
            if joint.name == "la-j2" : la_j2 = joint
            if joint.name == "la-j3" : la_j3 = joint
            if joint.name == "ra-j1" : ra_j1 = joint
            if joint.name == "ra-j2" : ra_j2 = joint
            if joint.name == "ra-j3" : ra_j3 = joint

        joints = [la_j1, la_j2, la_j3, ra_j1, ra_j2, ra_j3]     # Confirm binding
        
        ####################  Rendering  ######################
        for row in sequence:
            for idx, angle_rad in enumerate(row):
                joints[idx].jointMotion.rotationValue = float(angle_rad)
            _APP.activeViewport.refresh()
            time.sleep(control_interval)
            
    except Exception as e:
        _UI.messageBox(f"Error occured:\n{traceback.format_exc()}")
        _UI.messageBox(f"Error message:\n{str(e)}")
