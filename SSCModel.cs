using NetTopologySuite.Operation.Valid;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics.Metrics;
using System.Drawing;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using System.Xml.Linq;

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
            bool isBKS2NTU = tree.Name == "treeBKS2NTU";
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
                    string elementType = element.GetAttribute("type");
                    bool isValid = true;
                    if (isBKS2NTU && elementType == "OBSVerticalProfile")
                    {
                        XmlNode elementFileInfo = element.SelectSingleNode("FileInfo");
                        XmlNode elementSSCModel = elementFileInfo.SelectSingleNode("SSCModelID");
                        if (elementSSCModel == null || string.IsNullOrEmpty(elementSSCModel.InnerText))
                        {
                            isValid = false; // No SSC model associated
                        }
                    }
                    if (!isValid) continue; // Skip invalid elements
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
            FillTree(treeBKS2NTU, "VesselMountedADCP | OBSVerticalProfile");
        }

        private void SetCheck(TreeView tree)
        {
            XmlNodeList instrument = sscElement.SelectNodes($"Instrument");
            List<string> instrumentIds = new List<string>();
            foreach (XmlNode inst in instrument)
            {
                if (inst is XmlElement instElem)
                {
                    string ID = instElem.SelectSingleNode("ID")?.InnerText;
                    instrumentIds.Add(ID);
                }
            }
            foreach (TreeNode surveyNode in tree.Nodes)
            {
                foreach (TreeNode instrumentNode in surveyNode.Nodes)
                {
                    XmlNode? node = instrumentNode.Tag as XmlNode;
                    if (node is XmlElement elem)
                    {
                        string id = elem.GetAttribute("id");
                        if (instrumentIds.Contains(id))
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
            else if (modelType == "BKS2NTU")
                SetCheck(treeBKS2NTU);
            else if (modelType == "BKS2SSC")
                SetCheck(treeBKS2SSC);

        }

        private void InitializeSSCModel()
        {
            txtModelName.Text = "New SSC Model";
            txtA.Text = string.Empty;
            txtB.Text = string.Empty;
            txtC.Text = string.Empty;
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
            treeBKS2NTU.CheckBoxes = true;
            treeNTU2SSC.AfterCheck += Tree_AfterCheck;
            treeBKS2SSC.AfterCheck += Tree_AfterCheck;
            treeBKS2NTU.AfterCheck += Tree_AfterCheck;
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
                    rbBKS2NTU.Enabled = false;
                    treeBKS2SSC.Enabled = false;
                    treeBKS2NTU.Enabled = false;
                }
                else if (modelType == "BKS2SSC")
                {
                    rbBKS2SSC.Checked = true;
                    rbNTU2SSC.Enabled = false;
                    rbBKS2NTU.Enabled = false;
                    treeNTU2SSC.Enabled = false;
                    treeBKS2NTU.Enabled = false;
                }
                else if (modelType == "BKS2NTU")
                {
                    rbBKS2NTU.Checked = true;
                    rbBKS2SSC.Enabled = false;
                    rbNTU2SSC.Enabled = false;
                    treeNTU2SSC.Enabled = false;
                    treeBKS2SSC.Enabled = false;
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
                treeBKS2NTU.Enabled = false;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private void rbBKS2SSC_CheckedChanged(object sender, EventArgs e)
        {
            if (rbBKS2SSC.Checked)
            {
                treeBKS2SSC.Enabled = true;
                treeNTU2SSC.Enabled = false;
                treeBKS2NTU.Enabled = false;
            }
            isSaved = false; // Mark as unsaved changes
        }

        private void rbBKS2NTU_CheckedChanged(object sender, EventArgs e)
        {
            if (rbBKS2NTU.Checked)
            {
                treeBKS2NTU.Enabled = true;
                treeNTU2SSC.Enabled = false;
                treeBKS2SSC.Enabled = false;
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
            tree = rbNTU2SSC.Checked ? treeNTU2SSC
                : rbBKS2SSC.Checked ? treeBKS2SSC
                : treeBKS2NTU;
            if (rbManual.Checked)
                return true; // Manual mode, no selection needed
            else
            {
                int counter = 0;
                int waterSamples = 0;
                int obss = 0;
                int adcps = 0;
                foreach (TreeNode surveyNode in tree.Nodes)
                {
                    foreach (TreeNode instrumentNode in surveyNode.Nodes)
                    {
                        XmlElement element = instrumentNode.Tag as XmlElement;
                        if (instrumentNode.Checked && element != null)
                        {
                            if (element.GetAttribute("type") == "WaterSample")
                                waterSamples++;
                            if (element.GetAttribute("type") == "OBSVerticalProfile")
                                obss++;
                            if (element.GetAttribute("type") == "VesselMountedADCP")
                                adcps++;
                            counter++;
                        }
                    }
                }
                if (counter == 0)
                {
                    MessageBox.Show(text: "At least one instrument must be selected in Auto mode.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                    return false; // No instruments selected, return failure
                }
                else
                {
                    if (rbNTU2SSC.Checked && (obss == 0 || waterSamples == 0))
                    {
                        MessageBox.Show(text: "At least one OBS and one Water Sample must be selected for NTU to SSC model.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                        return false; // Instruments selection invalid
                    }
                    if (rbBKS2SSC.Checked && (adcps == 0 || waterSamples == 0))
                    {
                        MessageBox.Show(text: "At least one ADCP and one Water Sample must be selected for BKS to SSC model.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                        return false; // Instruments selection invalid
                    }
                    if (rbBKS2NTU.Checked && (adcps == 0 || obss == 0))
                    {
                        MessageBox.Show(text: "At least one ADCP and one OBS must be selected for BKS to NTU model.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                        return false; // Instruments selection invalid
                    }
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
            TreeView tree;
            string label1;
            string label2;
            if (rbNTU2SSC.Checked)
            {
                sscElement = _Globals.Config.CreateElement("NTU2SSC");
                modelType = "NTU2SSC";
                tree = treeNTU2SSC;
                label1 = "NTU";
                label2 = "SSC";
            }
            else if (rbBKS2SSC.Checked)
            {
                sscElement = _Globals.Config.CreateElement("BKS2SSC");
                modelType = "BKS2SSC";
                tree = treeBKS2SSC;
                label1 = "AbsoluteBackscatter";
                label2 = "SSC";
            }
            else
            {
                sscElement = _Globals.Config.CreateElement("BKS2NTU");
                modelType = "BKS2NTU";
                tree = treeBKS2NTU;
                label1 = "AbsoluteBackscatter";
                label2 = "SSC";
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
                foreach (TreeNode surveyNode in tree.Nodes)
                {
                    foreach (TreeNode instrumentNode in surveyNode.Nodes)
                    {
                        XmlElement element = instrumentNode.Tag as XmlElement;
                        if (instrumentNode.Checked && element != null)
                        {
                            XmlElement instrumentElement = _Globals.Config.CreateElement("Instrument");
                            XmlElement instrumentID = _Globals.Config.CreateElement("ID");
                            instrumentID.InnerText = element.GetAttribute("id");
                            instrumentElement.AppendChild(instrumentID);
                            XmlElement instrumentType = _Globals.Config.CreateElement("Type");
                            instrumentType.InnerText = element.GetAttribute("type");
                            instrumentElement.AppendChild(instrumentType);
                            sscElement.AppendChild(instrumentElement);
                        }
                    }
                }
                Dictionary<string, string> inputs = null;
                inputs = new Dictionary<string, string>
                {
                    { "Task", modelType },
                    { "Project", _Globals.Config.OuterXml.ToString() },
                    { "SSCModel", sscElement.OuterXml.ToString() },
                };
                string xmlInput = _Tools.GenerateInput(inputs);
                XmlDocument result = _Tools.CallPython(xmlInput);
                Dictionary<string, string> outputs = _Tools.ParseOutput(result);
                if (outputs.ContainsKey("Error"))
                {
                    MessageBox.Show(outputs["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                XmlElement aElement = _Globals.Config.CreateElement("A");
                aElement.InnerText = outputs["A"];
                sscElement.AppendChild(aElement);
                XmlElement bElement = _Globals.Config.CreateElement("B");
                bElement.InnerText = outputs["B"];
                sscElement.AppendChild(bElement);
                XmlElement rmseElement = _Globals.Config.CreateElement("RMSE");
                rmseElement.InnerText = outputs["RMSE"];
                sscElement.AppendChild(rmseElement);
                XmlElement r2Element = _Globals.Config.CreateElement("R2");
                r2Element.InnerText = outputs["R2"];
                sscElement.AppendChild(r2Element);
                XmlElement Data = _Globals.Config.CreateElement("Data");
                double[] data1 = ParseArray(outputs[label1]);
                double[] data2 = ParseArray(outputs[label2]);
                for (int i = 0; i < data1.Length; i++)
                {
                    XmlElement point = _Globals.Config.CreateElement("Point");
                    XmlElement dataValue1 = _Globals.Config.CreateElement(label1);
                    dataValue1.InnerText = data1[i].ToString();
                    point.AppendChild(dataValue1);
                    XmlElement dataValue2 = _Globals.Config.CreateElement(label2);
                    dataValue2.InnerText = data2[i].ToString();
                    point.AppendChild(dataValue2);
                    Data.AppendChild(point);
                }
                sscElement.AppendChild(Data);
                XmlElement root = _Globals.Config.CreateElement("Pairs");
                var matches = Regex.Matches(outputs["Pairs"], @"\{([^}]+)\}");
                foreach (Match match in matches)
                {
                    XmlElement pair = _Globals.Config.CreateElement("Pair");
                    var kvs = Regex.Matches(match.Value, @"'([^']+)'\s*:\s*'([^']+)'");
                    foreach (Match kv in kvs)
                    {
                        string key = kv.Groups[1].Value;
                        string value = kv.Groups[2].Value;
                        XmlElement kvElement = _Globals.Config.CreateElement(key);
                        kvElement.InnerText = value;
                        pair.AppendChild(kvElement);
                    }
                    root.AppendChild(pair);
                }
                sscElement.AppendChild(root);
            }
        }

        static double[] ParseArray(string raw)
        {
            return raw
                .Trim('[', ']')                                // remove brackets
                .Split(new[] { ' ', '\t', '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries)
                .Select(s => double.Parse(s, CultureInfo.InvariantCulture))
                .ToArray();
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
            TreeView tree;
            string label1;
            string label2;
            if (rbNTU2SSC.Checked)
            {
                modelType = "NTU2SSC";
                tree = treeNTU2SSC;
                label1 = "NTU";
                label2 = "SSC";
            }
            else if (rbBKS2SSC.Checked)
            {
                modelType = "BKS2SSC";
                tree = treeBKS2SSC;
                label1 = "AbsoluteBackscatter";
                label2 = "SSC";
            }
            else
            {
                modelType = "BKS2NTU";
                tree = treeBKS2NTU;
                label1 = "AbsoluteBackscatter";
                label2 = "SSC";
            }
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
            XmlNode? r2Node = sscElement.SelectSingleNode("R2");
            if (r2Node != null)
                sscElement.RemoveChild(r2Node);
            XmlNode? rmseNode = sscElement.SelectSingleNode("RMSE");
            if (rmseNode != null)
                sscElement.RemoveChild(rmseNode);
            XmlNode? dataNode = sscElement.SelectSingleNode("Data");
            if (dataNode != null)
                sscElement.RemoveChild(dataNode);
            XmlNode? pairsNode = sscElement.SelectSingleNode("Pairs");
            if (pairsNode != null)
                sscElement.RemoveChild(pairsNode);
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
                foreach (TreeNode surveyNode in tree.Nodes)
                {
                    foreach (TreeNode instrumentNode in surveyNode.Nodes)
                    {
                        XmlElement element = instrumentNode.Tag as XmlElement;
                        if (instrumentNode.Checked && element != null)
                        {
                            XmlElement instrumentElement = _Globals.Config.CreateElement("Instrument");
                            XmlElement instrumentID = _Globals.Config.CreateElement("ID");
                            instrumentID.InnerText = element.GetAttribute("id");
                            instrumentElement.AppendChild(instrumentID);
                            XmlElement instrumentType = _Globals.Config.CreateElement("Type");
                            instrumentType.InnerText = element.GetAttribute("type");
                            instrumentElement.AppendChild(instrumentType);
                            sscElement.AppendChild(instrumentElement);
                        }
                    }
                }

                Dictionary<string, string> inputs = null;

                inputs = new Dictionary<string, string>
                {
                    { "Task", modelType },
                    { "Project", _Globals.Config.OuterXml.ToString() },
                    { "SSCModel", sscElement.OuterXml.ToString() },
                };
                string xmlInput = _Tools.GenerateInput(inputs);
                XmlDocument result = _Tools.CallPython(xmlInput);
                Dictionary<string, string> outputs = _Tools.ParseOutput(result);
                if (outputs.ContainsKey("Error"))
                {
                    MessageBox.Show(outputs["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                XmlElement aElement = _Globals.Config.CreateElement("A");
                aElement.InnerText = outputs["A"];
                sscElement.AppendChild(aElement);
                XmlElement bElement = _Globals.Config.CreateElement("B");
                bElement.InnerText = outputs["B"];
                sscElement.AppendChild(bElement);
                XmlElement rmseElement = _Globals.Config.CreateElement("RMSE");
                rmseElement.InnerText = outputs["RMSE"];
                sscElement.AppendChild(rmseElement);
                XmlElement r2Element = _Globals.Config.CreateElement("R2");
                r2Element.InnerText = outputs["R2"];
                sscElement.AppendChild(r2Element);
                XmlElement Data = _Globals.Config.CreateElement("Data");
                double[] data1 = ParseArray(outputs[label1]);
                double[] data2 = ParseArray(outputs[label2]);
                for (int i = 0; i < data1.Length; i++)
                {
                    XmlElement point = _Globals.Config.CreateElement("Point");
                    XmlElement dataValue1 = _Globals.Config.CreateElement(label1);
                    dataValue1.InnerText = data1[i].ToString();
                    point.AppendChild(dataValue1);
                    XmlElement dataValue2 = _Globals.Config.CreateElement(label2);
                    dataValue2.InnerText = data2[i].ToString();
                    point.AppendChild(dataValue2);
                    Data.AppendChild(point);
                }
                sscElement.AppendChild(Data);
                XmlElement root = _Globals.Config.CreateElement("Pairs");
                var matches = Regex.Matches(outputs["Pairs"], @"\{([^}]+)\}");
                foreach (Match match in matches)
                {
                    XmlElement pair = _Globals.Config.CreateElement("Pair");
                    var kvs = Regex.Matches(match.Value, @"'([^']+)'\s*:\s*'([^']+)'");
                    foreach (Match kv in kvs)
                    {
                        string key = kv.Groups[1].Value;
                        string value = kv.Groups[2].Value;
                        XmlElement kvElement = _Globals.Config.CreateElement(key);
                        kvElement.InnerText = value;
                        pair.AppendChild(kvElement);
                    }
                    root.AppendChild(pair);
                }
                sscElement.AppendChild(root);
            }
            _project.SaveConfig(saveMode: 1);
        }  
    }
}
