using Python.Runtime;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public static class _Utils
    {
        public static string[] ParseCSVAndReturnColumns(string filePath, string separator, int headerLine)
        {
            var inputs = new Dictionary<string, string>
            {
                { "Task", "GetColumnsFromCSV" },
                { "Path", filePath },
                { "Sep", separator },
                { "Header", headerLine.ToString() }
            };
            string xmlInput = _Tools.GenerateInput(inputs);
            XmlDocument doc = _Tools.CallPython(xmlInput);
            Dictionary<string, string> output = _Tools.ParseOutput(doc);
            if (output.ContainsKey("Error"))
            {
                MessageBox.Show(output["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return Array.Empty<string>();
            }
            int nColumns = Convert.ToInt32(output["NColumns"]);
            if (nColumns == 0)
            {
                MessageBox.Show("No columns found in the CSV file.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return Array.Empty<string>();
            }
            else
            {
                var columns = new string[nColumns];
                for (int i = 0; i < nColumns; i++)
                {
                    columns[i] = output[$"Column{i}"] ?? $"Column{i}";
                }
                return columns;
            }
        }
    }
}
