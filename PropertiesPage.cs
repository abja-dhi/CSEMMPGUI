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
    public partial class PropertiesPage : Form
    {
        private bool isSaved = false;
        private void PopulateFields()
        {
            XmlNode settings = ConfigData.GetSettings();
            txtProjectName.Text = settings.SelectSingleNode("Name")?.InnerText ?? string.Empty;
            txtProjectDir.Text = settings.SelectSingleNode("Directory")?.InnerText ?? string.Empty;
            txtProjectEPSG.Text = settings.SelectSingleNode("EPSG")?.InnerText ?? string.Empty;
            txtProjectDescription.Text = settings.SelectSingleNode("Description")?.InnerText ?? string.Empty;
        }

        private void Save()
        {
            string projectName = txtProjectName.Text.Trim();
            string projectDir = txtProjectDir.Text.Trim();
            string projectEPSG = txtProjectEPSG.Text.Trim();
            string projectDescription = txtProjectDescription.Text.Trim();
            ConfigData.SetSettings(
                directory: projectDir,
                name: projectName,
                epsg: projectEPSG,
                description: projectDescription);
            isSaved = true;
            ConfigData.SaveConfig();
        }

        public PropertiesPage()
        {
            InitializeComponent();
        }

        private void PropertiesPage_Load(object sender, EventArgs e)
        {
            PopulateFields();
            isSaved = true;
        }


        private void menuSave_Click(object sender, EventArgs e)
        {
            Save();
        }

        private void saveStatus(object sender, EventArgs e)
        {
            isSaved = false; // Mark as unsaved when any field changes
        }

        private void PropertiesPage_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (isSaved)
            {
                return; // No need to prompt if changes are saved
            }
            DialogResult results = MessageBox.Show(
                "Do you want to save changes to the project properties?",
                "Save Changes",
                MessageBoxButtons.YesNoCancel,
                MessageBoxIcon.Question);
            if (results == DialogResult.Yes)
            {
                Save();
            }
            else if (results == DialogResult.Cancel)
            {
                e.Cancel = true; // Cancel the form close
            }

        }

        private void btnProjectDir_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog fbd = new FolderBrowserDialog
            {
                Description = "Select Project Directory",
                ShowNewFolderButton = true,
                SelectedPath = txtProjectDir.Text.Trim(),
                InitialDirectory = ConfigData.GetProjectDir()
            };
            if (fbd.ShowDialog() == DialogResult.OK)
            {
                txtProjectDir.Text = fbd.SelectedPath;
                isSaved = false; // Mark as unsaved when directory changes
            }
        }
    }
}
