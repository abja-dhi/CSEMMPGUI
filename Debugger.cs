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
    public partial class Debugger : Form
    {
        public Debugger(string text)
        {
            InitializeComponent();
            txtOutput.Text = text;
        }
    }
}
