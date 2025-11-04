from pyEMMP.utils_xml import XMLUtils
from pyEMMP import *
import matplotlib.pyplot as plt

project = r"C:\Users\abja\AppData\Roaming\PlumeTrack\Test Project 1.mtproj"
sscmodelid = "27"
project_xml = XMLUtils(project)
sscmodel = project_xml.find_element(elem_id=sscmodelid, _type="BKS2NTU")
# ssc_params = BKS2NTU(project=project, sscmodel=sscmodel)
result = PlotBKS2NTUTrans(project=project, sscmodelid=sscmodelid, beam_sel="mean", field_name="SSC", yAxisMode="bin", cmap="turbo", mask=True, vmin=None, vmax=None, title="BKS2NTU Transient Plot Test")
plt.show()
print(result)