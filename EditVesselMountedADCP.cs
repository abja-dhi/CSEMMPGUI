using Python.Runtime;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public partial class EditVesselMountedADCP : Form
    {

        public bool isSaved; // Track if survey has been saved
        public XmlElement adcpElement;


        public EditVesselMountedADCP(XmlNode adcpNode)
        {
            InitializeComponent();
            InitializeADCP(adcpNode);
        }

        public void InitializeADCP(XmlNode adcpNode)
        {
            adcpElement = adcpNode as XmlElement;
            if (adcpElement == null)
            {
                MessageBox.Show("Invalid ADCP node provided.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                this.Close();
                return; // Ensure no further code is executed if adcpElement is null
            }
            txtName.Text = adcpElement.GetAttribute("name");
            // Pd0 related attributes
            XmlNode pd0Node = adcpElement.SelectSingleNode("Pd0");
            txtPD0Path.Text = pd0Node?.SelectSingleNode("Path")?.InnerText ?? string.Empty;
            XmlNode configurationNode = pd0Node?.SelectSingleNode("Configuration");
            txtMagneticDeclination.Text = configurationNode?.SelectSingleNode("MagneticDeclination")?.InnerText ?? string.Empty;
            txtUTCOffset.Text = configurationNode?.SelectSingleNode("UTCOffset")?.InnerText ?? string.Empty;
            txtRotationAngle.Text = configurationNode?.SelectSingleNode("RotationAngle")?.InnerText ?? string.Empty;
            XmlNode crpOffsetNode = configurationNode?.SelectSingleNode("CRPOffset");
            txtCRPX.Text = crpOffsetNode?.SelectSingleNode("X")?.InnerText ?? string.Empty;
            txtCRPY.Text = crpOffsetNode?.SelectSingleNode("Y")?.InnerText ?? string.Empty;
            txtCRPZ.Text = crpOffsetNode?.SelectSingleNode("Z")?.InnerText ?? string.Empty;
            XmlNode rssiCoefficientsNode = configurationNode?.SelectSingleNode("RSSICoefficients");
            txtRSSI1.Text = rssiCoefficientsNode?.SelectSingleNode("Beam1")?.InnerText ?? string.Empty;
            txtRSSI2.Text = rssiCoefficientsNode?.SelectSingleNode("Beam2")?.InnerText ?? string.Empty;
            txtRSSI3.Text = rssiCoefficientsNode?.SelectSingleNode("Beam3")?.InnerText ?? string.Empty;
            txtRSSI4.Text = rssiCoefficientsNode?.SelectSingleNode("Beam4")?.InnerText ?? string.Empty;
            XmlNode maskingNode = pd0Node?.SelectSingleNode("Masking");
            txtFirstEnsemble.Text = maskingNode?.SelectSingleNode("FirstEnsemble")?.InnerText ?? string.Empty;
            txtLastEnsemble.Text = maskingNode?.SelectSingleNode("LastEnsemble")?.InnerText ?? string.Empty;
            XmlNode maskEchoIntensityNode = maskingNode?.SelectSingleNode("MaskEchoIntensity");
            checkMaskEchoIntensity.Checked = (maskEchoIntensityNode as XmlElement)?.GetAttribute("Enabled") == "true";
            txtMinEchoIntensity.Text = maskEchoIntensityNode?.SelectSingleNode("Min")?.InnerText ?? string.Empty;
            txtMaxEchoIntensity.Text = maskEchoIntensityNode?.SelectSingleNode("Max")?.InnerText ?? string.Empty;
            XmlNode maskPercentGoodNode = maskingNode?.SelectSingleNode("MaskPercentGood");
            checkMaskPercentGood.Checked = (maskPercentGoodNode as XmlElement)?.GetAttribute("Enabled") == "true";
            txtMinPercentGood.Text = maskPercentGoodNode?.SelectSingleNode("Min")?.InnerText ?? string.Empty;
            XmlNode maskCorrelationMagnitudeNode = maskingNode?.SelectSingleNode("MaskCorrelationMagnitude");
            checkMaskCorrelationMagnitude.Checked = (maskCorrelationMagnitudeNode as XmlElement)?.GetAttribute("Enabled") == "true";
            txtMinCorrelationMagnitude.Text = maskCorrelationMagnitudeNode?.SelectSingleNode("Min")?.InnerText ?? string.Empty;
            txtMaxCorrelationMagnitude.Text = maskCorrelationMagnitudeNode?.SelectSingleNode("Max")?.InnerText ?? string.Empty;
            XmlNode maskCurrentSpeedNode = maskingNode?.SelectSingleNode("MaskCurrentSpeed");
            checkMaskingVelocity.Checked = (maskCurrentSpeedNode as XmlElement)?.GetAttribute("Enabled") == "true";
            txtMinVelocity.Text = maskCurrentSpeedNode?.SelectSingleNode("Min")?.InnerText ?? string.Empty;
            txtMaxVelocity.Text = maskCurrentSpeedNode?.SelectSingleNode("Max")?.InnerText ?? string.Empty;
            XmlNode maskErrorVelocityNode = maskingNode?.SelectSingleNode("MaskErrorVelocity");
            checkMaskingErrorVelocity.Checked = (maskErrorVelocityNode as XmlElement)?.GetAttribute("Enabled") == "true";
            txtMinErrorVelocity.Text = maskErrorVelocityNode?.SelectSingleNode("Min")?.InnerText ?? string.Empty;
            txtMaxErrorVelocity.Text = maskErrorVelocityNode?.SelectSingleNode("Max")?.InnerText ?? string.Empty;
            // Position related attributes
            XmlNode positionNode = adcpElement.SelectSingleNode("PositionData");
            txtPositionPath.Text = positionNode?.SelectSingleNode("Path")?.InnerText ?? string.Empty;
            comboDateTime.Items.Clear();
            comboX.Items.Clear();
            comboY.Items.Clear();
            comboHeading.Items.Clear();
            XmlNode positionColumns = positionNode?.SelectSingleNode("Columns");
            if (positionColumns != null)
            {
                foreach (XmlNode columnNode in positionColumns.ChildNodes)
                {
                    if (columnNode.NodeType == XmlNodeType.Element)
                    {
                        string columnName = columnNode.InnerText.Trim();
                        comboDateTime.Items.Add(columnName);
                        comboX.Items.Add(columnName);
                        comboY.Items.Add(columnName);
                        comboHeading.Items.Add(columnName);
                    }
                }
            }
            void SelectComboItem(ComboBox combo, string value)
            {
                int index = combo.Items.IndexOf(value.Trim());
                if (index >= 0)
                    combo.SelectedIndex = index;
            }
            SelectComboItem(comboDateTime, positionNode?.SelectSingleNode("DateTimeColumn")?.InnerText ?? "");
            SelectComboItem(comboX, positionNode?.SelectSingleNode("XColumn")?.InnerText ?? "");
            SelectComboItem(comboY, positionNode?.SelectSingleNode("YColumn")?.InnerText ?? "");
            SelectComboItem(comboHeading, positionNode?.SelectSingleNode("HeadingColumn")?.InnerText ?? "");

            // Enable controls based on loaded data
            boxConfiguration.Enabled = !string.IsNullOrEmpty(txtPD0Path.Text);
            boxMasking.Enabled = !string.IsNullOrEmpty(txtPD0Path.Text);
            boxPosition.Enabled = !string.IsNullOrEmpty(txtPositionPath.Text);
            btnPrintConfig.Enabled = !string.IsNullOrEmpty(txtPD0Path.Text);
            isSaved = true; // Mark as saved after loading

        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            Save();
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
                    Save(); // Save the current instrument
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not exit
                }
            }
            this.Close(); // Close the form
        }

        public int LoadPd0(string pd0Path)
        {
            Dictionary<string, string> inputs = new Dictionary<string, string>
                {
                    { "Task", "LoadPd0" },
                    { "Path", pd0Path},
                };

            string xmlInput = _Tools.GenerateInput(inputs);
            XmlDocument result = _Tools.CallPython(xmlInput);
            Dictionary<string, string> outputs = _Tools.ParseOutput(result);
            if (outputs.ContainsKey("Error"))
            {
                MessageBox.Show(outputs["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            int nEnsembles = Convert.ToInt32(outputs["NEnsembles"]);
            return nEnsembles;
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
                int nEnsembles = LoadPd0(ofd.FileName);
                txtPD0Path.Text = ofd.FileName;
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

        public int UpdateADCP()
        {
            adcpElement.SetAttribute("name", txtName.Text.Trim());
            XmlElement pd0Element = adcpElement.SelectSingleNode("Pd0") as XmlElement;
            XmlNode? pathNode = pd0Element?.SelectSingleNode("Path");
            if (pathNode != null)
            {
                pathNode.InnerText = txtPD0Path.Text.Trim();
            }
            else
            {
                return -1; // Return error if PD0 path node is not found
            }
            XmlElement configurationElement = pd0Element?.SelectSingleNode("Configuration") as XmlElement;
            XmlNode? magneticDeclinationNode = configurationElement?.SelectSingleNode("MagneticDeclination");
            if (magneticDeclinationNode != null)
            {
                magneticDeclinationNode.InnerText = txtMagneticDeclination.Text.Trim();
            }
            else
            {
                return -1; // Return error if MagneticDeclination node is not found
            }
            XmlNode? utcOffsetNode = configurationElement?.SelectSingleNode("UTCOffset");
            if (utcOffsetNode != null)
            {
                utcOffsetNode.InnerText = txtUTCOffset.Text.Trim();
            }
            else
            {
                return -1; // Return error if UTCOffset node is not found
            }
            XmlNode? rotationAngleNode = configurationElement?.SelectSingleNode("RotationAngle");
            if (rotationAngleNode != null)
            {
                rotationAngleNode.InnerText = txtRotationAngle.Text.Trim();
            }
            else
            {
                return -1; // Return error if RotationAngle node is not found
            }
            XmlElement crpOffsetElement = configurationElement?.SelectSingleNode("CRPOffset") as XmlElement;
            if (crpOffsetElement != null)
            {
                XmlNode? xNode = crpOffsetElement.SelectSingleNode("X");
                if (xNode != null)
                {
                    xNode.InnerText = txtCRPX.Text.Trim();
                }
                else
                {
                    return -1; // Return error if X node is not found
                }
                XmlNode? yNode = crpOffsetElement.SelectSingleNode("Y");
                if (yNode != null)
                {
                    yNode.InnerText = txtCRPY.Text.Trim();
                }
                else
                {
                    return -1; // Return error if Y node is not found
                }
                XmlNode? zNode = crpOffsetElement.SelectSingleNode("Z");
                if (zNode != null)
                {
                    zNode.InnerText = txtCRPZ.Text.Trim();
                }
                else
                {
                    return -1; // Return error if Z node is not found
                }
            }
            else
            {
                return -1; // Return error if CRPOffset element is not found
            }
            XmlElement rssiCoefficientsElement = configurationElement?.SelectSingleNode("RSSICoefficients") as XmlElement;
            if (rssiCoefficientsElement != null)
            {
                XmlNode? beam1Node = rssiCoefficientsElement.SelectSingleNode("Beam1");
                if (beam1Node != null)
                {
                    beam1Node.InnerText = txtRSSI1.Text.Trim();
                }
                else
                {
                    return -1; // Return error if Beam1 node is not found
                }
                XmlNode? beam2Node = rssiCoefficientsElement.SelectSingleNode("Beam2");
                if (beam2Node != null)
                {
                    beam2Node.InnerText = txtRSSI2.Text.Trim();
                }
                else
                {
                    return -1; // Return error if Beam2 node is not found
                }
                XmlNode? beam3Node = rssiCoefficientsElement.SelectSingleNode("Beam3");
                if (beam3Node != null)
                {
                    beam3Node.InnerText = txtRSSI3.Text.Trim();
                }
                else
                {
                    return -1; // Return error if Beam3 node is not found
                }
                XmlNode? beam4Node = rssiCoefficientsElement.SelectSingleNode("Beam4");
                if (beam4Node != null)
                {
                    beam4Node.InnerText = txtRSSI4.Text.Trim();
                }
                else
                {
                    return -1; // Return error if Beam4 node is not found
                }
            }
            else
            {
                return -1; // Return error if RSSICoefficients element is not found
            }
            XmlElement maskingElement = pd0Element?.SelectSingleNode("Masking") as XmlElement;
            if (maskingElement != null)
            {
                XmlNode? firstEnsembleNode = maskingElement.SelectSingleNode("FirstEnsemble");
                if (firstEnsembleNode != null)
                {
                    firstEnsembleNode.InnerText = txtFirstEnsemble.Text.Trim();
                }
                else
                {
                    return -1; // Return error if FirstEnsemble node is not found
                }
                XmlNode? lastEnsembleNode = maskingElement.SelectSingleNode("LastEnsemble");
                if (lastEnsembleNode != null)
                {
                    lastEnsembleNode.InnerText = txtLastEnsemble.Text.Trim();
                }
                else
                {
                    return -1; // Return error if LastEnsemble node is not found
                }
                XmlElement maskEchoIntensityElement = maskingElement.SelectSingleNode("MaskEchoIntensity") as XmlElement;
                if (maskEchoIntensityElement != null)
                {
                    maskEchoIntensityElement.SetAttribute("Enabled", checkMaskEchoIntensity.Checked.ToString().ToLower());
                    XmlNode? minNode = maskEchoIntensityElement.SelectSingleNode("Min");
                    if (minNode != null)
                    {
                        minNode.InnerText = txtMinEchoIntensity.Text.Trim();
                    }
                    else
                    {
                        return -1; // Return error if Min node is not found
                    }
                    XmlNode? maxNode = maskEchoIntensityElement.SelectSingleNode("Max");
                    if (maxNode != null)
                    {
                        maxNode.InnerText = txtMaxEchoIntensity.Text.Trim();
                    }
                    else
                    {
                        return -1; // Return error if Max node is not found
                    }
                }
                else
                {
                    return -1; // Return error if MaskEchoIntensity element is not found
                }
                XmlElement maskPercentGoodElement = maskingElement.SelectSingleNode("MaskPercentGood") as XmlElement;
                if (maskPercentGoodElement != null)
                {
                    maskPercentGoodElement.SetAttribute("Enabled", checkMaskPercentGood.Checked.ToString().ToLower());
                    XmlNode? minNode = maskPercentGoodElement.SelectSingleNode("Min");
                    if (minNode != null)
                    {
                        minNode.InnerText = txtMinPercentGood.Text.Trim();
                    }
                    else
                    {
                        return -1; // Return error if Min node is not found
                    }
                }
                else
                {
                    return -1; // Return error if MaskPercentGood element is not found
                }
                XmlElement maskCorrelationMagnitudeElement = maskingElement.SelectSingleNode("MaskCorrelationMagnitude") as XmlElement;
                if (maskCorrelationMagnitudeElement != null)
                {
                    maskCorrelationMagnitudeElement.SetAttribute("Enabled", checkMaskCorrelationMagnitude.Checked.ToString().ToLower());
                    XmlNode? minNode = maskCorrelationMagnitudeElement.SelectSingleNode("Min");
                    if (minNode != null)
                    {
                        minNode.InnerText = txtMinCorrelationMagnitude.Text.Trim();
                    }
                    else
                    {
                        return -1; // Return error if Min node is not found
                    }
                    XmlNode? maxNode = maskCorrelationMagnitudeElement.SelectSingleNode("Max");
                    if (maxNode != null)
                    {
                        maxNode.InnerText = txtMaxCorrelationMagnitude.Text.Trim();
                    }
                    else
                    {
                        return -1; // Return error if Max node is not found
                    }
                }
                else
                {
                    return -1; // Return error if MaskCorrelationMagnitude element is not found
                }
                XmlElement maskCurrentSpeedElement = maskingElement.SelectSingleNode("MaskCurrentSpeed") as XmlElement;
                if (maskCurrentSpeedElement != null)
                {
                    maskCurrentSpeedElement.SetAttribute("Enabled", checkMaskingVelocity.Checked.ToString().ToLower());
                    XmlNode? minNode = maskCurrentSpeedElement.SelectSingleNode("Min");
                    if (minNode != null)
                    {
                        minNode.InnerText = txtMinVelocity.Text.Trim();
                    }
                    else
                    {
                        return -1; // Return error if Min node is not found
                    }
                    XmlNode? maxNode = maskCurrentSpeedElement.SelectSingleNode("Max");
                    if (maxNode != null)
                    {
                        maxNode.InnerText = txtMaxVelocity.Text.Trim();
                    }
                    else
                    {
                        return -1; // Return error if Max node is not found
                    }
                }
                else
                {
                    return -1; // Return error if MaskCurrentSpeed element is not found
                }
                XmlElement maskErrorVelocityElement = maskingElement.SelectSingleNode("MaskErrorVelocity") as XmlElement;
                if (maskErrorVelocityElement != null)
                {
                    maskErrorVelocityElement.SetAttribute("Enabled", checkMaskingErrorVelocity.Checked.ToString().ToLower());
                    XmlNode? minNode = maskErrorVelocityElement.SelectSingleNode("Min");
                    if (minNode != null)
                    {
                        minNode.InnerText = txtMinErrorVelocity.Text.Trim();
                    }
                    else
                    {
                        return -1; // Return error if Min node is not found
                    }
                    XmlNode? maxNode = maskErrorVelocityElement.SelectSingleNode("Max");
                    if (maxNode != null)
                    {
                        maxNode.InnerText = txtMaxErrorVelocity.Text.Trim();
                    }
                    else
                    {
                        return -1; // Return error if Max node is not found
                    }
                }
                else
                {
                    return -1; // Return error if MaskErrorVelocity element is not found
                }
            }
            else
            {
                return -1; // Return error if Masking element is not found
            }
            XmlElement positionElement = adcpElement.SelectSingleNode("PositionData") as XmlElement;
            if (positionElement != null)
            {
                XmlNode? positionPathNode = positionElement.SelectSingleNode("Path");
                if (positionPathNode != null)
                {
                    positionPathNode.InnerText = txtPositionPath.Text.Trim();
                }
                else
                {
                    return -1; // Return error if PositionData Path node is not found
                }
                XmlNode? dateTimeColumnNode = positionElement.SelectSingleNode("DateTimeColumn");
                if (dateTimeColumnNode != null)
                {
                    dateTimeColumnNode.InnerText = comboDateTime.Text.Trim();
                }
                else
                {
                    return -1; // Return error if DateTimeColumn node is not found
                }
                XmlNode? xColumnNode = positionElement.SelectSingleNode("XColumn");
                if (xColumnNode != null)
                {
                    xColumnNode.InnerText = comboX.Text.Trim();
                }
                else
                {
                    return -1; // Return error if XColumn node is not found
                }
                XmlNode? yColumnNode = positionElement.SelectSingleNode("YColumn");
                if (yColumnNode != null)
                {
                    yColumnNode.InnerText = comboY.Text.Trim();
                }
                else
                {
                    return -1; // Return error if YColumn node is not found
                }
                XmlNode? headingColumnNode = positionElement.SelectSingleNode("HeadingColumn");
                if (headingColumnNode != null)
                {
                    headingColumnNode.InnerText = comboHeading.Text.Trim();
                }
                else
                {
                    return -1; // Return error if HeadingColumn node is not found
                }
            }
            else
            {
                return -1; // Return error if PositionData element is not found
            }

            return 1;
        }

        private string GetFullPath(string filePath)
        {
            if (Path.IsPathRooted(filePath))
            {
                return filePath;
            }
            else
            {
                string directory = _ClassConfigurationManager.GetSetting(settingName: "Directory");
                return Path.Combine(directory, filePath);
            }
        }

        public void Save()
        {
            if (String.IsNullOrEmpty(txtName.Text.Trim()))
            {
                MessageBox.Show("Please enter a name for the ADCP.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return; // Do not save if name is empty
            }
            if (String.IsNullOrEmpty(txtPD0Path.Text.Trim()))
            {
                MessageBox.Show("Please select a PD0 file.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return; // Do not save if PD0 path is empty
            }
            if (String.IsNullOrEmpty(txtPositionPath.Text.Trim()))
            {
                MessageBox.Show("Please select a position file.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return; // Do not save if position path is empty
            }
            if (comboDateTime.SelectedIndex < 0 || comboX.SelectedIndex < 0 || comboY.SelectedIndex < 0 || comboHeading.SelectedIndex < 0)
            {
                MessageBox.Show("Please select valid columns for DateTime, X, Y, and Heading.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return; // Do not save if any column is not selected
            }
            if (!File.Exists(GetFullPath(txtPD0Path.Text.Trim())))
            {
                MessageBox.Show("The specified PD0 file does not exist.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return; // Do not save if PD0 file does not exist
            }
            if (!File.Exists(GetFullPath(txtPositionPath.Text.Trim())))
            {
                MessageBox.Show("The specified position file does not exist.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return; // Do not save if position file does not exist
            }
            // Update the ADCP element with the current values
            int result = UpdateADCP();
            if (result < 0)
            {
                MessageBox.Show("Failed to update ADCP configuration.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return; // Do not save if update fails
            }
            // Save the updated ADCP element to the XML document
            _ClassConfigurationManager.SaveConfig(saveMode: 1);
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

        private void EditVesselMountedADCP_FormClosing(object sender, FormClosingEventArgs e)
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
                    Save(); // Save the current instrument
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Cancel the form closing event
                    return; // User chose to cancel, do not exit
                }
            }
        }

        
    }
}
