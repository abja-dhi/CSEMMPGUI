
import xml.etree.ElementTree as ET
from .tasks import *

def Call(XML):
    root = ET.fromstring(XML)
    task_type = root.find("Task").text

    if task_type == "LoadPd0":
        filepath = root.find("Path").text
        results = LoadPd0(filepath)
        
    elif task_type == "Extern2CSVSingle":
        filepath = root.find("Path").text
        results = Extern2CSVSingle(filepath)

    elif task_type == "Extern2CSVBatch":
        folderpath = root.find("Path").text
        results = Extern2CSVBatch(folderpath)

    elif task_type == "GetColumnsFromCSV":
        filepath = root.find("Path").text
        header = int(root.find("Header").text)
        sep = root.find("Sep").text
        results = GetColumnsFromCSV(filepath, header, sep)
        print(results)
        
    else:
        return "<Result><Error>Unknown task type</Error></Result>"

    return GenerateOutputXML(results)