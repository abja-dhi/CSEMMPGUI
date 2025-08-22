using DHI.Mike1D.ResultDataAccess;
using Microsoft.VisualBasic;
using System.Xml;
using Python.Runtime;


namespace CSEMMPGUI_v1
{
    public partial class __PlumeTrack : Form
    {
        public bool isSaved; // Track if project has been saved
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
            treeProject.Nodes.Clear();
            XmlNode? root = _Globals.Config.DocumentElement;
            string name = _project.GetSetting(settingName: "Name");
            if (string.IsNullOrEmpty(name))
            {
                name = txtName.Text.Trim(); // Default name if not set
            }
            TreeNode rootNode = new TreeNode(name);
            rootNode.Tag = root;
            treeProject.Nodes.Add(rootNode);
            AddChildNodes(root, rootNode); // Recursively add child nodes
            treeProject.ExpandAll(); // Expand all nodes for better visibility
        }

        private void InitializeProject()
        {
            txtName.Text = "New Project";
            _project.InitializeProject();
            isSaved = true;
            FillTree(); // Populate the tree view with project structure
        }

        public __PlumeTrack()
        {
            InitializeComponent();
            InitializeProject();

            this.KeyPreview = true; // Enable form to capture key events
            this.KeyDown += __PlumeTrack_KeyDown; // Attach key down event handler
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            if (!isSaved) // If project has changed
            {
                // Show a message box to ask the user if they want to save changes
                DialogResult result = MessageBox.Show(
                "The current project has unsaved changes. Do you want to save them before creating a new project?",
                "Unsaved Changes",
                MessageBoxButtons.YesNoCancel,
                MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveProject(); // Save the project
                    if (status == 1)
                        InitializeProject(); // Initialize a new project if save was successful
                    else
                        return;
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not create a new project
                }
                else if (result == DialogResult.No)
                {
                    InitializeProject(); // Initialize a new project without saving
                }
            }
            else
            {
                InitializeProject(); // Initialize a new project if no unsaved changes
            }

        }

        private void menuOpen_Click(object sender, EventArgs e)
        {
            if (!isSaved) // If project has changed
            {
                // Show a message box to ask the user if they want to save changes
                DialogResult result = MessageBox.Show(
                text: "Do you want to save the current project before loading a new one?",
                caption: "Unsaved changes",
                buttons: MessageBoxButtons.YesNoCancel,
                icon: MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveProject(); // Save the current project
                    if (status == 0)
                        return;
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not load a new project
                }
            }
            using OpenFileDialog ofd = new OpenFileDialog
            {
                Filter = "MT Project Files (*.mtproj)|*.mtproj",
                Title = "Load Project",
                InitialDirectory = _project.GetSetting(settingName: "Directory")
            };
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                string filePath = ofd.FileName;
                _project.LoadConfig(filePath);
                txtName.Text = _project.GetSetting(settingName: "Name") ?? "New Project";
                isSaved = true; // Mark the project as saved after loading
                FillTree(); // Repopulate the tree view with the loaded project structure
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveProject();
        }

        private void menuProperties_Click(object sender, EventArgs e)
        {
            PropertiesPage propertiesPage = new();
            propertiesPage.ShowDialog();
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                text: "Do you want to save the current project before exiting?",
                caption: "Unsaved changes",
                buttons: MessageBoxButtons.YesNoCancel,
                icon: MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveProject(); // Save the current project
                    if (status == 1)
                    {
                        this.Close();
                        return;
                    }
                    else
                        return;
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not exit
                }
                else if (result == DialogResult.No)
                {
                    this.Close(); // Exit without saving
                }
            }
        }

        private void frmMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                text: "Do you want to save the current project before exiting?",
                caption: "Unsaved changes",
                buttons: MessageBoxButtons.YesNoCancel,
                icon: MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveProject(); // Save the current project
                    if (status == 0)
                        e.Cancel = true; // Cancel closing if save failed
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // User chose to cancel, do not close the form
                }
            }
        }

        private void frmMain_Activated(object sender, EventArgs e)
        {
            FillTree(); // Refresh the tree view when the form is activated
        }

        private void menuAddSurvey_Click(object sender, EventArgs e)
        {
            Survey addSurvey = new Survey(null);
            addSurvey.ShowDialog();
            FillTree(); // Refresh the tree view after adding a survey
        }

        private void menuAddModel_Click(object sender, EventArgs e)
        {
            Model addModel = new Model(null);
            addModel.ShowDialog();
            FillTree(); // Refresh the tree view after adding a model
        }

        private void menuAddSSCModel_Click(object sender, EventArgs e)
        {
            SSCModel addSSCModel = new SSCModel(null);
            addSSCModel.ShowDialog();
            FillTree(); // Refresh the tree view after adding a model
        }

        private void processPositionFileToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ViSea_Extern viSea_Extern = new();
            viSea_Extern.ShowDialog();
        }

        private void menuAboutUs_Click(object sender, EventArgs e)
        {
            _AboutUs aboutUs = new();
            aboutUs.ShowDialog();
        }

        private void treeProject_NodeMouseClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            if (e.Button == MouseButtons.Right)
            {
                treeProject.SelectedNode = e.Node;
                // Check type of associated XML node
                if (e.Node.Tag is XmlNode xmlNode)
                {
                    string? type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                    itemDelete.Visible = type != "Project"; // Disable delete for the root project node
                }
                cmenuNode.Show(treeProject, e.Location);
            }
        }

        private void treeProject_NodeMouseDoubleClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            TreeNode? selectedNode = treeProject.SelectedNode;
            if (selectedNode != null && selectedNode.Tag is XmlNode xmlNode)
            {
                string type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                string name = xmlNode.Attributes?["name"]?.Value ?? xmlNode.Name;

                switch (type)
                {
                    case "Project":
                        PropertiesPage propertiesPage = new();
                        propertiesPage.ShowDialog();
                        break;
                    case "Survey":
                        Survey editSurvey = new Survey(xmlNode);
                        editSurvey.ShowDialog();
                        break;
                    case "Model":
                        Model editModel = new Model(xmlNode);
                        editModel.ShowDialog();
                        break;
                    case "VesselMountedADCP":
                        VesselMountedADCP editVesselMountedADCP = new VesselMountedADCP(null, xmlNode);
                        editVesselMountedADCP.ShowDialog();
                        break;
                    case "WaterSample":
                        WaterSample editWaterSample = new WaterSample(null, xmlNode);
                        editWaterSample.ShowDialog();
                        break;
                    case "OBSVerticalProfile":
                        OBSVerticalProfile editOBSVerticalProfile = new OBSVerticalProfile(null, xmlNode);
                        editOBSVerticalProfile.ShowDialog();
                        break;
                    case "NTU2SSC":
                    case "BKS2SSC":
                        SSCModel editSSCModel = new SSCModel(xmlNode);
                        editSSCModel.ShowDialog();
                        break;
                }
            }
            FillTree(); // Refresh the tree view after double-clicking an item
        }

        private void itemOpen_Click(object sender, EventArgs e)
        {
            TreeNode? selectedNode = treeProject.SelectedNode;
            if (selectedNode != null && selectedNode.Tag is XmlNode xmlNode)
            {
                string type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                string name = xmlNode.Attributes?["name"]?.Value ?? xmlNode.Name;

                switch (type)
                {
                    case "Project":
                        PropertiesPage propertiesPage = new();
                        propertiesPage.ShowDialog();
                        break;
                    case "Survey":
                        Survey editSurvey = new Survey(xmlNode);
                        editSurvey.ShowDialog();
                        break;
                    case "Model":
                        Model editModel = new Model(xmlNode);
                        editModel.ShowDialog();
                        break;
                    case "VesselMountedADCP":
                        VesselMountedADCP editVesselMountedADCP = new VesselMountedADCP(null, xmlNode);
                        editVesselMountedADCP.ShowDialog();
                        break;
                    case "WaterSample":
                        WaterSample editWaterSample = new WaterSample(null, xmlNode);
                        editWaterSample.ShowDialog();
                        break;
                    case "OBSVerticalProfile":
                        OBSVerticalProfile editOBSVerticalProfile = new OBSVerticalProfile(null, xmlNode);
                        editOBSVerticalProfile.ShowDialog();
                        break;
                    case "NTU2SSC":
                    case "BKS2SSC":
                        SSCModel editSSCModel = new SSCModel(xmlNode);
                        editSSCModel.ShowDialog();
                        break;
                }
            }
            FillTree(); // Refresh the tree view after opening an item
        }

        private void itemPlot_Click(object sender, EventArgs e)
        {
            TreeNode? selectedNode = treeProject.SelectedNode;
            if (selectedNode != null && selectedNode.Tag is XmlNode xmlNode)
            {
                string type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                string name = xmlNode.Attributes?["name"]?.Value ?? xmlNode.Name;

                switch (type)
                {
                    case "Project":
                        MessageBox.Show($"Plotting project: {name}", "Open Project", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        break;
                    case "Survey":
                        MessageBox.Show($"Plotting survey: {name}", "Open Survey", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement survey opening logic here
                        break;
                    case "Model":
                        PlotModel plotModel = new PlotModel(xmlNode);
                        plotModel.ShowDialog();
                        break;
                    case "VesselMountedADCP":
                        MessageBox.Show($"Plotting vessel-mounted ADCP: {name}", "Open Vessel-Mounted ADCP", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement vessel-mounted ADCP opening logic here
                        break;
                    case "WaterSample":
                        MessageBox.Show($"Plotting water sample: {name}", "Open Water Sample", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement water sample opening logic here
                        break;
                    case "OBSVerticalProfile":
                        MessageBox.Show($"Plotting OBS vertical profile: {name}", "Open OBS Vertical Profile", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement OBS vertical profile opening logic here
                        break;
                    case "NTU2SSC":
                    case "BKS2SSC":
                        MessageBox.Show($"Plotting SSC model: {name}", "Open SSC Model", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        break;
                }
            }
        }

        private void itemDelete_Click(object sender, EventArgs e)
        {
            TreeNode? selectedNode = treeProject.SelectedNode;
            if (selectedNode != null && selectedNode.Tag is XmlNode xmlNode)
            {
                string type = xmlNode.Attributes?["type"]?.Value ?? string.Empty;
                string name = xmlNode.Attributes?["name"]?.Value ?? xmlNode.Name;
                string id = xmlNode.Attributes?["id"]?.Value ?? string.Empty;

                switch (type)
                {
                    case "Survey":
                        DialogResult resultSurvey = MessageBox.Show($"Are you sure you want to delete the survey: {name}?", "Delete Survey", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultSurvey == DialogResult.Yes)
                        {
                            _project.DeleteNode(type: "Survey", id: id);
                        }
                        break;
                    case "Model":
                        DialogResult resultMode = MessageBox.Show($"Are you sure you want to delete the model: {name}?", "Delete Model", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultMode == DialogResult.Yes)
                        {
                            _project.DeleteNode(type: "Model", id: id);
                        }
                        break;
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
                    case "NTU2SSC":
                        DialogResult resultSSCModel = MessageBox.Show($"Are you sure you want to delete the NTU to SSC model: {name}?", "Delete SSC Model", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultSSCModel == DialogResult.Yes)
                        {
                            _project.DeleteNode(type: "NTU2SSC", id: id);
                        }
                        break;
                    case "BKS2SSC":
                        DialogResult resultBKS2SSC = MessageBox.Show($"Are you sure you want to delete the BKS to SSC model: {name}?", "Delete SSC Model", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultBKS2SSC == DialogResult.Yes)
                        {
                            _project.DeleteNode(type: "BKS2SSC", id: id);
                        }
                        break;
                }
            }
            isSaved = false; // Mark the project as unsaved after deletion
            FillTree();
        }

        private int SaveProject()
        {
            string oldtName = _project.GetSetting(settingName: "Name");
            string oldPath = _project.GetProjectPath();
            string currentName = txtName.Text.Trim();
            if (string.IsNullOrEmpty(txtName.Text.Trim()))
            {
                MessageBox.Show("Project name cannot be empty. Please enter a valid project name.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0; // Indicate failure
            }
            _project.SetSetting(settingName: "Name", value: currentName);
            string projectPath = _project.GetProjectPath();
            if (projectPath == "0")
            {
                MessageBox.Show("Project directory is not set. Please set the project directory first.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            if (!_project.isSaved)
            {
                if (File.Exists(projectPath))
                {
                    DialogResult result = MessageBox.Show(
                        text: "Project already exists. Do you want to overwrite it?",
                        caption: "Overwrite Project",
                        buttons: MessageBoxButtons.YesNo,
                        icon: MessageBoxIcon.Warning);
                    if (result == DialogResult.No)
                    {
                        return 0; // User chose not to overwrite
                    }
                }
                try
                {
                    _project.SaveConfig(saveMode: 1); // Save the project configuration
                    isSaved = true; // Mark the project as saved
                    FillTree(); // Refresh the tree view after saving
                    return 1; // Indicate success
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error saving project: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return 0; // Indicate failure
                }
            }
            else
            {
                if (oldtName != currentName)
                {
                    if (File.Exists(oldPath))
                    {
                        File.Delete(oldPath); // Delete the old project file if it exists
                    }
                    try
                    {
                        _project.SaveConfig(saveMode: 1); // Save the project configuration with the new name
                        isSaved = true; // Mark the project as saved
                        FillTree(); // Refresh the tree view after saving
                        return 1; // Indicate success
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Error saving project: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return 0; // Indicate failure
                    }
                }
                else
                {
                    try
                    {
                        _project.SaveConfig(saveMode: 0); // Save the project configuration without changing the name
                        isSaved = true; // Mark the project as saved
                        FillTree(); // Refresh the tree view after saving
                        return 1; // Indicate success
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Error saving project: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return 0; // Indicate failure
                    }
                }
            }
        }

        private void __PlumeTrack_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Control && e.KeyCode == Keys.S) // Ctrl + S
            {
                e.SuppressKeyPress = true; // Prevent default behavior
                SaveProject(); // Save the project
            }
            else if (e.Control && e.KeyCode == Keys.N) // Ctrl + N
            {
                e.SuppressKeyPress = true; // Prevent default behavior
                menuNew_Click(sender, e); // Create a new project
            }
            else if (e.Control && e.KeyCode == Keys.O) // Ctrl + O
            {
                e.SuppressKeyPress = true; // Prevent default behavior
                menuOpen_Click(sender, e); // Open an existing project
            }
        }
    }
}
