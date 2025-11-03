from pyEMMP.utils_xml import XMLUtils
from pyEMMP import NTU2SSC, BKS2NTU

project = r"C:\Users\abja\AppData\Roaming\PlumeTrack\Test Project 1.mtproj"
sscmodelid = "27"
project_xml = XMLUtils(project)
sscmodel = project_xml.find_element(elem_id=sscmodelid, _type="BKS2NTU")
ssc_params = BKS2NTU(project=project, sscmodel=sscmodel)
