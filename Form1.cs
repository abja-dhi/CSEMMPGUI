using Microsoft.VisualBasic;
using System.Xml;


namespace CSEMMPGUI_v1
{
    public partial class frmMain : Form
    {

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
                    XmlDocument doc = new XmlDocument();
                    doc.Load(fileName);
                    treeProject.Nodes.Clear();
                    XmlNode root = doc.DocumentElement;
                    TreeNode rootNode = new TreeNode(root.Name);
                    treeProject.Nodes.Add(rootNode);
                    AddChildNodes(root, rootNode);
                    treeProject.ExpandAll();
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error loading project: " + ex.Message);
                }
            }
        }

        private void menuProperties_Click(object sender, EventArgs e)
        {
            PropertiesPage propertiesPage = new PropertiesPage();
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


        // Helper Functions
        private void AddChildNodes(XmlNode xmlNode, TreeNode treeNode)
        {
            foreach (XmlNode child in xmlNode.ChildNodes)
            {
                if (child.NodeType == XmlNodeType.Element)
                {
                    TreeNode childNode = new TreeNode(child.Name);
                    treeNode.Nodes.Add(childNode);
                    AddChildNodes(child, childNode);
                }
            }
        }

        private void menuAddModel_Click(object sender, EventArgs e)
        {
            AddModel addModel = new AddModel();
            var result = addModel.ShowDialog();

        }
    }
}
