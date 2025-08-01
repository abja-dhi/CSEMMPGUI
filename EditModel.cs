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
    public partial class EditModel : Form
    {
        public XmlNode modelNode;
        public bool isSaved = false;
        public EditModel(string modelName)
        {
            InitializeComponent();
            
        }

        private void Save()
        {
            
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            Save();
        }

        private void setStatus(object sender, EventArgs e)
        {
            isSaved = false;
        }

        private void EditModel_FormClosing(object sender, FormClosingEventArgs e)
        {
            
        }

        
    }
}
