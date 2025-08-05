using DHI.Mike1D.ResultDataAccess;
using Microsoft.VisualBasic;
using System.Xml;
using Python.Runtime;


namespace CSEMMPGUI_v1
{
    public partial class __PlumeTrack : Form
    {
        TreeNode? currentNode;
        public bool isSaved; // Track if project has been saved
        int saveMode;
        public __PlumeTrack()
        {
            InitializeComponent();
            _ClassConfigurationManager.InitializeProject(name: txtName.Text);
            isSaved = false;
            saveMode = 0;
            FillTree(); // Populate the tree view with project structure
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
                    Save(); // Save the project
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not create a new project
                }
            }
            _ClassConfigurationManager.InitializeProject(name: "New Project");
            txtName.Text = "New Project"; // Reset the project name
            FillTree(); // Clear and repopulate the tree view
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
                    Save(); // Save the current project
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
                InitialDirectory = _ClassConfigurationManager.GetSetting(settingName: "Directory")
            };
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                string filePath = ofd.FileName;
                _ClassConfigurationManager.LoadConfig(filePath);
                txtName.Text = _ClassConfigurationManager.GetSetting(settingName: "Name") ?? "Project";
                FillTree(); // Repopulate the tree view with the loaded project structure
            }
            isSaved = true; // Reset the saved state after loading a project

        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            Save();
            isSaved = true; // Mark the project as saved after saving
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
                    Save(); // Save the current project
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not exit
                }
            }

        }

        private void menuAddSurvey_Click(object sender, EventArgs e)
        {
            AddSurvey addSurvey = new();
            addSurvey.ShowDialog();
            FillTree(); // Refresh the tree view after adding a survey
        }

        private void menuAddModel_Click(object sender, EventArgs e)
        {
            AddModel addModel = new();
            addModel.ShowDialog();
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

        private void txtName_Leave(object sender, EventArgs e)
        {
            string? currentName = _ClassConfigurationManager.GetSetting(settingName: "Name");
            if (string.IsNullOrEmpty(txtName.Text.Trim()))
            {
                MessageBox.Show("Project name cannot be empty.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                txtName.Text = currentName ?? "Project";
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
                    Save(); // Save the current project
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // User chose to cancel, do not close the form
                }
            }
        }

        private void Save()
        {
            string? currentPath = _ClassConfigurationManager.GetProjectPath();
            string? projectDir = _ClassConfigurationManager.GetSetting(settingName: "Directory");
            if (!string.IsNullOrEmpty(currentPath))
            {
                string newPath = Path.Combine(projectDir, $"{txtName.Text.Trim()}.mtproj");
                MessageBox.Show(currentPath);
                if (File.Exists(currentPath))
                {
                    File.Move(currentPath, newPath);
                }
            }
            _ClassConfigurationManager.SetSetting("Name", txtName.Text.Trim());
            _ClassConfigurationManager.SaveConfig(saveMode);
            isSaved = true; // Mark the project as saved after saving
            saveMode++;
        }

        private void FillTree()
        {
            treeProject.Nodes.Clear();
            XmlNode? root = _Globals.Config.DocumentElement;
            string name = _ClassConfigurationManager.GetSetting(settingName: "Name");
            if (root.Attributes?["type"] != null)
            {
                TreeNode rootNode = new TreeNode(name);
                rootNode.Tag = root;
                treeProject.Nodes.Add(rootNode);
                AddChildNodes(root, rootNode); // Recursively add child nodes
                treeProject.ExpandAll(); // Expand all nodes for better visibility
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
                        MessageBox.Show($"Opening survey: {name}", "Open Survey", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement survey opening logic here
                        break;
                    case "Model":
                        EditModel editModel = new EditModel(xmlNode);
                        editModel.ShowDialog();
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

        private void itemDelete_Click(object sender, EventArgs e)
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
                        MessageBox.Show($"Opening survey: {name}", "Open Survey", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement survey opening logic here
                        break;
                    case "Model":
                        MessageBox.Show($"Opening model: {name}", "Open Model", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement model opening logic here
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
                        MessageBox.Show($"Opening survey: {name}", "Open Survey", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement survey opening logic here
                        break;
                    case "Model":
                        EditModel editModel = new EditModel(xmlNode);
                        editModel.ShowDialog();
                        break;
                    case "VesselMountedADCP":
                        EditVesselMountedADCP editVesselMountedADCP = new EditVesselMountedADCP(xmlNode);
                        editVesselMountedADCP.ShowDialog();
                        break;
                    case "WaterSample":
                        MessageBox.Show($"Opening water sample: {name}", "Open Water Sample", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement water sample opening logic here
                        break;
                }
            }
        }

        private void frmMain_Activated(object sender, EventArgs e)
        {
            FillTree(); // Refresh the tree view when the form is activated
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
                        MessageBox.Show($"Opening project: {name}", "Open Project", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        break;
                    case "Survey":
                        MessageBox.Show($"Opening survey: {name}", "Open Survey", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement survey opening logic here
                        break;
                    case "Model":
                        PlotModel plotModel = new PlotModel(xmlNode);
                        plotModel.ShowDialog();
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
    }
}
