import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from adcp import ADCP
from watersample import WaterSample


tree = ET.parse(r'C:\Users\abja\AppData\Roaming\PlumeTrack\Untitled-Project.mtproj')