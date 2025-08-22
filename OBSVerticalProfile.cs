using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics.Metrics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.ExplorerBar;

namespace CSEMMPGUI_v1
{
    public partial class OBSVerticalProfile : Form
    {

        public _SurveyManager? surveyManager;
        public XmlDocument? project;
        public int id;
        XmlElement? obsElement;
        public bool isSaved;
        int mode; // 0 = new, 1 = edit
        int _headerLine;
        string _delimiter;
        public _ClassConfigurationManager _project = new();

        private void InitializeOBS()
        {
            if (surveyManager.survey == null)
            {
                throw new Exception("SurveyManager.survey is null. Cannot create instrument element.");
            }
            id = _project.GetNextId();
            txtName.Text = "New OBS Vertical Profile";
            txtFilePath.Text = string.Empty;
            checkMaskingDateTime.Checked = false;
            checkMaskingDepth.Checked = false;
            checkMaskingNTU.Checked = false;
            txtMaskingStartDateTime.Text = string.Empty;
            txtMaskingEndDateTime.Text = string.Empty;
            txtMaskingMinDepth.Text = string.Empty;
            txtMaskingMaxDepth.Text = string.Empty;
            txtMaskingMinNTU.Text = string.Empty;
            txtMaskingMaxNTU.Text = string.Empty;
            comboDateTime.Items.Clear();
            comboDepth.Items.Clear();
            comboNTU.Items.Clear();
            comboSSCModel.Items.Clear();
            comboDateTime.Text = string.Empty;
            comboDepth.Text = string.Empty;
            comboNTU.Text = string.Empty;
            comboSSCModel.Text = string.Empty;
            lblSSCModel.Enabled = false;
            comboSSCModel.Enabled = false;
            tblColumnInfo.Enabled = false;
            tblMasking.Enabled = false;
            // Create the instrument element
            obsElement = surveyManager.survey.OwnerDocument.CreateElement("OBSVerticalProfile");
            obsElement.SetAttribute("id", id.ToString());
            obsElement.SetAttribute("type", "OBSVerticalProfile");
            obsElement.SetAttribute("name", "New OBS Vertical Profile");
            project = surveyManager.survey.OwnerDocument;
            isSaved = true;
        }

        private void PopulateOBS()
        {
            txtName.Text = obsElement.GetAttribute("name");
            XmlNode fileInfoNode = obsElement.SelectSingleNode("FileInfo");
            txtFilePath.Text = fileInfoNode?.SelectSingleNode("Path")?.InnerText ?? string.Empty;
            XmlNode columns = fileInfoNode?.SelectSingleNode("Columns");
            foreach (XmlNode columnNode in columns.ChildNodes)
            {
                if (columnNode.NodeType == XmlNodeType.Element)
                {
                    string columnName = columnNode.InnerText.Trim();
                    comboDateTime.Items.Add(columnName);
                    comboDepth.Items.Add(columnName);
                    comboNTU.Items.Add(columnName);
                }
            }
            void SelectComboItem(ComboBox combo, string value)
            {
                int index = combo.Items.IndexOf(value.Trim());
                if (index >= 0)
                    combo.SelectedIndex = index;
            }
            SelectComboItem(comboDateTime, fileInfoNode?.SelectSingleNode("DateTimeColumn")?.InnerText ?? "");
            SelectComboItem(comboDepth, fileInfoNode?.SelectSingleNode("DepthColumn")?.InnerText ?? "");
            SelectComboItem(comboNTU, fileInfoNode?.SelectSingleNode("NTUColumn")?.InnerText ?? "");
            List<XmlElement> ntu2sscModels = _project.GetObjects("NTU2SSC");
            if (ntu2sscModels.Count > 0)
            {
                comboSSCModel.Items.Clear();
                foreach (XmlElement model in ntu2sscModels)
                {
                    comboSSCModel.Items.Add(new
                    {
                        Display = model.GetAttribute("name"),
                        Tag = model.GetAttribute("id")
                    });
                }
                comboSSCModel.DisplayMember = "Display";
                string sscModelId = fileInfoNode?.SelectSingleNode("SSCModel")?.InnerText ?? string.Empty;
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

            XmlNode maskingNode = obsElement.SelectSingleNode("Masking");
            XmlNode maskingDateTimeNode = maskingNode.SelectSingleNode("MaskDateTime");
            checkMaskingDateTime.Checked = (maskingDateTimeNode as XmlElement)?.GetAttribute("Enabled") == "true";
            txtMaskingStartDateTime.Text = maskingDateTimeNode.SelectSingleNode("Start")?.InnerText ?? string.Empty;
            txtMaskingEndDateTime.Text = maskingDateTimeNode.SelectSingleNode("End")?.InnerText ?? string.Empty;
            XmlNode maskingDepthNode = maskingNode.SelectSingleNode("MaskDepth");
            checkMaskingDepth.Checked = (maskingDepthNode as XmlElement)?.GetAttribute("Enabled") == "true";
            txtMaskingMinDepth.Text = maskingDepthNode.SelectSingleNode("Min")?.InnerText ?? string.Empty;
            txtMaskingMaxDepth.Text = maskingDepthNode.SelectSingleNode("Max")?.InnerText ?? string.Empty;
            XmlNode maskingNTUNode = maskingNode.SelectSingleNode("MaskNTU");
            checkMaskingNTU.Checked = (maskingNTUNode as XmlElement)?.GetAttribute("Enabled") == "true";
            txtMaskingMinNTU.Text = maskingNTUNode.SelectSingleNode("Min")?.InnerText ?? string.Empty;
            txtMaskingMaxNTU.Text = maskingNTUNode.SelectSingleNode("Max")?.InnerText ?? string.Empty;
            
            isSaved = true;
        }

        public OBSVerticalProfile(_SurveyManager? _surveyManager, XmlNode? obsNode)
        {
            InitializeComponent();
            if (obsNode == null)
            {
                surveyManager = _surveyManager;
                InitializeOBS();
                mode = 0;
                this.Text = "Add OBS Vertical Profile";
            }
            else
            {
                obsElement = obsNode as XmlElement;
                PopulateOBS();
                menuNew.Visible = false;
                tblColumnInfo.Enabled = true;
                tblMasking.Enabled = true;
                mode = 1;
                this.Text = "Edit OBS Vertical Profile";
            }

            this.KeyPreview = true; // Enable form to capture key events
            this.KeyDown += OBSVerticalProfile_KeyDown; // Attach key down event handler
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current OBS vertical profile has unsaved changes. Do you want to save them before creating a new one?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveOBS();
                    if (status == 1)
                        InitializeOBS(); // Reinitialize the form for a new instrument
                    else
                        return; // Prevent creating a new instrument if save failed

                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not create a new instrument
                }
                else if (result == DialogResult.No)
                {
                    InitializeOBS(); // Reinitialize the form for a new instrument without saving
                }
            }
            else
            {
                InitializeOBS(); // Reinitialize the form for a new instrument if there are no unsaved changes
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveOBS();
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current OBS vertical profile has unsaved changes. Do you want to save them before creating a new one?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveOBS();
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
                    this.Close(); // Close the form without saving
                }
            }
            else
            {
                this.Close(); // Close the form if there are no unsaved changes
            }
        }

        private void OBSVerticalProfile_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current OBS vertical profile has unsaved changes. Do you want to save them before exiting?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveOBS();
                    if (status == 0)
                        e.Cancel = true; // Cancel the closing event if save failed
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

        public void updateCombo(ComboBox combo, string[] items, int index)
        {
            combo.Items.Clear();
            combo.Items.AddRange(items);
            combo.SelectedIndex = index;
        }
        
        private void btnLoadPath_Click(object sender, EventArgs e)
        {
            string[] columns = Array.Empty<string>();
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "OBS Vertical Profile File (*.csv;*.txt)|*.csv;*.txt";
            openFileDialog.Title = "Select OBS Vertical Profile File";
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                string filePath = openFileDialog.FileName;
                int nLines = File.ReadAllLines(filePath).Length;
                UtilsCSVImportOptions csvOptions = new UtilsCSVImportOptions(nLines);
                if (csvOptions.ShowDialog() == DialogResult.OK)
                {
                    _headerLine = csvOptions._headerLine;
                    _delimiter = csvOptions._delimiter;
                    columns = _Utils.ParseCSVAndReturnColumns(filePath, _delimiter, _headerLine);
                    if (columns.Length < 3)
                    {
                        MessageBox.Show("The selected CSV file does not contain enough columns for OBS Vertical Profile data.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
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
            List<XmlElement> ntu2sscModels = _project.GetObjects(type: "NTU2SSC");
            if (ntu2sscModels.Count > 0)
            {
                comboSSCModel.Items.Clear();
                foreach (XmlElement model in ntu2sscModels)
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
                    "No NTU to SSC models found. Please add one and update the setting later",
                    Text = "Warning",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);
                comboSSCModel.Items.Clear();
                comboSSCModel.Enabled = false; // Disable if no models are available
                lblSSCModel.Enabled = false; // Disable label if no models are available
            }
            txtFilePath.Text = openFileDialog.FileName;
            tblColumnInfo.Enabled = true;
            updateCombo(comboDateTime, columns, 0);
            updateCombo(comboDepth, columns, 1);
            updateCombo(comboNTU, columns, 2);
            tblMasking.Enabled = true;
            isSaved = false; // Mark as unsaved after loading a new position file
        }

        private void checkMaskingDateTime_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskingDateTime.Checked)
            {
                lblMaskingStartDateTime.Enabled = true;
                txtMaskingStartDateTime.Enabled = true;
                lblMaskingEndDateTime.Enabled = true;
                txtMaskingEndDateTime.Enabled = true;
            }
            else
            {
                lblMaskingStartDateTime.Enabled = false;
                txtMaskingStartDateTime.Enabled = false;
                lblMaskingEndDateTime.Enabled = false;
                txtMaskingEndDateTime.Enabled = false;
            }
            isSaved = false; // Mark as unsaved when masking options change
        }

        private void checkMaskingDepth_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskingDepth.Checked)
            {
                lblMaskingMinDepth.Enabled = true;
                txtMaskingMinDepth.Enabled = true;
                lblMaskingMaxDepth.Enabled = true;
                txtMaskingMaxDepth.Enabled = true;
            }
            else
            {
                lblMaskingMinDepth.Enabled = false;
                txtMaskingMinDepth.Enabled = false;
                lblMaskingMaxDepth.Enabled = false;
                txtMaskingMaxDepth.Enabled = false;
            }
            isSaved = false; // Mark as unsaved when masking options change
        }

        private void checkMaskingNTU_CheckedChanged(object sender, EventArgs e)
        {
            if (checkMaskingNTU.Checked)
            {
                lblMaskingMinNTU.Enabled = true;
                txtMaskingMinNTU.Enabled = true;
                lblMaskingMaxNTU.Enabled = true;
                txtMaskingMaxNTU.Enabled = true;
            }
            else
            {
                lblMaskingMinNTU.Enabled = false;
                txtMaskingMinNTU.Enabled = false;
                lblMaskingMaxNTU.Enabled = false;
                txtMaskingMaxNTU.Enabled = false;
            }
        }

        private int SaveOBS()
        {
            if (String.IsNullOrEmpty(txtName.Text.Trim()))
            {
                MessageBox.Show("Please enter a name for the OBS Vertical Profile.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            if (String.IsNullOrEmpty(txtFilePath.Text.Trim()))
            {
                MessageBox.Show("Please select a file path for the OBS Vertical Profile.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            if (!File.Exists(_Utils.GetFullPath(txtFilePath.Text.Trim())))
            {
                MessageBox.Show("The specified file path does not exist. Please select a valid file.", "File Not Found", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0; // Prevent saving if file does not exist
            }
            if (comboDateTime.SelectedItem == null || comboDepth.SelectedItem == null || comboNTU.SelectedItem == null)
            {
                MessageBox.Show("Please select valid columns for DateTime, Depth, and NTU.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return 0; // Prevent saving if any column is not selected
            }
            if (comboDateTime.SelectedIndex < 0 || comboDepth.SelectedIndex < 0 || comboNTU.SelectedIndex < 0)
            {
                MessageBox.Show("Please select valid columns for DateTime, Depth, and NTU.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return 0; // Prevent saving if any column is not selected
            }
            if (mode == 0)
                SAVE();
            else
                UPDATE();
            isSaved = true; // Mark as saved after successful save
            return 1;
        }

        private void SAVE()
        {
            obsElement.SetAttribute("name", txtName.Text.Trim());
            while (obsElement.HasChildNodes && obsElement.FirstChild != null)
            {
                obsElement.RemoveChild(obsElement.FirstChild);
            }
            // Pd0 related attributes
            XmlElement fileInfo = project.CreateElement("FileInfo");
            XmlElement filePath = project.CreateElement("Path");
            filePath.InnerText = txtFilePath.Text.Trim();
            fileInfo.AppendChild(filePath);
            XmlElement fileColumns = project.CreateElement("Columns");
            for (int i = 0; i < comboDateTime.Items.Count; i++)
            {
                XmlElement column = project.CreateElement($"Column{i}");
                column.InnerText = comboDateTime.Items[i].ToString();
                fileColumns.AppendChild(column);
            }
            fileInfo.AppendChild(fileColumns);
            XmlElement dateTimeColumn = project.CreateElement("DateTimeColumn");
            dateTimeColumn.InnerText = comboDateTime.Text.Trim() ?? string.Empty;
            fileInfo.AppendChild(dateTimeColumn);
            XmlElement depthColumn = project.CreateElement("DepthColumn");
            depthColumn.InnerText = comboDepth.Text.Trim() ?? string.Empty;
            fileInfo.AppendChild(depthColumn);
            XmlElement ntuColumn = project.CreateElement("NTUColumn");
            ntuColumn.InnerText = comboNTU.Text.Trim() ?? string.Empty;
            fileInfo.AppendChild(ntuColumn);
            XmlElement ntu2sscModel = project.CreateElement("SSCModel");
            List<XmlElement> ntu2sscModels = _project.GetObjects(type: "NTU2SSC");
            if (ntu2sscModels.Count == 0)
            {
                ntu2sscModel.InnerText = string.Empty;
            }
            else
            {
                var selectedItem = comboSSCModel.SelectedItem;
                string selectedId = selectedItem != null ? ((dynamic)selectedItem).Tag : ntu2sscModels[0].GetAttribute("id");
                ntu2sscModel.InnerText = selectedId;
            }
            fileInfo.AppendChild(ntu2sscModel);
            obsElement.AppendChild(fileInfo);
            XmlElement masking = project.CreateElement("Masking");
            XmlElement maskingDateTime = project.CreateElement("MaskDateTime");
            maskingDateTime.SetAttribute("Enabled", checkMaskingDateTime.Checked.ToString().ToLower());
            XmlElement maskingStartDateTime = project.CreateElement("Start");
            maskingStartDateTime.InnerText = txtMaskingStartDateTime.Text.Trim();
            maskingDateTime.AppendChild(maskingStartDateTime);
            XmlElement maskingEndDateTime = project.CreateElement("End");
            maskingEndDateTime.InnerText = txtMaskingEndDateTime.Text.Trim();
            maskingDateTime.AppendChild(maskingEndDateTime);
            masking.AppendChild(maskingDateTime);
            XmlElement maskingDepth = project.CreateElement("MaskDepth");
            maskingDepth.SetAttribute("Enabled", checkMaskingDepth.Checked.ToString().ToLower());
            XmlElement maskingMinDepth = project.CreateElement("Min");
            maskingMinDepth.InnerText = txtMaskingMinDepth.Text.Trim();
            maskingDepth.AppendChild(maskingMinDepth);
            XmlElement maskingMaxDepth = project.CreateElement("Max");
            maskingMaxDepth.InnerText = txtMaskingMaxDepth.Text.Trim();
            maskingDepth.AppendChild(maskingMaxDepth);
            masking.AppendChild(maskingDepth);
            XmlElement maskingNTU = project.CreateElement("MaskNTU");
            maskingNTU.SetAttribute("Enabled", checkMaskingNTU.Checked.ToString().ToLower());
            XmlElement maskingMinNTU = project.CreateElement("Min");
            maskingMinNTU.InnerText = txtMaskingMinNTU.Text.Trim();
            maskingNTU.AppendChild(maskingMinNTU);
            XmlElement maskingMaxNTU = project.CreateElement("Max");
            maskingMaxNTU.InnerText = txtMaskingMaxNTU.Text.Trim();
            maskingNTU.AppendChild(maskingMaxNTU);
            masking.AppendChild(maskingNTU);
            obsElement.AppendChild(masking);
            
            surveyManager.survey.AppendChild(obsElement);
            surveyManager.SaveSurvey(name: surveyManager.GetAttribute(attribute: "name"));
            _project.SaveConfig(saveMode: 1);
        }

        private void UPDATE()
        {
            obsElement.SetAttribute("name", txtName.Text.Trim());
            XmlElement? fileInfo = obsElement.SelectSingleNode("FileInfo") as XmlElement;
            XmlNode? pathNode = fileInfo?.SelectSingleNode("Path");
            pathNode.InnerText = txtFilePath.Text.Trim();
            XmlElement? columnsElement = fileInfo?.SelectSingleNode("Columns") as XmlElement;
            columnsElement.RemoveAll(); // Clear existing columns
            for (int i = 0; i < comboDateTime.Items.Count; i++)
            {
                XmlElement columnElement = obsElement.OwnerDocument.CreateElement($"Column{i}");
                columnElement.InnerText = comboDateTime.Items[i].ToString();
                columnsElement.AppendChild(columnElement);
            }
            XmlNode? dateTimeColumn = fileInfo?.SelectSingleNode("DateTimeColumn");
            dateTimeColumn.InnerText = comboDateTime.SelectedItem?.ToString() ?? string.Empty;
            XmlNode? depthColumn = fileInfo?.SelectSingleNode("DepthColumn");
            depthColumn.InnerText = comboDepth.SelectedItem?.ToString() ?? string.Empty;
            XmlNode? ntuColumn = fileInfo?.SelectSingleNode("NTUColumn");
            ntuColumn.InnerText = comboNTU.SelectedItem?.ToString() ?? string.Empty;
            XmlNode? sscModelNode = fileInfo?.SelectSingleNode("SSCModel");
            var selectedItem = comboSSCModel.SelectedItem;
            string selectedId = selectedItem != null ? ((dynamic)selectedItem).Tag : string.Empty;
            sscModelNode.InnerText = selectedId;
            XmlElement? maskingNode = obsElement.SelectSingleNode("Masking") as XmlElement;
            XmlElement maskingDateTimeNode = maskingNode.SelectSingleNode("MaskDateTime") as XmlElement;
            maskingDateTimeNode.SetAttribute("Enabled", checkMaskingDateTime.Checked.ToString().ToLower());
            XmlNode? startNode = maskingDateTimeNode.SelectSingleNode("Start");
            startNode.InnerText = txtMaskingStartDateTime.Text.Trim();
            XmlNode? endNode = maskingDateTimeNode.SelectSingleNode("End");
            endNode.InnerText = txtMaskingEndDateTime.Text.Trim();
            XmlElement maskingDepthNode = maskingNode.SelectSingleNode("MaskDepth") as XmlElement;
            maskingDepthNode.SetAttribute("Enabled", checkMaskingDepth.Checked.ToString().ToLower());
            XmlNode? minDepthNode = maskingDepthNode.SelectSingleNode("Min");
            minDepthNode.InnerText = txtMaskingMinDepth.Text.Trim();
            XmlNode? maxDepthNode = maskingDepthNode.SelectSingleNode("Max");
            maxDepthNode.InnerText = txtMaskingMaxDepth.Text.Trim();
            XmlElement maskingNTUNode = maskingNode.SelectSingleNode("MaskNTU") as XmlElement;
            maskingNTUNode.SetAttribute("Enabled", checkMaskingNTU.Checked.ToString().ToLower());
            XmlNode? minNTUNode = maskingNTUNode.SelectSingleNode("Min");
            minNTUNode.InnerText = txtMaskingMinNTU.Text.Trim();
            XmlNode? maxNTUNode = maskingNTUNode.SelectSingleNode("Max");
            maxNTUNode.InnerText = txtMaskingMaxNTU.Text.Trim();
            _project.SaveConfig(saveMode: 1);
        }

        private void OBSVerticalProfile_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Control && e.KeyCode == Keys.S) // Ctrl + S
            {
                e.SuppressKeyPress = true; // Prevent default behavior
                SaveOBS(); // Save the project
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
