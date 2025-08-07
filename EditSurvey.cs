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
    public partial class EditSurvey : Form
    {
        public bool isSaved; // Track if survey has been saved
        public _SurveyManager surveyManager;

        public EditSurvey(XmlNode surveyNode)
        {
            InitializeComponent();
            XmlElement? surveyElement = surveyNode as XmlElement;
            string? surveyName = surveyElement?.GetAttribute("name");
            surveyManager = new _SurveyManager
            {
                Name = surveyName ?? "New Survey",
                survey = surveyElement
            };
            txtSurveyName.Text = surveyManager.GetAttribute(attribute: "name");
            isSaved = true; // Initially, the survey is not saved
            FillTree();
        }

        private void FillTree()
        {
            treeSurvey.Nodes.Clear();
            XmlNode? root = surveyManager.survey;
            string name = surveyManager.GetAttribute("name");
            if (root.Attributes?["type"] != null)
            {
                TreeNode rootNode = new TreeNode(name);
                rootNode.Tag = root;
                treeSurvey.Nodes.Add(rootNode);
                AddChildNodes(root, rootNode); // Recursively add child nodes
                treeSurvey.ExpandAll(); // Expand all nodes for better visibility
            }
        }

        private void AddChildNodes(XmlNode xmlNode, TreeNode treeNode)
        {
            foreach (XmlNode child in xmlNode.ChildNodes)
            {
                if (child.NodeType != XmlNodeType.Element || child.Name == "Settings")
                    continue; // Skip non-element nodes and the Settings node

                XmlAttribute? typeAttr = child.Attributes?["type"];
                if (typeAttr != null)
                {
                    string name = child.Attributes["name"]?.Value ?? child.Name;
                    TreeNode childNode = new TreeNode(name);
                    childNode.Tag = child;
                    treeNode.Nodes.Add(childNode);
                    AddChildNodes(child, childNode); // Recursively add child nodes
                }
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            surveyManager.SaveSurvey(name: txtSurveyName.Text);
            isSaved = true;
            FillTree(); // Refresh the tree view after saving
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current survey has unsaved changes. Do you want to save them before exiting?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    surveyManager.SaveSurvey(name: txtSurveyName.Text);
                    isSaved = true; // Mark as saved after saving
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not exit
                }
            }
            this.Close(); // Close the AddSurvey form
        }

        private void menuADCPVesselMounted_Click(object sender, EventArgs e)
        {
            AddVesselMountedADCP vesselMountedADCP = new AddVesselMountedADCP(surveyManager);
            vesselMountedADCP.ShowDialog();
            FillTree(); // Refresh the tree after adding a new ADCP
        }

        private void menuADCPSeabedLander_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This feature is not yet implemented.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void menuOBSVerticalProfile_Click(object sender, EventArgs e)
        {
            AddOBSVerticalProfile obsVerticalProfile = new AddOBSVerticalProfile(surveyManager);
            obsVerticalProfile.ShowDialog();
        }

        private void menuOBSTransect_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This feature is not yet implemented.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void menuWaterSample_Click(object sender, EventArgs e)
        {
            AddWaterSample waterSample = new AddWaterSample(surveyManager);
            waterSample.ShowDialog();
            FillTree(); // Refresh the tree after adding a new water sample
        }

        private void EditSurvey_Activated(object sender, EventArgs e)
        {
            FillTree();
        }

        private void EditSurvey_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current survey has unsaved changes. Do you want to save them before exiting?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    surveyManager.SaveSurvey(name: txtSurveyName.Text);
                    isSaved = true; // Mark as saved after saving
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Cancel the form closing event
                    return; // User chose to cancel, do not exit
                }
            }
        }

        private void treeSurvey_NodeMouseClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            if (e.Button == MouseButtons.Right)
            {
                treeSurvey.SelectedNode = e.Node;
                // Check type of associated XML node
                if (e.Node.Tag is XmlNode xmlNode)
                {
                    string? type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                    itemDelete.Visible = type != "Survey"; // Disable delete for the root survey node
                    itemOpen.Visible = type != "Survey"; // Disable open for the root survey node
                }
                cmenuNode.Show(treeSurvey, e.Location);
            }
        }

        private void itemOpen_Click(object sender, EventArgs e)
        {
            TreeNode? selectedNode = treeSurvey.SelectedNode;
            if (selectedNode != null && selectedNode.Tag is XmlNode xmlNode)
            {
                string type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                string name = xmlNode.Attributes?["name"]?.Value ?? xmlNode.Name;

                switch (type)
                {
                    case "VesselMountedADCP":
                        EditVesselMountedADCP editVesselMountedADCP = new EditVesselMountedADCP(xmlNode);
                        editVesselMountedADCP.ShowDialog();
                        break;
                    case "WaterSample":
                        EditWaterSample editWaterSample = new EditWaterSample(xmlNode);
                        editWaterSample.ShowDialog();
                        break;
                    case "OBSVerticalProfile":
                        EditOBSVerticalProfile editOBSVerticalProfile = new EditOBSVerticalProfile(xmlNode);
                        editOBSVerticalProfile.ShowDialog();
                        break;
                }
            }
            FillTree(); // Refresh the tree view after opening an item
            isSaved = false;
        }

        private void itemDelete_Click(object sender, EventArgs e)
        {
            TreeNode? selectedNode = treeSurvey.SelectedNode;
            if (selectedNode != null && selectedNode.Tag is XmlNode xmlNode)
            {
                string type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                string name = xmlNode.Attributes?["name"]?.Value ?? xmlNode.Name;
                string id = xmlNode.Attributes?["id"]?.Value ?? string.Empty;

                switch (type)
                {
                    case "VesselMountedADCP":
                        DialogResult resultVesselMountedADCP = MessageBox.Show($"Are you sure you want to delete the vessel-mounted ADCP: {name}?", "Delete Vessel Mounted ADCP", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultVesselMountedADCP == DialogResult.Yes)
                        {
                            _ClassConfigurationManager.DeleteNode(type: "VesselMountedADCP", id: id);
                        }
                        break;
                    case "WaterSample":
                        DialogResult resultWaterSample = MessageBox.Show($"Are you sure you want to delete the water sample: {name}?", "Delete Water Sample", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultWaterSample == DialogResult.Yes)
                        {
                            _ClassConfigurationManager.DeleteNode(type: "WaterSample", id: id);
                        }
                        break;
                    case "OBSVerticalProfile":
                        DialogResult resultOBSVerticalProfile = MessageBox.Show($"Are you sure you want to delete the OBS vertical profile: {name}?", "Delete OBS Vertical Profile", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultOBSVerticalProfile == DialogResult.Yes)
                        {
                            _ClassConfigurationManager.DeleteNode(type: "OBSVerticalProfile", id: id);
                        }
                        break;
                }
            }
            isSaved = false; // Mark the project as unsaved after deletion
            FillTree();
        }

        private void treeSurvey_NodeMouseDoubleClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            TreeNode? selectedNode = treeSurvey.SelectedNode;
            if (selectedNode != null && selectedNode.Tag is XmlNode xmlNode)
            {
                string type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                string name = xmlNode.Attributes?["name"]?.Value ?? xmlNode.Name;

                switch (type)
                {
                    case "VesselMountedADCP":
                        EditVesselMountedADCP editVesselMountedADCP = new EditVesselMountedADCP(xmlNode);
                        editVesselMountedADCP.ShowDialog();
                        break;
                    case "WaterSample":
                        EditWaterSample editWaterSample = new EditWaterSample(xmlNode);
                        editWaterSample.ShowDialog();
                        break;
                }
            }
            FillTree(); // Refresh the tree view after double-clicking an item
            isSaved = false; // Mark the project as unsaved after opening an item
        }

        private void itemPlot_Click(object sender, EventArgs e)
        {
            TreeNode? selectedNode = treeSurvey.SelectedNode;
            if (selectedNode != null && selectedNode.Tag is XmlNode xmlNode)
            {
                string type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                string name = xmlNode.Attributes?["name"]?.Value ?? xmlNode.Name;

                switch (type)
                {
                    case "Survey":
                        MessageBox.Show($"Opening survey: {name}", "Open Survey", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement survey opening logic here
                        break;
                    case "VesselMountedADCP":
                        MessageBox.Show($"Opening vessel-mounted ADCP: {name}", "Open Vessel-Mounted ADCP", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement vessel-mounted ADCP opening logic here
                        break;
                    case "WaterSample":
                        MessageBox.Show($"Opening water sample: {name}", "Open Water Sample", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement water sample opening logic here
                        break;
                }
            }
        }

        private void txtSurveyName_TextChanged(object sender, EventArgs e)
        {
            isSaved = false; // Mark as unsaved when the survey name changes
        }
    }
}
