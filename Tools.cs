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
    public static class Tools
    {
        public static void InitPython()
        {
            string pythonDll = @"C:\Program Files\Python311\python311.dll";
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
                sys.path.append(@"C:\Users\abja\OneDrive - DHI\61803553-05 EMMP Support Group\github\CSEMMPGUI");
                dynamic backend = Py.Import("backend.backend");
                string resultXML = backend.Call(xmlInputStr);
                MessageBox.Show(resultXML);
                resultXML = resultXML.ToString();
                Console.WriteLine(resultXML);
                var doc = new XmlDocument();
                doc.LoadXml(resultXML);
                return doc;
            }
            PythonEngine.Shutdown();
        }

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

        public static int SaveXML(XmlElement item, string filePath)
        {
            try
            {
                XmlDocument doc = new XmlDocument();
                XmlDeclaration declaration = doc.CreateXmlDeclaration("1.0", "UTF-8", null);
                doc.AppendChild(declaration);

                XmlNode imported = doc.ImportNode(item, true);
                doc.AppendChild(imported);
                doc.Save(filePath);
                return 1; // Success
            }
            catch (Exception ex)
            {
                return 0; // Error
            }
        }

        public static void ExternToCSV()
        {
            if (!PythonEngine.IsInitialized)
            {
                InitPython();
            }
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Filter = "ViSea Extern.dat Files (*extern.dat)|*extern.dat";
            ofd.Title = "Open ViSea Extern.dat File";
            ofd.InitialDirectory = ConfigData.GetProjectDir();
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                string filePath = ofd.FileName;
                var inputs = new Dictionary<string, string>
                {
                    { "Task", "Extern2CSVSingle" },
                    { "Path", filePath }
                };
                string xmlInputStr = GenerateInput(inputs);
                
                try
                {
                    using (Py.GIL())
                    {
                        XmlDocument doc = CallPython(xmlInputStr);
                        string result = doc.SelectSingleNode("/Result/Result")?.InnerText ?? "-1";
                        if (result == "-1")
                            MessageBox.Show("An error occurred while processing the file.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        else if (result == "0")
                            MessageBox.Show("File processed successfully.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        else if (result == "1")
                            MessageBox.Show("File was already converted.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                        else
                            MessageBox.Show("Unknown result code: " + result, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }

                }
                //catch
                //{
                //    MessageBox.Show("An error occurred while processing the PD0 file.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                //}
                finally
                {
                    PythonEngine.Shutdown();
                }
            }
        }

        public static string[] ParseCSVAndReturnColumns(string filePath, string separator, int headerLine)
        {
            if (!PythonEngine.IsInitialized)
            {
                InitPython();
            }
            var inputs = new Dictionary<string, string>
            {
                { "Task", "GetColumnsFromCSV" },
                { "Path", filePath },
                { "Sep", separator },
                { "Header", headerLine.ToString() }
            };
            string xmlInput = GenerateInput(inputs);
            XmlDocument doc = CallPython(xmlInput);
            int nColumns = Convert.ToInt32(doc.SelectSingleNode("/Result/NColumns")?.InnerText ?? "0");
            if (nColumns == 0)
            {
                MessageBox.Show("No columns found in the CSV file.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return Array.Empty<string>();
            }
            else
            {
                var columns = new string[nColumns];
                for (int i = 0; i < nColumns; i++)
                {
                    columns[i] = doc.SelectSingleNode($"/Result/Column{i}")?.InnerText ?? $"Column{i}";
                }
                return columns;
            }
        }

        public static void ClearChildNodes(XmlElement el)
        {
            if (el == null) return;
            while (el.HasChildNodes)
            {
                el.RemoveChild(el.FirstChild);
            }
        }
    }
}
