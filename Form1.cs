using DHI.Mike1D.ResultDataAccess;
using Microsoft.VisualBasic;
using System.Xml;
using Python.Runtime;


namespace CSEMMPGUI_v1
{
    public partial class frmMain : Form
    {
        TreeNode? currentNode;
        public bool isSaved = true; // Track if project has been saved

        public frmMain()
        {
            InitializeComponent();
            ConfigurationManager.InitializeProject(name: txtName.Text);
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
            ConfigurationManager.InitializeProject(name: "Project");
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
                InitialDirectory = ConfigurationManager.GetSetting(settingName: "Directory")
            };
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                string filePath = ofd.FileName;
                ConfigurationManager.LoadConfig(filePath);
                txtName.Text = ConfigurationManager.GetSetting(settingName: "Name") ?? "Project";
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
        }

        private void menuAddModel_Click(object sender, EventArgs e)
        {
            AddModel addModel = new();
            addModel.ShowDialog();
        }

        private void processPositionFileToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ViSea_Extern viSea_Extern = new();
            viSea_Extern.ShowDialog();
        }

        private void menuAboutUs_Click(object sender, EventArgs e)
        {
            AboutUs aboutUs = new();
            aboutUs.ShowDialog();
        }

        private void txtName_Leave(object sender, EventArgs e)
        {
            string? currentName = ConfigurationManager.GetSetting(settingName: "Name");
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
            string? currentPath = ConfigurationManager.GetProjectPath();
            if (!string.IsNullOrEmpty(currentPath))
            {
                string newPath = Path.Combine(currentPath, $"{txtName.Text.Trim()}.mtproj");
                if (File.Exists(currentPath))
                {
                    File.Move(currentPath, newPath);
                }
            }
            ConfigurationManager.SetSetting("Name", txtName.Text.Trim());
            ConfigurationManager.SaveConfig();
            isSaved = true; // Mark the project as saved after saving
        }

        
    }
}
