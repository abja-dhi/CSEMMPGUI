using Python.Runtime;
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
    public partial class AddSurvey : Form
    {
        public bool isSaved = true; // Track if survey has been saved
        public SurveyManager surveyManager = new();

        public AddSurvey()
        {
            InitializeComponent();
            surveyManager.Initialize();
            txtSurveyName.Text = surveyManager.GetAttribute(attribute: "name");
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current survey has unsaved changes. Do you want to save them before creating a new survey?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    surveyManager.SaveSurvey(name: txtSurveyName.Text);
                    isSaved = true; // Mark as saved after saving
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not create a new survey
                }
            }
            surveyManager.Initialize();
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            surveyManager.SaveSurvey(name: txtSurveyName.Text);
            isSaved = true;
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current survey has unsaved changes. Do you want to save them before exiting?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    surveyManager.SaveSurvey(name: txtSurveyName.Text);
                    isSaved = true; // Mark as saved after saving
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not exit
                }
            }
            this.Close(); // Close the AddSurvey form
        }

        private void menuADCPVesselMounted_Click(object sender, EventArgs e)
        {
            VesselMountedADCP vesselMountedADCP = new VesselMountedADCP(surveyManager);
            vesselMountedADCP.ShowDialog();
        }

        private void menuADCPSeabedLander_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This feature is not yet implemented.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void menuOBSVerticalProfile_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This feature is not yet implemented.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void menuOBSTransect_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This feature is not yet implemented.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void menuWaterSample_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This feature is not yet implemented.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
    }
}
