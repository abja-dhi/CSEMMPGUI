using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CSEMMPGUI_v1
{
    public partial class UtilsCSVColumnSelector : Form
    {
        string[] _columns;
        string[] _items;
        bool[] _status;
        public string[] _selectedColumns;
        public UtilsCSVColumnSelector(string[] columns, string[] items, bool[] status)
        {
            InitializeComponent();
            _columns = columns;
            _items = items;
            _status = status;
            for (int i = 0; i < items.Length; i++)
            {
                if (tableMain.Controls["lbl" + i.ToString()] is Label lbl)
                {
                    lbl.Text = items[i];
                    lbl.Visible = true;
                    if (tableMain.Controls["combo" + i.ToString()] is ComboBox combo)
                    {
                        combo.Items.Clear();
                        combo.Items.AddRange(columns);
                        combo.SelectedIndex = 0; // Default to the first column
                        combo.Visible = true;
                        if (!status[i])
                            combo.Items.Insert(0, "");
                    }

                    if (status[i] == true && tableMain.Controls["star" + i.ToString()] is Label star)
                        star.Visible = true;
                }
            }
        }

        private void btnOK_Click(object sender, EventArgs e)
        {
            _selectedColumns = new string[_items.Length];
            for (int i = 0; i < _items.Length; i++)
            {
                if (tableMain.Controls["combo" + i.ToString()] is ComboBox combo)
                {
                    if (_status[i] == false && combo.SelectedIndex == 0)
                    {
                        _selectedColumns[i] = "-1"; // If the column is not selected, set to -1
                    }
                    else if (_status[i] == false)
                    {
                        _selectedColumns[i] = (combo.SelectedIndex - 1).ToString();
                    }
                    else
                    {
                        _selectedColumns[i] = combo.SelectedIndex.ToString();
                    }
                }
            }
            this.DialogResult = DialogResult.OK;
            this.Close();
        }

        private void UtilsCSVColumnSelector_FormClosing(object sender, FormClosingEventArgs e)
        {
            this.DialogResult = DialogResult.Cancel;
        }
    }
}
