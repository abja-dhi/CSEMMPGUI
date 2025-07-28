using Python.Runtime;
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
    public partial class AddSurvey : Form
    {
        private XmlElement survey;
        private bool _isSaved = true;

        private void InitializeSurvey()
        {
            string surveyName = ConfigData.GetDefaultSurveyName();
            txtSurveyName.Text = surveyName;
            survey = ConfigData.Config.CreateElement("Survey");
            survey.SetAttribute("type", "Survey");
            survey.SetAttribute("name", surveyName);

            TreeNode rootNode = new TreeNode(surveyName);
            rootNode.Tag = survey;
            treeSurvey.Nodes.Add(rootNode);
        }

        private void FillTree()
        {
            string surveyName = txtSurveyName.Text.Trim();
            treeSurvey.Nodes.Clear();
            TreeNode rootNode = new TreeNode(surveyName);
            rootNode.Tag = survey;
            treeSurvey.Nodes.Add(rootNode);

            foreach (XmlNode child in survey.ChildNodes)
            {
                if (child is XmlElement subElement)
                {
                    string label = subElement.Attributes["name"]?.Value ?? "Unnamed";
                    TreeNode childNode = new TreeNode($"{subElement.Name} ({label})");
                    childNode.Tag = subElement;
                    rootNode.Nodes.Add(childNode);
                }
            }

            treeSurvey.ExpandAll();
        }

        public AddSurvey()
        {
            InitializeComponent();
            InitializeSurvey();
        }

        private void menuADCPVesselMounted_Click(object sender, EventArgs e)
        {
            VesselMountedADCP vesselMountedADCP = new VesselMountedADCP(survey);
            DialogResult isVesselMountedADCPAdded = vesselMountedADCP.ShowDialog();
            if (isVesselMountedADCPAdded == DialogResult.OK)
            {
                _isSaved = false;
                FillTree();
            }
        }

        private void menuADCPSeabedLander_Click(object sender, EventArgs e)
        {
            SeabedLanderADCP seabedLanderADCP = new SeabedLanderADCP();
            seabedLanderADCP.ShowDialog();
        }

        private void menuOBSVerticalProfile_Click(object sender, EventArgs e)
        {
            OBSVerticalProfile obsVerticalProfile = new OBSVerticalProfile();
            obsVerticalProfile.ShowDialog();
        }

        private void menuOBSTransect_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This feature is not implemented yet.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void menuWaterSample_Click(object sender, EventArgs e)
        {
            WaterSample waterSample = new WaterSample(survey);
            DialogResult isWaterSampleAdded = waterSample.ShowDialog();
            if (isWaterSampleAdded == DialogResult.OK)
            {
                _isSaved = false;
                FillTree();
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            if (survey != null && survey.HasChildNodes)
            {
                string surveyName = txtSurveyName.Text.Trim();
                if (string.IsNullOrWhiteSpace(surveyName))
                {
                    MessageBox.Show("Survey name cannot be empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }

                survey.SetAttribute("name", surveyName); // ensure name is up-to-date

                // Prompt for where to save the .mssurvey file
                string surveyPath = Path.Combine(ConfigData.GetProjectDir(), surveyName + ".mtsurvey");

                // Save standalone .mssurvey file
                XmlDocument surveyDoc = new XmlDocument();
                XmlDeclaration decl = surveyDoc.CreateXmlDeclaration("1.0", "UTF-8", null);
                surveyDoc.AppendChild(decl);
                surveyDoc.AppendChild(surveyDoc.ImportNode(survey, true));
                surveyDoc.Save(surveyPath);

                // Inject into project .mtproj
                XmlNode root = ConfigData.Config.DocumentElement;
                XmlNode existing = root.SelectNodes("Survey")
                    .Cast<XmlNode>()
                    .FirstOrDefault(s => s.Attributes?["name"]?.Value == surveyName);

                if (existing != null)
                {
                    DialogResult result = MessageBox.Show(
                        $"A survey named \"{surveyName}\" already exists in the project.\nDo you want to replace it?",
                        "Replace Survey?",
                        MessageBoxButtons.YesNo,
                        MessageBoxIcon.Question);

                    if (result == DialogResult.No)
                        return;

                    root.ReplaceChild(ConfigData.Config.ImportNode(survey, true), existing);
                }
                else
                {
                    root.AppendChild(ConfigData.Config.ImportNode(survey, true));
                }

                ConfigData.SaveConfig();
            }



        }

        private void txtSurveyName_Leave(object sender, EventArgs e)
        {
            if (!string.IsNullOrWhiteSpace(txtSurveyName.Text))
            {
                if (treeSurvey.Nodes.Count > 0)
                {
                    treeSurvey.Nodes[0].Text = txtSurveyName.Text;
                }
                else
                {
                    treeSurvey.Nodes.Add(txtSurveyName.Text);
                }
            }
        }

        private void SaveSurvey()
        {
            if (survey == null)
            {
                MessageBox.Show("No survey to save.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Update the survey name from the textbox
            string surveyName = txtSurveyName.Text.Trim();
            if (string.IsNullOrWhiteSpace(surveyName))
            {
                MessageBox.Show("Survey name cannot be empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }
            survey.SetAttribute("name", surveyName);

            string surveyPath = Path.Combine(ConfigData.GetProjectDir(), surveyName + ".mtsurvey");

            // Save survey as a standalone XML file
            XmlDocument surveyDoc = new XmlDocument();
            XmlDeclaration decl = surveyDoc.CreateXmlDeclaration("1.0", "UTF-8", null);
            surveyDoc.AppendChild(decl);
            XmlNode imported = surveyDoc.ImportNode(survey, true);
            surveyDoc.AppendChild(imported);
            surveyDoc.Save(surveyPath);

            // Add or replace this survey in the project .mtproj
            XmlNode root = ConfigData.Config.DocumentElement;
            XmlNode existing = root.SelectNodes("Survey")
                .Cast<XmlNode>()
                .FirstOrDefault(s => s.Attributes?["name"]?.Value == surveyName);

            if (existing != null)
            {
                DialogResult result = MessageBox.Show(
                    $"A survey with the name \"{surveyName}\" already exists in the project.\nDo you want to replace it?",
                   "Replace Survey?",
                    MessageBoxButtons.YesNo,
                    MessageBoxIcon.Question);
                if (result == DialogResult.No)
                {
                    return;
                }
                root.ReplaceChild(ConfigData.Config.ImportNode(survey, true), existing);
            }

            else
                root.AppendChild(ConfigData.Config.ImportNode(survey, true));

            ConfigData.SaveConfig(); // saves the .mtproj file

        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            // Check if survey has child nodes (any subelement has been added)
            if (survey != null && survey.HasChildNodes)
            {
                DialogResult result = MessageBox.Show(
                    "Do you want to save this survey before starting a new one?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);

                if (result == DialogResult.Cancel)
                {
                    return; // Do nothing
                }
                else if (result == DialogResult.Yes)
                {
                    SaveSurvey(); // Implement this method separately
                }
                // if No, continue to clear and start new
            }

            // Reset UI and XML
            treeSurvey.Nodes.Clear();
            InitializeSurvey();
        }

        private void menuOpen_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog
            {
                Filter = "Survey Files (*.mssurvey)|*.mssurvey",
                Title = "Open Survey File",
                InitialDirectory = ConfigData.GetProjectDir()
            };

            if (ofd.ShowDialog() != DialogResult.OK)
                return;

            XmlDocument doc = new XmlDocument();
            try
            {
                doc.Load(ofd.FileName);
                XmlNode loadedSurvey = doc.SelectSingleNode("/Survey");

                if (loadedSurvey == null || loadedSurvey.Attributes["name"] == null)
                {
                    MessageBox.Show("Invalid survey file format.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                // Reset the form and TreeView
                treeSurvey.Nodes.Clear();

                // Store the loaded <Survey> node directly (no importing)
                survey = loadedSurvey as XmlElement;

                // Update Survey Name in UI
                string surveyName = survey.GetAttribute("name");
                txtSurveyName.Text = surveyName;

                // Build TreeView from survey contents
                TreeNode rootNode = new TreeNode(surveyName);
                rootNode.Tag = survey;
                treeSurvey.Nodes.Add(rootNode);

                foreach (XmlNode child in survey.ChildNodes)
                {
                    if (child is XmlElement subElement)
                    {
                        string label = subElement.Attributes["name"]?.Value ?? "Unnamed";
                        TreeNode childNode = new TreeNode($"{subElement.Name} ({label})");
                        childNode.Tag = subElement;
                        rootNode.Nodes.Add(childNode);
                    }
                }

                treeSurvey.ExpandAll();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Failed to open survey file:\n{ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void AddSurvey_Activated(object sender, EventArgs e)
        {
            FillTree();
        }

        private void AddSurvey_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!_isSaved)
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
                    SaveSurvey(); // Save changes
                }
                else if (result == DialogResult.No)
                {
                    // Do nothing, just close
                }
            }
        }

        private void menuViSeaExtern2CSVSingle_Click(object sender, EventArgs e)
        {
            Tools.ExternToCSV();
        }
    }
}
