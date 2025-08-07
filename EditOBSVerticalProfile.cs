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
    public partial class EditOBSVerticalProfile : Form
    {

        public bool isSaved; // Track if survey has been saved
        public XmlElement obsElement; // OBS Vertical Profile element

        public EditOBSVerticalProfile(XmlNode obsNode)
        {
            InitializeComponent();
            InitializeOBS(obsNode);
        }

        public void InitializeOBS(XmlNode obsNode)
        {
            obsElement = obsNode as XmlElement;
            if (obsElement == null)
            {
                MessageBox.Show("Invalid OBS Vertical Profile provided.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                this.Close();
                return; // Ensure no further code is executed if adcpElement is null
            }
            txtName.Text = obsElement.GetAttribute("name");
            XmlNode fileInfoNode = obsElement.SelectSingleNode("FileInfo");
            txtFilePath.Text = fileInfoNode?.SelectSingleNode("Path")?.InnerText ?? string.Empty;
            XmlNode columns = fileInfoNode?.SelectSingleNode("Columns");
            if (columns != null)
            {
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

            XmlNode maskingNode = obsElement.SelectSingleNode("Masking");
            if (maskingNode != null)
            {
                XmlNode maskingDateTimeNode = maskingNode.SelectSingleNode("MaskDateTime");
                if (maskingDateTimeNode != null)
                {
                    checkMaskingDateTime.Checked = (maskingDateTimeNode as XmlElement)?.GetAttribute("Enabled") == "true";
                    txtMaskingStartDateTime.Text = maskingDateTimeNode.SelectSingleNode("Start")?.InnerText ?? string.Empty;
                    txtMaskingEndDateTime.Text = maskingDateTimeNode.SelectSingleNode("End")?.InnerText ?? string.Empty;
                }
                XmlNode maskingDepthNode = maskingNode.SelectSingleNode("MaskDepth");
                if (maskingDepthNode != null)
                {
                    checkMaskingDepth.Checked = (maskingDepthNode as XmlElement)?.GetAttribute("Enabled") == "true";
                    txtMaskingMinDepth.Text = maskingDepthNode.SelectSingleNode("Min")?.InnerText ?? string.Empty;
                    txtMaskingMaxDepth.Text = maskingDepthNode.SelectSingleNode("Max")?.InnerText ?? string.Empty;
                }
                XmlNode maskingNTUNode = maskingNode.SelectSingleNode("MaskNTU");
                if (maskingNTUNode != null)
                {
                    checkMaskingNTU.Checked = (maskingNTUNode as XmlElement)?.GetAttribute("Enabled") == "true";
                    txtMaskingMinNTU.Text = maskingNTUNode.SelectSingleNode("Min")?.InnerText ?? string.Empty;
                    txtMaskingMaxNTU.Text = maskingNTUNode.SelectSingleNode("Max")?.InnerText ?? string.Empty;
                }
            }
            isSaved = true; // Mark as saved after loading the OBS Vertical Profile
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
                    int headerLines = csvOptions._headerLines;
                    string delimiter = csvOptions._delimiter;
                    columns = _Utils.ParseCSVAndReturnColumns(filePath, delimiter, headerLines);
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
            txtFilePath.Text = openFileDialog.FileName;
            tblColumnInfo.Enabled = true;
            updateCombo(comboDateTime, columns, 0);
            updateCombo(comboDepth, columns, 1);
            updateCombo(comboNTU, columns, 2);
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

        public int UpdateOBS()
        {
            obsElement.SetAttribute("name", txtName.Text.Trim());
            XmlElement? fileInfo = obsElement.SelectSingleNode("FileInfo") as XmlElement;
            XmlNode? pathNode = fileInfo?.SelectSingleNode("Path");
            if (pathNode != null)
            {
                pathNode.InnerText = txtFilePath.Text.Trim();
            }
            else
            {
                return -1; // Path node not found
            }
            XmlNode? dateTimeColumn = fileInfo?.SelectSingleNode("DateTimeColumn");
            if (dateTimeColumn != null)
            {
                dateTimeColumn.InnerText = comboDateTime.SelectedItem?.ToString() ?? string.Empty;
            }
            else
            {
                return -1; // DateTime column node not found
            }
            XmlNode? depthColumn = fileInfo?.SelectSingleNode("DepthColumn");
            if (depthColumn != null)
            {
                depthColumn.InnerText = comboDepth.SelectedItem?.ToString() ?? string.Empty;
            }
            else
            {
                return -1; // Depth column node not found
            }
            XmlNode? ntuColumn = fileInfo?.SelectSingleNode("NTUColumn");
            if (ntuColumn != null)
            {
                ntuColumn.InnerText = comboNTU.SelectedItem?.ToString() ?? string.Empty;
            }
            else
            {
                return -1; // NTU column node not found
            }
            XmlElement? maskingNode = obsElement.SelectSingleNode("Masking") as XmlElement;
            if (maskingNode != null)
            {
                XmlElement maskingDateTimeNode = maskingNode.SelectSingleNode("MaskDateTime") as XmlElement;
                if (maskingDateTimeNode != null)
                {
                    maskingDateTimeNode.SetAttribute("Enabled", checkMaskingDateTime.Checked.ToString().ToLower());
                    XmlNode? startNode = maskingDateTimeNode.SelectSingleNode("Start");
                    if (startNode != null)
                    {
                        startNode.InnerText = txtMaskingStartDateTime.Text.Trim();
                    }
                    else
                    {
                        return -1; // Start node not found
                    }
                    XmlNode? endNode = maskingDateTimeNode.SelectSingleNode("End");
                    if (endNode != null)
                    {
                        endNode.InnerText = txtMaskingEndDateTime.Text.Trim();
                    }
                    else
                    {
                        return -1; // End node not found
                    }
                }
                else
                {
                    return -1; // Masking DateTime node not found
                }
                XmlElement maskingDepthNode = maskingNode.SelectSingleNode("MaskDepth") as XmlElement;
                if (maskingDepthNode != null)
                {
                    maskingDepthNode.SetAttribute("Enabled", checkMaskingDepth.Checked.ToString().ToLower());
                    XmlNode? minNode = maskingDepthNode.SelectSingleNode("Min");
                    if (minNode != null)
                    {
                        minNode.InnerText = txtMaskingMinDepth.Text.Trim();
                    }
                    else
                    {
                        return -1; // Min Depth node not found
                    }
                    XmlNode? maxNode = maskingDepthNode.SelectSingleNode("Max");
                    if (maxNode != null)
                    {
                        maxNode.InnerText = txtMaskingMaxDepth.Text.Trim();
                    }
                    else
                    {
                        return -1; // Max Depth node not found
                    }
                }
                else
                {
                    return -1; // Masking Depth node not found
                }
                XmlElement maskingNTUNode = maskingNode.SelectSingleNode("MaskNTU") as XmlElement;
                if (maskingNTUNode != null)
                {
                    maskingNTUNode.SetAttribute("Enabled", checkMaskingNTU.Checked.ToString().ToLower());
                    XmlNode? minNode = maskingNTUNode.SelectSingleNode("Min");
                    if (minNode != null)
                    {
                        minNode.InnerText = txtMaskingMinNTU.Text.Trim();
                    }
                    else
                    {
                        return -1; // Min NTU node not found
                    }
                    XmlNode? maxNode = maskingNTUNode.SelectSingleNode("Max");
                    if (maxNode != null)
                    {
                        maxNode.InnerText = txtMaskingMaxNTU.Text.Trim();
                    }
                    else
                    {
                        return -1; // Max NTU node not found
                    }
                }
                else
                {
                    return -1; // Masking NTU node not found
                }
            }
            else
            {
                return -1; // Masking node not found
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
                MessageBox.Show("Please enter a name for the OBS Vertical Profile.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return; // Prevent saving if name is empty
            }
            if (String.IsNullOrEmpty(txtFilePath.Text.Trim()))
            {
                MessageBox.Show("Please select a file path for the OBS Vertical Profile.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return; // Prevent saving if file path is empty
            }
            if (comboDateTime.SelectedItem == null || comboDepth.SelectedItem == null || comboNTU.SelectedItem == null)
            {
                MessageBox.Show("Please select valid columns for DateTime, Depth, and NTU.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return; // Prevent saving if any column is not selected
            }
            if (comboDateTime.SelectedIndex < 0 || comboDepth.SelectedIndex < 0 || comboNTU.SelectedIndex < 0)
            {
                MessageBox.Show("Please select valid columns for DateTime, Depth, and NTU.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return; // Prevent saving if any column is not selected
            }
            if (!File.Exists(GetFullPath(txtFilePath.Text.Trim())))
            {
                MessageBox.Show("The specified file path does not exist. Please select a valid file.", "File Not Found", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return; // Prevent saving if file does not exist
            }
            int result = UpdateOBS();
            if (result < 0)
            {
                MessageBox.Show("Failed to update the OBS Vertical Profile. Please check the XML structure.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return; // Prevent saving if update failed
            }
            _ClassConfigurationManager.SaveConfig(saveMode: 1);
            isSaved = true; // Mark as saved after successful save
        }

        private void AddOBSVerticalProfile_FormClosing(object sender, FormClosingEventArgs e)
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
