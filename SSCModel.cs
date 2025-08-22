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

namespace CSEMMPGUI_v1
{
    public partial class SSCModel : Form
    {

        public bool isSaved;
        public XmlElement? sscElement;
        public int mode;
        public string modelType;
        public _ClassConfigurationManager _project = new();

        public bool _updatingChecks;


        private void Tree_AfterCheck(object sender, TreeViewEventArgs e)
        {
            if (_updatingChecks) return;
            try
            {
                _updatingChecks = true;

                // If a parent (e.g., Survey) is checked/unchecked, cascade to all descendants
                SetCheckedRecursive(e.Node, e.Node.Checked);

                // After changing a child, update parents to reflect "all children checked" state
                UpdateParents(e.Node);
            }
            finally
            {
                _updatingChecks = false;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private void SetCheckedRecursive(TreeNode node, bool isChecked)
        {
            foreach (TreeNode child in node.Nodes)
            {
                child.Checked = isChecked;
                if (child.Nodes.Count > 0)
                    SetCheckedRecursive(child, isChecked);
            }
        }

        private void UpdateParents(TreeNode node)
        {
            TreeNode? parent = node.Parent;
            while (parent != null)
            {
                bool allChecked = true;
                foreach (TreeNode child in parent.Nodes)
                {
                    if (!child.Checked)
                    {
                        allChecked = false;
                        break;
                    }
                }

                parent.Checked = allChecked;
                parent = parent.Parent;
            }
        }

        private void FillTree(TreeView tree, string elements)
        {
            tree.Nodes.Clear();
            foreach (XmlElement survey in _Globals.Config.SelectNodes("//Survey"))
            {
                string surveyName = survey.GetAttribute("name");
                TreeNode surveyNode = new TreeNode(surveyName);
                surveyNode.Tag = survey;
                foreach (XmlElement element in survey.SelectNodes(elements))
                {
                    string elementName = element.GetAttribute("name");
                    string elementID = element.GetAttribute("id");
                    TreeNode elementNode = new TreeNode(elementName);
                    elementNode.Tag = element;
                    surveyNode.Nodes.Add(elementNode);
                }
                if (surveyNode.Nodes.Count > 0)
                {
                    tree.Nodes.Add(surveyNode);
                }
            }
            tree.ExpandAll();
        }

        private void FillTrees()
        {
            FillTree(treeNTU2SSC, "OBSVerticalProfile | WaterSample");
            FillTree(treeBKS2SSC, "VesselMountedADCP | WaterSample");
        }

        private void SetCheck(TreeView tree)
        {
            foreach (TreeNode surveyNode in tree.Nodes)
            {
                foreach (TreeNode instrumentNode in surveyNode.Nodes)
                {
                    XmlNode? node = instrumentNode.Tag as XmlNode;
                    if (node is XmlElement elem)
                    {
                        string id = elem.GetAttribute("id");
                        XmlNode instrument = sscElement.SelectSingleNode($"Instrument[text()='{id}']") ?? null;
                        if (instrument != null)
                        {
                            instrumentNode.Checked = true;
                        }
                        else
                        {
                            instrumentNode.Checked = false;
                        }
                    }
                }
            }
        }

        private void SetChecks()
        {
            if (modelType == "NTU2SSC")
                SetCheck(treeNTU2SSC);
            else
                SetCheck(treeBKS2SSC);

        }

        private void InitializeSSCModel()
        {
            txtModelName.Text = "New SSC Model";
            txtA.Text = string.Empty;
            txtB.Text = string.Empty;
            //txtC.Text = string.Empty;
            comboFits.SelectedIndex = 0;
            FillTrees();
            isSaved = true;
        }

        private void PopulateSSCModel()
        {
            if (sscElement == null)
            {
                MessageBox.Show("Invalid SSC model node provided.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                this.Close();
                return;
            }
            txtModelName.Text = sscElement?.GetAttribute("name");
            string calcMode = sscElement.SelectSingleNode("Mode")?.InnerText;
            if (calcMode == "Manual")
                rbManual.Checked = true;
            else
                rbAuto.Checked = true;
            txtA.Text = sscElement.SelectSingleNode("A")?.InnerText ?? string.Empty;
            txtB.Text = sscElement.SelectSingleNode("B")?.InnerText ?? string.Empty;
            //txtC.Text = sscElement.SelectSingleNode("C")?.InnerText ?? string.Empty;
            comboFits.SelectedItem = sscElement.SelectSingleNode("Fit")?.InnerText ?? "Linear";
            FillTrees();
            SetChecks();
            isSaved = true;
        }

        public SSCModel(XmlNode? sscModelNode)
        {
            InitializeComponent();
            treeNTU2SSC.CheckBoxes = true;
            treeBKS2SSC.CheckBoxes = true;
            treeNTU2SSC.AfterCheck += Tree_AfterCheck;
            treeBKS2SSC.AfterCheck += Tree_AfterCheck;
            if (sscModelNode == null)
            {
                InitializeSSCModel();
                mode = 0; // New SSC model mode
                this.Text = "Add SSC Model";
            }
            else
            {
                sscElement = sscModelNode as XmlElement;
                modelType = sscElement?.GetAttribute("type");
                PopulateSSCModel();
                menuNew.Visible = false; // Hide New menu option if editing an existing SSC model
                if (modelType == "NTU2SSC")
                {
                    rbNTU2SSC.Checked = true;
                    rbBKS2SSC.Enabled = false;
                    treeBKS2SSC.Enabled = false;
                }
                else
                {
                    rbNTU2SSC.Enabled = false;
                    rbBKS2SSC.Checked = true;
                    treeNTU2SSC.Enabled = false;
                }
                mode = 1; // Edit SSC model mode
                this.Text = "Edit SSC Model";
            }
        }

        private void menuNew_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    text: "You have unsaved changes. Do you want to save before creating a new model?",
                    caption: "Confirm New Model",
                    buttons: MessageBoxButtons.YesNoCancel,
                    icon: MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    int status = SaveSSCModel();
                    if (status == 1)
                        InitializeSSCModel();
                    else
                        return;

                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel
                }
                else
                {
                    InitializeSSCModel(); // User chose not to save, proceed with new model
                }
            }
            else
            {
                InitializeSSCModel();
            }
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveSSCModel();
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
                    int status = SaveSSCModel();
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

        private void SSCModel_FormClosing(object sender, FormClosingEventArgs e)
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
                    int status = SaveSSCModel();
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

        private void rbNTU2SSC_CheckedChanged(object sender, EventArgs e)
        {
            if (rbNTU2SSC.Checked)
            {
                treeNTU2SSC.Enabled = true;
                treeBKS2SSC.Enabled = false;
            }
            else
            {
                treeNTU2SSC.Enabled = false;
                treeBKS2SSC.Enabled = true;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private void rbManual_CheckedChanged(object sender, EventArgs e)
        {
            if (rbManual.Checked)
            {
                tableManual.Enabled = true;
                tableTrees.Enabled = false;
            }
            else
            {
                tableManual.Enabled = false;
                tableTrees.Enabled = true;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private bool ValidateSelection()
        {
            TreeView tree;
            if (rbNTU2SSC.Checked)
            {
                tree = treeNTU2SSC;
            }
            else
            {
                tree = treeBKS2SSC;
            }
            if (rbManual.Checked)
                return true; // Manual mode, no selection needed
            else
            {
                int counter = 0;
                foreach (TreeNode surveyNode in tree.Nodes)
                {
                    foreach (TreeNode instrumentNode in surveyNode.Nodes)
                    {
                        XmlElement element = instrumentNode.Tag as XmlElement;
                        if (instrumentNode.Checked && element != null)
                        {
                            counter++;
                        }
                    }
                }
                if (counter == 0)
                {
                    return false; // No instruments selected, return failure
                }
                else
                {
                    return true; // Instruments added successfully
                }
            }
        }

        private int SaveSSCModel()
        {
            if (String.IsNullOrEmpty(txtModelName.Text))
            {
                MessageBox.Show(text: "Model name cannot be empty.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return 0;
            }
            if (rbManual.Checked && (String.IsNullOrEmpty(txtA.Text) || String.IsNullOrEmpty(txtB.Text)))
            {
                MessageBox.Show(text: "All coefficients A, B, and C must be provided.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return 0;
            }
            if (!ValidateSelection())
            {
                MessageBox.Show(text: "Please select at least one instrument in Auto mode.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return 0;
            }
            if (mode == 0)
                SAVE();
            else
                UPDATE();
            isSaved = true;
            return 1; // Return 1 to indicate success
        }

        private void CreateSSCModel()
        {
            if (rbNTU2SSC.Checked)
            {
                sscElement = _Globals.Config.CreateElement("NTU2SSC");
                modelType = "NTU2SSC";
                TreeView tree = treeNTU2SSC;
            }
            else
            {
                sscElement = _Globals.Config.CreateElement("BKS2SSC");
                modelType = "BKS2SSC";
                TreeView tree = treeBKS2SSC;
            }
            sscElement.SetAttribute("name", txtModelName.Text);
            sscElement.SetAttribute("type", modelType);
            sscElement.SetAttribute("id", _project.GetNextId().ToString());
            XmlElement modeElement = _Globals.Config.CreateElement("Mode");
            modeElement.InnerText = rbManual.Checked ? "Manual" : "Auto";
            sscElement.AppendChild(modeElement);
            XmlElement fitElement = _Globals.Config.CreateElement("Fit");
            fitElement.InnerText = comboFits.SelectedItem?.ToString() ?? "Linear";
            sscElement.AppendChild(fitElement);
            if (rbManual.Checked)
            {
                XmlElement aElement = _Globals.Config.CreateElement("A");
                aElement.InnerText = txtA.Text;
                sscElement.AppendChild(aElement);
                XmlElement bElement = _Globals.Config.CreateElement("B");
                bElement.InnerText = txtB.Text;
                sscElement.AppendChild(bElement);
            }
            else
            {
                foreach (TreeNode surveyNode in treeNTU2SSC.Nodes)
                {
                    foreach (TreeNode instrumentNode in surveyNode.Nodes)
                    {
                        XmlElement element = instrumentNode.Tag as XmlElement;
                        if (instrumentNode.Checked && element != null)
                        {
                            XmlElement instrumentElement = _Globals.Config.CreateElement("Instrument");
                            instrumentElement.InnerText = element.GetAttribute("id");
                            sscElement.AppendChild(instrumentElement);
                        }
                    }
                }
            }
        }

        private void SAVE()
        {
            CreateSSCModel();
            var doc = _Globals.Config.DocumentElement;
            if (doc != null)
            {
                doc.AppendChild(sscElement);
            }
            _project.SaveConfig(saveMode: 1);
            int id = _project.GetNextId();
            _Globals.Config.DocumentElement.SetAttribute("nextid", (id + 1).ToString());
        }

        private void UPDATE()
        {
            sscElement.SetAttribute("name", txtModelName.Text);
            XmlNode? modeNode = sscElement.SelectSingleNode("Mode");
            modeNode.InnerText = rbManual.Checked ? "Manual" : "Auto";
            XmlNode? fitNode = sscElement.SelectSingleNode("Fit");
            fitNode.InnerText = comboFits.SelectedItem?.ToString() ?? "Linear";
            // Remove existing A and B nodes if they exist for fresh update
            XmlNode? aNode = sscElement.SelectSingleNode("A");
            if (aNode != null)
                sscElement.RemoveChild(aNode);
            XmlNode? bNode = sscElement.SelectSingleNode("B");
            if (bNode != null)
                sscElement.RemoveChild(bNode);
            // Clear existing instruments before adding new ones
            XmlNodeList existingInstruments = sscElement.SelectNodes("Instrument");
            foreach (XmlNode instrument in existingInstruments)
            {
                sscElement.RemoveChild(instrument);
            }
            if (rbManual.Checked)
            {
                XmlElement aElement = _Globals.Config.CreateElement("A");
                aElement.InnerText = txtA.Text;
                sscElement.AppendChild(aElement);
                XmlElement bElement = _Globals.Config.CreateElement("B");
                bElement.InnerText = txtB.Text;
                sscElement.AppendChild(bElement);
            }
            else
            {
                TreeView tree = rbNTU2SSC.Checked ? treeNTU2SSC : treeBKS2SSC;
                foreach (TreeNode surveyNode in tree.Nodes)
                {
                    foreach (TreeNode instrumentNode in surveyNode.Nodes)
                    {
                        XmlElement element = instrumentNode.Tag as XmlElement;
                        if (instrumentNode.Checked && element != null)
                        {
                            XmlElement instrumentElement = _Globals.Config.CreateElement("Instrument");
                            instrumentElement.InnerText = element.GetAttribute("id");
                            sscElement.AppendChild(instrumentElement);
                        }
                    }
                }
            }
            _project.SaveConfig(saveMode: 1);
        }
    }
}
