namespace CSEMMPGUI_v1
{
    partial class __PlumeTrack
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(__PlumeTrack));
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
            menuAddSSCModel = new ToolStripMenuItem();
            menuUtilities = new ToolStripMenuItem();
            processPositionFileToolStripMenuItem = new ToolStripMenuItem();
            sSCModelsToolStripMenuItem = new ToolStripMenuItem();
            nTUSSCToolStripMenuItem = new ToolStripMenuItem();
            backscatterSSCToolStripMenuItem = new ToolStripMenuItem();
            menuHelp = new ToolStripMenuItem();
            menuExamples = new ToolStripMenuItem();
            menuDocumentation = new ToolStripMenuItem();
            menuAboutUs = new ToolStripMenuItem();
            cmenuNode = new ContextMenuStrip(components);
            itemOpen = new ToolStripMenuItem();
            itemPlot = new ToolStripMenuItem();
            itemDelete = new ToolStripMenuItem();
            colorDialog1 = new ColorDialog();
            splitter = new SplitContainer();
            treeProject = new TreeView();
            menuSaveAs = new ToolStripMenuItem();
            menuStrip1.SuspendLayout();
            cmenuNode.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)splitter).BeginInit();
            splitter.Panel1.SuspendLayout();
            splitter.SuspendLayout();
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
            menuProject.DropDownItems.AddRange(new ToolStripItem[] { menuNew, menuOpen, menuSave, menuSaveAs, menuProperties, menuExit });
            menuProject.Name = "menuProject";
            menuProject.Size = new Size(56, 20);
            menuProject.Text = "Project";
            // 
            // menuNew
            // 
            menuNew.Name = "menuNew";
            menuNew.Size = new Size(180, 22);
            menuNew.Text = "New...";
            menuNew.Click += menuNew_Click;
            // 
            // menuOpen
            // 
            menuOpen.Name = "menuOpen";
            menuOpen.Size = new Size(180, 22);
            menuOpen.Text = "Open...";
            menuOpen.Click += menuOpen_Click;
            // 
            // menuSave
            // 
            menuSave.Name = "menuSave";
            menuSave.Size = new Size(180, 22);
            menuSave.Text = "Save...";
            menuSave.Click += menuSave_Click;
            // 
            // menuProperties
            // 
            menuProperties.Name = "menuProperties";
            menuProperties.Size = new Size(180, 22);
            menuProperties.Text = "Properties";
            menuProperties.Click += menuProperties_Click;
            // 
            // menuExit
            // 
            menuExit.Name = "menuExit";
            menuExit.Size = new Size(180, 22);
            menuExit.Text = "Exit";
            menuExit.Click += menuExit_Click;
            // 
            // menuAddLayer
            // 
            menuAddLayer.DropDownItems.AddRange(new ToolStripItem[] { menuAddSurvey, menuAddModel, menuAddSSCModel });
            menuAddLayer.Name = "menuAddLayer";
            menuAddLayer.Size = new Size(72, 20);
            menuAddLayer.Text = "Add Layer";
            // 
            // menuAddSurvey
            // 
            menuAddSurvey.Name = "menuAddSurvey";
            menuAddSurvey.Size = new Size(163, 22);
            menuAddSurvey.Text = "Add Survey";
            menuAddSurvey.Click += menuAddSurvey_Click;
            // 
            // menuAddModel
            // 
            menuAddModel.Name = "menuAddModel";
            menuAddModel.Size = new Size(163, 22);
            menuAddModel.Text = "Add MIKE Model";
            menuAddModel.Click += menuAddModel_Click;
            // 
            // menuAddSSCModel
            // 
            menuAddSSCModel.Name = "menuAddSSCModel";
            menuAddSSCModel.Size = new Size(163, 22);
            menuAddSSCModel.Text = "Add SSC Model";
            menuAddSSCModel.Click += menuAddSSCModel_Click;
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
            menuExamples.Size = new Size(157, 22);
            menuExamples.Text = "Examples";
            // 
            // menuDocumentation
            // 
            menuDocumentation.Name = "menuDocumentation";
            menuDocumentation.Size = new Size(157, 22);
            menuDocumentation.Text = "Documentation";
            // 
            // menuAboutUs
            // 
            menuAboutUs.Name = "menuAboutUs";
            menuAboutUs.Size = new Size(157, 22);
            menuAboutUs.Text = "About us";
            menuAboutUs.Click += menuAboutUs_Click;
            // 
            // cmenuNode
            // 
            cmenuNode.Items.AddRange(new ToolStripItem[] { itemOpen, itemPlot, itemDelete });
            cmenuNode.Name = "contextMenuStrip1";
            cmenuNode.Size = new Size(108, 70);
            // 
            // itemOpen
            // 
            itemOpen.Name = "itemOpen";
            itemOpen.Size = new Size(107, 22);
            itemOpen.Text = "Open";
            itemOpen.Click += itemOpen_Click;
            // 
            // itemPlot
            // 
            itemPlot.Name = "itemPlot";
            itemPlot.Size = new Size(107, 22);
            itemPlot.Text = "Plot";
            itemPlot.Click += itemPlot_Click;
            // 
            // itemDelete
            // 
            itemDelete.Name = "itemDelete";
            itemDelete.Size = new Size(107, 22);
            itemDelete.Text = "Delete";
            itemDelete.Click += itemDelete_Click;
            // 
            // splitter
            // 
            splitter.Dock = DockStyle.Fill;
            splitter.Location = new Point(0, 24);
            splitter.Name = "splitter";
            // 
            // splitter.Panel1
            // 
            splitter.Panel1.Controls.Add(treeProject);
            splitter.Size = new Size(884, 437);
            splitter.SplitterDistance = 294;
            splitter.TabIndex = 1;
            // 
            // treeProject
            // 
            treeProject.Dock = DockStyle.Fill;
            treeProject.Location = new Point(0, 0);
            treeProject.Name = "treeProject";
            treeProject.Size = new Size(294, 437);
            treeProject.TabIndex = 0;
            // 
            // menuSaveAs
            // 
            menuSaveAs.Name = "menuSaveAs";
            menuSaveAs.Size = new Size(180, 22);
            menuSaveAs.Text = "Save As...";
            menuSaveAs.Click += menuSaveAs_Click;
            // 
            // __PlumeTrack
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(884, 461);
            Controls.Add(splitter);
            Controls.Add(menuStrip1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MainMenuStrip = menuStrip1;
            Name = "__PlumeTrack";
            Text = "Plume Track";
            Activated += frmMain_Activated;
            FormClosing += frmMain_FormClosing;
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            cmenuNode.ResumeLayout(false);
            splitter.Panel1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)splitter).EndInit();
            splitter.ResumeLayout(false);
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
        private ContextMenuStrip cmenuNode;
        private ToolStripMenuItem itemOpen;
        private ToolStripMenuItem itemDelete;
        private ToolStripMenuItem processPositionFileToolStripMenuItem;
        private ColorDialog colorDialog1;
        private ToolStripMenuItem menuAboutUs;
        private ToolStripMenuItem sSCModelsToolStripMenuItem;
        private ToolStripMenuItem nTUSSCToolStripMenuItem;
        private ToolStripMenuItem backscatterSSCToolStripMenuItem;
        private ToolStripMenuItem itemPlot;
        private ToolStripMenuItem menuAddSSCModel;
        private SplitContainer splitter;
        private TreeView treeProject;
        private ToolStripMenuItem menuSaveAs;
    }
}
