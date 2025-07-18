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
            menuStrip1 = new MenuStrip();
            menuProject = new ToolStripMenuItem();
            menuNew = new ToolStripMenuItem();
            menuLoad = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuSaveAs = new ToolStripMenuItem();
            menuProperties = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
            menuAddLayer = new ToolStripMenuItem();
            menuAddSurvey = new ToolStripMenuItem();
            menuAddModel = new ToolStripMenuItem();
            menuUtilities = new ToolStripMenuItem();
            processPositionFileToolStripMenuItem = new ToolStripMenuItem();
            menuHelp = new ToolStripMenuItem();
            menuExamples = new ToolStripMenuItem();
            menuDocumentation = new ToolStripMenuItem();
            treeProject = new TreeView();
            cmenuNode = new ContextMenuStrip(components);
            itemOpen = new ToolStripMenuItem();
            itemDelete = new ToolStripMenuItem();
            colorDialog1 = new ColorDialog();
            menuStrip1.SuspendLayout();
            cmenuNode.SuspendLayout();
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
            menuProject.DropDownItems.AddRange(new ToolStripItem[] { menuNew, menuLoad, menuSave, menuSaveAs, menuProperties, menuExit });
            menuProject.Name = "menuProject";
            menuProject.Size = new Size(56, 20);
            menuProject.Text = "Project";
            // 
            // menuNew
            // 
            menuNew.Name = "menuNew";
            menuNew.Size = new Size(127, 22);
            menuNew.Text = "New...";
            // 
            // menuLoad
            // 
            menuLoad.Name = "menuLoad";
            menuLoad.Size = new Size(127, 22);
            menuLoad.Text = "Open...";
            menuLoad.Click += menuLoad_Click;
            // 
            // menuSave
            // 
            menuSave.Name = "menuSave";
            menuSave.Size = new Size(127, 22);
            menuSave.Text = "Save...";
            // 
            // menuSaveAs
            // 
            menuSaveAs.Name = "menuSaveAs";
            menuSaveAs.Size = new Size(127, 22);
            menuSaveAs.Text = "Save As...";
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
            menuUtilities.DropDownItems.AddRange(new ToolStripItem[] { processPositionFileToolStripMenuItem });
            menuUtilities.Name = "menuUtilities";
            menuUtilities.Size = new Size(58, 20);
            menuUtilities.Text = "Utilities";
            // 
            // processPositionFileToolStripMenuItem
            // 
            processPositionFileToolStripMenuItem.Name = "processPositionFileToolStripMenuItem";
            processPositionFileToolStripMenuItem.Size = new Size(181, 22);
            processPositionFileToolStripMenuItem.Text = "Process Position File";
            // 
            // menuHelp
            // 
            menuHelp.DropDownItems.AddRange(new ToolStripItem[] { menuExamples, menuDocumentation });
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
            // treeProject
            // 
            treeProject.ContextMenuStrip = cmenuNode;
            treeProject.Dock = DockStyle.Left;
            treeProject.Location = new Point(0, 24);
            treeProject.Name = "treeProject";
            treeProject.Size = new Size(200, 437);
            treeProject.TabIndex = 1;
            treeProject.NodeMouseClick += treeProject_NodeMouseClick;
            treeProject.NodeMouseDoubleClick += treeProject_NodeMouseDoubleClick;
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
            itemOpen.Click += itemOpen_Click;
            // 
            // itemDelete
            // 
            itemDelete.Name = "itemDelete";
            itemDelete.Size = new Size(107, 22);
            itemDelete.Text = "Delete";
            itemDelete.Click += itemDelete_Click;
            // 
            // frmMain
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(884, 461);
            Controls.Add(treeProject);
            Controls.Add(menuStrip1);
            MainMenuStrip = menuStrip1;
            Name = "frmMain";
            Text = "MT Validation Tool";
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            cmenuNode.ResumeLayout(false);
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menuStrip1;
        private ToolStripMenuItem menuProject;
        private ToolStripMenuItem menuUtilities;
        private ToolStripMenuItem menuHelp;
        private ToolStripMenuItem menuNew;
        private ToolStripMenuItem menuLoad;
        private ToolStripMenuItem menuSave;
        private ToolStripMenuItem menuSaveAs;
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
    }
}
