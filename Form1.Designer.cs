namespace CSEMMPGUI_v1
{
    partial class frmMain
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(frmMain));
            menuStrip1 = new MenuStrip();
            menuProject = new ToolStripMenuItem();
            menuNew = new ToolStripMenuItem();
            menuOpen = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuProperties = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
            menuAddLayer = new ToolStripMenuItem();
            menuAddSurvey = new ToolStripMenuItem();
            menuAddModel = new ToolStripMenuItem();
            menuUtilities = new ToolStripMenuItem();
            processPositionFileToolStripMenuItem = new ToolStripMenuItem();
            sSCModelsToolStripMenuItem = new ToolStripMenuItem();
            nTUSSCToolStripMenuItem = new ToolStripMenuItem();
            backscatterSSCToolStripMenuItem = new ToolStripMenuItem();
            menuHelp = new ToolStripMenuItem();
            menuExamples = new ToolStripMenuItem();
            menuDocumentation = new ToolStripMenuItem();
            menuAboutUs = new ToolStripMenuItem();
            treeProject = new TreeView();
            cmenuNode = new ContextMenuStrip(components);
            itemOpen = new ToolStripMenuItem();
            itemDelete = new ToolStripMenuItem();
            colorDialog1 = new ColorDialog();
            tableLayoutPanel1 = new TableLayoutPanel();
            lblName = new Label();
            txtName = new TextBox();
            menuStrip1.SuspendLayout();
            cmenuNode.SuspendLayout();
            tableLayoutPanel1.SuspendLayout();
            SuspendLayout();
            // 
            // menuStrip1
            // 
            menuStrip1.Items.AddRange(new ToolStripItem[] { menuProject, menuAddLayer, menuUtilities, menuHelp });
            menuStrip1.Location = new Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new Size(884, 24);
            menuStrip1.TabIndex = 0;
            menuStrip1.Text = "Project";
            // 
            // menuProject
            // 
            menuProject.DropDownItems.AddRange(new ToolStripItem[] { menuNew, menuOpen, menuSave, menuProperties, menuExit });
            menuProject.Name = "menuProject";
            menuProject.Size = new Size(56, 20);
            menuProject.Text = "Project";
            // 
            // menuNew
            // 
            menuNew.Name = "menuNew";
            menuNew.Size = new Size(127, 22);
            menuNew.Text = "New...";
            menuNew.Click += menuNew_Click;
            // 
            // menuOpen
            // 
            menuOpen.Name = "menuOpen";
            menuOpen.Size = new Size(127, 22);
            menuOpen.Text = "Open...";
            menuOpen.Click += menuOpen_Click;
            // 
            // menuSave
            // 
            menuSave.Name = "menuSave";
            menuSave.Size = new Size(127, 22);
            menuSave.Text = "Save...";
            menuSave.Click += menuSave_Click;
            // 
            // menuProperties
            // 
            menuProperties.Name = "menuProperties";
            menuProperties.Size = new Size(127, 22);
            menuProperties.Text = "Properties";
            menuProperties.Click += menuProperties_Click;
            // 
            // menuExit
            // 
            menuExit.Name = "menuExit";
            menuExit.Size = new Size(127, 22);
            menuExit.Text = "Exit";
            menuExit.Click += menuExit_Click;
            // 
            // menuAddLayer
            // 
            menuAddLayer.DropDownItems.AddRange(new ToolStripItem[] { menuAddSurvey, menuAddModel });
            menuAddLayer.Name = "menuAddLayer";
            menuAddLayer.Size = new Size(72, 20);
            menuAddLayer.Text = "Add Layer";
            // 
            // menuAddSurvey
            // 
            menuAddSurvey.Name = "menuAddSurvey";
            menuAddSurvey.Size = new Size(134, 22);
            menuAddSurvey.Text = "Add Survey";
            menuAddSurvey.Click += menuAddSurvey_Click;
            // 
            // menuAddModel
            // 
            menuAddModel.Name = "menuAddModel";
            menuAddModel.Size = new Size(134, 22);
            menuAddModel.Text = "Add Model";
            menuAddModel.Click += menuAddModel_Click;
            // 
            // menuUtilities
            // 
            menuUtilities.DropDownItems.AddRange(new ToolStripItem[] { processPositionFileToolStripMenuItem, sSCModelsToolStripMenuItem });
            menuUtilities.Name = "menuUtilities";
            menuUtilities.Size = new Size(58, 20);
            menuUtilities.Text = "Utilities";
            // 
            // processPositionFileToolStripMenuItem
            // 
            processPositionFileToolStripMenuItem.Name = "processPositionFileToolStripMenuItem";
            processPositionFileToolStripMenuItem.Size = new Size(181, 22);
            processPositionFileToolStripMenuItem.Text = "Process Position File";
            processPositionFileToolStripMenuItem.Click += processPositionFileToolStripMenuItem_Click;
            // 
            // sSCModelsToolStripMenuItem
            // 
            sSCModelsToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { nTUSSCToolStripMenuItem, backscatterSSCToolStripMenuItem });
            sSCModelsToolStripMenuItem.Name = "sSCModelsToolStripMenuItem";
            sSCModelsToolStripMenuItem.Size = new Size(181, 22);
            sSCModelsToolStripMenuItem.Text = "SSC Models";
            // 
            // nTUSSCToolStripMenuItem
            // 
            nTUSSCToolStripMenuItem.Name = "nTUSSCToolStripMenuItem";
            nTUSSCToolStripMenuItem.Size = new Size(173, 22);
            nTUSSCToolStripMenuItem.Text = "NTU -> SSC";
            // 
            // backscatterSSCToolStripMenuItem
            // 
            backscatterSSCToolStripMenuItem.Name = "backscatterSSCToolStripMenuItem";
            backscatterSSCToolStripMenuItem.Size = new Size(173, 22);
            backscatterSSCToolStripMenuItem.Text = "Backscatter -> SSC";
            // 
            // menuHelp
            // 
            menuHelp.DropDownItems.AddRange(new ToolStripItem[] { menuExamples, menuDocumentation, menuAboutUs });
            menuHelp.Name = "menuHelp";
            menuHelp.Size = new Size(44, 20);
            menuHelp.Text = "Help";
            // 
            // menuExamples
            // 
            menuExamples.Name = "menuExamples";
            menuExamples.Size = new Size(180, 22);
            menuExamples.Text = "Examples";
            // 
            // menuDocumentation
            // 
            menuDocumentation.Name = "menuDocumentation";
            menuDocumentation.Size = new Size(180, 22);
            menuDocumentation.Text = "Documentation";
            // 
            // menuAboutUs
            // 
            menuAboutUs.Name = "menuAboutUs";
            menuAboutUs.Size = new Size(180, 22);
            menuAboutUs.Text = "About us";
            menuAboutUs.Click += menuAboutUs_Click;
            // 
            // treeProject
            // 
            treeProject.ContextMenuStrip = cmenuNode;
            treeProject.Dock = DockStyle.Left;
            treeProject.Location = new Point(0, 24);
            treeProject.Name = "treeProject";
            treeProject.Size = new Size(200, 437);
            treeProject.TabIndex = 1;
            // 
            // cmenuNode
            // 
            cmenuNode.Items.AddRange(new ToolStripItem[] { itemOpen, itemDelete });
            cmenuNode.Name = "contextMenuStrip1";
            cmenuNode.Size = new Size(108, 48);
            // 
            // itemOpen
            // 
            itemOpen.Name = "itemOpen";
            itemOpen.Size = new Size(107, 22);
            itemOpen.Text = "Open";
            // 
            // itemDelete
            // 
            itemDelete.Name = "itemDelete";
            itemDelete.Size = new Size(107, 22);
            itemDelete.Text = "Delete";
            // 
            // tableLayoutPanel1
            // 
            tableLayoutPanel1.ColumnCount = 2;
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 16.666666F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 83.3333359F));
            tableLayoutPanel1.Controls.Add(lblName, 0, 0);
            tableLayoutPanel1.Controls.Add(txtName, 1, 0);
            tableLayoutPanel1.Dock = DockStyle.Top;
            tableLayoutPanel1.Location = new Point(200, 24);
            tableLayoutPanel1.Name = "tableLayoutPanel1";
            tableLayoutPanel1.RowCount = 1;
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableLayoutPanel1.Size = new Size(684, 29);
            tableLayoutPanel1.TabIndex = 2;
            // 
            // lblName
            // 
            lblName.AutoSize = true;
            lblName.Dock = DockStyle.Fill;
            lblName.Location = new Point(3, 0);
            lblName.Name = "lblName";
            lblName.Size = new Size(108, 29);
            lblName.TabIndex = 0;
            lblName.Text = "Project Name";
            lblName.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtName
            // 
            txtName.Dock = DockStyle.Fill;
            txtName.Location = new Point(117, 3);
            txtName.Name = "txtName";
            txtName.Size = new Size(564, 23);
            txtName.TabIndex = 1;
            txtName.Text = "Project";
            txtName.Leave += txtName_Leave;
            // 
            // frmMain
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(884, 461);
            Controls.Add(tableLayoutPanel1);
            Controls.Add(treeProject);
            Controls.Add(menuStrip1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MainMenuStrip = menuStrip1;
            Name = "frmMain";
            Text = "MT Validation Tool";
            FormClosing += frmMain_FormClosing;
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            cmenuNode.ResumeLayout(false);
            tableLayoutPanel1.ResumeLayout(false);
            tableLayoutPanel1.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menuStrip1;
        private ToolStripMenuItem menuProject;
        private ToolStripMenuItem menuUtilities;
        private ToolStripMenuItem menuHelp;
        private ToolStripMenuItem menuNew;
        private ToolStripMenuItem menuOpen;
        private ToolStripMenuItem menuSave;
        private ToolStripMenuItem menuExit;
        private ToolStripMenuItem menuExamples;
        private ToolStripMenuItem menuDocumentation;
        private ToolStripMenuItem menuProperties;
        private ToolStripMenuItem menuAddLayer;
        private ToolStripMenuItem menuAddSurvey;
        private ToolStripMenuItem menuAddModel;
        private TreeView treeProject;
        private ContextMenuStrip cmenuNode;
        private ToolStripMenuItem itemOpen;
        private ToolStripMenuItem itemDelete;
        private ToolStripMenuItem processPositionFileToolStripMenuItem;
        private ColorDialog colorDialog1;
        private ToolStripMenuItem menuAboutUs;
        private ToolStripMenuItem sSCModelsToolStripMenuItem;
        private ToolStripMenuItem nTUSSCToolStripMenuItem;
        private ToolStripMenuItem backscatterSSCToolStripMenuItem;
        private TableLayoutPanel tableLayoutPanel1;
        private Label lblName;
        private TextBox txtName;
    }
}
