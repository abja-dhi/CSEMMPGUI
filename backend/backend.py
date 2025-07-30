
import xml.etree.ElementTree as ET
from .tasks import *

currd = r"C:\Users\abja\OneDrive - DHI\61803553-05 EMMP Support Group\github\CSEMMPGUI\tests"
test_log = f"{currd}\test_log.txt"

def Call(XML):

    root = ET.fromstring(XML)
    task_type = root.find("Task").text

    if task_type == "LoadPd0":
        filepath = root.find("Path").text
        results = InstrumentSummaryADCP(filepath, task=1)
        
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

    elif task_type == "InstrumentSummaryADCP":
        filepath = root.find("Path").text
        results = InstrumentSummaryADCP(filepath, task=2)
        print(results)
        
    else:
        results = {"Status": "Error", "Message": "Unknown task type"}

    return GenerateOutputXML(results)