using DHI.Mike1D.ResultDataAccess;
using Microsoft.VisualBasic;
using System.Xml;
using Python.Runtime;


namespace CSEMMPGUI_v1
{
    public partial class frmMain : Form
    {
        TreeNode currentNode;

        private void FillTree()
        {
            treeProject.Nodes.Clear();
            XmlNode root = ConfigData.Config.DocumentElement;
            string name = root.SelectSingleNode("Settings/Name")?.InnerText ?? "Project";
            if (root.Attributes?["type"] != null)
            {
                TreeNode rootNode = new TreeNode(name);
                rootNode.Tag = root;
                treeProject.Nodes.Add(rootNode);
                AddChildNodes(root, rootNode);
                treeProject.ExpandAll();
            }
        }

        // Helper Functions
        private void AddChildNodes(XmlNode xmlNode, TreeNode treeNode)
        {
            foreach (XmlNode child in xmlNode.ChildNodes)
            {
                // Skip non-elements and <Settings>
                if (child.NodeType != XmlNodeType.Element || child.Name == "Settings")
                    continue;

                XmlAttribute typeAttr = child.Attributes?["type"];
                if (typeAttr != null)
                {
                    string displayName = child.Attributes?["name"]?.Value ?? child.Name;
                    TreeNode childNode = new TreeNode(displayName);
                    childNode.Tag = child;
                    treeNode.Nodes.Add(childNode);
                    AddChildNodes(child, childNode);
                }
            }
        }

        private int Save()
        {
            if (ConfigData.IsModified)
            {
                DialogResult results = MessageBox.Show(
                    "Do want to save the current project?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel);
                if (results == DialogResult.Yes)
                {
                    string path = ConfigData.GetProjectPath();
                    if (string.IsNullOrEmpty(path) || !File.Exists(path))
                    {
                        using SaveFileDialog sfd = new SaveFileDialog
                        {
                            Filter = "MT Project Files (*.mtproj)|*.mtproj",
                            Title = "Save Project",
                            InitialDirectory = ConfigData.GetProjectDir()
                        };
                        if (sfd.ShowDialog() == DialogResult.OK)
                        {
                            path = sfd.FileName;
                            if (!Path.GetExtension(path).Equals(".mtproj", StringComparison.OrdinalIgnoreCase))
                            {
                                path += ".mtproj";
                            }
                            ConfigData.SetProjectPath(path);
                        }
                        else
                        {
                            return 0; // User cancelled, do not proceed
                        }
                    }
                    ConfigData.Config.Save(path);
                    return 1; // Save successful
                }
                else if (results == DialogResult.No)
                {
                    return 1; // User chose not to save, proceed without saving
                }
                else
                {
                    return 0; // User cancelled, do not proceed
                }
            }
            else
            {
                return 1; // No changes to save, proceed without saving
            }
        }


        private int SaveAs()
        {
            string path = "";
            if (ConfigData.IsModified)
            {
                using SaveFileDialog sfd = new SaveFileDialog
                {
                    Filter = "MT Project Files (*.mtproj)|*.mtproj",
                    Title = "Save Project",
                    InitialDirectory = ConfigData.GetProjectDir()
                };
                if (sfd.ShowDialog() == DialogResult.OK)
                {
                    path = sfd.FileName;
                    ConfigData.SetProjectPath(path);
                }
                else
                {
                    return 0; // User cancelled, do not proceed
                }
            }
            ConfigData.Config.Save(path);
            return 1; // Save successful
        }

        public static void DeleteModel(string modelName)
        {
            XmlNode root = ConfigData.Config.DocumentElement;

            XmlNode modelToDelete = root.SelectNodes("Model")
                .Cast<XmlNode>()
                .FirstOrDefault(m =>
                    string.Equals(m.Attributes?["name"]?.Value?.Trim(), modelName, StringComparison.OrdinalIgnoreCase));

            if (modelToDelete != null)
            {
                root.RemoveChild(modelToDelete);
            }
        }

        public frmMain()
        {
            string pythonDll = @"C:\Program Files\Python311\python311.dll";
            Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", pythonDll);
            PythonEngine.Initialize();
            InitializeComponent();
            ConfigData.InitializeProject();
            
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            int result = Save();
            if (result == 0)
            {
                return; // User cancelled or an error occurred
            }
            ConfigData.InitializeProject();
            FillTree();
        }

        private void menuOpen_Click(object sender, EventArgs e)
        {
            int result = Save();
            if (result == 0)
            {
                return; // User cancelled or an error occurred
            }
            FileDialog loadProject = new OpenFileDialog();
            loadProject.Filter = "MT Project Files (*.mtproj)|*.mtproj|All Files (*.*)|*.*";
            if (loadProject.ShowDialog() == DialogResult.OK)
            {
                string fileName = loadProject.FileName;
                try
                {

                    // Load the project file
                    ConfigData.Config.Load(fileName);
                    FillTree();

                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error loading project: " + ex.Message);
                }
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            string path = ConfigData.GetProjectPath();
            if (string.IsNullOrEmpty(path) || !File.Exists(path))
            {
                using SaveFileDialog sfd = new SaveFileDialog
                {
                    Filter = "MT Project Files (*.mtproj)|*.mtproj",
                    Title = "Save Project",
                    InitialDirectory = ConfigData.GetProjectDir()
                };
                if (sfd.ShowDialog() == DialogResult.OK)
                {
                    path = sfd.FileName;
                    if (!Path.GetExtension(path).Equals(".mtproj", StringComparison.OrdinalIgnoreCase))
                    {
                        path += ".mtproj";
                    }
                    ConfigData.SetProjectPath(path);
                }
                else
                {
                    return; // User cancelled, do not proceed
                }
            }
            ConfigData.Config.Save(path);
        }

        private void menuSaveAs_Click(object sender, EventArgs e)
        {
            int result = SaveAs();
        }

        private void menuProperties_Click(object sender, EventArgs e)
        {
            PropertiesPage propertiesPage = new PropertiesPage();
            var result = propertiesPage.ShowDialog();
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            int result = 1;
            MessageBox.Show("Exiting the application.");
        }

        private void treeProject_NodeMouseClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            if (e.Button == MouseButtons.Right)
            {
                treeProject.SelectedNode = e.Node;
                currentNode = e.Node;
                cmenuNode.Show(treeProject, e.Location);
            }
        }

        private void itemOpen_Click(object sender, EventArgs e)
        {
            if (currentNode?.Tag is XmlNode xml)
            {
                string type = xml.Attributes["type"]?.Value;
                string name = xml.Attributes["name"]?.Value ?? xml.Name;

                // Use switch for type-specific windows
                switch (type)
                {
                    case "Project":
                        PropertiesPage propertiesPage = new PropertiesPage();
                        propertiesPage.ShowDialog();
                        break;
                    case "Survey":
                        // OpenSurveyWindow(xml);
                        MessageBox.Show("Opening Survey Window for: " + name);
                        break;
                    case "ADCP":
                        // OpenAdcpWindow(xml);
                        MessageBox.Show("Opening ADCP Window for: " + name);
                        break;
                    case "Model":
                        // OpenModelWindow(xml);
                        EditModel editModel = new EditModel(name);
                        editModel.ShowDialog();
                        break;
                }
            }
        }

        private void itemDelete_Click(object sender, EventArgs e)
        {
            if (currentNode?.Tag is XmlNode xml)
            {
                string type = xml.Attributes["type"]?.Value;
                string name = xml.Attributes["name"]?.Value ?? xml.Name;

                // Use switch for type-specific windows
                switch (type)
                {
                    case "Project":
                        PropertiesPage propertiesPage = new PropertiesPage();
                        propertiesPage.ShowDialog();
                        break;
                    case "Survey":
                        // OpenSurveyWindow(xml);
                        MessageBox.Show("Opening Survey Window for: " + name);
                        break;
                    case "ADCP":
                        // OpenAdcpWindow(xml);
                        MessageBox.Show("Opening ADCP Window for: " + name);
                        break;
                    case "Model":
                        // OpenModelWindow(xml);
                        DeleteModel(name);
                        break;
                }
                FillTree();
            }
        }

        private void treeProject_NodeMouseDoubleClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            currentNode = e.Node;
            if (e.Node != null)
            {
                treeProject.SelectedNode = e.Node;
                currentNode = e.Node;
                itemOpen_Click(sender, EventArgs.Empty); // Reuse the existing Open logic
            }
        }

        private void menuAddSurvey_Click(object sender, EventArgs e)
        {
            AddSurvey addSurvey = new AddSurvey();
            var result = addSurvey.ShowDialog();
        }

        private void menuAddModel_Click(object sender, EventArgs e)
        {
            AddModel addModel = new AddModel();
            var result = addModel.ShowDialog();
            FillTree();
        }

        private void frmMain_FormClosing(object sender, FormClosingEventArgs e)
        {

        }

        private void frmMain_Activated(object sender, EventArgs e)
        {
            FillTree();
        }

        private void menuAboutUs_Click(object sender, EventArgs e)
        {
            AboutUs aboutUs = new AboutUs();
            aboutUs.ShowDialog();
        }
    }
}
