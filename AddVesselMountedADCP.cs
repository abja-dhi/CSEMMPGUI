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
using Python.Runtime;

namespace CSEMMPGUI_v1
{
    public partial class AddVesselMountedADCP : Form
    {

        public _SurveyManager surveyManager;
        public XmlDocument? project;
        public int id; // ID of the instrument
        XmlElement? instrument;
        public bool isSaved; // Track if survey has been saved

        public AddVesselMountedADCP(_SurveyManager _surveyManager)
        {
            InitializeComponent();
            surveyManager = _surveyManager;
            Initialize();
        }

        public void Initialize()
        {
            if (surveyManager.survey == null)
            {
                throw new InvalidOperationException("SurveyManager.survey is null. Cannot create instrument element.");
            }
            id = _ClassConfigurationManager.NObjects(type: "//VesselMountedADCP") + 1;
            txtPD0Path.Text = string.Empty;
            txtPositionPath.Text = string.Empty;
            txtName.Text = $"VesselMountedADCP {id}";
            txtMagneticDeclination.Text = "0.0";
            txtUTCOffset.Text = "0.0";
            txtRotationAngle.Text = "0.0";
            txtCRPX.Text = "0.0";
            txtCRPY.Text = "0.0";
            txtCRPZ.Text = "0.0";
            txtRSSI1.Text = String.Empty;
            txtRSSI2.Text = String.Empty;
            txtRSSI3.Text = String.Empty;
            txtRSSI4.Text = String.Empty;
            txtFirstEnsemble.Text = "1";
            txtLastEnsemble.Text = "1";
            checkMaskEchoIntensity.Checked = false;
            txtMinEchoIntensity.Text = "0";
            txtMaxEchoIntensity.Text = "255";
            txtMinEchoIntensity.Enabled = false;
            txtMaxEchoIntensity.Enabled = false;
            checkMaskPercentGood.Checked = false;
            txtMinPercentGood.Text = "0";
            txtMinPercentGood.Enabled = false;
            checkMaskCorrelationMagnitude.Checked = false;
            txtMinCorrelationMagnitude.Text = "0";
            txtMaxCorrelationMagnitude.Text = "255";
            txtMinCorrelationMagnitude.Enabled = false;
            txtMaxCorrelationMagnitude.Enabled = false;
            checkMaskingVelocity.Checked = false;
            txtMinVelocity.Text = String.Empty;
            txtMaxVelocity.Text = String.Empty;
            txtMinVelocity.Enabled = false;
            txtMaxVelocity.Enabled = false;
            checkMaskingErrorVelocity.Checked = false;
            txtMinErrorVelocity.Text = String.Empty;
            txtMaxErrorVelocity.Text = String.Empty;
            txtMinErrorVelocity.Enabled = false;
            txtMaxErrorVelocity.Enabled = false;
            boxConfiguration.Enabled = false;
            boxMasking.Enabled = false;
            boxPosition.Enabled = false;
            btnPrintConfig.Enabled = false;
            rbSingle.Checked = true; // Default to single file mode
            comboDateTime.Items.Clear();
            comboX.Items.Clear();
            comboY.Items.Clear();
            comboHeading.Items.Clear();
            comboDateTime.Text = string.Empty;
            comboX.Text = string.Empty;
            comboY.Text = string.Empty;
            comboHeading.Text = string.Empty;
            // Create the instrument element
            instrument = surveyManager.survey.OwnerDocument.CreateElement("VesselMountedADCP");
            instrument.SetAttribute("id", id.ToString());
            instrument.SetAttribute("type", "VesselMountedADCP");
            instrument.SetAttribute("name", $"VesselMountedADCP {id}");
            project = surveyManager.survey.OwnerDocument;
            isSaved = false; // Initially, the instrument is not saved
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current instrument has unsaved changes. Do you want to save them before creating a new instrument?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    SaveInstrument();
                    isSaved = true; // Mark as saved after saving
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not create a new instrument
                }
            }
            Initialize(); // Reinitialize the instrument
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveInstrument();
            isSaved = true; // Mark as saved after saving
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current instrument has unsaved changes. Do you want to save them before exiting?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    SaveInstrument(); // Save the current instrument
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not exit
                }
            }
            this.Close(); // Close the form
        }

        private void btnLoadPD0_Click(object sender, EventArgs e)
        {
            var ofd = new OpenFileDialog
            {
                Filter = "PD0 files (*.000)|*.000",
                Title = "Select PD0 File",
                InitialDirectory = _ClassConfigurationManager.GetSetting(settingName: "Directory")
            };
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                Dictionary<string, string> inputs = new Dictionary<string, string>
                {
                    { "Task", "LoadPd0" },
                    { "Path", ofd.FileName },
                };

                string xmlInput = _Tools.GenerateInput(inputs);
                XmlDocument result = _Tools.CallPython(xmlInput);
                Dictionary<string, string> outputs = _Tools.ParseOutput(result);
                if (outputs.ContainsKey("Error"))
                {
                    MessageBox.Show(outputs["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                txtPD0Path.Text = ofd.FileName;
                int nEnsembles = Convert.ToInt32(outputs["NEnsembles"]);
                txtLastEnsemble.Maximum = nEnsembles;
                txtLastEnsemble.Value = nEnsembles;
                boxConfiguration.Enabled = true;
                boxMasking.Enabled = true;
                btnPrintConfig.Enabled = true;
                isSaved = false; // Mark as unsaved after loading a new PD0 file
            }
        }

        private void btnLoadPosition_Click(object sender, EventArgs e)
        {
            string[] columns = Array.Empty<string>();
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "Position File (*.csv)|*.csv";
            openFileDialog.Title = "Select a Position File";
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                string filePath = openFileDialog.FileName;
                int nLines = File.ReadAllLines(filePath).Length;
                UtilsCSVImportOptions csvOptions = new UtilsCSVImportOptions(nLines);
                if (csvOptions.ShowDialog() == DialogResult.OK)
                {
                    int headerLines = csvOptions._headerLines;
                    string delimiter = csvOptions._delimiter;
                    columns = _Utils.ParseCSVAndReturnColumns(filePath, delimiter, headerLines);
                    if (columns.Length < 4)
                    {
                        MessageBox.Show("The selected CSV file does not contain enough columns for position data.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return;
                    }
                }
                else
                {
                    return; // User cancelled the CSV options dialog
                }
            }
            else
            {
                return; // User cancelled the file dialog
            }
            txtPositionPath.Text = openFileDialog.FileName;
            boxPosition.Enabled = true;
            updateCombo(comboDateTime, columns, 0);
            updateCombo(comboX, columns, 1);
            updateCombo(comboY, columns, 2);
            updateCombo(comboHeading, columns, 3);
            isSaved = false; // Mark as unsaved after loading a new position file
        }

        public void updateCombo(ComboBox combo, string[] items, int index)
        {
            combo.Items.Clear();
            combo.Items.AddRange(items);
            combo.SelectedIndex = index;
        }

        private void input_Changed(object sender, EventArgs e)
        {
            isSaved = false; // Mark as unsaved when the name changes
        }

        public int CreateInstrument()
        {
            if (String.IsNullOrEmpty(txtPD0Path.Text.Trim()))
            {
                MessageBox.Show("Please select a PD0 file before saving.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            if (String.IsNullOrEmpty(txtPositionPath.Text.Trim()))
            {
                MessageBox.Show("Please select a position file before saving.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            instrument.SetAttribute("name", txtName.Text.Trim());
            while (instrument.HasChildNodes && instrument.FirstChild != null)
            {
                instrument.RemoveChild(instrument.FirstChild);
            }
            if (surveyManager.survey == null)
            {
                throw new InvalidOperationException("SurveyManager.survey is null. Cannot save instrument.");
                return 0;
            }
            // Pd0 related attributes
            XmlElement pd0 = project.CreateElement("Pd0");
            XmlElement pd0Path = project.CreateElement("Path");
            pd0Path.InnerText = txtPD0Path.Text.Trim();
            pd0.AppendChild(pd0Path);
            XmlElement configuration = project.CreateElement("Configuration");
            XmlElement magneticDeclination = project.CreateElement("MagneticDeclination");
            magneticDeclination.InnerText = txtMagneticDeclination.Text.Trim();
            configuration.AppendChild(magneticDeclination);
            XmlElement utcOffset = project.CreateElement("UTCOffset");
            utcOffset.InnerText = txtUTCOffset.Text.Trim();
            configuration.AppendChild(utcOffset);
            XmlElement rotationAngle = project.CreateElement("RotationAngle");
            rotationAngle.InnerText = txtRotationAngle.Text.Trim();
            configuration.AppendChild(rotationAngle);
            XmlElement crpOffset = project.CreateElement("CRPOffset");
            XmlElement crpOffsetX = project.CreateElement("X");
            crpOffsetX.InnerText = txtCRPX.Text.Trim();
            XmlElement crpOffsetY = project.CreateElement("Y");
            crpOffsetY.InnerText = txtCRPY.Text.Trim();
            XmlElement crpOffsetZ = project.CreateElement("Z");
            crpOffsetZ.InnerText = txtCRPZ.Text.Trim();
            crpOffset.AppendChild(crpOffsetX);
            crpOffset.AppendChild(crpOffsetY);
            crpOffset.AppendChild(crpOffsetZ);
            configuration.AppendChild(crpOffset);

            XmlElement rssiCoefficients = project.CreateElement("RSSICoefficients");
            XmlElement rssiBeam1 = project.CreateElement("Beam1");
            rssiBeam1.InnerText = txtRSSI1.Text.Trim();
            XmlElement rssiBeam2 = project.CreateElement("Beam2");
            rssiBeam2.InnerText = txtRSSI2.Text.Trim();
            XmlElement rssiBeam3 = project.CreateElement("Beam3");
            rssiBeam3.InnerText = txtRSSI3.Text.Trim();
            XmlElement rssiBeam4 = project.CreateElement("Beam4");
            rssiBeam4.InnerText = txtRSSI4.Text.Trim();
            rssiCoefficients.AppendChild(rssiBeam1);
            rssiCoefficients.AppendChild(rssiBeam2);
            rssiCoefficients.AppendChild(rssiBeam3);
            rssiCoefficients.AppendChild(rssiBeam4);
            configuration.AppendChild(rssiCoefficients);

            pd0.AppendChild(configuration);

            XmlElement masking = project.CreateElement("Masking");
            XmlElement firstEnsemble = project.CreateElement("FirstEnsemble");
            firstEnsemble.InnerText = txtFirstEnsemble.Text.Trim();
            masking.AppendChild(firstEnsemble);
            XmlElement lastEnsemble = project.CreateElement("LastEnsemble");
            lastEnsemble.InnerText = txtLastEnsemble.Text.Trim();
            masking.AppendChild(lastEnsemble);
            XmlElement maskEchoIntensity = project.CreateElement("MaskEchoIntensity");
            maskEchoIntensity.SetAttribute("Enabled", checkMaskEchoIntensity.Checked.ToString().ToLower());
            XmlElement maskEchoIntensityMin = project.CreateElement("Min");
            maskEchoIntensityMin.InnerText = txtMinEchoIntensity.Text.Trim();
            maskEchoIntensity.AppendChild(maskEchoIntensityMin);
            XmlElement maskEchoIntensityMax = project.CreateElement("Max");
            maskEchoIntensityMax.InnerText = txtMaxEchoIntensity.Text.Trim();
            maskEchoIntensity.AppendChild(maskEchoIntensityMax);
            masking.AppendChild(maskEchoIntensity);

            XmlElement maskPercentGood = project.CreateElement("MaskPercentGood");
            maskPercentGood.SetAttribute("Enabled", checkMaskPercentGood.Checked.ToString().ToLower());
            XmlElement maskPercentGoodMin = project.CreateElement("Min");
            maskPercentGoodMin.InnerText = txtMinPercentGood.Text.Trim();
            maskPercentGood.AppendChild(maskPercentGoodMin);
            masking.AppendChild(maskPercentGood);

            XmlElement maskCorrelationMagnitude = project.CreateElement("MaskCorrelationMagnitude");
            maskCorrelationMagnitude.SetAttribute("Enabled", checkMaskCorrelationMagnitude.Checked.ToString().ToLower());
            XmlElement maskCorrelationMagnitudeMin = project.CreateElement("Min");
            maskCorrelationMagnitudeMin.InnerText = txtMinCorrelationMagnitude.Text.Trim();
            maskCorrelationMagnitude.AppendChild(maskCorrelationMagnitudeMin);
            XmlElement maskCorrelationMagnitudeMax = project.CreateElement("Max");
            maskCorrelationMagnitudeMax.InnerText = txtMaxCorrelationMagnitude.Text.Trim();
            maskCorrelationMagnitude.AppendChild(maskCorrelationMagnitudeMax);
            masking.AppendChild(maskCorrelationMagnitude);

            XmlElement maskCurrentSpeed = project.CreateElement("MaskCurrentSpeed");
            maskCurrentSpeed.SetAttribute("Enabled", checkMaskingVelocity.Checked.ToString().ToLower());
            XmlElement maskCurrentSpeedMin = project.CreateElement("Min");
            maskCurrentSpeedMin.InnerText = txtMinVelocity.Text.Trim();
            maskCurrentSpeed.AppendChild(maskCurrentSpeedMin);
            XmlElement maskCurrentSpeedMax = project.CreateElement("Max");
            maskCurrentSpeedMax.InnerText = txtMaxVelocity.Text.Trim();
            maskCurrentSpeed.AppendChild(maskCurrentSpeedMax);
            masking.AppendChild(maskCurrentSpeed);

            XmlElement maskErrorVelocity = project.CreateElement("MaskErrorVelocity");
            maskErrorVelocity.SetAttribute("Enabled", checkMaskingErrorVelocity.Checked.ToString().ToLower());
            XmlElement maskErrorVelocityMin = project.CreateElement("Min");
            maskErrorVelocityMin.InnerText = txtMinErrorVelocity.Text.Trim();
            maskErrorVelocity.AppendChild(maskErrorVelocityMin);
            XmlElement maskErrorVelocityMax = project.CreateElement("Max");
            maskErrorVelocityMax.InnerText = txtMaxErrorVelocity.Text.Trim();
            maskErrorVelocity.AppendChild(maskErrorVelocityMax);
            masking.AppendChild(maskErrorVelocity);

            pd0.AppendChild(masking);

            instrument.AppendChild(pd0);

            // Position related attributes
            XmlElement position = project.CreateElement("PositionData");
            XmlElement positionPath = project.CreateElement("Path");
            positionPath.InnerText = txtPositionPath.Text.Trim();
            position.AppendChild(positionPath);

            XmlElement positionColumns = project.CreateElement("Columns");

            for (int i = 0; i < comboDateTime.Items.Count; i++)
            {
                XmlElement column = project.CreateElement($"Column{i}");
                column.InnerText = comboDateTime.Items[i].ToString();
                positionColumns.AppendChild(column);
            }
            position.AppendChild(positionColumns);

            XmlElement dateTimeColumn = project.CreateElement("DateTimeColumn");
            dateTimeColumn.InnerText = comboDateTime.Text.Trim() ?? string.Empty;
            position.AppendChild(dateTimeColumn);

            XmlElement xColumn = project.CreateElement("XColumn");
            xColumn.InnerText = comboX.Text.Trim() ?? string.Empty;
            position.AppendChild(xColumn);

            XmlElement yColumn = project.CreateElement("YColumn");
            yColumn.InnerText = comboY.Text.Trim() ?? string.Empty;
            position.AppendChild(yColumn);

            XmlElement headingColumn = project.CreateElement("HeadingColumn");
            headingColumn.InnerText = comboHeading.Text.Trim() ?? string.Empty;
            position.AppendChild(headingColumn);

            instrument.AppendChild(position);

            return 1;
        }

        public void SaveInstrument()
        {
            if (instrument == null)
            {
                throw new InvalidOperationException("Instrument is not initialized. Cannot save.");
            }
            int status = CreateInstrument();
            if (status == 0)
                return;
            string id = instrument.GetAttribute("id");
            if (surveyManager.survey == null)
            {
                throw new InvalidOperationException("SurveyManager.survey is null. Cannot save instrument.");
            }
            string surveyId = surveyManager.survey.GetAttribute("id");
            string xpath = $"//Survey[@id='{surveyId}']/VesselMountedADCP[@id='{id}' and @type='VesselMountedADCP']";
            XmlNode? existingInstrument = surveyManager.survey.SelectSingleNode(xpath);
            if (existingInstrument != null)
            {
                // Update existing instrument
                XmlNode imported = surveyManager.survey.OwnerDocument.ImportNode(instrument, true);
                surveyManager.survey.ReplaceChild(imported, existingInstrument);
            }
            else
            {
                // Add new instrument
                surveyManager.survey.AppendChild(instrument);
            }
            surveyManager.SaveSurvey(name: surveyManager.GetAttribute(attribute: "name"));
            _ClassConfigurationManager.SaveConfig(1);
            isSaved = true; // Mark as saved after saving
        }

        private void btnPrintConfig_Click(object sender, EventArgs e)
        {
            if (String.IsNullOrEmpty(txtPD0Path.Text.Trim()))
            {
                return; // No PD0 file selected, nothing to print
            }
            VesselMountedADCPPrintConfig printConfigForm = new VesselMountedADCPPrintConfig(txtPD0Path.Text.Trim());
            printConfigForm.ShowDialog();
        }

        private void AddVesselMountedADCP_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current instrument has unsaved changes. Do you want to save them before exiting?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    SaveInstrument(); // Save the current instrument
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Cancel the form closing event
                    return; // User chose to cancel, do not exit
                }
            }
        }

        private void rbSingle_CheckedChanged(object sender, EventArgs e)
        {
            if (rbSingle.Checked)
            {
                lblPD0File.Text = ".000 File";
                lblPositionFile.Visible = true;
                txtPositionPath.Visible = true;
                btnLoadPosition.Visible = true;
                boxFileInfo.Text = "File Information";
            }
            else
            {
                lblPD0File.Text = "Folder";
                lblPositionFile.Visible = false;
                txtPositionPath.Visible = false;
                btnLoadPosition.Visible = false;
                boxFileInfo.Text = "Folder Information";
            }
        }
    }
}
