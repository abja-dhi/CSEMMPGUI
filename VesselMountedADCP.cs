using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics.Metrics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public partial class VesselMountedADCP : Form
    {

        public _SurveyManager? surveyManager;
        public XmlDocument? project;
        public int id;
        XmlElement? adcpElement;
        public bool isSaved;
        public int mode;
        public _ClassConfigurationManager _project = new();

        private void InitializeADCP()
        {
            id = _project.GetNextId();
            txtPD0Path.Text = string.Empty;
            txtPositionPath.Text = string.Empty;
            txtName.Text = "New Vessel Mounted ADCP";
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
            txtTransectShiftX.Text = "0.0";
            txtTransectShiftY.Text = "0.0";
            txtTransectShiftZ.Text = "0.0";
            txtTransectShiftT.Text = "0.0";
            txtC.Text = "-139.0";
            txtPdbw.Text = "9";
            txtEr.Text = "39";
            checkFirstEnsemble.Checked = false;
            txtFirstEnsemble.Text = "1";
            txtFirstEnsemble.Enabled = false;
            checkLastEnsemble.Checked = false;
            txtLastEnsemble.Text = "1";
            txtLastEnsemble.Enabled = false;
            checkStartDatetime.Checked = false;
            txtStartDatetime.Text = String.Empty;
            txtStartDatetime.Enabled = false;
            checkEndDatetime.Checked = false;
            txtEndDatetime.Text = String.Empty;
            txtEndDatetime.Enabled = false;
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
            checkMaskingAbs.Checked = false;
            txtMinAbs.Text = String.Empty;
            txtMaxAbs.Text = String.Empty;
            txtMinAbs.Enabled = false;
            txtMaxAbs.Enabled = false;
            boxConfiguration.Enabled = false;
            boxMasking.Enabled = false;
            boxPosition.Enabled = false;
            btnPrintConfig.Enabled = false;
            rbSingle.Checked = true; // Default to single file mode
            comboDateTime.Items.Clear();
            comboX.Items.Clear();
            comboY.Items.Clear();
            comboHeading.Items.Clear();
            comboSSCModel.Items.Clear();
            comboDateTime.Text = string.Empty;
            comboX.Text = string.Empty;
            comboY.Text = string.Empty;
            comboHeading.Text = string.Empty;
            comboSSCModel.Text = string.Empty;
            txtPitch.Text = "0.0";
            txtRoll.Text = "0.0";
            rbSingle.Checked = true; // Default to single file mode
            project = surveyManager.survey.OwnerDocument;
            isSaved = true; // Initially, the instrument is not saved
        }

        private void PopulateADCP()
        {
            txtName.Text = adcpElement.GetAttribute("name");
            // Pd0 related attributes
            XmlNode pd0Node = adcpElement.SelectSingleNode("Pd0");
            txtPD0Path.Text = pd0Node?.SelectSingleNode("Path")?.InnerText ?? string.Empty;
            List<XmlElement> bks2sscModels = _project.GetObjects("BKS2SSC");
            if (bks2sscModels.Count > 0)
            {
                comboSSCModel.Items.Clear();
                foreach (XmlElement model in bks2sscModels)
                {
                    comboSSCModel.Items.Add(new
                    {
                        Display = model.GetAttribute("name"),
                        Tag = model.GetAttribute("id")
                    });
                }
                comboSSCModel.DisplayMember = "Display";
                string sscModelId = pd0Node?.SelectSingleNode("SSCModel")?.InnerText ?? string.Empty;
                if (!string.IsNullOrEmpty(sscModelId))
                {
                    for (int i = 0; i < comboSSCModel.Items.Count; i++)
                    {
                        string itemTag = ((dynamic)comboSSCModel.Items[i]).Tag;
                        if (itemTag == sscModelId)
                        {
                            comboSSCModel.SelectedIndex = i;
                            break;
                        }
                    }
                }
                comboSSCModel.Enabled = true; // Enable if models are available
                lblSSCModel.Enabled = true; // Enable label if models are available
            }
            else
            {
                comboSSCModel.Items.Clear();
                comboSSCModel.Enabled = false; // Disable if no models are available
                lblSSCModel.Enabled = false; // Disable label if no models are available
            }
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
            XmlNode transectShiftNode = configurationNode?.SelectSingleNode("TransectShift");
            txtTransectShiftX.Text = transectShiftNode?.SelectSingleNode("X")?.InnerText ?? string.Empty;
            txtTransectShiftY.Text = transectShiftNode?.SelectSingleNode("Y")?.InnerText ?? string.Empty;
            txtTransectShiftZ.Text = transectShiftNode?.SelectSingleNode("Z")?.InnerText ?? string.Empty;
            txtTransectShiftT.Text = transectShiftNode?.SelectSingleNode("T")?.InnerText ?? string.Empty;
            txtC.Text = configurationNode?.SelectSingleNode("C")?.InnerText ?? string.Empty;
            txtPdbw.Text = configurationNode?.SelectSingleNode("Pdbw")?.InnerText ?? string.Empty;
            txtEr.Text = configurationNode?.SelectSingleNode("Er")?.InnerText ?? string.Empty;
            XmlNode maskingNode = pd0Node?.SelectSingleNode("Masking");
            XmlNode maskFirstEnsemble = maskingNode?.SelectSingleNode("FirstEnsemble");
            checkFirstEnsemble.Checked = (maskFirstEnsemble as XmlElement)?.GetAttribute("Enabled") == "true";
            txtFirstEnsemble.Value = int.TryParse(maskFirstEnsemble?.InnerText, out int firstEnsemble) ? firstEnsemble : 1;
            XmlNode maskLastEnsemble = maskingNode?.SelectSingleNode("LastEnsemble");
            checkLastEnsemble.Checked = (maskLastEnsemble as XmlElement)?.GetAttribute("Enabled") == "true";
            txtLastEnsemble.Value = int.TryParse(maskLastEnsemble?.InnerText, out int lastEnsemble) ? lastEnsemble : 1;
            XmlNode maskStartDatetime = maskingNode?.SelectSingleNode("StartDatetime");
            checkStartDatetime.Checked = (maskStartDatetime as XmlElement)?.GetAttribute("Enabled") == "true";
            txtStartDatetime.Text = maskStartDatetime?.InnerText ?? string.Empty;
            XmlNode maskEndDatetime = maskingNode?.SelectSingleNode("EndDatetime");
            checkEndDatetime.Checked = (maskEndDatetime as XmlElement)?.GetAttribute("Enabled") == "true";
            txtEndDatetime.Text = maskEndDatetime?.InnerText ?? string.Empty;
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

        public VesselMountedADCP(_SurveyManager? _surveyManager, XmlNode? adcpNode)
        {
            InitializeComponent();
            if (adcpNode == null)
            {
                surveyManager = _surveyManager;
                InitializeADCP();
                mode = 0; // New ADCP
                this.Text = "Add Vessel Mounted ADCP";
            }
            else
            {
                adcpElement = adcpNode as XmlElement;
                PopulateADCP();
                menuNew.Visible = false;
                tableMode.Visible = false;
                rbSingle.Checked = true; // Default to single file mode
                mode = 1; // Edit ADCP
                this.Text = "Edit Vessel Mounted ADCP";
            }

            this.KeyPreview = true; // Enable form to capture key events
            this.KeyDown += VesselMountedADCP_KeyDown; // Attach key down event handler
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current vessel mounted ADCP has unsaved changes. Do you want to save them before creating a new one?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveADCP();
                    if (status == 1)
                        InitializeADCP(); // Reinitialize the form for a new instrument
                    else
                        return; // If saving failed, do not create a new instrument
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not create a new instrument
                }
                else if (result == DialogResult.No)
                {
                    InitializeADCP(); // Reinitialize the form for a new instrument without saving
                }
            }
            else
            {
                InitializeADCP(); // Reinitialize the form for a new instrument
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveADCP();
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current vessel mounted ADCP has unsaved changes. Do you want to save them before exiting?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveADCP();
                    if (status == 1)
                    {
                        this.Close();
                        return;
                    }
                    else
                        return;
                }
                else if (result == DialogResult.Cancel)
                {
                    return;
                }
                else if (result == DialogResult.No)
                {
                    this.Close(); // Close without saving
                }
            }
            else
            {
                this.Close(); // Close without any prompt if already saved
            }
        }

        private void VesselMountedADCP_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current vessel mounted ADCP has unsaved changes. Do you want to save them before exiting?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveADCP();
                    if (status == 0)
                        e.Cancel = true;
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Cancel the closing event
                }
            }
        }

        private void input_Changed(object sender, EventArgs e)
        {
            isSaved = false; // Mark as unsaved changes
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
                lblName.Text = "Name";
                btnPrintConfig.Enabled = true;
            }
            else
            {
                lblPD0File.Text = "Folder";
                lblPositionFile.Visible = false;
                txtPositionPath.Visible = false;
                btnLoadPosition.Visible = false;
                boxFileInfo.Text = "Folder Information";
                lblName.Text = "Prefix";
                btnPrintConfig.Enabled = false; // Disable print config for folder mode
            }
        }

        private bool IsValidFolder(string folderPath)
        {
            string[] pd0Files = Directory.GetFiles(txtPD0Path.Text, "*r.000");

            if (pd0Files.Length == 0)
            {
                MessageBox.Show("No .000 files were found in the selected folder.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                rbSingle.Checked = true; // Revert to single mode
                return false;
            }

            List<string> missingCsvFiles = new();

            foreach (string pd0Path in pd0Files)
            {
                string baseName = Path.GetFileNameWithoutExtension(pd0Path);
                if (baseName.EndsWith("r", StringComparison.OrdinalIgnoreCase))
                    baseName = baseName.Substring(0, baseName.Length - 1);

                string[] matches = Directory.GetFiles(folderPath, baseName + "*.csv");
                if (matches.Length == 0)
                    missingCsvFiles.Add(baseName + "*.csv");
            }

            if (missingCsvFiles.Count > 0)
            {
                string message = "The following .csv files are missing for corresponding .000 files:\n\n" +
                                 string.Join("\n", missingCsvFiles);
                MessageBox.Show(message, "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                rbSingle.Checked = true; // Revert to single mode
                return false;
            }

            return true;
        }

        public void updateCombo(ComboBox combo, string[] items, int index)
        {
            combo.Items.Clear();
            combo.Items.AddRange(items);
            combo.SelectedIndex = index;
        }

        //public int LoadPd0(string pd0Path)
        //{
        //    Dictionary<string, string> inputs = new Dictionary<string, string>
        //        {
        //            { "Task", "LoadPd0" },
        //            { "Path", pd0Path},
        //        };

        //    string xmlInput = _Tools.GenerateInput(inputs);
        //    XmlDocument result = _Tools.CallPython(xmlInput);
        //    Dictionary<string, string> outputs = _Tools.ParseOutput(result);
        //    if (outputs.ContainsKey("Error"))
        //    {
        //        MessageBox.Show(outputs["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        //        return 0;
        //    }
        //    int nEnsembles = Convert.ToInt32(outputs["NEnsembles"]);
        //    return nEnsembles;
        //}

        private void btnLoadPD0_Click(object sender, EventArgs e)
        {
            if (rbSingle.Checked)
            {
                var ofd = new OpenFileDialog
                {
                    Filter = "PD0 files (*.000)|*.000",
                    Title = "Select PD0 File",
                    InitialDirectory = _project.GetSetting(settingName: "Directory")
                };
                if (ofd.ShowDialog() == DialogResult.OK)
                {
                    //int nEnsembles = LoadPd0(ofd.FileName);
                    txtPD0Path.Text = ofd.FileName;
                    //txtLastEnsemble.Maximum = nEnsembles;
                    //txtLastEnsemble.Value = nEnsembles;
                    boxConfiguration.Enabled = true;
                    boxMasking.Enabled = true;
                    tableMaskingEnsembles.Enabled = true;
                    btnPrintConfig.Enabled = true;
                    isSaved = false; // Mark as unsaved after loading a new PD0 file
                }
                else
                {
                    return; // User cancelled the file dialog
                }
            }
            else
            {
                using (FolderBrowserDialog fbd = new FolderBrowserDialog())
                {
                    string[] columns = Array.Empty<string>();
                    fbd.Description = "Select folder containing .000 and .csv files";
                    fbd.SelectedPath = _project.GetSetting("Directory");

                    if (fbd.ShowDialog() == DialogResult.OK)
                    {
                        txtPD0Path.Text = fbd.SelectedPath;
                        bool valid = IsValidFolder(fbd.SelectedPath);
                        if (valid)
                        {
                            boxConfiguration.Enabled = true;
                            boxMasking.Enabled = true;
                            btnPrintConfig.Enabled = true;
                            // Get the first  position file in the folder to select columns
                            string[] pd0Files = Directory.GetFiles(txtPD0Path.Text, "*r.000");
                            // Get the .csv files that correspond to the .000 files by basename
                            string[] positionFiles = pd0Files
                                .Select(pd0 =>
                                {
                                    string filename = Path.GetFileNameWithoutExtension(pd0);
                                    if (filename.EndsWith("r", StringComparison.OrdinalIgnoreCase))
                                        filename = filename.Substring(0, filename.Length - 1); // Remove trailing "r"

                                    string[] matches = Directory.GetFiles(txtPD0Path.Text, filename + "*.csv");
                                    return matches.FirstOrDefault(); // or LastOrDefault() if you want most recent-looking
                                })
                                .ToArray();
                            string firstPositionFile = positionFiles.FirstOrDefault(File.Exists);
                            int nLines = File.ReadAllLines(firstPositionFile).Length;
                            UtilsCSVImportOptions csvOptions = new UtilsCSVImportOptions(nLines);
                            if (csvOptions.ShowDialog() == DialogResult.OK)
                            {
                                int headerLines = csvOptions._headerLine;
                                string delimiter = csvOptions._delimiter;
                                columns = _Utils.ParseCSVAndReturnColumns(firstPositionFile, delimiter, headerLines);
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
                            boxPosition.Enabled = true;
                            updateCombo(comboDateTime, columns, 0);
                            updateCombo(comboX, columns, 1);
                            updateCombo(comboY, columns, 2);
                            updateCombo(comboHeading, columns, 3);
                            tableMaskingEnsembles.Enabled = false;
                            txtFirstEnsemble.Text = "1";
                            txtLastEnsemble.Text = "9999";
                            btnPrintConfig.Enabled = false;
                            isSaved = false; // Mark as unsaved after loading a new position file
                        }
                        else
                        {
                            return; // If validation fails, do not proceed
                        }
                    }
                    else
                    {
                        return;
                    }
                }
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
                    int headerLines = csvOptions._headerLine;
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
            List<XmlElement> bks2sscModels = _project.GetObjects(type: "BKS2SSC");
            if (bks2sscModels.Count > 0)
            {
                comboSSCModel.Items.Clear();
                foreach (XmlElement model in bks2sscModels)
                {
                    comboSSCModel.Items.Add(new
                    {
                        Display = model.GetAttribute("name"),
                        Tag = model.GetAttribute("id")
                    });
                }
                comboSSCModel.DisplayMember = "Display";
                comboSSCModel.Enabled = true; // Enable if models are available
                lblSSCModel.Enabled = true; // Enable label if models are available
                comboSSCModel.SelectedIndex = 0; // Select the first model by default
            }
            else
            {
                MessageBox.Show(
                    "No Backscatter to SSC models found. Please add one and update the setting later",
                    Text = "Warning",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);
                comboSSCModel.Items.Clear();
                comboSSCModel.Enabled = false; // Disable if no models are available
                lblSSCModel.Enabled = false; // Disable label if no models are available
            }
            isSaved = false; // Mark as unsaved after loading a new position file
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

        private void checkFirstEnsemble_CheckedChanged(object sender, EventArgs e)
        {
            if (checkFirstEnsemble.Checked)
            {
                txtFirstEnsemble.Enabled = true;
            }
            else
            {
                txtFirstEnsemble.Enabled = false;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private void checkLastEnsemble_CheckedChanged(object sender, EventArgs e)
        {
            if (checkLastEnsemble.Checked)
            {
                txtLastEnsemble.Enabled = true;
            }
            else
            {
                txtLastEnsemble.Enabled = false;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private void checkStartDatetime_CheckedChanged(object sender, EventArgs e)
        {
            if (checkStartDatetime.Checked)
            {
                txtStartDatetime.Enabled = true;
            }
            else
            {
                txtStartDatetime.Enabled = false;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private void checkEndDatetime_CheckedChanged(object sender, EventArgs e)
        {
            if (checkEndDatetime.Checked)
            {
                txtEndDatetime.Enabled = true;
            }
            else
            {
                txtEndDatetime.Enabled = false;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private void checkMaskEchoIntensity_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskEchoIntensity.Checked)
            {
                lblMaxEchoIntensity.Enabled = true;
                txtMaxEchoIntensity.Enabled = true;
                lblMinEchoIntensity.Enabled = true;
                txtMinEchoIntensity.Enabled = true;
            }
            else
            {
                lblMaxEchoIntensity.Enabled = false;
                txtMaxEchoIntensity.Enabled = false;
                lblMinEchoIntensity.Enabled = false;
                txtMinEchoIntensity.Enabled = false;
            }
            isSaved = false; // Mark as unsaved changes
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
            isSaved = false; // Mark as unsaved changes
        }

        private void checkMaskCorrelationMagnitude_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskCorrelationMagnitude.Checked)
            {
                lblMinCorrelationMagnitude.Enabled = true;
                txtMinCorrelationMagnitude.Enabled = true;
                lblMaxCorrelationMagnitude.Enabled = true;
                txtMaxCorrelationMagnitude.Enabled = true;
            }
            else
            {
                lblMinCorrelationMagnitude.Enabled = false;
                txtMinCorrelationMagnitude.Enabled = false;
                lblMaxCorrelationMagnitude.Enabled = false;
                txtMaxCorrelationMagnitude.Enabled = false;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private void checkMaskingVelocity_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskingVelocity.Checked)
            {
                lblMinVelocity.Enabled = true;
                txtMinVelocity.Enabled = true;
                lblMaxVelocity.Enabled = true;
                txtMaxVelocity.Enabled = true;
            }
            else
            {
                lblMinVelocity.Enabled = false;
                txtMinVelocity.Enabled = false;
                lblMaxVelocity.Enabled = false;
                txtMaxVelocity.Enabled = false;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private void checkMaskingErrorVelocity_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskingErrorVelocity.Checked)
            {
                lblMinErrorVelocity.Enabled = true;
                txtMinErrorVelocity.Enabled = true;
                lblMaxErrorVelocity.Enabled = true;
                txtMaxErrorVelocity.Enabled = true;
            }
            else
            {
                lblMinErrorVelocity.Enabled = false;
                txtMinErrorVelocity.Enabled = false;
                lblMaxErrorVelocity.Enabled = false;
                txtMaxErrorVelocity.Enabled = false;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private int SaveADCP()
        {
            if (String.IsNullOrEmpty(txtName.Text.Trim()))
            {
                MessageBox.Show("Please enter a name for the instrument before saving.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            if (rbBatch.Checked && !IsValidFolder(txtPD0Path.Text.Trim()))
            {
                MessageBox.Show("Please select a valid folder containing .000 files and corresponding .csv files before saving.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0; // Do not save if folder is invalid
            }
            if (rbSingle.Checked && String.IsNullOrEmpty(txtPD0Path.Text.Trim()))
            {
                MessageBox.Show("Please select a PD0 file before saving.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            if (!rbSingle.Checked && String.IsNullOrEmpty(txtPD0Path.Text.Trim()))
            {
                MessageBox.Show("Please select a folder containing .000 files before saving.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            if (rbSingle.Checked && String.IsNullOrEmpty(txtPositionPath.Text.Trim()))
            {
                MessageBox.Show("Please select a position file before saving.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            if (rbSingle.Checked && !File.Exists(_Utils.GetFullPath(txtPD0Path.Text.Trim())))
            {
                MessageBox.Show("The specified PD0 file does not exist.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0; // Do not save if PD0 file does not exist
            }
            if (rbSingle.Checked && !File.Exists(_Utils.GetFullPath(txtPositionPath.Text.Trim())))
            {
                MessageBox.Show("The specified position file does not exist.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0; // Do not save if position file does not exist
            }
            if (comboDateTime.SelectedIndex < 0 || comboX.SelectedIndex < 0 || comboY.SelectedIndex < 0 || comboHeading.SelectedIndex < 0)
            {
                MessageBox.Show("Please select valid columns for DateTime, X, Y, and Heading.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0; // Do not save if any column is not selected
            }
            if (mode == 0)
                SAVE();
            else
                UPDATE();
            isSaved = true;
            return 1;
        }

        private void CreateADCP(string name, string pd0FilePath, string positionFilePath)
        {
            adcpElement = project.CreateElement("VesselMountedADCP");
            id = _project.GetNextId();
            adcpElement.SetAttribute("id", id.ToString());
            adcpElement.SetAttribute("type", "VesselMountedADCP");
            adcpElement.SetAttribute("name", name);
            while (adcpElement.HasChildNodes && adcpElement.FirstChild != null)
            {
                adcpElement.RemoveChild(adcpElement.FirstChild);
            }
            // Pd0 related attributes
            XmlElement pd0 = project.CreateElement("Pd0");
            XmlElement pd0Path = project.CreateElement("Path");
            pd0Path.InnerText = pd0FilePath;
            pd0.AppendChild(pd0Path);
            XmlElement bks2sscModel = project.CreateElement("SSCModel");
            List<XmlElement> bks2sscModels = _project.GetObjects(type: "BKS2SSC");
            if (bks2sscModels.Count == 0)
            {
                bks2sscModel.InnerText = string.Empty;
            }
            else
            {
                var selectedItem = comboSSCModel.SelectedItem;
                string selectedId = selectedItem != null ? ((dynamic)selectedItem).Tag : bks2sscModels[0].GetAttribute("id");
                bks2sscModel.InnerText = selectedId;
            }
            pd0.AppendChild(bks2sscModel);
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

            XmlElement transectShoft = project.CreateElement("TransectShift");
            XmlElement transectShiftX = project.CreateElement("X");
            transectShiftX.InnerText = txtTransectShiftX.Text.Trim();
            XmlElement transectShiftY = project.CreateElement("Y");
            transectShiftY.InnerText = txtTransectShiftY.Text.Trim();
            XmlElement transectShiftZ = project.CreateElement("Z");
            transectShiftZ.InnerText = txtTransectShiftZ.Text.Trim();
            XmlElement transectShiftT = project.CreateElement("T");
            transectShiftT.InnerText = txtTransectShiftT.Text.Trim();
            transectShoft.AppendChild(transectShiftX);
            transectShoft.AppendChild(transectShiftY);
            transectShoft.AppendChild(transectShiftZ);
            transectShoft.AppendChild(transectShiftT);
            configuration.AppendChild(transectShoft);

            XmlElement c = project.CreateElement("C");
            c.InnerText = txtC.Text.Trim();
            configuration.AppendChild(c);

            XmlElement pdbw = project.CreateElement("Pdbw");
            pdbw.InnerText = txtPdbw.Text.Trim();
            configuration.AppendChild(pdbw);

            XmlElement er = project.CreateElement("Er");
            er.InnerText = txtEr.Text.Trim();
            configuration.AppendChild(er);

            pd0.AppendChild(configuration);

            XmlElement masking = project.CreateElement("Masking");
            XmlElement firstEnsemble = project.CreateElement("FirstEnsemble");
            firstEnsemble.SetAttribute("Enabled", checkFirstEnsemble.Checked.ToString().ToLower());
            firstEnsemble.InnerText = txtFirstEnsemble.Text.Trim();
            masking.AppendChild(firstEnsemble);
            XmlElement lastEnsemble = project.CreateElement("LastEnsemble");
            lastEnsemble.SetAttribute("Enabled", checkLastEnsemble.Checked.ToString().ToLower());
            lastEnsemble.InnerText = txtLastEnsemble.Text.Trim();
            masking.AppendChild(lastEnsemble);
            XmlElement startDatetime = project.CreateElement("StartDatetime");
            startDatetime.SetAttribute("Enabled", checkStartDatetime.Checked.ToString().ToLower());
            startDatetime.InnerText = txtStartDatetime.Text.Trim();
            masking.AppendChild(startDatetime);
            XmlElement endDatetime = project.CreateElement("EndDatetime");
            endDatetime.SetAttribute("Enabled", checkEndDatetime.Checked.ToString().ToLower());
            endDatetime.InnerText = txtEndDatetime.Text.Trim();
            masking.AppendChild(endDatetime);
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

            adcpElement.AppendChild(pd0);

            // Position related attributes
            XmlElement position = project.CreateElement("PositionData");
            XmlElement positionPath = project.CreateElement("Path");
            positionPath.InnerText = positionFilePath;
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

            XmlElement pitchValue = project.CreateElement("Pitch");
            pitchValue.InnerText = txtPitch.Text.Trim();
            position.AppendChild(pitchValue);

            XmlElement rollValue = project.CreateElement("Roll");
            rollValue.InnerText = txtRoll.Text.Trim();
            position.AppendChild(rollValue);

            adcpElement.AppendChild(position);
        }

        private void SAVE()
        {
            if (rbSingle.Checked)
            {
                string name = txtName.Text.Trim();
                string pd0FilePath = _Utils.GetFullPath(txtPD0Path.Text.Trim());
                string positionFilePath = _Utils.GetFullPath(txtPositionPath.Text.Trim());
                CreateADCP(name, pd0FilePath, positionFilePath);
                surveyManager.survey.AppendChild(adcpElement);
                surveyManager.SaveSurvey(name: surveyManager.GetAttribute(attribute: "name"));
                _project.SaveConfig(saveMode: 1);
            }
            else
            {
                string[] pd0Files = Directory.GetFiles(txtPD0Path.Text, "*r.000");
                // Get the .csv files that correspond to the .000 files by basename
                string[] positionFiles = pd0Files
                    .Select(pd0 =>
                    {
                        string filename = Path.GetFileNameWithoutExtension(pd0);
                        if (filename.EndsWith("r", StringComparison.OrdinalIgnoreCase))
                            filename = filename.Substring(0, filename.Length - 1); // Remove trailing "r"

                        string[] matches = Directory.GetFiles(txtPD0Path.Text, filename + "*.csv");
                        return matches.FirstOrDefault(); // or LastOrDefault() if you want most recent-looking
                    })
                    .ToArray();
                string prefix = txtName.Text.Trim();
                for (int i = 0; i < pd0Files.Length; i++)
                {
                    string pd0FilePath = pd0Files[i];
                    string positionFilePath = positionFiles[i];
                    string name = $"{prefix} {i + 1}";
                    CreateADCP(name, pd0FilePath, positionFilePath);
                    surveyManager.survey.AppendChild(adcpElement);
                    surveyManager.SaveSurvey(name: surveyManager.GetAttribute(attribute: "name"));
                    _project.SaveConfig(saveMode: 1);
                }
            }
        }

        private void UPDATE()
        {
            adcpElement.SetAttribute("name", txtName.Text.Trim());
            XmlElement pd0Element = adcpElement.SelectSingleNode("Pd0") as XmlElement;
            XmlNode? pathNode = pd0Element?.SelectSingleNode("Path");
            pathNode.InnerText = txtPD0Path.Text.Trim();
            XmlNode? sscModelNode = pd0Element?.SelectSingleNode("SSCModel");
            var selectedItem = comboSSCModel.SelectedItem;
            string selectedId = selectedItem != null ? ((dynamic)selectedItem).Tag : string.Empty;
            sscModelNode.InnerText = selectedId;
            XmlElement configurationElement = pd0Element?.SelectSingleNode("Configuration") as XmlElement;
            XmlNode? magneticDeclinationNode = configurationElement?.SelectSingleNode("MagneticDeclination");
            magneticDeclinationNode.InnerText = txtMagneticDeclination.Text.Trim();
            XmlNode? utcOffsetNode = configurationElement?.SelectSingleNode("UTCOffset");
            utcOffsetNode.InnerText = txtUTCOffset.Text.Trim();
            XmlNode? rotationAngleNode = configurationElement?.SelectSingleNode("RotationAngle");
            rotationAngleNode.InnerText = txtRotationAngle.Text.Trim();
            XmlElement crpOffsetElement = configurationElement?.SelectSingleNode("CRPOffset") as XmlElement;
            XmlNode? xNode = crpOffsetElement.SelectSingleNode("X");
            xNode.InnerText = txtCRPX.Text.Trim();
            XmlNode? yNode = crpOffsetElement.SelectSingleNode("Y");
            yNode.InnerText = txtCRPY.Text.Trim();
            XmlNode? zNode = crpOffsetElement.SelectSingleNode("Z");
            zNode.InnerText = txtCRPZ.Text.Trim();
            XmlElement rssiCoefficientsElement = configurationElement?.SelectSingleNode("RSSICoefficients") as XmlElement;
            XmlNode? beam1Node = rssiCoefficientsElement.SelectSingleNode("Beam1");
            beam1Node.InnerText = txtRSSI1.Text.Trim();
            XmlNode? beam2Node = rssiCoefficientsElement.SelectSingleNode("Beam2");
            beam2Node.InnerText = txtRSSI2.Text.Trim();
            XmlNode? beam3Node = rssiCoefficientsElement.SelectSingleNode("Beam3");
            beam3Node.InnerText = txtRSSI3.Text.Trim();
            XmlNode? beam4Node = rssiCoefficientsElement.SelectSingleNode("Beam4");
            beam4Node.InnerText = txtRSSI4.Text.Trim();
            XmlElement transectShiftElement = configurationElement?.SelectSingleNode("TransectShift") as XmlElement;
            XmlNode? transectShiftXNode = transectShiftElement.SelectSingleNode("X");
            transectShiftXNode.InnerText = txtTransectShiftX.Text.Trim();
            XmlNode? transectShiftYNode = transectShiftElement.SelectSingleNode("Y");
            transectShiftYNode.InnerText = txtTransectShiftY.Text.Trim();
            XmlNode? transectShiftZNode = transectShiftElement.SelectSingleNode("Z");
            transectShiftZNode.InnerText = txtTransectShiftZ.Text.Trim();
            XmlNode? transectShiftTNode = transectShiftElement.SelectSingleNode("T");
            transectShiftTNode.InnerText = txtTransectShiftT.Text.Trim();
            XmlNode? cNode = configurationElement?.SelectSingleNode("C");
            cNode.InnerText = txtC.Text.Trim();
            XmlNode? pdbwNode = configurationElement?.SelectSingleNode("Pdbw");
            pdbwNode.InnerText = txtPdbw.Text.Trim();
            XmlNode? erNode = configurationElement?.SelectSingleNode("Er");
            erNode.InnerText = txtEr.Text.Trim();
            XmlElement maskingElement = pd0Element?.SelectSingleNode("Masking") as XmlElement;
            XmlElement? firstEnsembleNode = maskingElement.SelectSingleNode("FirstEnsemble") as XmlElement;
            firstEnsembleNode.SetAttribute("Enabled", checkFirstEnsemble.Checked.ToString().ToLower());
            firstEnsembleNode.InnerText = txtFirstEnsemble.Text.Trim();
            XmlElement? lastEnsembleNode = maskingElement.SelectSingleNode("LastEnsemble") as XmlElement;
            lastEnsembleNode.SetAttribute("Enabled", checkLastEnsemble.Checked.ToString().ToLower());
            lastEnsembleNode.InnerText = txtLastEnsemble.Text.Trim();
            XmlElement? startDatetimeNode = maskingElement.SelectSingleNode("StartDatetime") as XmlElement;
            startDatetimeNode.SetAttribute("Enabled", checkStartDatetime.Checked.ToString().ToLower());
            startDatetimeNode.InnerText = txtStartDatetime.Text.Trim();
            XmlElement? endDatetimeNode = maskingElement.SelectSingleNode("EndDatetime") as XmlElement;
            endDatetimeNode.SetAttribute("Enabled", checkEndDatetime.Checked.ToString().ToLower());
            endDatetimeNode.InnerText = txtEndDatetime.Text.Trim();
            XmlElement maskEchoIntensityElement = maskingElement.SelectSingleNode("MaskEchoIntensity") as XmlElement;
            maskEchoIntensityElement.SetAttribute("Enabled", checkMaskEchoIntensity.Checked.ToString().ToLower());
            XmlNode? minEchoIntensityNode = maskEchoIntensityElement.SelectSingleNode("Min");
            minEchoIntensityNode.InnerText = txtMinEchoIntensity.Text.Trim();
            XmlNode? maxEchoIntensityNode = maskEchoIntensityElement.SelectSingleNode("Max");
            maxEchoIntensityNode.InnerText = txtMaxEchoIntensity.Text.Trim();
            XmlElement maskPercentGoodElement = maskingElement.SelectSingleNode("MaskPercentGood") as XmlElement;
            maskPercentGoodElement.SetAttribute("Enabled", checkMaskPercentGood.Checked.ToString().ToLower());
            XmlNode? minPercentGoodNode = maskPercentGoodElement.SelectSingleNode("Min");
            minPercentGoodNode.InnerText = txtMinPercentGood.Text.Trim();
            XmlElement maskCorrelationMagnitudeElement = maskingElement.SelectSingleNode("MaskCorrelationMagnitude") as XmlElement;
            maskCorrelationMagnitudeElement.SetAttribute("Enabled", checkMaskCorrelationMagnitude.Checked.ToString().ToLower());
            XmlNode? minCorrelationMagnitudeNode = maskCorrelationMagnitudeElement.SelectSingleNode("Min");
            minCorrelationMagnitudeNode.InnerText = txtMinCorrelationMagnitude.Text.Trim();
            XmlNode? maxCorrelationMagnitudeNode = maskCorrelationMagnitudeElement.SelectSingleNode("Max");
            maxCorrelationMagnitudeNode.InnerText = txtMaxCorrelationMagnitude.Text.Trim();
            XmlElement maskCurrentSpeedElement = maskingElement.SelectSingleNode("MaskCurrentSpeed") as XmlElement;
            maskCurrentSpeedElement.SetAttribute("Enabled", checkMaskingVelocity.Checked.ToString().ToLower());
            XmlNode? minCurrentSpeedNode = maskCurrentSpeedElement.SelectSingleNode("Min");
            minCurrentSpeedNode.InnerText = txtMinVelocity.Text.Trim();
            XmlNode? maxCurrentSpeedNode = maskCurrentSpeedElement.SelectSingleNode("Max");
            maxCurrentSpeedNode.InnerText = txtMaxVelocity.Text.Trim();
            XmlElement maskErrorVelocityElement = maskingElement.SelectSingleNode("MaskErrorVelocity") as XmlElement;
            maskErrorVelocityElement.SetAttribute("Enabled", checkMaskingErrorVelocity.Checked.ToString().ToLower());
            XmlNode? minErrorVelocityNode = maskErrorVelocityElement.SelectSingleNode("Min");
            minErrorVelocityNode.InnerText = txtMinErrorVelocity.Text.Trim();
            XmlNode? maxErrorVelocityNode = maskErrorVelocityElement.SelectSingleNode("Max");
            maxErrorVelocityNode.InnerText = txtMaxErrorVelocity.Text.Trim();
            XmlElement positionElement = adcpElement.SelectSingleNode("PositionData") as XmlElement;
            XmlNode? positionPathNode = positionElement.SelectSingleNode("Path");
            positionPathNode.InnerText = txtPositionPath.Text.Trim();
            XmlNode? dateTimeColumnNode = positionElement.SelectSingleNode("DateTimeColumn");
            dateTimeColumnNode.InnerText = comboDateTime.Text.Trim();
            XmlNode? xColumnNode = positionElement.SelectSingleNode("XColumn");
            xColumnNode.InnerText = comboX.Text.Trim();
            XmlNode? yColumnNode = positionElement.SelectSingleNode("YColumn");
            yColumnNode.InnerText = comboY.Text.Trim();
            XmlNode? headingColumnNode = positionElement.SelectSingleNode("HeadingColumn");
            headingColumnNode.InnerText = comboHeading.Text.Trim();
            XmlNode? pitchNode = positionElement.SelectSingleNode("Pitch");
            pitchNode.InnerText = txtPitch.Text.Trim();
            XmlNode? rollNode = positionElement.SelectSingleNode("Roll");
            rollNode.InnerText = txtRoll.Text.Trim();
            _project.SaveConfig(saveMode: 1);
        }

        private void VesselMountedADCP_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Control && e.KeyCode == Keys.S) // Ctrl + S
            {
                e.SuppressKeyPress = true; // Prevent default behavior
                SaveADCP(); // Save the project
            }
            else if (e.Control && e.KeyCode == Keys.N) // Ctrl + N
            {
                if (mode == 0)
                {
                    e.SuppressKeyPress = true; // Prevent default behavior
                    menuNew_Click(sender, e); // Create a new project
                }
            }
        }
    }
}
