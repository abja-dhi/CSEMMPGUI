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
    public partial class PropertiesPage : Form
    {
        private XmlDocument project;
        public PropertiesPage(XmlDocument node)
        {
            InitializeComponent();
            project = node;
        }
        public string projectDir => txtProjectDir.Text;
        public string projectName => txtProjectName.Text;
        public string projectEPSG => txtProjectEPSG.Text;
        private void PropertiesPage_Load(object sender, EventArgs e)
        {

        }

        private void PropertiesPage_FormClosed(object sender, FormClosedEventArgs e)
        {
            
        }
    }
}
