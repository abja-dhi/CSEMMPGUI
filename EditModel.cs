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
            modelNode = ConfigData.GetModelByName(modelName);
            if (modelNode != null)
            {
                txtModelName.Text = modelNode.Attributes?["name"]?.Value ?? string.Empty;
                txtFilePath.Text = modelNode.SelectSingleNode("Path")?.InnerText ?? string.Empty;
            }
            else
            {
                MessageBox.Show($"Model '{modelName}' not found.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Save()
        {
            modelNode.Attributes["name"].Value = txtModelName.Text.Trim();
            modelNode.SelectSingleNode("Path").InnerText = txtFilePath.Text;
            ConfigData.SaveConfig();
            isSaved = true;
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
            if (isSaved || modelNode == null) return;

            string originalName = modelNode.Attributes?["name"]?.Value ?? string.Empty;
            string originalPath = modelNode.SelectSingleNode("Path")?.InnerText?.Trim() ?? string.Empty;

            string currentName = txtModelName.Text.Trim();
            string currentPath = txtFilePath.Text.Trim();

            bool isModified = !string.Equals(originalName, currentName, StringComparison.Ordinal) ||
                              !string.Equals(originalPath, currentPath, StringComparison.Ordinal);

            if (isModified)
            {
                DialogResult result = MessageBox.Show(
                    "Do you want to save the changes to this model?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Question);

                if (result == DialogResult.Yes)
                {
                    Save(); // save changes
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // keep the form open
                }
                // result == No → do nothing, discard changes
            }
        }

        
    }
}
