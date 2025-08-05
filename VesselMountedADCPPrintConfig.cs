using DHI;
using Python.Runtime;
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
using static System.Windows.Forms.VisualStyles.VisualStyleElement.ExplorerBar;
using Python.Runtime;

namespace CSEMMPGUI_v1
{
    public partial class VesselMountedADCPPrintConfig : Form
    {
        public string pathToPd0;
        public VesselMountedADCPPrintConfig(string pd0Path)
        {
            InitializeComponent();
            pathToPd0 = pd0Path;
        }

        private void VesselMountedADCPPrintConfig_Load(object sender, EventArgs e)
        {
            Dictionary<string, string> inputs = new Dictionary<string, string>
            {
                { "Task", "InstrumentSummaryADCP" },
                { "Path", pathToPd0 },
            };
            string xmlInput = _Tools.GenerateInput(inputs);
            XmlDocument result = _Tools.CallPython(xmlInput);
            Dictionary<string, string> outputs = _Tools.ParseOutput(result);
            if (outputs.ContainsKey("Error"))
            {
                MessageBox.Show(outputs["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            string config = outputs["Config"];
            config = config.Replace("_br_", Environment.NewLine);
            txtConfig.Text = config;
            this.Text = $"Instrument Summary for {pathToPd0}";
        }
    }
}
