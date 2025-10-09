using DHI.Mike1D.ResultDataAccess;
using DHI.Mike1D.ResultDataAccess.Epanet;
using Microsoft.VisualBasic;
using Microsoft.Web.WebView2.WinForms;
using Microsoft.Web.WebView2.Wpf;
using Python.Runtime;
using System.Xml;
using System.Xml.Linq;


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
                if (child.NodeType != XmlNodeType.Element || child.Name == "Settings" || child.Name == "MapSettings")
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
            TreeNode rootNode = new TreeNode(name);
            rootNode.Tag = root;
            treeProject.Nodes.Add(rootNode);
            AddChildNodes(root, rootNode); // Recursively add child nodes
            treeProject.ExpandAll(); // Expand all nodes for better visibility
        }

        private void InitializeProject()
        {
            _project.InitializeProject();
            isSaved = true;
            FillTree(); // Populate the tree view with project structure
        }

        public __PlumeTrack(string[] args)
        {
            InitializeComponent();
            if (args.Length > 0)
            {
                string projectFilePath = args[0];
                if (File.Exists(projectFilePath) && Path.GetExtension(projectFilePath).Equals(".mtproj", StringComparison.OrdinalIgnoreCase))
                {
                    _project.LoadConfig(projectFilePath);
                    isSaved = true; // Mark the project as saved after loading
                    FillTree(); // Populate the tree view with the loaded project structure
                }
                else
                {
                    MessageBox.Show("The specified project file does not exist or is not a valid .mtproj file. A new project will be created.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    InitializeProject();
                }
            }
            else
                InitializeProject();

            this.KeyPreview = true; // Enable form to capture key events
            this.KeyDown += __PlumeTrack_KeyDown; // Attach key down event handler

            this.Load += async (s, e) =>
            {
                await webView.EnsureCoreWebView2Async();
                webView.Source = new Uri(Path.Combine(_Globals.basePath, "load_data_message.html"));
            };
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            if (!_Globals.isSaved || !isSaved) // If project has changed
            {
                // Show a message box to ask the user if they want to save changes
                DialogResult result = MessageBox.Show(
                "Do you want to save the current project before creating a new project?",
                "Unsaved Changes",
                MessageBoxButtons.YesNoCancel,
                MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveProject(); // Save the project
                    if (status == 1)
                    {
                        InitializeProject(); // Initialize a new project if save was successful
                        _Globals.isSaved = false;
                    }
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
                    _Globals.isSaved = false;
                }
            }
            else
            {
                InitializeProject(); // Initialize a new project if no unsaved changes
                _Globals.isSaved = false;
            }

        }

        private void menuOpen_Click(object sender, EventArgs e)
        {
            if (!_Globals.isSaved || !isSaved) // If project has changed
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
                isSaved = true; // Mark the project as saved after loading
                FillTree(); // Repopulate the tree view with the loaded project structure
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveProject();
        }

        private void menuSaveAs_Click(object sender, EventArgs e)
        {
            _Globals.isSaved = false; // Force Save As dialog
            SaveProject();
        }

        private void menuProperties_Click(object sender, EventArgs e)
        {
            PropertiesPage propertiesPage = new();
            propertiesPage.ShowDialog();
        }

        private void menuMapOptions_Click(object sender, EventArgs e)
        {
            MapOptions mapOptions = new();
            mapOptions.ShowDialog();
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!_Globals.isSaved || !isSaved)
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
                        Application.Exit();
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
                    Application.Exit(); // Exit without saving
                }
            }
        }

        private void frmMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!_Globals.isSaved || !isSaved)
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

        private void menuAddHDModel_Click(object sender, EventArgs e)
        {
            ModelHD addHDModel = new ModelHD(null);
            addHDModel.ShowDialog();
            FillTree(); // Refresh the tree view after adding a model
        }

        private void menuAddMTModel_Click(object sender, EventArgs e)
        {
            ModelMT addMTModel = new ModelMT(null);
            addMTModel.ShowDialog();
            FillTree(); // Refresh the tree view after adding a model
        }

        private void menuAddSSCModel_Click(object sender, EventArgs e)
        {
            SSCModel addSSCModel = new SSCModel(null);
            addSSCModel.ShowDialog();
            FillTree(); // Refresh the tree view after adding a model
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

                    if (type == "NTU2SSC" || type == "BKS2SSC" || type == "BKS2NTU")
                    {
                        XmlNode? modeNode = xmlNode.SelectSingleNode("Mode");
                        string mode = modeNode?.InnerText ?? string.Empty;

                        itemPlot.Visible = mode != "Manual";

                    }
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
                    case "HDModel":
                        ModelHD editHDModel = new ModelHD(xmlNode);
                        editHDModel.ShowDialog();
                        break;
                    case "MTDModel":
                        ModelMT editMTModel = new ModelMT(xmlNode);
                        editMTModel.ShowDialog();
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
                    case "BKS2NTU":
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
                    case "HDModel":
                        ModelHD editHDModel = new ModelHD(xmlNode);
                        editHDModel.ShowDialog();
                        break;
                    case "MTDModel":
                        ModelMT editMTModel = new ModelMT(xmlNode);
                        editMTModel.ShowDialog();
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
                    case "BKS2NTU":
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
                string id = xmlNode.Attributes?["id"]?.Value ?? string.Empty;


                switch (type)
                {
                    case "Project":
                        ProjectPlot projectPlot = new ProjectPlot();
                        projectPlot.Show();
                        break;
                    case "Survey":
                        MessageBox.Show($"Plotting survey: {name}", "Open Survey", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        // Implement survey opening logic here
                        break;
                    case "HDModel":
                        ModelHDPlot modelHDPlot = new ModelHDPlot(id);
                        modelHDPlot.Show();
                        break;
                    case "MTModel":
                        ModelMTPlot modelMTPlot = new ModelMTPlot(id);
                        modelMTPlot.Show();
                        break;
                    case "VesselMountedADCP":
                        VesselMountedADCPPlot vesselMountedADCPPlot = new VesselMountedADCPPlot(id);
                        vesselMountedADCPPlot.Show();
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
                        SSCModelPlot sscModelPlot = new SSCModelPlot(id, "NTU2SSC");
                        sscModelPlot.Show();
                        break;
                    case "BKS2SSC":
                        SSCModelPlot bks2sscModelPlot = new SSCModelPlot(id, "BKS2SSC");
                        bks2sscModelPlot.Show();
                        break;
                    case "BKS2NTU":
                        SSCModelPlot sSCModelPlot = new SSCModelPlot(id, "BKS2NTU");
                        sSCModelPlot.Show();
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
                        DialogResult resultNTU2SSCModel = MessageBox.Show($"Are you sure you want to delete the NTU to SSC model: {name}?", "Delete NTU to SSC Model", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultNTU2SSCModel == DialogResult.Yes)
                        {
                            _project.DeleteNode(type: "NTU2SSC", id: id);
                        }
                        break;
                    case "BKS2SSC":
                        DialogResult resultBKS2SSCModel = MessageBox.Show($"Are you sure you want to delete the Absolute Backscatter to SSC model: {name}?", "Delete Absolute Backscatter to SSC Model", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultBKS2SSCModel == DialogResult.Yes)
                        {
                            _project.DeleteNode(type: "BKS2SSC", id: id);
                        }
                        break;
                    case "BKS2NTU":
                        DialogResult resultBKS2NTUModel = MessageBox.Show($"Are you sure you want to delete the Absolute Backscatter to NTU model: {name}?", "Delete Absolute Backscatter to NTU Model", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        if (resultBKS2NTUModel == DialogResult.Yes)
                        {
                            _project.DeleteNode(type: "BKS2NTU", id: id);
                        }
                        break;
                }
            }
            isSaved = false; // Mark the project as unsaved after deletion
            FillTree();
        }

        private int SaveProject()
        {
            if (!_Globals.isSaved)
            {
                string directory = _project.GetSetting(settingName: "Directory");
                if (directory == Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData))
                    directory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
                SaveFileDialog sfd = new SaveFileDialog
                {
                    Filter = "MT Project Files (*.mtproj)|*.mtproj",
                    Title = "Save Project",
                    InitialDirectory = directory,
                    FileName = _project.GetSetting(settingName: "Name") + ".mtproj",
                    OverwritePrompt = true
                };
                if (sfd.ShowDialog() == DialogResult.OK)
                {
                    string fileNameWithoutExtension = Path.GetFileNameWithoutExtension(sfd.FileName);
                    string selectedDirectory = Path.GetDirectoryName(sfd.FileName);
                    _project.SetSetting(settingName: "Name", value: fileNameWithoutExtension);
                    _project.SetSetting(settingName: "Directory", value: selectedDirectory);
                    _project.SaveConfig(saveMode: 1); // Save the project configuration with the new name and directory
                    _Globals.isSaved = true;
                    return 1;
                }
                else if (sfd.ShowDialog() == DialogResult.Cancel)
                {
                    return 0; // Indicate cancellation
                }
            }
            else
            {
                _project.SaveConfig(saveMode: 1); // Save the project configuration
                isSaved = true;
                return 1; // Indicate success    
            }
            return 1;
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

        private void map2D_CheckedChanged(object sender, EventArgs e)
        {
            string name = _project.GetSetting("Name");
            string mapViewer2DPath = Path.Combine(_Globals.dataPath, "PlumeTrack", $"MapViewer2D_{name}.html");
            string mapViewer3DPath = Path.Combine(_Globals.dataPath, "PlumeTrack", $"MapViewer3D_{name}.html");
            if (map2D.Checked)
            {
                if (File.Exists(mapViewer2DPath))
                {
                    webView.Source = new Uri(mapViewer2DPath);
                    return;
                }
                Dictionary<string, string> inputs2D = new Dictionary<string, string>
                {
                    { "Task", "MapViewer2D" },
                    { "Project", _Globals.Config.OuterXml.ToString() },
                };
                string xmlInput2D = _Tools.GenerateInput(inputs2D);
                XmlDocument result2D = _Tools.CallPython(xmlInput2D);
                Dictionary<string, string> outputs2D = _Tools.ParseOutput(result2D);
                if (outputs2D.ContainsKey("Error"))
                {
                    MessageBox.Show(outputs2D["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                webView.Source = new Uri(outputs2D["Result"]);
            }
            else if (map3D.Checked)
            {
                if (File.Exists(mapViewer3DPath))
                {
                    webView.Source = new Uri(mapViewer3DPath);
                    return;
                }
                Dictionary<string, string> inputs3D = new Dictionary<string, string>
                {
                    { "Task", "MapViewer3D" },
                    { "Project", _Globals.Config.OuterXml.ToString() },
                };
                string xmlInput3D = _Tools.GenerateInput(inputs3D);
                XmlDocument result3D = _Tools.CallPython(xmlInput3D);
                Dictionary<string, string> outputs3D = _Tools.ParseOutput(result3D);
                if (outputs3D.ContainsKey("Error"))
                {
                    MessageBox.Show(outputs3D["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                webView.Source = new Uri(outputs3D["Result"]);
            }

        }

        private void map2D_Click(object sender, EventArgs e)
        {
            string name = _project.GetSetting("Name");
            string mapViewer2DPath = Path.Combine(_Globals.dataPath, "PlumeTrack", $"MapViewer2D_{name}.html");
            string mapViewer3DPath = Path.Combine(_Globals.dataPath, "PlumeTrack", $"MapViewer3D_{name}.html");
            if (File.Exists(mapViewer2DPath))
            {
                webView.Source = new Uri(mapViewer2DPath);
                return;
            }
            Dictionary<string, string> inputs2D = new Dictionary<string, string>
                {
                    { "Task", "MapViewer2D" },
                    { "Project", _Globals.Config.OuterXml.ToString() },
                };
            string xmlInput2D = _Tools.GenerateInput(inputs2D);
            XmlDocument result2D = _Tools.CallPython(xmlInput2D);
            Dictionary<string, string> outputs2D = _Tools.ParseOutput(result2D);
            if (outputs2D.ContainsKey("Error"))
            {
                MessageBox.Show(outputs2D["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            webView.Source = new Uri(outputs2D["Result"]);
        }

        private void map3D_Click(object sender, EventArgs e)
        {
            string name = _project.GetSetting("Name");
            string mapViewer2DPath = Path.Combine(_Globals.dataPath, "PlumeTrack", $"MapViewer2D_{name}.html");
            string mapViewer3DPath = Path.Combine(_Globals.dataPath, "PlumeTrack", $"MapViewer3D_{name}.html");
            if (File.Exists(mapViewer3DPath))
            {
                webView.Source = new Uri(mapViewer3DPath);
                return;
            }
            Dictionary<string, string> inputs3D = new Dictionary<string, string>
                {
                    { "Task", "MapViewer3D" },
                    { "Project", _Globals.Config.OuterXml.ToString() },
                };
            string xmlInput3D = _Tools.GenerateInput(inputs3D);
            XmlDocument result3D = _Tools.CallPython(xmlInput3D);
            Dictionary<string, string> outputs3D = _Tools.ParseOutput(result3D);
            if (outputs3D.ContainsKey("Error"))
            {
                MessageBox.Show(outputs3D["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            webView.Source = new Uri(outputs3D["Result"]);
        }
    }
}
