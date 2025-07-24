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
        public bool isSaved = false;
        public AddModel()
        {
            InitializeComponent();
            txtModelName.Text = ConfigData.GetDefaultModelName();
        }

        private void SaveMtModel(string modelName, string modelPath)
        {
            string projectDir = ConfigData.GetProjectDir();
            if (string.IsNullOrWhiteSpace(projectDir) || !Directory.Exists(projectDir))
            {
                MessageBox.Show("Project directory not found or invalid.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            string mtmodelPath = Path.Combine(projectDir, modelName + ".mtmodel");

            XmlDocument modelDoc = new XmlDocument();
            XmlDeclaration xmlDecl = modelDoc.CreateXmlDeclaration("1.0", "UTF-8", null);
            modelDoc.AppendChild(xmlDecl);

            XmlElement modelElement = modelDoc.CreateElement("Model");
            modelElement.SetAttribute("type", "Model");
            modelElement.SetAttribute("name", modelName);

            XmlElement pathElement = modelDoc.CreateElement("Path");
            pathElement.InnerText = modelPath;
            modelElement.AppendChild(pathElement);

            modelDoc.AppendChild(modelElement);
            modelDoc.Save(mtmodelPath);
            MessageBox.Show($"Model saved successfully at {mtmodelPath}", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void Save()
        {
            string modelName = txtModelName.Text.Trim();
            string modelPath = txtFilePath.Text.Trim();

            if (string.IsNullOrEmpty(modelName) || string.IsNullOrEmpty(modelPath))
            {
                MessageBox.Show("Model name and path cannot be empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            XmlNode root = ConfigData.Config.DocumentElement;
            XmlNode existingModel = ConfigData.GetModelByName(modelName);

            if (existingModel != null)
            {
                string existingPath = existingModel.SelectSingleNode("Path")?.InnerText?.Trim();

                if (string.Equals(existingPath, modelPath, StringComparison.OrdinalIgnoreCase))
                {
                    return;
                }
                else
                {
                    DialogResult result = MessageBox.Show(
                        "A model with this name already exists but with a different path.\nDo you want to overwrite it?",
                        "Overwrite Model?",
                        MessageBoxButtons.YesNoCancel,
                        MessageBoxIcon.Question);

                    if (result == DialogResult.Yes)
                    {
                        XmlNode pathNode = existingModel.SelectSingleNode("Path");
                        if (pathNode == null)
                        {
                            pathNode = ConfigData.Config.CreateElement("Path");
                            existingModel.AppendChild(pathNode);
                        }
                        pathNode.InnerText = modelPath;
                        ConfigData.SaveConfig();
                        SaveMtModel(modelName, modelPath); // <- Save .mtmodel file
                        return;
                    }
                    else
                    {
                        return;
                    }
                }
            }
            else
            {
                ConfigData.AddModelByName(modelName, modelPath);
                ConfigData.SaveConfig();
                SaveMtModel(modelName, modelPath); // <- Save .mtmodel file
            }
        }

        private void btnLoad_Click(object sender, EventArgs e)
        {
            FileDialog loadModel = new OpenFileDialog();
            loadModel.Filter = "DFSU Files (*.dfsu)|*.dfsu|DFS2 Files (*.dfs2)|*.dfs2|DFS3 Files (*.dfs3)|*.dfs3";
            loadModel.InitialDirectory = ConfigData.GetProjectDir();
            if (loadModel.ShowDialog() == DialogResult.OK)
            {
                string fileName = loadModel.FileName;
                txtFilePath.Text = fileName;

            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtFilePath.Text) || string.IsNullOrWhiteSpace(txtModelName.Text))
            {
                return;
            }
            Save();
            isSaved = true;
        }

        private void AddModel_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (isSaved)
            {
                return;
            }
            else
            {
                bool hasInput = !string.IsNullOrWhiteSpace(txtFilePath.Text) || !string.IsNullOrWhiteSpace(txtModelName.Text);
                if (hasInput)
                {
                    DialogResult result = MessageBox.Show(
                    "You have unsaved changes. Do you want to save before closing?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                    if (result == DialogResult.Cancel)
                    {
                        e.Cancel = true; // Cancel the form closing
                    }
                    else if (result == DialogResult.Yes)
                    {
                        Save();
                        isSaved = true;
                    }
                    else if (result == DialogResult.No)
                    {
                        isSaved = false;
                    }
                }
                else
                {
                    return;
                }

            }
        }

        private void menuOpen_Click(object sender, EventArgs e)
        {
            OpenFileDialog openModel = new OpenFileDialog
            {
                Filter = "Model XML Files (*.mtmodel)|*.mtmodel",
                Title = "Open Model File",
                InitialDirectory = ConfigData.GetProjectDir()
            };

            if (openModel.ShowDialog() == DialogResult.OK)
            {
                XmlDocument modelDoc = new XmlDocument();
                try
                {
                    modelDoc.Load(openModel.FileName);
                    XmlNode modelNode = modelDoc.SelectSingleNode("/Model");

                    if (modelNode != null && modelNode.Attributes["name"] != null)
                    {
                        string modelName = modelNode.Attributes["name"].Value;
                        string modelPath = modelNode.SelectSingleNode("Path")?.InnerText;

                        txtModelName.Text = modelName ?? "";
                        txtFilePath.Text = modelPath ?? "";
                    }
                    else
                    {
                        MessageBox.Show("Invalid model file.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error loading model file:\n{ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }
    }
}
