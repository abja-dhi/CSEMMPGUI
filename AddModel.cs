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
using System.Xml;

namespace CSEMMPGUI_v1
{
    public partial class AddModel : Form
    {
        public bool isSaved;
        public XmlElement modelElement;

        private void InitializeModel()
        {
            int NModels = _ClassConfigurationManager.NModels();
            txtModelName.Text = "Model " + (NModels + 1).ToString();
            isSaved = true;
            modelElement = _Globals.Config.CreateElement("Model");
            modelElement.SetAttribute("name", txtModelName.Text);
            modelElement.SetAttribute("type", "Model");
            modelElement.SetAttribute("id", (NModels + 1).ToString());
            txtFilePath.Text = string.Empty;
        }

        public AddModel()
        {
            InitializeComponent();
            InitializeModel();
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    text: "You have unsaved changes. Do you want to save before creating a new model?",
                    caption: "Confirm New Model",
                    buttons: MessageBoxButtons.YesNoCancel,
                    icon: MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    Save();
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel
                }
            }
            InitializeModel();
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            Save();
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    text: "You have unsaved changes. Do you want to save before exiting?",
                    caption: "Confirm Exit",
                    buttons: MessageBoxButtons.YesNoCancel,
                    icon: MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    Save();
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel
                }
            }
            this.Close(); // Close the form
        }

        private void btnLoad_Click(object sender, EventArgs e)
        {
            var ofd = new OpenFileDialog
            {
                Title = "Select Model DFSU File",
                Filter = "DFSU (*.dfsu)|*.dfsu",
                Multiselect = false,
                InitialDirectory = _ClassConfigurationManager.GetSetting(settingName: "Directory"),
            };
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                txtFilePath.Text = ofd.FileName;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private void AddModel_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    text: "You have unsaved changes. Do you want to save before exiting?",
                    caption: "Confirm Exit",
                    buttons: MessageBoxButtons.YesNoCancel,
                    icon: MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    Save();
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Cancel the closing event
                }
            }
        }

        private void input_Changed(object sender, EventArgs e)
        {
            isSaved = false; // Mark as unsaved changes
        }

        private string GetFullPath(string filePath)
        {
            if (Path.IsPathRooted(filePath))
            {
                return filePath;
            }
            else
            {
                string directory = _ClassConfigurationManager.GetSetting(settingName: "Directory");
                return Path.Combine(directory, filePath);
            }
        }

        private void Save()
        {
            if (String.IsNullOrEmpty(txtModelName.Text))
            {
                MessageBox.Show(text: "Model name cannot be empty.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return;
            }
            if (String.IsNullOrEmpty(txtFilePath.Text))
            {
                MessageBox.Show(text: "File path cannot be empty.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return;
            }
            if (!File.Exists(GetFullPath(txtFilePath.Text.Trim())))
            {
                MessageBox.Show(text: "File does not exist at the specified path.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return;
            }
            modelElement.SetAttribute("name", txtModelName.Text);
            XmlElement path = _Globals.Config.CreateElement("Path");
            path.InnerText = GetFullPath(txtFilePath.Text.Trim());
            modelElement.AppendChild(path);
            var doc = _Globals.Config.DocumentElement;
            if (doc != null)
            {
                doc.AppendChild(modelElement);
            }
            _ClassConfigurationManager.SaveConfig(saveMode: 1);
            isSaved = true;
        }
    }
}
