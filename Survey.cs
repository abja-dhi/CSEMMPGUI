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
    public partial class Survey : Form
    {

        public bool isSaved;
        public _SurveyManager surveyManager;
        public int mode;
        public _ClassConfigurationManager _project = new();

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

        private void InitializeSurvey()
        {
            surveyManager = new _SurveyManager();
            surveyManager.Initialize();
            txtSurveyName.Text = surveyManager.GetAttribute(attribute: "name");
            FillTree();
            isSaved = true;
        }

        private void PopulateSurvey(XmlElement? surveyElement)
        {
            string name = surveyElement?.GetAttribute("name");
            surveyManager = new _SurveyManager { Name = name, survey = surveyElement };
            txtSurveyName.Text = surveyManager.GetAttribute(attribute: "name");
            FillTree();
            isSaved = true;
        }

        public Survey(XmlNode? surveyNode)
        {
            InitializeComponent();
            if (surveyNode == null)
            {
                InitializeSurvey();
                mode = 0; // New survey mode
                this.Text = "Add Survey";
            }
            else
            {
                XmlElement? surveyElement = surveyNode as XmlElement;
                PopulateSurvey(surveyElement);
                menuNew.Visible = false;
                mode = 1; // Edit survey mode
                this.Text = "Edit Survey";
            }

            this.KeyPreview = true; // Enable form to capture key events
            this.KeyDown += Survey_KeyDown; // Attach key down event handler
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current survey has unsaved changes. Do you want to save them before creating a new survey?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = Save();
                    if (status == 0)
                        return; // If saving failed, do not create a new survey
                    surveyManager.Initialize();
                    isSaved = true; // Mark as saved after saving
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not create a new survey
                }
                else
                {
                    surveyManager.Initialize(); // Reset survey manager without saving
                    isSaved = true; // Mark as saved after initializing
                }
            }
            else
            {
                InitializeSurvey();
                isSaved = true; // Mark as saved after initializing
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            int status = Save();
            FillTree();
            isSaved = true;
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current survey has unsaved changes. Do you want to save them before creating a new survey?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = Save();
                    if (status == 0)
                        return; // If saving failed, do not close the survey form
                    this.Close();
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not create a new survey
                }
                else
                {
                    this.Close(); // Close the survey form without saving
                }
            }
            else
            {
                this.Close(); // Close the survey form if there are no unsaved changes
            }
        }

        private void Survey_FormClosing(object sender, FormClosingEventArgs e)
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
                    int status = Save();
                    if (status == 0)
                    {
                        e.Cancel = true; // Cancel the closing event if saving failed
                        return; // Do not close the form
                    }
                    isSaved = true; // Mark as saved after saving
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Cancel the closing event
                    return; // User chose to cancel, do not close the form
                }
            }
        }

        private void Survey_Activated(object sender, EventArgs e)
        {
            FillTree();
        }

        private void input_Changed(object sender, EventArgs e)
        {
            isSaved = false; // Mark as unsaved changes
        }

        private void menuADCPVesselMounted_Click(object sender, EventArgs e)
        {
            VesselMountedADCP vesselMountedADCPForm = new VesselMountedADCP(surveyManager, null);
            vesselMountedADCPForm.ShowDialog();
            FillTree();
        }

        private void menuADCPSeabedLander_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This feature is not yet implemented.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void menuOBSVerticalProfile_Click(object sender, EventArgs e)
        {
            OBSVerticalProfile obsVeticalProfileForm = new OBSVerticalProfile(surveyManager, null);
            obsVeticalProfileForm.ShowDialog();
            FillTree();
        }

        private void menuOBSTransect_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This feature is not yet implemented.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void menuWaterSample_Click(object sender, EventArgs e)
        {
            WaterSample waterSampleForm = new WaterSample(surveyManager, null);
            waterSampleForm.ShowDialog();
            FillTree();
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

        private void treeSurvey_NodeMouseDoubleClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            TreeNode? selectedNode = treeSurvey.SelectedNode;
            if (selectedNode != null && selectedNode.Tag is XmlNode xmlNode)
            {
                string type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                switch (type)
                {
                    case "VesselMountedADCP":
                        VesselMountedADCP editVesselMountedADCP = new VesselMountedADCP(surveyManager, xmlNode);
                        editVesselMountedADCP.ShowDialog();
                        break;
                    case "WaterSample":
                        WaterSample editWaterSample = new WaterSample(surveyManager, xmlNode);
                        editWaterSample.ShowDialog();
                        break;
                    case "OBSVerticalProfile":
                        OBSVerticalProfile editOBSVerticalProfile = new OBSVerticalProfile(surveyManager, xmlNode);
                        editOBSVerticalProfile.ShowDialog();
                        break;
                }
            }
            FillTree();
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
                        VesselMountedADCP editVesselMountedADCP = new VesselMountedADCP(surveyManager, xmlNode);
                        editVesselMountedADCP.ShowDialog();
                        break;
                    case "WaterSample":
                        WaterSample editWaterSample = new WaterSample(surveyManager, xmlNode);
                        editWaterSample.ShowDialog();
                        break;
                    case "OBSVerticalProfile":
                        OBSVerticalProfile editOBSVerticalProfile = new OBSVerticalProfile(surveyManager, xmlNode);
                        editOBSVerticalProfile.ShowDialog();
                        break;
                }
            }
            FillTree(); // Refresh the tree view after opening an item
        }

        private void itemPlot_Click(object sender, EventArgs e)
        {
            TreeNode? selectedNode = treeSurvey.SelectedNode;
            if (selectedNode != null && selectedNode.Tag is XmlNode xmlNode)
            {
                string type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                string name = xmlNode.Attributes?["name"]?.Value ?? xmlNode.Name;
                string id = xmlNode.Attributes?["id"]?.Value ?? string.Empty;

                switch (type)
                {
                    case "Survey":
                        MessageBox.Show($"Plotting survey: {name}", "Plot Survey", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement survey opening logic here
                        break;
                    case "VesselMountedADCP":
                        VesselMountedADCPPlot vesselMountedADCPPlot = new VesselMountedADCPPlot(id);
                        vesselMountedADCPPlot.Show();
                        break;
                    case "WaterSample":
                        MessageBox.Show($"Plotting water sample: {name}", "Plot Water Sample", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement water sample opening logic here
                        break;
                    case "OBSVerticalProfile":
                        MessageBox.Show($"Plotting OBS vertical profile: {name}", "Plot OBS Vertical Profile", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement OBS vertical profile opening logic here
                        break;
                }
            }
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
                            _project.DeleteNode(type: "VesselMountedADCP", id: id);
                        }
                        break;
                    case "WaterSample":
                        DialogResult resultWaterSample = MessageBox.Show($"Are you sure you want to delete the water sample: {name}?", "Delete Water Sample", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultWaterSample == DialogResult.Yes)
                        {
                            _project.DeleteNode(type: "WaterSample", id: id);
                        }
                        break;
                    case "OBSVerticalProfile":
                        DialogResult resultOBSVerticalProfile = MessageBox.Show($"Are you sure you want to delete the OBS vertical profile: {name}?", "Delete OBS Vertical Profile", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultOBSVerticalProfile == DialogResult.Yes)
                        {
                            _project.DeleteNode(type: "OBSVerticalProfile", id: id);
                        }
                        break;
                }
            }
            FillTree();
            isSaved = false; // Mark the project as unsaved after deletion
        }

        private int Save()
        {
            try
            {
                string name = txtSurveyName.Text.Trim();
                double waterDensity = double.TryParse(txtDensity.Text, out double density) ? density : 1023.0; // Default to 1023.0 if parsing fails
                double waterSalinity = double.TryParse(txtSalinity.Text, out double salinity) ? salinity : 32.0; // Default to 32.0 if parsing fails
                double waterTemperature = double.TryParse(txtTemperature.Text, out double temperature) ? temperature : 10.0; // Default to 10.0 if parsing fails
                double waterPH = double.TryParse(txtPH.Text, out double pH) ? pH : 8.1; // Default to 8.1 if parsing fails
                double sedimentDiameter = double.TryParse(txtSedimentDiameter.Text, out double diameter) ? diameter : 2.5e-4; // Default to 2.5e-4 if parsing fails
                double sedimentDensity = double.TryParse(txtSedimentDensity.Text, out double densitySediment) ? densitySediment : 2650.0; // Default to 2650.0 if parsing fails
                surveyManager.SaveSurvey(name: name,
                    waterDensity: waterDensity, waterSalinity: waterSalinity, waterTemperature: waterTemperature, waterPH: waterPH,
                    sedimentDiameter: sedimentDiameter, sedimentDensity: sedimentDensity);
                return 1;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error saving survey: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0; // Return 0 to indicate failure
            }

        }

        private void Survey_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Control && e.KeyCode == Keys.S) // Ctrl + S
            {
                e.SuppressKeyPress = true; // Prevent default behavior
                surveyManager.SaveSurvey(name: txtSurveyName.Text);
                FillTree();
                isSaved = true;
            }
            else if (e.Control && e.KeyCode == Keys.N) // Ctrl + N
            {
                if (mode == 0)
                {
                    e.SuppressKeyPress = true; // Prevent default behavior
                    menuNew_Click(sender, e); // Create a new project
                }
            }
        }
    }
}
