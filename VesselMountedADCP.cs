using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using Python.Runtime;

namespace CSEMMPGUI_v1
{
    public partial class VesselMountedADCP : Form
    {
        public VesselMountedADCP()
        {
            string pythonDll = @"C:\Program Files\Python311\python311.dll";
            Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", pythonDll);
            PythonEngine.Initialize();
            InitializeComponent();
        }

        private void btnLoadPD0_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "PD0 Files (*.000)|*.000";
            openFileDialog.Title = "Select a PD0 File";
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                string filePath = openFileDialog.FileName;
                var sb = new StringBuilder();
                using (var writer = XmlWriter.Create(sb, new XmlWriterSettings { OmitXmlDeclaration = true }))
                {
                    writer.WriteStartElement("Input");
                    writer.WriteElementString("Task", "LoadPd0");
                    writer.WriteElementString("Path", filePath);
                    writer.WriteEndElement();
                }
                string xmlInputStr = sb.ToString();
                try
                {
                    using (Py.GIL())
                    {
                        dynamic sys = Py.Import("sys");
                        sys.path.append(@"C:\Users\abja\OneDrive - DHI\61803553-05 EMMP Support Group\github\CSEMMPGUI");
                        dynamic backend = Py.Import("backend.backend");
                        string resultXML = backend.Call(xmlInputStr).ToString();
                        var doc = new XmlDocument();
                        doc.LoadXml(resultXML);
                        string beams = doc.SelectSingleNode("/Result/NBeams")?.InnerText ?? "N/A";
                        string ensembles = doc.SelectSingleNode("/Result/NEnsembles")?.InnerText ?? "N/A";
                        MessageBox.Show($"Beams: {beams}\nEnsembles: {ensembles}", "Load PD0 Result", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        txtPD0Path.Text = filePath;
                        txtLastEnsemble.Maximum = Convert.ToInt32(ensembles);
                        txtLastEnsemble.Value = Convert.ToInt32(ensembles);
                        boxConfiguration.Enabled = true;
                        boxMasking.Enabled = true;
                    }
                    
                }
                catch
                {
                    MessageBox.Show("An error occurred while processing the PD0 file.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                finally
                {
                    PythonEngine.Shutdown();
                }
            }
        }
    }
}
