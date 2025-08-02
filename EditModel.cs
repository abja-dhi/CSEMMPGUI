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
        public bool isSaved;
        public XmlElement modelElement;

        private void InitializeModel(XmlNode modelNode)
        {
            int NModels = _ClassConfigurationManager.NModels();
            modelElement = modelNode as XmlElement;
            if (modelElement == null)
            {
                MessageBox.Show(text: "Invalid model node provided.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                this.Close();
            }
            txtModelName.Text = modelElement.GetAttribute("name");
            XmlNode pathNode = modelElement.SelectSingleNode("Path");
            if (pathNode != null)
            {
                txtFilePath.Text = pathNode.InnerText;
            }
            else
            {
                txtFilePath.Text = string.Empty;
            }
            isSaved = true;

        }

        public EditModel(XmlNode modelNode)
        {
            InitializeComponent();
            InitializeModel(modelNode);
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

        private void EditModel_FormClosing(object sender, FormClosingEventArgs e)
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

        private void txtFilePath_Leave(object sender, EventArgs e)
        {
            if (!String.IsNullOrEmpty(txtFilePath.Text))
            {
                string filePath = GetFullPath(txtFilePath.Text.Trim());
                if (!File.Exists(filePath))
                {
                    MessageBox.Show(text: "File does not exist at the specified path.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                    txtFilePath.Focus();
                }
                if (Path.GetExtension(filePath).ToLower() != ".dfsu")
                {
                    MessageBox.Show(text: "Please select a valid DFSU file.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                    txtFilePath.Focus();
                }
                txtFilePath.Text = filePath; // Update the text box with the full path
            }

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
            if (modelElement == null)
            {
                MessageBox.Show(text: "Model element is not initialized.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return;
            }
            modelElement.SetAttribute("name", txtModelName.Text);
            XmlNode path = modelElement.SelectSingleNode("Path");
            path.InnerText = GetFullPath(txtFilePath.Text.Trim());
            _ClassConfigurationManager.SaveConfig(saveMode: 1);
            isSaved = true; // Mark as saved
        }

        
    }
}
