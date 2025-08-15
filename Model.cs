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
    public partial class Model : Form
    {

        public bool isSaved;
        public XmlElement? modelElement;
        public int mode;

        private void InitializeModel()
        {
            txtModelName.Text = "New Model";
            int id = _ClassConfigurationManager.GetNextId();
            modelElement = _Globals.Config.CreateElement("Model");
            modelElement.SetAttribute("name", txtModelName.Text);
            modelElement.SetAttribute("type", "Model");
            modelElement.SetAttribute("id", id.ToString());
            txtFilePath.Text = string.Empty;
            isSaved = true;

        }

        private void PopulateModel()
        {
            if (modelElement == null)
            {
                MessageBox.Show(text: "Invalid model node provided.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                this.Close();
                return;
            }
            txtModelName.Text = modelElement.GetAttribute("name");
            XmlNode? pathNode = modelElement.SelectSingleNode("Path");
            txtFilePath.Text = pathNode?.InnerText ?? string.Empty;
            isSaved = true;
        }

        public Model(XmlNode? modelNode)
        {
            InitializeComponent();
            if (modelNode == null)
            {
                InitializeModel();
                mode = 0; // New model mode
                this.Text = "Add Model";
            }
            else
            {
                modelElement = modelNode as XmlElement;
                PopulateModel();
                menuNew.Visible = false; // Hide New menu option if editing an existing model
                mode = 1; // Edit model mode
                this.Text = "Edit Model";
            }
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
                    SaveModel();
                    InitializeModel();
                    return;
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel
                }
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveModel();
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
                    SaveModel();
                    this.Close();
                    return;
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel
                }
            }
        }

        private void Model_FormClosing(object sender, FormClosingEventArgs e)
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
                    SaveModel();
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

        private void SaveModel()
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
            if (!File.Exists(_Utils.GetFullPath(txtFilePath.Text.Trim())))
            {
                MessageBox.Show(text: "File does not exist at the specified path.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return;
            }
            if (mode == 0)
                SAVE();
            else
                UPDATE();
            isSaved = true;
        }

        private void SAVE()
        {
            modelElement?.SetAttribute("name", txtModelName.Text);
            XmlElement path = _Globals.Config.CreateElement("Path");
            path.InnerText = _Utils.GetFullPath(txtFilePath.Text.Trim());
            modelElement?.AppendChild(path);
            var doc = _Globals.Config.DocumentElement;
            if (doc != null)
            {
                doc.AppendChild(modelElement);
            }
            _ClassConfigurationManager.SaveConfig(saveMode: 1);
            int id = _ClassConfigurationManager.GetNextId();
            _Globals.Config.DocumentElement.SetAttribute("nextid", (id + 1).ToString());
        }
        
        private void UPDATE()
        {
            modelElement?.SetAttribute("name", txtModelName.Text);
            XmlNode path = modelElement.SelectSingleNode("Path");
            path.InnerText = _Utils.GetFullPath(txtFilePath.Text.Trim());
            _ClassConfigurationManager.SaveConfig(saveMode: 1);
        }

    }
}
