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
    public partial class AddSSCModel : Form
    {
        public bool isSaved;
        public XmlElement ntu2sscElement;
        public XmlElement bks2sscElement;
        public int mode;
        public _ClassConfigurationManager _project = new();
        public bool _updatingChecks;
        
        private void FillTrees()
        {
            treeNTU2SSC.Nodes.Clear();
            foreach (XmlElement survey in _Globals.Config.SelectNodes("//Survey"))
            {
                string surveyName = survey.GetAttribute("name");
                TreeNode surveyNode = new TreeNode(surveyName);
                surveyNode.Tag = survey;
                foreach (XmlElement obsVerticalProfile in survey.SelectNodes("OBSVerticalProfile | WaterSample"))
                {
                    string obsName = obsVerticalProfile.GetAttribute("name");
                    string obsID = obsVerticalProfile.GetAttribute("id");
                    TreeNode node = new TreeNode(obsName);
                    node.Tag = obsVerticalProfile;
                    surveyNode.Nodes.Add(node);
                }
                if (surveyNode.Nodes.Count > 0)
                {
                    treeNTU2SSC.Nodes.Add(surveyNode);
                }
            }
            treeNTU2SSC.ExpandAll();
            treeBKS2SSC.Nodes.Clear();
            foreach (XmlElement survey in _Globals.Config.SelectNodes("//Survey"))
            {
                string surveyName = survey.GetAttribute("name");
                TreeNode surveyNode = new TreeNode(surveyName);
                surveyNode.Tag = survey;
                foreach (XmlElement vesselMountedADCP in survey.SelectNodes("VesselMountedADCP | WaterSample"))
                {
                    string adcpName = vesselMountedADCP.GetAttribute("name");
                    string adcpID = vesselMountedADCP.GetAttribute("id");
                    TreeNode node = new TreeNode(adcpName);
                    node.Tag = vesselMountedADCP;
                    surveyNode.Nodes.Add(node);
                }
                if (surveyNode.Nodes.Count > 0)
                {
                    treeBKS2SSC.Nodes.Add(surveyNode);
                }
            }
            treeBKS2SSC.ExpandAll();
        }

        private void InitializeSSC()
        {
            int id = _project.GetNextId();
            txtModelName.Text = "New SSC Model";
            isSaved = true;
            ntu2sscElement = _Globals.Config.CreateElement("NTU2SSC");
            ntu2sscElement.SetAttribute("name", "New SSC Model");
            ntu2sscElement.SetAttribute("type", "NTU2SSC");
            ntu2sscElement.SetAttribute("id", id.ToString());
            bks2sscElement = _Globals.Config.CreateElement("BKS2SSC");
            bks2sscElement.SetAttribute("name", "New SSC Model");
            bks2sscElement.SetAttribute("type", "BKS2SSC");
            bks2sscElement.SetAttribute("id", id.ToString());
            txtA.Text = String.Empty;
            txtB.Text = String.Empty;
            txtC.Text = String.Empty;
            FillTrees();
            comboModels.SelectedIndex = 0;
        }

        private void PopulateSSC(XmlElement? element)
        {

        }

        public AddSSCModel(XmlNode? sscNode)
        {
            InitializeComponent();
            if (sscNode == null)
            {
                InitializeSSC();
                mode = 0; // New model mode
                this.Text = "Add SSC Model";
            }
            else
            {
                XmlElement? element = sscNode as XmlElement;
                PopulateSSC(element);
                menuNew.Visible = false;
                mode = 1; // Edit model mode
                this.Text = "Edit SSC Model";
            }
            treeNTU2SSC.CheckBoxes = true;
            treeBKS2SSC.CheckBoxes = true;
            treeNTU2SSC.AfterCheck += Tree_AfterCheck;
            treeBKS2SSC.AfterCheck += Tree_AfterCheck;
        }

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
                    Save();
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel
                }
            }
            InitializeSSC();
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            Save();
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
                    Save();
                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel
                }
            }
            this.Close(); // Close the form
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
                    Save();
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

        private void Save()
        {
            if (String.IsNullOrEmpty(txtModelName.Text))
            {
                MessageBox.Show(text: "Model name cannot be empty.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return;
            }
            if (rbManual.Checked && (String.IsNullOrEmpty(txtA.Text) || String.IsNullOrEmpty(txtB.Text) || String.IsNullOrEmpty(txtC.Text)))
            {
                MessageBox.Show(text: "All coefficients A, B, and C must be provided.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return;
            }
            CreateModel();
            var doc = _Globals.Config.DocumentElement;
            if (doc != null)
            {
                if (rbNTU2SSC.Checked)
                {
                    doc.AppendChild(ntu2sscElement);
                }
                else if (rbBKS2SSC.Checked)
                {
                    doc.AppendChild(bks2sscElement);
                }
            }
            _project.SaveConfig(saveMode: 1);
            int nextId = _project.GetNextId();
            _Globals.Config.DocumentElement?.SetAttribute("nextId", (nextId+1).ToString());
            isSaved = true;
        }

        public void CreateModel()
        {
            if (rbNTU2SSC.Checked)
            {
                ntu2sscElement.SetAttribute("name", txtModelName.Text);
                ntu2sscElement.SetAttribute("type", "NTU2SSC");
                if (rbManual.Checked)
                {
                    ntu2sscElement.SetAttribute("calcmode", "Manual");
                    XmlElement coeffsElement = _Globals.Config.CreateElement("Coefficients");
                    XmlElement aElement = _Globals.Config.OwnerDocument.CreateElement("A");
                    aElement.InnerText = txtA.Text.Trim();
                    XmlElement bElement = _Globals.Config.OwnerDocument.CreateElement("B");
                    bElement.InnerText = txtB.Text.Trim();
                    XmlElement cElement = _Globals.Config.OwnerDocument.CreateElement("C");
                    cElement.InnerText = txtC.Text.Trim();
                    coeffsElement.AppendChild(aElement);
                    coeffsElement.AppendChild(bElement);
                    coeffsElement.AppendChild(cElement);
                    ntu2sscElement.AppendChild(coeffsElement);
                }
                else if (rbAuto.Checked)
                {
                    ntu2sscElement.SetAttribute("calcmode", "Auto");
                    foreach (TreeNode surveyNode in treeNTU2SSC.Nodes)
                    {
                        if (surveyNode.Tag is XmlElement surveyElement)
                        {
                            string surveyId = surveyElement.GetAttribute("id");
                            XmlElement surveyIdElement = _Globals.Config.CreateElement("SurveyID");
                            surveyIdElement.InnerText = surveyId;
                            foreach (TreeNode childNode in surveyNode.Nodes)
                            {
                                if (childNode.Checked && childNode.Tag is XmlElement childElement)
                                {
                                    string childId = childElement.GetAttribute("id");
                                    XmlElement childIdElement = _Globals.Config.CreateElement("Instrument");
                                    childIdElement.InnerText = childId;
                                    surveyIdElement.AppendChild(childIdElement);
                                }
                            }
                            if (surveyIdElement.HasChildNodes)
                            {
                                ntu2sscElement.AppendChild(surveyIdElement);
                            }
                        }
                    }
                }
            }
            else if (rbBKS2SSC.Checked)
            {
                bks2sscElement.SetAttribute("name", txtModelName.Text);
                bks2sscElement.SetAttribute("type", "BKS2SSC");
                if (rbManual.Checked)
                {
                    bks2sscElement.SetAttribute("calcmode", "Manual");
                    XmlElement coeffsElement = _Globals.Config.CreateElement("Coefficients");
                    XmlElement aElement = _Globals.Config.CreateElement("A");
                    aElement.InnerText = txtA.Text.Trim();
                    XmlElement bElement = _Globals.Config.CreateElement("B");
                    bElement.InnerText = txtB.Text.Trim();
                    XmlElement cElement = _Globals.Config.CreateElement("C");
                    cElement.InnerText = txtC.Text.Trim();
                    coeffsElement.AppendChild(aElement);
                    coeffsElement.AppendChild(bElement);
                    coeffsElement.AppendChild(cElement);
                    bks2sscElement.AppendChild(coeffsElement);
                }
                else if (rbAuto.Checked)
                {
                    bks2sscElement.SetAttribute("calcmode", "Auto");
                    foreach (TreeNode surveyNode in treeNTU2SSC.Nodes)
                    {
                        if (surveyNode.Tag is XmlElement surveyElement)
                        {
                            string surveyId = surveyElement.GetAttribute("id");
                            XmlElement surveyIdElement = _Globals.Config.CreateElement("SurveyID");
                            surveyIdElement.InnerText = surveyId;
                            foreach (TreeNode childNode in surveyNode.Nodes)
                            {
                                if (childNode.Checked && childNode.Tag is XmlElement childElement)
                                {
                                    string childId = childElement.GetAttribute("id");
                                    XmlElement childIdElement = _Globals.Config.CreateElement("Instrument");
                                    childIdElement.InnerText = childId;
                                    surveyIdElement.AppendChild(childIdElement);
                                }
                            }
                            if (surveyIdElement.ChildNodes.Count > 0)
                            {
                                bks2sscElement.AppendChild(surveyIdElement);
                            }
                        }
                    }
                }
            }
        }
    }
}
