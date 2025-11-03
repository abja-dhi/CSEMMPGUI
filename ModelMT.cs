using DHI.Generic.MikeZero.DFS;
using DHI.Generic.MikeZero.DFS.dfs123;
using DHI.Generic.MikeZero.DFS.dfsu;
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
    public partial class ModelMT : Form
    {

        public bool isSaved;
        public XmlElement? modelElement;
        public int mode;
        public _ClassConfigurationManager _project = new();

        private void InitializeModel()
        {
            txtModelName.Text = "New MT Model";
            txtFilePath.Text = string.Empty;
            isSaved = true;
        }

        private void PopulateModel()
        {
            if (modelElement == null)
            {
                MessageBox.Show(text: "Invalid MT model node provided.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                this.Close();
                return;
            }
            txtModelName.Text = modelElement.GetAttribute("name");
            XmlNode? pathNode = modelElement.SelectSingleNode("Path");
            txtFilePath.Text = pathNode?.InnerText ?? string.Empty;
            updateCombo(txtFilePath.Text);
            XmlNode? itemNode = modelElement.SelectSingleNode("ItemNumber");
            if (itemNode != null && int.TryParse(itemNode.InnerText, out int itemIndex))
            {
                itemIndex = itemIndex - 1; // Convert to zero-based index
                if (itemIndex >= 0 && itemIndex < comboModelItem.Items.Count)
                {
                    comboModelItem.SelectedIndex = itemIndex;
                }
            }
            comboModelItem.Enabled = true;
            isSaved = true;
        }

        public ModelMT(XmlNode? modelNode)
        {
            InitializeComponent();
            if (modelNode == null)
            {
                InitializeModel();
                mode = 0; // New model mode
                this.Text = "Add MT Model";
            }
            else
            {
                modelElement = modelNode as XmlElement;
                PopulateModel();
                menuNew.Visible = false; // Hide New menu option if editing an existing model
                mode = 1; // Edit model mode
                this.Text = "Edit MT Model";
            }

            this.KeyPreview = true; // Enable form to capture key events
            this.KeyDown += Model_KeyDown; // Attach key down event handler
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    text: "You have unsaved changes. Do you want to save before creating a new MT model?",
                    caption: "Confirm New MT Model",
                    buttons: MessageBoxButtons.YesNoCancel,
                    icon: MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveModel();
                    if (status == 1)
                        InitializeModel();
                    else
                        return;

                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel
                }
                else
                {
                    InitializeModel(); // User chose not to save, proceed with new model
                }
            }
            else
            {
                InitializeModel();
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveModel();
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    text: "You have unsaved changes. Do you want to save before exiting?",
                    caption: "Confirm Exit",
                    buttons: MessageBoxButtons.YesNoCancel,
                    icon: MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveModel();
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
                    return; // User chose to cancel
                }
                else
                {
                    this.Close(); // User chose not to save, proceed with exit  
                }
            }
            else
            {
                this.Close(); // Close the form if there are no unsaved changes
            }
        }

        private void Model_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    text: "You have unsaved changes. Do you want to save before exiting?",
                    caption: "Confirm Exit",
                    buttons: MessageBoxButtons.YesNoCancel,
                    icon: MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveModel();
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

        private void updateCombo(string fileName)
        {
            comboModelItem.Items.Clear();
            string extension = System.IO.Path.GetExtension(fileName).ToLower();
            if (extension == ".dfs2")
            {
                IDfs2File dfsFile = DfsFileFactory.Dfs2FileOpen(fileName);
                int NItems = dfsFile.ItemInfo.Count;
                for (int i = 0; i < NItems; i++)
                {
                    string name = dfsFile.ItemInfo[i].Name;
                    comboModelItem.Items.Add(name);
                }
                dfsFile.Close();

            }
            else if (extension == ".dfs3")
            {
                IDfs3File dfsFile = DfsFileFactory.Dfs3FileOpen(fileName);
                int NItems = dfsFile.ItemInfo.Count;
                for (int i = 0; i < NItems; i++)
                {
                    string name = dfsFile.ItemInfo[i].Name;
                    comboModelItem.Items.Add(name);
                }
                dfsFile.Close();
            }
            else if (extension == ".dfsu")
            {
                IDfsuFile dfsFile = DfsuFile.Open(fileName);
                int NItems = dfsFile.ItemInfo.Count;
                for (int i = 0; i < NItems; i++)
                {
                    string name = dfsFile.ItemInfo[i].Name;
                    comboModelItem.Items.Add(name);
                }
                dfsFile.Close();
            }
            if (comboModelItem.Items.Count > 0)
                comboModelItem.SelectedIndex = 0;
        }

        private void btnLoad_Click(object sender, EventArgs e)
        {
            var ofd = new OpenFileDialog
            {
                Title = "Select Model File",
                Filter = "DFSU (*.dfsu)|*.dfsu",
                Multiselect = false,
            };
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                txtFilePath.Text = ofd.FileName;
                updateCombo(txtFilePath.Text);
                comboModelItem.Enabled = true;
                isSaved = false; // Mark as unsaved changes
            }
        }

        private int SaveModel()
        {
            if (String.IsNullOrEmpty(txtModelName.Text))
            {
                MessageBox.Show(text: "Model name cannot be empty.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return 0;
            }
            if (String.IsNullOrEmpty(txtFilePath.Text))
            {
                MessageBox.Show(text: "File path cannot be empty.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return 0;
            }
            if (!File.Exists(_Utils.GetFullPath(txtFilePath.Text.Trim())))
            {
                MessageBox.Show(text: "File does not exist at the specified path.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return 0;
            }
            if (comboModelItem.SelectedIndex < 0)
            {
                MessageBox.Show(text: "Please select a valid item from the model file.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return 0;
            }
            if (mode == 0)
                SAVE();
            else
                UPDATE();
            isSaved = true;
            return 1; // Return 1 to indicate success
        }

        private void SAVE()
        {
            int id = _project.GetNextId();
            modelElement = _Globals.Config.CreateElement("MTModel");
            modelElement.SetAttribute("name", txtModelName.Text);
            modelElement.SetAttribute("type", "MTModel");
            modelElement.SetAttribute("id", id.ToString());
            modelElement?.SetAttribute("name", txtModelName.Text);
            XmlElement path = _Globals.Config.CreateElement("Path");
            path.InnerText = _Utils.GetFullPath(txtFilePath.Text.Trim());
            modelElement?.AppendChild(path);
            XmlElement item = _Globals.Config.CreateElement("ItemNumber");
            item.InnerText = (comboModelItem.SelectedIndex + 1).ToString();
            modelElement?.AppendChild(item);
            var doc = _Globals.Config.DocumentElement;
            if (doc != null)
            {
                doc.AppendChild(modelElement);
            }
            _project.SaveConfig(saveMode: 1);
        }

        private void UPDATE()
        {
            modelElement?.SetAttribute("name", txtModelName.Text);
            XmlNode path = modelElement.SelectSingleNode("Path");
            path.InnerText = _Utils.GetFullPath(txtFilePath.Text.Trim());
            XmlNode item = modelElement.SelectSingleNode("ItemNumber");
            item.InnerText = (comboModelItem.SelectedIndex + 1).ToString();
            _project.SaveConfig(saveMode: 1);
        }

        private void Model_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Control && e.KeyCode == Keys.S) // Ctrl + S
            {
                e.SuppressKeyPress = true; // Prevent default behavior
                SaveModel(); // Save the project
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

        private void menuDfs22Dfsu_Click(object sender, EventArgs e)
        {
            var ofd = new OpenFileDialog
            {
                Title = "Select Model File",
                Filter = "DFS2 (*.dfs2)|*.dfs2",
                Multiselect = false,
            };
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                var input = new Dictionary<string, string>
                {
                    {"Task", "Dfs2ToDfsu" },
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
                    MessageBox.Show("Dfs2 file converted to Dfsu successfully.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
        }
    }
}
