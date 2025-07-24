
import xml.etree.ElementTree as ET
from .tasks import *

def Call(XML):
    root = ET.fromstring(XML)
    task_type = root.find("Task").text

    if task_type == "LoadPd0":
        filepath = root.find("Path").text
        results = LoadPd0(filepath)
        
    elif task_type == "GenerateOutputXML":
        pass
        
    else:
        return "<Result><Error>Unknown task type</Error></Result>"

    return GenerateOutputXML(results)