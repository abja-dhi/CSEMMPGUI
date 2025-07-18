using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using DHI.Generic.MikeZero;
using DHI.Generic.MikeZero.DFS;
using DHI.Generic.MikeZero.DFS.dfsu;
using DHI.Generic.MikeZero.DFS.dfs123;
using DHI.Generic.MikeZero.DFS.mesh;

namespace CSEMMPGUI_v1
{
    public partial class AddModel : Form
    {
        public AddModel()
        {
            InitializeComponent();
        }

        private void btnLoad_Click(object sender, EventArgs e)
        {
            FileDialog loadModel = new OpenFileDialog();
            loadModel.Filter = "DFSU Files (*.dfsu)|*.dfsu|DFS2 Files (*.dfs2)|*.dfs2|DFS3 Files (*.dfs3)|*.dfs3";
            if (loadModel.ShowDialog() == DialogResult.OK)
            {
                tableFileInfo.Visible = true;
                string fileName = loadModel.FileName;
                txtFilePath.Text = fileName;
                ParseAndDisplayFileInfo(fileName);
            }
        }

        private void txtFilePath_Leave(object sender, EventArgs e)
        {
            string fileName = txtFilePath.Text.Trim();
            if (!string.IsNullOrEmpty(fileName))
            {
                if (System.IO.File.Exists(fileName))
                {
                    tableFileInfo.Visible = true;
                    ParseAndDisplayFileInfo(fileName);
                }
                else
                {
                    MessageBox.Show("File does not exist or is invalid.");
                }
            }
        }


        // Helper Functions
        private void ParseAndDisplayFileInfo(string filePath)
        {
            try
            {
                if (filePath.EndsWith(".dfsu", StringComparison.OrdinalIgnoreCase))
                {
                    IDfsuFile dfsu = DfsuFile.Open(filePath);
                    int numberOfElements = dfsu.NumberOfElements;
                    int numberOfNodes = dfsu.NumberOfNodes;
                    int numberOfLayers = dfsu.NumberOfLayers;
                    int numberOfItems = dfsu.ItemInfo.Count;
                    DateTime[] dateTimes = dfsu.GetDateTimes();
                    string fileType = dfsu.DfsuFileType.ToString();
                    lblNumberOfNodes.Text = numberOfNodes.ToString();
                    lblNumberOfElements.Text = numberOfElements.ToString();
                    lblStartingTime.Text = dateTimes[0].ToString();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error loading model: " + ex.Message);
            }
        }

        
    }
}
