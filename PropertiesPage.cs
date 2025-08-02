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
        public bool isSaved;

        public PropertiesPage()
        {
            InitializeComponent();
            PopulateFields();
            isSaved = true; // Initially, fields are populated and considered saved
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            Save();
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult results = MessageBox.Show(
                    "Do you want to save changes to the project properties before exiting?",
                    "Save Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Question);
                if (results == DialogResult.Yes)
                {
                    Save();
                }
                else if (results == DialogResult.Cancel)
                {
                    return; // Cancel the exit
                }
            }
            this.Close(); // Close the properties page
        }

        private void btnProjectDir_Click(object sender, EventArgs e)
        {
            using var fbd = new FolderBrowserDialog
            {
                Description = "Select Project Directory",
                ShowNewFolderButton = true,
                SelectedPath = txtProjectDir.Text.Trim(),
                InitialDirectory = _ClassConfigurationManager.GetSetting(settingName: "Directory")
            };
            if (fbd.ShowDialog() == DialogResult.OK)
            {
                txtProjectDir.Text = fbd.SelectedPath;
                isSaved = false; // Mark as unsaved when directory changes
            }
        }

        private void inputChanged(object sender, EventArgs e)
        {
            isSaved = false; // Mark as unsaved when any input changes
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

        private void Save()
        {
            _ClassConfigurationManager.SetSetting(settingName: "Directory", txtProjectDir.Text.Trim());
            _ClassConfigurationManager.SetSetting(settingName: "EPSG", txtProjectEPSG.Text.Trim());
            _ClassConfigurationManager.SetSetting(settingName: "Description", txtProjectDescription.Text.Trim());
            isSaved = true;
        }

        private void PopulateFields()
        {
            txtProjectDir.Text = _ClassConfigurationManager.GetSetting(settingName: "Directory");
            txtProjectEPSG.Text = _ClassConfigurationManager.GetSetting(settingName: "EPSG");
            txtProjectDescription.Text = _ClassConfigurationManager.GetSetting(settingName: "Description");
            isSaved = true; // Initially, fields are populated and considered saved
        }

        
    }
}
