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

namespace CSEMMPGUI_v1
{
    public partial class VesselMountedADCP : Form
    {
        private XmlDocument project;
        public VesselMountedADCP(XmlDocument node)
        {
            InitializeComponent();
            project = node;
        }
    }
}
