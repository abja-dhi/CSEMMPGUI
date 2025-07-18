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
    public partial class AddSurvey : Form
    {
        public AddSurvey()
        {
            InitializeComponent();
        }

        private void seabedLanderToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Insufficient budget! Consider upgrading!");
            Button button1 = new Button();
            button1.Location = new Point(1, 1);
            
        }
    }
}
