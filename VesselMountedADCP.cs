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
    public partial class VesselMountedADCP : Form
    {

        private readonly XmlElement _parentSurvey;
        private XmlElement _vesselMountedADCP;
        private bool _isSaved = false;
        public VesselMountedADCP(XmlElement parentSurvey)
        {
            string pythonDll = @"C:\Program Files\Python311\python311.dll";
            Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", pythonDll);
            PythonEngine.Initialize();
            InitializeComponent();
            _parentSurvey = parentSurvey ?? throw new ArgumentNullException(nameof(parentSurvey));
            int vesselMountedADCPCount = _parentSurvey.SelectNodes("./VesselMountedADCP[@type='Vessel Mounted ADCP']").Count;

            string defaultName = $"Vessel Mounted ADCP {vesselMountedADCPCount + 1}";
            txtName.Text = defaultName;

            _vesselMountedADCP = _parentSurvey.OwnerDocument.CreateElement("VesselMountedADCP");
            _vesselMountedADCP.SetAttribute("type", "Vessel Mounted ADCP");
            _vesselMountedADCP.SetAttribute("name", defaultName);
        }

        private void btnLoadPD0_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "PD0 Files (*.000)|*.000";
            openFileDialog.Title = "Select a PD0 File";
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                string filePath = openFileDialog.FileName;
                var sb = new StringBuilder();
                using (var writer = XmlWriter.Create(sb, new XmlWriterSettings { OmitXmlDeclaration = true }))
                {
                    writer.WriteStartElement("Input");
                    writer.WriteElementString("Task", "LoadPd0");
                    writer.WriteElementString("Path", filePath);
                    writer.WriteEndElement();
                }
                string xmlInputStr = sb.ToString();
                try
                {
                    using (Py.GIL())
                    {
                        XmlDocument doc = Tools.CallPython(xmlInputStr);
                        string beams = doc.SelectSingleNode("/Result/NBeams")?.InnerText ?? "N/A";
                        string ensembles = doc.SelectSingleNode("/Result/NEnsembles")?.InnerText ?? "N/A";
                        MessageBox.Show($"Beams: {beams}\nEnsembles: {ensembles}", "Load PD0 Result", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        txtPD0Path.Text = filePath;
                        txtLastEnsemble.Maximum = Convert.ToInt32(ensembles);
                        txtLastEnsemble.Value = Convert.ToInt32(ensembles);
                        boxConfiguration.Enabled = true;
                        boxMasking.Enabled = true;
                    }

                }
                //catch
                //{
                //    MessageBox.Show("An error occurred while processing the PD0 file.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                //}
                finally
                {
                    PythonEngine.Shutdown();
                }
            }
        }

        public void updateCombo(ComboBox combo, string[] items)
        {
            combo.Items.Clear();
            combo.Items.AddRange(items);
            combo.SelectedIndex = 0;
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
                CSVImportOptions csvOptions = new CSVImportOptions(nLines);
                if (csvOptions.ShowDialog() == DialogResult.OK)
                {
                    int headerLines = csvOptions._headerLines;
                    string delimiter = csvOptions._delimiter;
                    columns = Tools.ParseCSVAndReturnColumns(filePath, delimiter, headerLines);
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
            updateCombo(comboDateTime, columns);
            updateCombo(comboX, columns);
            updateCombo(comboY, columns);
            updateCombo(comboHeading, columns);

        }

        private (bool success, string msg) ValidateInputs()
        {
            if (String.IsNullOrEmpty(txtRSSI1.Text))
                return (false, "RSSI Beam 1 value is required.");
            if (String.IsNullOrEmpty(txtRSSI2.Text))
                return (false, "RSSI Beam 2 value is required.");
            if (String.IsNullOrEmpty(txtRSSI3.Text))
                return (false, "RSSI Beam 3 value is required.");
            if (String.IsNullOrEmpty(txtRSSI4.Text))
                return (false, "RSSI Beam 4 value is required.");

            return (true, string.Empty);
        }

        private void SaveVesselMountedADCP()
        {
            if (String.IsNullOrEmpty(txtPD0Path.Text) || string.IsNullOrEmpty(txtPositionPath.Text))
            {
                MessageBox.Show("Please load both PD0 and Position files before saving.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            string vmadcpName = txtName.Text.Trim();
            if (string.IsNullOrEmpty(vmadcpName))
            {
                MessageBox.Show("Please enter a name for the vessel mounted ADCP.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            var validation = ValidateInputs();
            if (!validation.success)
            {
                MessageBox.Show(validation.msg, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            _vesselMountedADCP.SetAttribute("name", vmadcpName);
            Tools.ClearChildNodes(_vesselMountedADCP);
            XmlDocument doc = _vesselMountedADCP.OwnerDocument;

            // Create PD0 Element
            XmlElement pd0 = doc.CreateElement("PD0");
            XmlElement pd0Path = doc.CreateElement("Path");
            pd0Path.InnerText = txtPD0Path.Text.Trim();
            pd0.AppendChild(pd0Path);
            //// Create Configuration Element
            XmlElement configuration = doc.CreateElement("Configuration");
            ////// Magnetic Declination
            XmlElement magneticDeclination = doc.CreateElement("MagneticDeclination");
            magneticDeclination.InnerText = txtMagneticDeclination.Text.Trim();
            configuration.AppendChild(magneticDeclination);
            /////// UTC Offset
            XmlElement utcOffset = doc.CreateElement("UTCOffset");
            utcOffset.InnerText = txtUTCOffset.Text.Trim();
            configuration.AppendChild(utcOffset);
            ////// Rotation Angle
            XmlElement rotationAngle = doc.CreateElement("RotationAngle");
            rotationAngle.InnerText = txtRotationAngle.Text.Trim();
            configuration.AppendChild(rotationAngle);
            ////// CRP Offset
            XmlElement crpOffset = doc.CreateElement("CRPOffset");
            XmlElement crpOffsetX = doc.CreateElement("X");
            crpOffsetX.InnerText = txtCRPX.Text.Trim();
            crpOffset.AppendChild(crpOffsetX);
            XmlElement crpOffsetY = doc.CreateElement("Y");
            crpOffsetY.InnerText = txtCRPY.Text.Trim();
            crpOffset.AppendChild(crpOffsetY);
            XmlElement crpOffsetZ = doc.CreateElement("Z");
            crpOffsetZ.InnerText = txtCRPZ.Text.Trim();
            crpOffset.AppendChild(crpOffsetZ);
            configuration.AppendChild(crpOffset);
            ////// RSSI Coefficients
            XmlElement rssiCoefficients = doc.CreateElement("RSSICoefficients");
            XmlElement rssiBeam1 = doc.CreateElement("Beam1");
            rssiBeam1.InnerText = txtRSSI1.Text.Trim();
            rssiCoefficients.AppendChild(rssiBeam1);
            XmlElement rssiBeam2 = doc.CreateElement("Beam2");
            rssiBeam2.InnerText = txtRSSI2.Text.Trim();
            rssiCoefficients.AppendChild(rssiBeam2);
            XmlElement rssiBeam3 = doc.CreateElement("Beam3");
            rssiBeam3.InnerText = txtRSSI3.Text.Trim();
            rssiCoefficients.AppendChild(rssiBeam3);
            XmlElement rssiBeam4 = doc.CreateElement("Beam4");
            rssiBeam4.InnerText = txtRSSI4.Text.Trim();
            rssiCoefficients.AppendChild(rssiBeam4);
            configuration.AppendChild(rssiCoefficients);

            pd0.AppendChild(configuration);

            //// Create Masking Element
            XmlElement masking = doc.CreateElement("Masking");
            ////// First and Last Ensemble
            XmlElement firstEnsemble = doc.CreateElement("FirstEnsemble");
            firstEnsemble.InnerText = txtFirstEnsemble.Text.Trim();
            masking.AppendChild(firstEnsemble);
            XmlElement lastEnsemble = doc.CreateElement("LastEnsemble");
            lastEnsemble.InnerText = txtLastEnsemble.Text.Trim();
            masking.AppendChild(lastEnsemble);
            ////// Echo Intensity
            XmlElement maskEchoIntensity = doc.CreateElement("MaskEchoIntensity");
            XmlElement maskEchoIntensityEnabled = doc.CreateElement("Enabled");
            maskEchoIntensityEnabled.InnerText = checkMaskEchoIntensity.Checked.ToString();
            maskEchoIntensity.AppendChild(maskEchoIntensityEnabled);
            if (checkMaskEchoIntensity.Checked)
            {
                XmlElement maskEchoIntensityMin = doc.CreateElement("Min");
                maskEchoIntensityMin.InnerText = txtMinEchoIntensity.Text.Trim();
                maskEchoIntensity.AppendChild(maskEchoIntensityMin);
                XmlElement maskEchoIntensityMax = doc.CreateElement("Max");
                maskEchoIntensityMax.InnerText = txtMaxEchoIntensity.Text.Trim();
                maskEchoIntensity.AppendChild(maskEchoIntensityMax);
            }
            masking.AppendChild(maskEchoIntensity);
            ////// Percent Good
            XmlElement maskPercentGood = doc.CreateElement("MaskPercentGood");
            XmlElement maskPercentGoodEnabled = doc.CreateElement("Enabled");
            maskPercentGoodEnabled.InnerText = checkMaskPercentGood.Checked.ToString();
            maskPercentGood.AppendChild(maskPercentGoodEnabled);
            if (checkMaskPercentGood.Checked)
            {
                XmlElement maskPercentGoodMin = doc.CreateElement("Min");
                maskPercentGoodMin.InnerText = txtMinPercentGood.Text.Trim();
                maskPercentGood.AppendChild(maskPercentGoodMin);
            }
            masking.AppendChild(maskPercentGood);
            ////// Correlation Magnitude
            XmlElement maskCorrelationMagnitude = doc.CreateElement("MaskCorrelationMagnitude");
            XmlElement maskCorrelationMagnitudeEnabled = doc.CreateElement("Enabled");
            maskCorrelationMagnitudeEnabled.InnerText = checkMaskCorrelationMagnitude.Checked.ToString();
            maskCorrelationMagnitude.AppendChild(maskCorrelationMagnitudeEnabled);
            if (checkMaskCorrelationMagnitude.Checked)
            {
                XmlElement maskCorrelationMagnitudeMin = doc.CreateElement("Min");
                maskCorrelationMagnitudeMin.InnerText = txtMinCorrelationMagnitude.Text.Trim();
                maskCorrelationMagnitude.AppendChild(maskCorrelationMagnitudeMin);
                XmlElement maskCorrelationMagnitudeMax = doc.CreateElement("Max");
                maskCorrelationMagnitudeMax.InnerText = txtMaxCorrelationMagnitude.Text.Trim();
                maskCorrelationMagnitude.AppendChild(maskCorrelationMagnitudeMax);
            }
            masking.AppendChild(maskCorrelationMagnitude);
            ////// Current Speed
            XmlElement maskCurrentSpeed = doc.CreateElement("MaskCurrentSpeed");
            XmlElement maskCurrentSpeedEnabled = doc.CreateElement("Enabled");
            maskCurrentSpeedEnabled.InnerText = checkMaskingVelocity.Checked.ToString();
            maskCurrentSpeed.AppendChild(maskCurrentSpeedEnabled);
            if (checkMaskingVelocity.Checked)
            {
                XmlElement maskCurrentSpeedMin = doc.CreateElement("Min");
                maskCurrentSpeedMin.InnerText = txtMinVelocity.Text.Trim();
                maskCurrentSpeed.AppendChild(maskCurrentSpeedMin);
                XmlElement maskCurrentSpeedMax = doc.CreateElement("Max");
                maskCurrentSpeedMax.InnerText = txtMaxVelocity.Text.Trim();
                maskCurrentSpeed.AppendChild(maskCurrentSpeedMax);
            }
            masking.AppendChild(maskCurrentSpeed);
            ////// Error Velocity
            XmlElement maskErrorVelocity = doc.CreateElement("MaskErrorVelocity");
            XmlElement maskErrorVelocityEnabled = doc.CreateElement("Enabled");
            maskErrorVelocityEnabled.InnerText = checkMaskingErrorVelocity.Checked.ToString();
            maskErrorVelocity.AppendChild(maskErrorVelocityEnabled);
            if (checkMaskingErrorVelocity.Checked)
            {
                XmlElement maskErrorVelocityMin = doc.CreateElement("Min");
                maskErrorVelocityMin.InnerText = txtMinErrorVelocity.Text.Trim();
                maskErrorVelocity.AppendChild(maskErrorVelocityMin);
                XmlElement maskErrorVelocityMax = doc.CreateElement("Max");
                maskErrorVelocityMax.InnerText = txtMaxErrorVelocity.Text.Trim();
                maskErrorVelocity.AppendChild(maskErrorVelocityMax);
            }
            masking.AppendChild(maskErrorVelocity);

            pd0.AppendChild(masking);

            _vesselMountedADCP.AppendChild(pd0);
            // Position Element
            XmlElement position = doc.CreateElement("PositionData");
            //// Position File Path
            XmlElement positionPath = doc.CreateElement("Path");
            positionPath.InnerText = txtPositionPath.Text.Trim();
            position.AppendChild(positionPath);
            //// Datetime Column
            XmlElement dateTimeColumn = doc.CreateElement("DateTimeColumn");
            dateTimeColumn.InnerText = comboDateTime.SelectedItem?.ToString() ?? string.Empty;
            position.AppendChild(dateTimeColumn);
            //// X Column
            XmlElement xColumn = doc.CreateElement("XColumn");
            xColumn.InnerText = comboX.SelectedItem?.ToString() ?? string.Empty;
            position.AppendChild(xColumn);
            //// Y Column
            XmlElement yColumn = doc.CreateElement("YColumn");
            yColumn.InnerText = comboY.SelectedItem?.ToString() ?? string.Empty;
            position.AppendChild(yColumn);
            //// Heading Column
            XmlElement headingColumn = doc.CreateElement("HeadingColumn");
            headingColumn.InnerText = comboHeading.SelectedItem?.ToString() ?? string.Empty;
            position.AppendChild(headingColumn);

            _vesselMountedADCP.AppendChild(position);


            string projDir = ConfigData.GetProjectDir();
            string vmadcpPath = Path.Combine(projDir, vmadcpName + ".mtvmadcp");
            XmlDocument vmadcpDoc = new XmlDocument();
            XmlDeclaration decl = vmadcpDoc.CreateXmlDeclaration("1.0", "UTF-8", null);
            vmadcpDoc.AppendChild(decl);
            vmadcpDoc.AppendChild(vmadcpDoc.ImportNode(_vesselMountedADCP, true));
            vmadcpDoc.Save(vmadcpPath);

            XmlNode existing = _parentSurvey.SelectNodes("VesselMountedADCP")
                .Cast<XmlNode>()
                .FirstOrDefault(n => string.Equals(n.Attributes?["name"]?.Value, vmadcpName, StringComparison.OrdinalIgnoreCase));

            if (existing != null)
            {
                DialogResult reslut = MessageBox.Show($"Vessel Mounted ADCP '{vmadcpName}' already exists. Do you want to update it?", "Info", MessageBoxButtons.YesNoCancel, MessageBoxIcon.Warning);
                if (reslut == DialogResult.Yes)
                {
                    _parentSurvey.ReplaceChild(_parentSurvey.OwnerDocument.ImportNode(_vesselMountedADCP, true), existing);
                }
                else
                {
                    return; // Do not save if user chooses not to update
                }
            }
            else
            {
                _parentSurvey.AppendChild(_parentSurvey.OwnerDocument.ImportNode(_vesselMountedADCP, true));
            }

            _isSaved = true;
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveVesselMountedADCP();
            if (_isSaved)
                this.DialogResult = DialogResult.OK;
        }

        private void VesselMountedADCP_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (_isSaved)
            {
                this.DialogResult = DialogResult.OK; // Indicate that the form was saved successfully
                return;
            }
            DialogResult result;
            if (String.IsNullOrEmpty(txtPD0Path.Text) && String.IsNullOrEmpty(txtPositionPath.Text))
            {
                this.DialogResult = DialogResult.Cancel;
                return;
            }
            else if (String.IsNullOrEmpty(txtPD0Path.Text) && !String.IsNullOrEmpty(txtPositionPath.Text))
            {
                result = MessageBox.Show(
                    "You have unsvaed changes in Position Data. Do you want to save?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    MessageBox.Show("Please load PD0 file before saving.", "Warning", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    e.Cancel = true; // Prevent closing if save failed
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Prevent closing if user cancels
                }
                else
                {
                    this.DialogResult = DialogResult.No; // Indicate that the form was closed without saving
                    // User chose No, so we can close without saving
                    _parentSurvey.RemoveChild(_vesselMountedADCP);
                    this.DialogResult = DialogResult.No;
                    return;
                }
            }
            else if (!String.IsNullOrEmpty(txtPD0Path.Text) && String.IsNullOrEmpty(txtPositionPath.Text))
            {
                result = MessageBox.Show(
                    "You have unsvaed changes in Pd0 File. Do you want to save?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    MessageBox.Show("Please load Position file before saving.", "Warning", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    e.Cancel = true; // Prevent closing if save failed
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Prevent closing if user cancels
                }
                else
                {
                    _parentSurvey.RemoveChild(_vesselMountedADCP);
                    this.DialogResult = DialogResult.No;
                    return;
                }
            }
            else
            {
                result = MessageBox.Show(
                    "You have unsaved changes. Do you want to save them?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    SaveVesselMountedADCP();
                    if (!_isSaved)
                    {
                        e.Cancel = true; // Prevent closing if save failed
                    }
                    else
                    {
                        e.Cancel = false;
                        this.DialogResult = DialogResult.OK; // Indicate that the form was saved successfully
                    }
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Prevent closing if user cancels
                }
                else
                {
                    _parentSurvey.RemoveChild(_vesselMountedADCP);
                    this.DialogResult = DialogResult.No; // Indicate that the form was closed without saving
                }
            }

        }

        private void checkMaskEchoIntensity_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskEchoIntensity.Checked)
            {
                lblMinEchoIntensity.Enabled = true;
                lblMaxEchoIntensity.Enabled = true;
                txtMinEchoIntensity.Enabled = true;
                txtMaxEchoIntensity.Enabled = true;
            }
            else
            {
                lblMinEchoIntensity.Enabled = false;
                lblMaxEchoIntensity.Enabled = false;
                txtMinEchoIntensity.Enabled = false;
                txtMaxEchoIntensity.Enabled = false;
            }
        }

        private void checkMaskPercentGood_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskPercentGood.Checked)
            {
                lblMinPercentGood.Enabled = true;
                txtMinPercentGood.Enabled = true;
            }
            else
            {
                lblMinPercentGood.Enabled = false;
                txtMinPercentGood.Enabled = false;
            }
        }

        private void checkMaskCorrelationMagnitude_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskCorrelationMagnitude.Checked)
            {
                lblMinCorrelationMagnitude.Enabled = true;
                lblMaxCorrelationMagnitude.Enabled = true;
                txtMinCorrelationMagnitude.Enabled = true;
                txtMaxCorrelationMagnitude.Enabled = true;
            }
            else
            {
                lblMinCorrelationMagnitude.Enabled = false;
                lblMaxCorrelationMagnitude.Enabled = false;
                txtMinCorrelationMagnitude.Enabled = false;
                txtMaxCorrelationMagnitude.Enabled = false;
            }
        }

        private void checkMaskingVelocity_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskingVelocity.Checked)
            {
                lblMinVelocity.Enabled = true;
                lblMaxVelocity.Enabled = true;
                txtMinVelocity.Enabled = true;
                txtMaxVelocity.Enabled = true;
            }
            else
            {
                lblMinVelocity.Enabled = false;
                lblMaxVelocity.Enabled = false;
                txtMinVelocity.Enabled = false;
                txtMaxVelocity.Enabled = false;
            }
        }

        private void checkMaskingErrorVelocity_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskingErrorVelocity.Checked)
            {
                lblMinErrorVelocity.Enabled = true;
                lblMaxErrorVelocity.Enabled = true;
                txtMinErrorVelocity.Enabled = true;
                txtMaxErrorVelocity.Enabled = true;
            }
            else
            {
                lblMinErrorVelocity.Enabled = false;
                lblMaxErrorVelocity.Enabled = false;
                txtMinErrorVelocity.Enabled = false;
                txtMaxErrorVelocity.Enabled = false;
            }
        }

        private void menuNew_Click(object sender, EventArgs e)
        {

        }

        private void btnPrintConfig_Click(object sender, EventArgs e)
        {
            VesselMountedADCPPrintConfig vesselMountedADCPPrintConfig = new VesselMountedADCPPrintConfig(txtPD0Path.Text);
            vesselMountedADCPPrintConfig.ShowDialog();
        }
    }
}
