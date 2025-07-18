using Microsoft.VisualBasic;
using System.Xml;


namespace CSEMMPGUI_v1
{
    public partial class frmMain : Form
    {
        TreeNode currentNode;
        XmlDocument project;

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

        


        public frmMain()
        {
            InitializeComponent();
            
        }


        private void menuLoad_Click(object sender, EventArgs e)
        {
            FileDialog loadProject = new OpenFileDialog();
            loadProject.Filter = "MT Project Files (*.mtproj)|*.mtproj|All Files (*.*)|*.*";
            if (loadProject.ShowDialog() == DialogResult.OK)
            {
                string fileName = loadProject.FileName;
                try
                {
                    // Load the project file
                    project.Load(fileName);
                    treeProject.Nodes.Clear();
                    XmlNode root = project.DocumentElement;
                    if (root.Attributes?["type"] != null)
                    {
                        TreeNode rootNode = new TreeNode(root.Attributes["name"]?.Value ?? root.Name);
                        rootNode.Tag = root;
                        treeProject.Nodes.Add(rootNode);
                        AddChildNodes(root, rootNode);
                        treeProject.ExpandAll();
                    }

                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error loading project: " + ex.Message);
                }
            }
        }

        private void menuProperties_Click(object sender, EventArgs e)
        {
            PropertiesPage propertiesPage = new PropertiesPage(project);
            var result = propertiesPage.ShowDialog();
            string projectDir = propertiesPage.projectDir;
            string projectName = propertiesPage.projectName;
            string projectEPSG = propertiesPage.projectEPSG;
            using (XmlWriter writer = XmlWriter.Create("Test.xml"))
            {
                writer.WriteStartDocument();
                writer.WriteStartElement("Project");
                writer.WriteElementString("Name", projectName);
                writer.WriteElementString("Directory", projectDir);
                writer.WriteElementString("EPSG", projectEPSG);
                writer.WriteEndElement();
                writer.WriteEndDocument();
            }

        }


        private void menuAddModel_Click(object sender, EventArgs e)
        {
            AddModel addModel = new AddModel(project);
            var result = addModel.ShowDialog();

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
                        PropertiesPage propertiesPage = new PropertiesPage(project);
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
                        MessageBox.Show("Opening Model Window for: " + name);
                        break;
                }
            }
        }

        private void itemDelete_Click(object sender, EventArgs e)
        {
            if (currentNode != null)
            {
                // Open the selected node
                string nodeName = currentNode.Text;
                MessageBox.Show("Deleting: " + nodeName);
                // Here you would add code to open the specific item, e.g., a model or a file.
            }
        }

        private void treeProject_NodeMouseDoubleClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            currentNode = e.Node;
            
        }
    }
}
