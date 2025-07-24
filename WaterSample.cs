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
    public partial class WaterSample : Form
    {
        private readonly XmlElement _parentSurvey;
        private XmlElement _waterSample;
        private bool _isSaved = false;

        private const string COL_SAMPLE = "colSample";
        private const string COL_DATETIME = "colDateTime";
        private const string COL_DEPTH = "colDepth";
        private const string COL_X = "colX";
        private const string COL_Y = "colY";
        private const string COL_SSC = "colSSC";
        private const string COL_NOTES = "colNotes";

        public WaterSample(XmlElement parentSurvey)
        {
            InitializeComponent();
            _parentSurvey = parentSurvey ?? throw new ArgumentNullException(nameof(parentSurvey));

            int waterSampleCount = _parentSurvey.SelectNodes("./WaterSample[@type='Water Sample']").Count;

            string defaultName = $"Water Sample {waterSampleCount + 1}";
            txtName.Text = defaultName;

            _waterSample = _parentSurvey.OwnerDocument.CreateElement("WaterSample");
            _waterSample.SetAttribute("type", "Water Sample");
            _waterSample.SetAttribute("name", defaultName);
        }

        private static bool RowHasAnyData(DataGridViewRow r)
        {
            foreach (DataGridViewCell c in r.Cells)
            {
                if (c.Value != null && !string.IsNullOrWhiteSpace(Convert.ToString(c.Value)))
                {
                    return true;
                }
            }
            return false;
        }

        private static void ClearChildNodes(XmlElement el)
        {
            if (el == null) return;
            while (el.HasChildNodes)
            {
                el.RemoveChild(el.FirstChild);
            }
        }

        private static string GetCellString(DataGridViewRow r, string colName)
        {
            if (!r.DataGridView.Columns.Contains(colName)) return string.Empty;
            object v = r.Cells[colName].Value;
            return v?.ToString().Trim() ?? string.Empty;
        }

        private static bool TryValidateDouble(string s)
        {
            if (string.IsNullOrWhiteSpace(s)) return true; // allow blank
            return double.TryParse(s, out _);
        }

        private void SaveWaterSample()
        {
            var rows = gridData.Rows.Cast<DataGridViewRow>()
                .Where(r => !r.IsNewRow && RowHasAnyData(r))
                .ToList();

            if (rows.Count == 0)
            {
                return;
            }
            string wsName = txtName.Text.Trim();
            if (string.IsNullOrEmpty(wsName))
            {
                MessageBox.Show("Please enter a name for the water sample.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            _waterSample.SetAttribute("name", wsName);
            ClearChildNodes(_waterSample);
            XmlDocument doc = _waterSample.OwnerDocument;

            for (int i = 0; i < rows.Count; i++)
            {
                DataGridViewRow r = rows[i];
                string sName = GetCellString(r, COL_SAMPLE);
                string sDateTime = GetCellString(r, COL_DATETIME);
                string sDepth = GetCellString(r, COL_DEPTH);
                string sX = GetCellString(r, COL_X);
                string sY = GetCellString(r, COL_Y);
                string sSSC = GetCellString(r, COL_SSC);
                string sNotes = GetCellString(r, COL_NOTES);

                if (!DateTime.TryParse(sDateTime, out _))
                {
                    MessageBox.Show($"Row {i + 1}: Invalid DateTime value.", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }
                if (!TryValidateDouble(sDepth) || !TryValidateDouble(sX) || !TryValidateDouble(sY) || !TryValidateDouble(sSSC))
                {
                    MessageBox.Show($"Row {i + 1}: One or more numeric fields (Depth/X/Y/SSC) invalid.", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }

                XmlElement sampleEl = doc.CreateElement("Sample");
                sampleEl.SetAttribute("id", i.ToString());
                if (!string.IsNullOrEmpty(sName)) sampleEl.SetAttribute("Sample Name", sName);
                if (!string.IsNullOrEmpty(sDateTime)) sampleEl.SetAttribute("DateTime", sDateTime);
                if (!string.IsNullOrEmpty(sDepth)) sampleEl.SetAttribute("Depth", sDepth);
                if (!string.IsNullOrEmpty(sX)) sampleEl.SetAttribute("X", sX);
                if (!string.IsNullOrEmpty(sY)) sampleEl.SetAttribute("Y", sY);
                if (!string.IsNullOrEmpty(sSSC)) sampleEl.SetAttribute("SSC", sSSC);
                if (!string.IsNullOrEmpty(sNotes)) sampleEl.SetAttribute("Notes", sNotes);

                _waterSample.AppendChild(sampleEl);
            }
            string projDir = ConfigData.GetProjectDir();
            string wsPath = Path.Combine(projDir, wsName + ".mtws");
            XmlDocument wsDoc = new XmlDocument();
            XmlDeclaration decl = wsDoc.CreateXmlDeclaration("1.0", "UTF-8", null);
            wsDoc.AppendChild(decl);
            wsDoc.AppendChild(wsDoc.ImportNode(_waterSample, true));
            wsDoc.Save(wsPath);

            XmlNode existing = _parentSurvey.SelectNodes("WaterSample")
                .Cast<XmlNode>()
                .FirstOrDefault(n => string.Equals(n.Attributes?["name"]?.Value, wsName, StringComparison.OrdinalIgnoreCase));

            if (existing != null)
            {
                DialogResult reslut = MessageBox.Show($"Water Sample '{wsName}' already exists. Do you want to update it?", "Info", MessageBoxButtons.YesNoCancel, MessageBoxIcon.Warning);
                if (reslut == DialogResult.Yes)
                {
                    _parentSurvey.ReplaceChild(_parentSurvey.OwnerDocument.ImportNode(_waterSample, true), existing);
                }
                else
                {
                    return; // Do not save if user chooses not to update
                }
            }
            else
            {
                _parentSurvey.AppendChild(_parentSurvey.OwnerDocument.ImportNode(_waterSample, true));
            }

            _isSaved = true;


        }

        private void NumericOnly_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (!char.IsControl(e.KeyChar) && !char.IsDigit(e.KeyChar) && e.KeyChar != '.')
            {
                e.Handled = true;
            }
            TextBox tb = sender as TextBox;
            if (e.KeyChar == '.' && tb.Text.Contains("."))
            {
                e.Handled = true;
            }
        }

        private void gridData_CellValidating(object sender, DataGridViewCellValidatingEventArgs e)
        {
            if (gridData.Columns[e.ColumnIndex].Name == "colDateTime")
            {
                if (!DateTime.TryParse(e.FormattedValue.ToString(), out _))
                {
                    gridData.Rows[e.RowIndex].ErrorText = "Invalid DateTime format.";
                    e.Cancel = true; // Cancel the edit
                }
            }
        }

        private void gridData_CellEndEdit(object sender, DataGridViewCellEventArgs e)
        {
            gridData.Rows[e.RowIndex].ErrorText = string.Empty;
        }

        private void gridData_EditingControlShowing(object sender, DataGridViewEditingControlShowingEventArgs e)
        {
            string colName = gridData.Columns[gridData.CurrentCell.ColumnIndex].Name;
            if (colName == "colDepth" || colName == "colX" || colName == "colY" || colName == "colSSC")
            {
                TextBox tb = e.Control as TextBox;
                if (tb != null)
                {
                    tb.KeyPress -= NumericOnly_KeyPress;
                    tb.KeyPress += NumericOnly_KeyPress;
                }
            }
            else
            {
                TextBox tb = e.Control as TextBox;
                if (tb != null)
                {
                    tb.KeyPress -= NumericOnly_KeyPress;
                }
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveWaterSample();
            if (_isSaved)
            {
                this.DialogResult = DialogResult.OK; // Indicate that the form was saved successfully
            }
        }

        private void WaterSample_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (_isSaved) return;

            bool hasData = gridData.Rows
                .Cast<DataGridViewRow>()
                .Any(r => !r.IsNewRow && RowHasAnyData(r));

            if (!hasData && string.IsNullOrWhiteSpace(txtName.Text))
                return;

            DialogResult result = MessageBox.Show(
                "You have unsaved changes. Do you want to save them?",
                "Unsaved Changes",
                MessageBoxButtons.YesNoCancel,
                MessageBoxIcon.Warning);
            if (result == DialogResult.Yes)
            {
                SaveWaterSample();
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
                this.DialogResult = DialogResult.No; // Indicate that the form was closed without saving
                // User chose No, so we can close without saving
                _parentSurvey.RemoveChild(_waterSample);
            }
        }
    }
}
