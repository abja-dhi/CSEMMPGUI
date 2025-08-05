using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Globalization;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;


namespace CSEMMPGUI_v1
{
    public partial class EditWaterSample : Form
    {
        public bool isSaved;
        public XmlElement? waterSampleElement;
        

        private const string COL_SAMPLE = "colSampleName";
        private const string COL_DATETIME = "colDateTime";
        private const string COL_DEPTH = "colDepth";
        private const string COL_X = "colX";
        private const string COL_Y = "colY";
        private const string COL_SSC = "colSSC";
        private const string COL_NOTES = "colNotes";

        public string[] allowedFormats = new[]
            {
                "MMMM d, yyyy HH:mm:ss",
                "MMM d, yyyy HH:mm:ss",
                "d MMMM, yyyy HH:mm:ss",
                "d MMM, yyyy HH:mm:ss"
            };

        public EditWaterSample(XmlNode waterSampleNode)
        {
            InitializeComponent();
            DateTime now = DateTime.Now;
            string tooltip = "Accepted formats are\n:";
            foreach (string format in allowedFormats)
            {
                tooltip += $"\n{now.ToString(format)}";
            }
            DataGridViewColumn colDateTime = gridData.Columns[COL_DATETIME];
            colDateTime.ToolTipText = tooltip.TrimEnd();
            InitializeWaterSample(waterSampleNode);
        }

        public void InitializeWaterSample(XmlNode waterSampleNode)
        {
            waterSampleElement = waterSampleNode as XmlElement;
            if (waterSampleElement == null)
            {
                MessageBox.Show("Invalid water sample node provided.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                this.Close();
                return;

            }
            txtName.Text = waterSampleElement.GetAttribute("name");
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
                    row.Cells[COL_X].Value = sampleElement.GetAttribute("X");
                    row.Cells[COL_Y].Value = sampleElement.GetAttribute("Y");
                    row.Cells[COL_SSC].Value = sampleElement.GetAttribute("SSC");
                    row.Cells[COL_NOTES].Value = sampleElement.GetAttribute("Notes");
                }
            }
            isSaved = true;
        }
        
        public int UpdateWaterSample()
        {
            if (waterSampleElement == null)
            {
                MessageBox.Show("Water sample element is not initialized.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return -1; // Return 0 to indicate failure
            }
            if (String.IsNullOrEmpty(txtName.Text.Trim()))
            {
                MessageBox.Show("Please assign a name to the water sample", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return -1; // Return 0 to indicate failure
            }
            if (!ValidateSampleGrid())
            {
                return -1; // Return 0 to indicate failure
            }
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
                string x = row.Cells[COL_X].Value?.ToString()?.Trim() ?? "";
                string y = row.Cells[COL_Y].Value?.ToString()?.Trim() ?? "";
                string ssc = row.Cells[COL_SSC].Value?.ToString()?.Trim() ?? "";
                string notes = row.Cells[COL_NOTES].Value?.ToString()?.Trim() ?? "";
                // Create new XML element
                XmlElement sampleNode = waterSampleElement.OwnerDocument.CreateElement("Sample");
                sampleNode.SetAttribute("Sample", sample);
                sampleNode.SetAttribute("DateTime", dt.ToString("o")); // ISO 8601
                sampleNode.SetAttribute("Depth", depth);
                sampleNode.SetAttribute("X", x);
                sampleNode.SetAttribute("Y", y);
                sampleNode.SetAttribute("SSC", ssc);
                sampleNode.SetAttribute("Notes", notes);
                waterSampleElement.AppendChild(sampleNode);
            }
            return 1; // Return 1 to indicate success
        }

        public int SaveInstrument()
        {
            int status = UpdateWaterSample();
            if (status < 0)
                return 0;
            _ClassConfigurationManager.SaveConfig(saveMode: 1);
            isSaved = true; // Mark as saved after saving
            return 1; // Return 1 to indicate success
        }

        public bool ValidateSampleGrid()
        {
            foreach (DataGridViewRow row in gridData.Rows)
            {
                if (row.IsNewRow) continue;

                string? sample = row.Cells[COL_SAMPLE].Value?.ToString()?.Trim();
                string? dtText = row.Cells[COL_DATETIME].Value?.ToString()?.Trim();
                string? depth = row.Cells[COL_DEPTH].Value?.ToString()?.Trim();
                string? x = row.Cells[COL_X].Value?.ToString()?.Trim();
                string? y = row.Cells[COL_Y].Value?.ToString()?.Trim();
                string? ssc = row.Cells[COL_SSC].Value?.ToString()?.Trim();

                // Check required fields
                if (string.IsNullOrWhiteSpace(sample) ||
                    string.IsNullOrWhiteSpace(dtText) ||
                    string.IsNullOrWhiteSpace(depth) ||
                    string.IsNullOrWhiteSpace(x) ||
                    string.IsNullOrWhiteSpace(y) ||
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

        private void menuSave_Click(object sender, EventArgs e)
        {
            int status = SaveInstrument();
            isSaved = true; // Mark as saved after saving
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            int status = 1;
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current instrument has unsaved changes. Do you want to save them before exiting?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    status = SaveInstrument(); // Save the current instrument
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel, do not exit
                }
            }
            if (status == 0)
            {
                MessageBox.Show("Failed to save the current instrument. Please resolve any issues before exiting.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return; // If saving failed, do not exit
            }
            this.Close(); // Close the form
        }

        private void AddWaterSample_FormClosing(object sender, FormClosingEventArgs e)
        {
            int status = 1;
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    "Current instrument has unsaved changes. Do you want to save them before exiting?",
                    "Unsaved Changes",
                    MessageBoxButtons.YesNoCancel,
                    MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    status = SaveInstrument(); // Save the current instrument
                }
                else if (result == DialogResult.Cancel)
                {
                    e.Cancel = true; // Cancel the form closing event
                    return; // User chose to cancel, do not exit
                }
            }
            if (status == 0)
            {
                MessageBox.Show("Failed to save the current instrument. Please resolve any issues before exiting.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                e.Cancel = true; // Cancel the form closing event
                return; // If saving failed, do not exit
            }

        }

        private void txtName_TextChanged(object sender, EventArgs e)
        {
            isSaved = false; // Mark as unsaved when the name changes
        }

        private void gridData_CellValueChanged(object sender, DataGridViewCellEventArgs e)
        {
            isSaved = false; // Mark as unsaved when any input changes
        }

        private void gridData_EditingControlShowing(object sender, DataGridViewEditingControlShowingEventArgs e)
        {
            TextBox tb = e.Control as TextBox;
            if (tb == null) return;

            // Always remove the handler first to avoid stacking
            tb.KeyPress -= NumericOnly_KeyPress;

            string colName = gridData.Columns[gridData.CurrentCell.ColumnIndex].Name;

            if (colName == COL_X || colName == COL_Y || colName == COL_DEPTH || colName == COL_SSC)
            {
                tb.KeyPress += NumericOnly_KeyPress;
            }
        }

        // Update the NumericOnly_KeyPress method signature to match the expected delegate nullability
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
    }
}
