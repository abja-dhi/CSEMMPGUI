from .project import Project
from .survey import Survey
from .model import Model
from .adcp import ADCP
from .pd0 import Pd0Decoder


def GenerateOutputXML(xml):
    result = ET.Element("Result")
    for key, value in xml.items():
        ET.SubElement(result, key).text = str(value)

def LoadPd0(filepath):
    pd0 = Pd0Decoder(filepath, cfg={})
    n_beams = pd0._n_beams
    n_ensembles = pd0._n_ensembles
    return {"NBeams": n_beams, "NEnsembles": n_ensembles}


def 