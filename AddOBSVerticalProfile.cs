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
    public partial class AddOBSVerticalProfile : Form
    {

        public _SurveyManager surveyManager;
        public XmlDocument? project;
        public int id; // ID of the instrument
        XmlElement? instrument;
        public bool isSaved; // Track if survey has been saved
        int headerLine;
        string delimiter;

        public AddOBSVerticalProfile(_SurveyManager _surveyManager)
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
            id = _ClassConfigurationManager.NObjects(type: "//OBSVerticalProfile") + 1;
            txtName.Text = $"OBS Vertical Profile {id}";
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
            comboDateTime.Text = string.Empty;
            comboDepth.Text = string.Empty;
            comboNTU.Text = string.Empty;
            tblColumnInfo.Enabled = false;
            tblMasking.Enabled = false;
            // Create the instrument element
            instrument = surveyManager.survey.OwnerDocument.CreateElement("OBSVerticalProfile");
            instrument.SetAttribute("id", id.ToString());
            instrument.SetAttribute("type", "OBSVerticalProfile");
            instrument.SetAttribute("name", $"OBS Vertical Profile {id}");
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
                    SaveInstrument(); // Save the current instrument
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Cancel the form closing event
                    return; // User chose to cancel, do not exit
                }
            }
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
                    headerLine = csvOptions._headerLine;
                    delimiter = csvOptions._delimiter;
                    columns = _Utils.ParseCSVAndReturnColumns(filePath, delimiter, headerLine);
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

        public int CreateInstrument()
        {
            if (String.IsNullOrEmpty(txtName.Text.Trim()))
            {
                MessageBox.Show("Please select a name before saving.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            if (String.IsNullOrEmpty(txtFilePath.Text.Trim()))
            {
                MessageBox.Show("Please select an OBS Vertical Profile file file before saving.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
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

            XmlElement elemHeaderLine = project.CreateElement("HeaderLine");
            elemHeaderLine.InnerText = headerLine.ToString();
            fileInfo.AppendChild(elemHeaderLine);

            XmlElement elemDelimiter = project.CreateElement("Delimiter");
            elemDelimiter.InnerText = delimiter;
            fileInfo.AppendChild(elemDelimiter);

            XmlElement dateTimeColumn = project.CreateElement("DateTimeColumn");
            dateTimeColumn.InnerText = comboDateTime.Text.Trim() ?? string.Empty;
            fileInfo.AppendChild(dateTimeColumn);

            XmlElement depthColumn = project.CreateElement("DepthColumn");
            depthColumn.InnerText = comboDepth.Text.Trim() ?? string.Empty;
            fileInfo.AppendChild(depthColumn);

            XmlElement ntuColumn = project.CreateElement("NTUColumn");
            ntuColumn.InnerText = comboNTU.Text.Trim() ?? string.Empty;
            fileInfo.AppendChild(ntuColumn);

            instrument.AppendChild(fileInfo);

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
            instrument.AppendChild(masking);

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
            string xpath = $"//Survey[@id='{surveyId}']/OBSVerticalProfile[@id='{id}' and @type='OBSVerticalProfile']";
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
    }
}
