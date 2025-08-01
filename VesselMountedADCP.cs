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

        private readonly XmlElement _parentSurvey;
        private XmlElement _vesselMountedADCP;
        private bool _isSaved = false;
        public VesselMountedADCP(SurveyManager surveyManager)
        {
            string pythonDll = @"C:\Program Files\Python311\python311.dll";
            Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", pythonDll);
            PythonEngine.Initialize();
            InitializeComponent();
            _parentSurvey = parentSurvey ?? throw new ArgumentNullException(nameof(parentSurvey));
            int vesselMountedADCPCount = _parentSurvey.SelectNodes("./VesselMountedADCP[@type='Vessel Mounted ADCP']").Count;

            string defaultName = $"Vessel Mounted ADCP {vesselMountedADCPCount + 1}";
            txtName.Text = defaultName;

            _vesselMountedADCP = _parentSurvey.OwnerDocument.CreateElement("VesselMountedADCP");
            _vesselMountedADCP.SetAttribute("type", "Vessel Mounted ADCP");
            _vesselMountedADCP.SetAttribute("name", defaultName);
        }

        
    }
}
