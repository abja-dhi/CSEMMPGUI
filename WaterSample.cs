using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics.Metrics;
using System.Drawing;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public partial class WaterSample : Form
    {

        public _SurveyManager? surveyManager;
        public XmlDocument? project;
        public int id;
        XmlElement? waterSampleElement;
        public bool isSaved;
        int mode; // 0 = new, 1 = edit
        _ClassConfigurationManager _project = new();

        private const string COL_SAMPLE = "colSampleName";
        private const string COL_DATETIME = "colDateTime";
        private const string COL_DEPTH = "colDepth";
        //private const string COL_X = "colX";
        //private const string COL_Y = "colY";
        private const string COL_SSC = "colSSC";
        private const string COL_NOTES = "colNotes";

        public string[] allowedFormats = new[]
            {
                "MMMM d, yyyy HH:mm:ss",
                "MMMM d yyyy HH:mm:ss",
                "MMM d, yyyy HH:mm:ss",
                "MMM. d, yyyy HH:mm:ss",
                "MMM d yyyy HH:mm:ss",
                "MMM. d yyyy HH:mm:ss",
                "d MMMM, yyyy HH:mm:ss",
                "d MMMM yyyy HH:mm:ss",
                "d MMM, yyyy HH:mm:ss",
                "d MMM. yyyy HH:mm:ss",
                "d MMM yyyy HH:mm:ss",
            };

        public string[] allowedFormatsToolTip = new[]
            {
                "MMMM d, yyyy HH:mm:ss",
                "MMM d, yyyy HH:mm:ss",
                "d MMMM, yyyy HH:mm:ss",
                "d MMM, yyyy HH:mm:ss"
            };

        private void InitializeWaterSample()
        {
            if (surveyManager.survey == null)
            {
                throw new Exception("SurveyManager.survey is null. Cannot create instrument element.");
            }
            id = _project.GetNextId();
            txtName.Text = "New WaterSample";
            gridData.Rows.Clear();
            waterSampleElement = surveyManager.survey.OwnerDocument.CreateElement("WaterSample");
            waterSampleElement.SetAttribute("id", id.ToString());
            waterSampleElement.SetAttribute("type", "WaterSample");
            waterSampleElement.SetAttribute("name", "New Water Sample");
            project = surveyManager.survey.OwnerDocument;
            isSaved = true;
        }

        private void PopulateWaterSample()
        {
            txtName.Text = waterSampleElement?.GetAttribute("name");
            gridData.Rows.Clear();
            foreach (XmlNode node in waterSampleElement.ChildNodes)
            {
                if (node is XmlElement sampleElement && node.Name == "Sample")
                {
                    int rowIndex = gridData.Rows.Add();
                    DataGridViewRow row = gridData.Rows[rowIndex];
                    row.Cells[COL_SAMPLE].Value = sampleElement.GetAttribute("Sample");
                    row.Cells[COL_DATETIME].Value = DateTime.Parse(sampleElement.GetAttribute("DateTime")).ToString("MMMM d, yyyy HH:mm:ss");
                    row.Cells[COL_DEPTH].Value = sampleElement.GetAttribute("Depth");
                    //row.Cells[COL_X].Value = sampleElement.GetAttribute("X");
                    //row.Cells[COL_Y].Value = sampleElement.GetAttribute("Y");
                    row.Cells[COL_SSC].Value = sampleElement.GetAttribute("SSC");
                    row.Cells[COL_NOTES].Value = sampleElement.GetAttribute("Notes");
                }
            }
            isSaved = true;
        }

        public WaterSample(_SurveyManager? _surveyManager, XmlNode? waterSampleNode)
        {
            InitializeComponent();
            DateTime now = DateTime.Now;
            string tooltip = "Accepted formats are\n:";
            foreach (string format in allowedFormatsToolTip)
            {
                tooltip += $"\n{now.ToString(format)}";
            }
            DataGridViewColumn colDateTime = gridData.Columns[COL_DATETIME];
            colDateTime.ToolTipText = tooltip.TrimEnd();
            if (waterSampleNode == null)
            {
                surveyManager = _surveyManager;
                InitializeWaterSample();
                mode = 0;
                this.Text = "Add Water Sample";
            }
            else
            {
                waterSampleElement = waterSampleNode as XmlElement;
                PopulateWaterSample();
                menuNew.Visible = false;
                menuUtilities.Visible = false;
                mode = 1;
                this.Text = "Edit Water Sample";
            }

            this.KeyPreview = true; // Enable form to capture key events
            this.KeyDown += WaterSample_KeyDown; // Attach key down event handler
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current water sample has unsaved changes. Do you want to save them before creating a new one?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveWaterSample();
                    if (status == 1)
                        InitializeWaterSample(); // Reinitialize the form for a new instrument
                    else
                        return;
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not create a new instrument
                }
                else if (result == DialogResult.No)
                {
                    InitializeWaterSample(); // Reinitialize the form for a new instrument
                }
            }
            else
            {
                InitializeWaterSample(); // Reinitialize the form for a new instrument
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveWaterSample();
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current water sample has unsaved changes. Do you want to save them before creating a new one?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveWaterSample();
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
                    this.Close();
                }
            }
            else
            {
                this.Close(); // Close the form if no unsaved changes
            }
        }

        private void WaterSample_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current water sample has unsaved changes. Do you want to save them before exiting?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveWaterSample();
                    if (status == 0)
                        e.Cancel = true; // Cancel the closing event if save failed
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Cancel the closing event
                }
            }
        }

        private void txtName_TextChanged(object sender, EventArgs e)
        {
            isSaved = false;
        }

        private void gridData_CellValueChanged(object sender, DataGridViewCellEventArgs e)
        {
            isSaved = false; // Mark as unsaved when any input changes
        }

        private void menuViSeaSample2CSV_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Filter = "ViSea Sample Data (*.txt;*.csv)|*.txt;*.csv";
            ofd.Title = "Select ViSea Sample Data File";
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                var input = new Dictionary<string, string>
                {
                    {"Task", "ViSeaSample2CSV" },
                    {"Path", _Utils.GetFullPath(ofd.FileName) }
                };
                string xmlInput = _Tools.GenerateInput(input);
                XmlDocument doc = _Tools.CallPython(xmlInput);
                Dictionary<string, string> output = _Tools.ParseOutput(doc);
                if (output.ContainsKey("Error"))
                {
                    MessageBox.Show(output["Error"], "Import Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                else
                {
                    MessageBox.Show("CSV file created successfully.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
        }

        private void menuImportCSV_Click(object sender, EventArgs e)
        {
            string[] columns = Array.Empty<string>();
            string[] items = new string[] { "Sample", "DateTime", "Depth", "SSC", "Notes" };
            bool[] status = new bool[] { true, true, true, true, false }; // Notes is optional
            int[] selectedColumns = new int[items.Length];
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "Water Sample Data (*.csv;*.txt)|*.csv;*.txt";
            openFileDialog.Title = "Select a Water Sample Data";
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
                    if (columns.Length > 0)
                    {
                        UtilsCSVColumnSelector columnSelector = new UtilsCSVColumnSelector(columns, items, status);
                        
                        if (columnSelector.ShowDialog() == DialogResult.OK)
                        {
                            string SelectedColumns = string.Join(",", columnSelector._selectedColumns);
                            var input = new Dictionary<string, string>
                            {
                                {"Task", "ReadCSV" },
                                {"Root", "WaterSample" },
                                {"SubElement", "Sample" },
                                {"Path", _Utils.GetFullPath(filePath) },
                                {"Header", headerLines.ToString() },
                                {"Sep", delimiter },
                                {"Items", string.Join(",", items) },
                                {"Columns", SelectedColumns }
                            };
                            string xmlInput = _Tools.GenerateInput(input);
                            XmlDocument doc = _Tools.CallPython(xmlInput);
                            Dictionary<string, string> output = _Tools.ParseOutput(doc);
                            if (output.ContainsKey("Error"))
                            {
                                MessageBox.Show(output["Error"], "Import Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                                return;
                            }
                            XmlDocument? csvData = new XmlDocument();
                            csvData.LoadXml(output["Result"]);
                            waterSampleElement.SetAttribute("type", "WaterSample");
                            waterSampleElement.SetAttribute("name", Path.GetFileNameWithoutExtension(filePath));
                            while (waterSampleElement.HasChildNodes && waterSampleElement.FirstChild != null)
                            {
                                waterSampleElement.RemoveChild(waterSampleElement.FirstChild);
                            }
                            foreach (XmlNode node in csvData.DocumentElement.ChildNodes)
                            {
                                if (node is XmlElement sampleElement && node.Name == "Sample")
                                {
                                    XmlElement newSample = surveyManager.survey.OwnerDocument.CreateElement("Sample");
                                    newSample.SetAttribute("Sample", sampleElement.GetAttribute("Sample"));
                                    newSample.SetAttribute("DateTime", sampleElement.GetAttribute("DateTime"));
                                    newSample.SetAttribute("Depth", sampleElement.GetAttribute("Depth"));
                                    //newSample.SetAttribute("X", sampleElement.GetAttribute("X"));
                                    //newSample.SetAttribute("Y", sampleElement.GetAttribute("Y"));
                                    newSample.SetAttribute("SSC", sampleElement.GetAttribute("SSC"));
                                    newSample.SetAttribute("Notes", sampleElement.GetAttribute("Notes"));
                                    waterSampleElement.AppendChild(newSample);
                                }
                            }
                            PopulateWaterSample();
                            isSaved = false; // Mark as unsaved after import
                        }
                        else
                        {
                            return;
                        }
                    }
                    else
                    {
                        MessageBox.Show("No valid columns found in the CSV file.", "Import Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
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
        }

        private void NumericOnly_KeyPress(object? sender, KeyPressEventArgs e)
        {
            TextBox? tb = sender as TextBox;
            if (tb == null) return;

            // Allow control characters (e.g., backspace)
            if (char.IsControl(e.KeyChar))
                return;

            // Allow one decimal point
            if (e.KeyChar == '.' && !tb.Text.Contains('.'))
                return;

            // Allow '-' only as the first character and only once
            if (e.KeyChar == '-' && tb.SelectionStart == 0 && !tb.Text.Contains('-'))
                return;

            // Allow digits
            if (char.IsDigit(e.KeyChar))
                return;

            // Otherwise, block the input
            e.Handled = true;
        }

        private void gridData_EditingControlShowing(object sender, DataGridViewEditingControlShowingEventArgs e)
        {
            TextBox tb = e.Control as TextBox;
            if (tb == null) return;

            // Always remove the handler first to avoid stacking
            tb.KeyPress -= NumericOnly_KeyPress;

            string colName = gridData.Columns[gridData.CurrentCell.ColumnIndex].Name;

            //if (colName == COL_X || colName == COL_Y || colName == COL_DEPTH || colName == COL_SSC)
            if (colName == COL_DEPTH || colName == COL_SSC)
            {
                tb.KeyPress += NumericOnly_KeyPress;
            }
        }

        private void gridData_KeyDown(object sender, KeyEventArgs e)
        {
            // Handle Enter key to move to the next row
            if (e.Control && e.KeyCode == Keys.C)
            {
                DataObject dataObj = gridData.GetClipboardContent();
                if (dataObj != null)
                {
                    Clipboard.SetDataObject(dataObj);
                }
                e.Handled = true; // Prevent default behavior
            }
            else if (e.Control && e.KeyCode == Keys.V)
            {
                PasteFromClipboard();
                e.Handled = true; // Prevent default behavior
            }
        }

        private void PasteFromClipboard()
        {
            if (gridData.IsCurrentCellInEditMode)
                gridData.EndEdit(); // Ensure current edit is committed

            string clipboardText = Clipboard.GetText();
            if (string.IsNullOrWhiteSpace(clipboardText))
                return;

            // Split lines and cells
            string[] lines = clipboardText.Split(new[] { "\r\n", "\n" }, StringSplitOptions.RemoveEmptyEntries);
            if (lines.Length == 0)
                return;

            // Dirty check: more than one column?
            if (lines.Any(line => line.Split('\t').Length > 1))
            {
                MessageBox.Show("Please paste only one column at a time.", "Paste Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            // Get current column and row
            int startRow = gridData.CurrentCell?.RowIndex ?? 0;
            int colIndex = gridData.CurrentCell?.ColumnIndex ?? -1;
            if (colIndex < 0 || colIndex >= gridData.ColumnCount)
                return;

            string colName = gridData.Columns[colIndex].Name;

            for (int i = 0; i < lines.Length; i++)
            {
                string value = lines[i].Trim();
                int rowIndex = startRow + i;

                // Add new row if needed
                while (rowIndex >= gridData.Rows.Count - 1)
                    gridData.Rows.Add();

                // Validate numeric columns
                //if ((colName == COL_X || colName == COL_Y || colName == COL_DEPTH || colName == COL_SSC) &&

                if ((colName == COL_DEPTH || colName == COL_SSC) &&
                    !string.IsNullOrWhiteSpace(value) &&
                    !double.TryParse(value, out _))
                {
                    MessageBox.Show($"Invalid numeric value '{value}' in column '{colName}' (row {rowIndex + 1}).", "Paste Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    continue;
                }

                // Validate datetime format
                if (colName == COL_DATETIME &&
                    !string.IsNullOrWhiteSpace(value) &&
                    !DateTime.TryParseExact(value, allowedFormats, CultureInfo.InvariantCulture, DateTimeStyles.None, out _))
                {
                    MessageBox.Show($"Invalid datetime format in row {rowIndex + 1}: '{value}'.", "Paste Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    continue;
                }
                if (!gridData.Rows[rowIndex].IsNewRow)
                    gridData.Rows[rowIndex].Cells[colIndex].Value = value;
            }
        }

        public bool ValidateSampleGrid()
        {
            foreach (DataGridViewRow row in gridData.Rows)
            {
                if (row.IsNewRow) continue;

                string? sample = row.Cells[COL_SAMPLE].Value?.ToString()?.Trim();
                string? dtText = row.Cells[COL_DATETIME].Value?.ToString()?.Trim();
                string? depth = row.Cells[COL_DEPTH].Value?.ToString()?.Trim();
                //string? x = row.Cells[COL_X].Value?.ToString()?.Trim();
                //string? y = row.Cells[COL_Y].Value?.ToString()?.Trim();
                string? ssc = row.Cells[COL_SSC].Value?.ToString()?.Trim();

                // Check required fields
                if (string.IsNullOrWhiteSpace(sample) ||
                    string.IsNullOrWhiteSpace(dtText) ||
                    string.IsNullOrWhiteSpace(depth) ||
                    //string.IsNullOrWhiteSpace(x) ||
                    //string.IsNullOrWhiteSpace(y) ||
                    string.IsNullOrWhiteSpace(ssc))
                {
                    MessageBox.Show($"Missing required data in row {row.Index + 1}.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return false;
                }

                // Check datetime format
                if (!DateTime.TryParseExact(dtText, allowedFormats, CultureInfo.InvariantCulture, DateTimeStyles.None, out _))
                {
                    MessageBox.Show($"Invalid DateTime format in row {row.Index + 1}: '{dtText}'. Expected formats: {string.Join(", ", allowedFormats)}", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return false;
                }
            }

            return true;
        }

        public int SaveWaterSample()
        {
            if (String.IsNullOrEmpty(txtName.Text.Trim()))
            {
                MessageBox.Show("Please assign a name to the water sample", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 0;
            }
            if (!ValidateSampleGrid())
            {
                return 0;
            }
            if (mode == 0)
                SAVE();
            else
                UPDATE();
            isSaved = true;
            return 1;
        }

        private void SAVE()
        {
            waterSampleElement?.SetAttribute("name", txtName.Text.Trim());
            while (waterSampleElement.HasChildNodes && waterSampleElement.FirstChild != null)
            {
                waterSampleElement.RemoveChild(waterSampleElement.FirstChild);
            }
            foreach (DataGridViewRow row in gridData.Rows)
            {
                if (row.IsNewRow) continue;

                // Get all cell values
                string sample = row.Cells[COL_SAMPLE].Value?.ToString()?.Trim() ?? "";
                string dtText = row.Cells[COL_DATETIME].Value?.ToString()?.Trim() ?? "";
                DateTime dt = DateTime.ParseExact(dtText, allowedFormats, CultureInfo.InvariantCulture, DateTimeStyles.None);
                string depth = row.Cells[COL_DEPTH].Value?.ToString()?.Trim() ?? "";
                //string x = row.Cells[COL_X].Value?.ToString()?.Trim() ?? "";
                //string y = row.Cells[COL_Y].Value?.ToString()?.Trim() ?? "";
                string ssc = row.Cells[COL_SSC].Value?.ToString()?.Trim() ?? "";
                string notes = row.Cells[COL_NOTES].Value?.ToString()?.Trim() ?? "";

                // Create new XML element
                XmlElement sampleNode = surveyManager.survey.OwnerDocument.CreateElement("Sample");

                sampleNode.SetAttribute("Sample", sample);
                sampleNode.SetAttribute("DateTime", dt.ToString("o")); // ISO 8601
                sampleNode.SetAttribute("Depth", depth);
                //sampleNode.SetAttribute("X", x);
                //sampleNode.SetAttribute("Y", y);
                sampleNode.SetAttribute("SSC", ssc);
                sampleNode.SetAttribute("Notes", notes);

                waterSampleElement.AppendChild(sampleNode);
            }
            surveyManager.survey.AppendChild(waterSampleElement);
            surveyManager.SaveSurvey(name: surveyManager.GetAttribute(attribute: "name"));
            _project.SaveConfig(saveMode: 1);
        }

        private void UPDATE()
        {
            waterSampleElement.SetAttribute("name", txtName.Text.Trim());
            while (waterSampleElement.HasChildNodes && waterSampleElement.FirstChild != null)
            {
                waterSampleElement.RemoveChild(waterSampleElement.FirstChild);
            }
            foreach (DataGridViewRow row in gridData.Rows)
            {
                if (row.IsNewRow) continue;
                // Get all cell values
                string sample = row.Cells[COL_SAMPLE].Value?.ToString()?.Trim() ?? "";
                string dtText = row.Cells[COL_DATETIME].Value?.ToString()?.Trim() ?? "";
                DateTime dt = DateTime.ParseExact(dtText, allowedFormats, CultureInfo.InvariantCulture, DateTimeStyles.None);
                string depth = row.Cells[COL_DEPTH].Value?.ToString()?.Trim() ?? "";
                //string x = row.Cells[COL_X].Value?.ToString()?.Trim() ?? "";
                //string y = row.Cells[COL_Y].Value?.ToString()?.Trim() ?? "";
                string ssc = row.Cells[COL_SSC].Value?.ToString()?.Trim() ?? "";
                string notes = row.Cells[COL_NOTES].Value?.ToString()?.Trim() ?? "";
                // Create new XML element
                XmlElement sampleNode = waterSampleElement.OwnerDocument.CreateElement("Sample");
                sampleNode.SetAttribute("Sample", sample);
                sampleNode.SetAttribute("DateTime", dt.ToString("o")); // ISO 8601
                sampleNode.SetAttribute("Depth", depth);
                //sampleNode.SetAttribute("X", x);
                //sampleNode.SetAttribute("Y", y);
                sampleNode.SetAttribute("SSC", ssc);
                sampleNode.SetAttribute("Notes", notes);
                waterSampleElement.AppendChild(sampleNode);
            }
            _project.SaveConfig(saveMode: 1);
        }

        private void WaterSample_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Control && e.KeyCode == Keys.S) // Ctrl + S
            {
                e.SuppressKeyPress = true; // Prevent default behavior
                SaveWaterSample(); // Save the project
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
