using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CSEMMPGUI_v1
{
    public partial class UtilsCSVImportOptions : Form
    {
        public string _delimiter = ",";
        public int _headerLine = 1;
        public UtilsCSVImportOptions(int nLines)
        {
            InitializeComponent();
            txtHeader.Maximum = nLines;
        }

        private void rbCustom_CheckedChanged(object sender, EventArgs e)
        {
            if (rbCustom.Checked)
            {
                txtCustom.Enabled = true;
            }
            else
            {
                txtCustom.Enabled = false;
            }
        }

        private void btnOK_Click(object sender, EventArgs e)
        {
            if (rbComma.Checked)
            {
                _delimiter = ",";
            }
            else if (rbSemiColon.Checked)
            {
                _delimiter = ";";
            }
            else if (rbWhiteSpaces.Checked)
            {
                _delimiter = "WhiteSpaces";
            }
            else if (rbTab.Checked)
            {
                _delimiter = "Tab";
            }
            else if (rbCustom.Checked)
            {
                _delimiter = txtCustom.Text;
            }
            _headerLine = (int)txtHeader.Value - 1;
            DialogResult = DialogResult.OK;
        }
    }
}
