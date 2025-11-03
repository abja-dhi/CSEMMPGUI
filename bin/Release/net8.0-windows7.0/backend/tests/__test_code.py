from pyEMMP.utils_xml import XMLUtils
from pyEMMP import NTU2SSC

project = r"C:\Users\abja\AppData\Roaming\PlumeTrack\Test Project 1.mtproj"
sscmodelid = "26"
project_xml = XMLUtils(project)
sscmodel = project_xml.find_element(elem_id=sscmodelid, _type="NTU2SSC")
ssc_params = NTU2SSC(project=project, sscmodel=sscmodel)
