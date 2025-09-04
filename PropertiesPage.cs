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
        public _ClassConfigurationManager _project = new();

        private void PopulateFields()
        {
            txtProjectEPSG.Text = _project.GetSetting(settingName: "EPSG");
            txtProjectDescription.Text = _project.GetSetting(settingName: "Description");
            isSaved = true; // Initially, fields are populated and considered saved
        }

        public PropertiesPage()
        {
            InitializeComponent();
            PopulateFields();
            isSaved = true; // Initially, fields are populated and considered saved

            this.KeyPreview = true; // Enable form to capture key events
            this.KeyDown += Properties_KeyDown; // Attach key down event handler
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
            _project.SetSetting(settingName: "EPSG", txtProjectEPSG.Text.Trim());
            _project.SetSetting(settingName: "Description", txtProjectDescription.Text.Trim());
            _project.SaveConfig(saveMode: 1);
            isSaved = true;
        }

        private void Properties_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Control && e.KeyCode == Keys.S) // Ctrl + S
            {
                e.SuppressKeyPress = true; // Prevent default behavior
                Save(); // Save the project
            }
        }
    }
}
