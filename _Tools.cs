using DHI;
using DHI.Mike1D.Generic;
using Python.Runtime;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public static class _Tools
    {
        public static string GenerateInput(Dictionary<string, string> inputs)
        {
            var sb = new StringBuilder();
            using (var writer = XmlWriter.Create(sb, new XmlWriterSettings { OmitXmlDeclaration = true }))
            {
                writer.WriteStartElement("Input");
                foreach (var input in inputs)
                {
                    writer.WriteElementString(input.Key, input.Value);
                }
                writer.WriteEndElement();
            }
            return sb.ToString();
        }


        public static void InitPython()
        {
            string pythonDll = _Globals.PythonDllPath;
            Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", pythonDll);
            PythonEngine.Initialize();
        }

        public static XmlDocument CallPython(string xmlInputStr)
        {
            if (!PythonEngine.IsInitialized)
            {
                InitPython();
            }
            using (Py.GIL())
            {
                dynamic sys = Py.Import("sys");
                sys.path.append(_Globals.PythonModulePath);
                dynamic backend = Py.Import(_Globals.BackendModuleName);
                string resultXML = backend.Call(xmlInputStr);
                resultXML = resultXML.ToString();
                var doc = new XmlDocument();
                doc.LoadXml(resultXML);
                return doc;
            }
            
        }
        
        
        public static Dictionary<string, string> ParseOutput(XmlDocument doc)
        {
            var outputs = new Dictionary<string, string>();
            XmlNode? resultsNode = doc.SelectSingleNode("//Result");
            if (resultsNode != null)
            {
                foreach (XmlNode child in resultsNode.ChildNodes)
                {
                    if (child is XmlElement element)
                    {
                        outputs[element.Name] = element.InnerText;
                    }
                }
            }
            return outputs;
        }


    }
}
