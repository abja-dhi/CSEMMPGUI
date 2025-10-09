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
            menuSaveAs = new ToolStripMenuItem();
            menuProperties = new ToolStripMenuItem();
            menuMapOptions = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
            menuAddLayer = new ToolStripMenuItem();
            menuAddSurvey = new ToolStripMenuItem();
            menuAddModel = new ToolStripMenuItem();
            menuAddHDModel = new ToolStripMenuItem();
            menuAddMTModel = new ToolStripMenuItem();
            menuAddSSCModel = new ToolStripMenuItem();
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
            tableMap = new TableLayoutPanel();
            map2D = new RadioButton();
            map3D = new RadioButton();
            webView = new Microsoft.Web.WebView2.WinForms.WebView2();
            menuStrip1.SuspendLayout();
            cmenuNode.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)splitter).BeginInit();
            splitter.Panel1.SuspendLayout();
            splitter.Panel2.SuspendLayout();
            splitter.SuspendLayout();
            tableMap.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)webView).BeginInit();
            SuspendLayout();
            // 
            // menuStrip1
            // 
            menuStrip1.Items.AddRange(new ToolStripItem[] { menuProject, menuAddLayer, menuHelp });
            menuStrip1.Location = new Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new Size(884, 24);
            menuStrip1.TabIndex = 0;
            menuStrip1.Text = "Project";
            // 
            // menuProject
            // 
            menuProject.DropDownItems.AddRange(new ToolStripItem[] { menuNew, menuOpen, menuSave, menuSaveAs, menuProperties, menuMapOptions, menuExit });
            menuProject.Name = "menuProject";
            menuProject.Size = new Size(56, 20);
            menuProject.Text = "Project";
            // 
            // menuNew
            // 
            menuNew.Name = "menuNew";
            menuNew.Size = new Size(167, 22);
            menuNew.Text = "New...";
            menuNew.Click += menuNew_Click;
            // 
            // menuOpen
            // 
            menuOpen.Name = "menuOpen";
            menuOpen.Size = new Size(167, 22);
            menuOpen.Text = "Open...";
            menuOpen.Click += menuOpen_Click;
            // 
            // menuSave
            // 
            menuSave.Name = "menuSave";
            menuSave.Size = new Size(167, 22);
            menuSave.Text = "Save...";
            menuSave.Click += menuSave_Click;
            // 
            // menuSaveAs
            // 
            menuSaveAs.Name = "menuSaveAs";
            menuSaveAs.Size = new Size(167, 22);
            menuSaveAs.Text = "Save As...";
            menuSaveAs.Click += menuSaveAs_Click;
            // 
            // menuProperties
            // 
            menuProperties.Name = "menuProperties";
            menuProperties.Size = new Size(167, 22);
            menuProperties.Text = "Project Properties";
            menuProperties.Click += menuProperties_Click;
            // 
            // menuMapOptions
            // 
            menuMapOptions.Name = "menuMapOptions";
            menuMapOptions.Size = new Size(167, 22);
            menuMapOptions.Text = "Map Options";
            menuMapOptions.Click += menuMapOptions_Click;
            // 
            // menuExit
            // 
            menuExit.Name = "menuExit";
            menuExit.Size = new Size(167, 22);
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
            menuAddModel.DropDownItems.AddRange(new ToolStripItem[] { menuAddHDModel, menuAddMTModel });
            menuAddModel.Name = "menuAddModel";
            menuAddModel.Size = new Size(163, 22);
            menuAddModel.Text = "Add MIKE Model";
            // 
            // menuAddHDModel
            // 
            menuAddHDModel.Name = "menuAddHDModel";
            menuAddHDModel.Size = new Size(193, 22);
            menuAddHDModel.Text = "Add HD Model Results";
            menuAddHDModel.Click += menuAddHDModel_Click;
            // 
            // menuAddMTModel
            // 
            menuAddMTModel.Name = "menuAddMTModel";
            menuAddMTModel.Size = new Size(193, 22);
            menuAddMTModel.Text = "Add MT Model Results";
            menuAddMTModel.Click += menuAddMTModel_Click;
            // 
            // menuAddSSCModel
            // 
            menuAddSSCModel.Name = "menuAddSSCModel";
            menuAddSSCModel.Size = new Size(163, 22);
            menuAddSSCModel.Text = "Add SSC Model";
            menuAddSSCModel.Click += menuAddSSCModel_Click;
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
            // 
            // splitter.Panel2
            // 
            splitter.Panel2.Controls.Add(tableMap);
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
            treeProject.NodeMouseClick += treeProject_NodeMouseClick;
            treeProject.NodeMouseDoubleClick += treeProject_NodeMouseDoubleClick;
            // 
            // tableMap
            // 
            tableMap.ColumnCount = 3;
            tableMap.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 50F));
            tableMap.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 50F));
            tableMap.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableMap.Controls.Add(map2D, 0, 0);
            tableMap.Controls.Add(map3D, 1, 0);
            tableMap.Controls.Add(webView, 0, 1);
            tableMap.Dock = DockStyle.Fill;
            tableMap.Location = new Point(0, 0);
            tableMap.Name = "tableMap";
            tableMap.RowCount = 2;
            tableMap.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableMap.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableMap.Size = new Size(586, 437);
            tableMap.TabIndex = 0;
            // 
            // map2D
            // 
            map2D.AutoSize = true;
            map2D.Dock = DockStyle.Fill;
            map2D.Location = new Point(3, 3);
            map2D.Name = "map2D";
            map2D.Size = new Size(44, 24);
            map2D.TabIndex = 0;
            map2D.Text = "2D";
            map2D.TextAlign = ContentAlignment.MiddleCenter;
            map2D.UseVisualStyleBackColor = true;
            map2D.Click += map2D_Click;
            // 
            // map3D
            // 
            map3D.AutoSize = true;
            map3D.Dock = DockStyle.Fill;
            map3D.Location = new Point(53, 3);
            map3D.Name = "map3D";
            map3D.Size = new Size(44, 24);
            map3D.TabIndex = 1;
            map3D.Text = "3D";
            map3D.TextAlign = ContentAlignment.MiddleCenter;
            map3D.UseVisualStyleBackColor = true;
            map3D.Click += map3D_Click;
            // 
            // webView
            // 
            webView.AllowExternalDrop = true;
            tableMap.SetColumnSpan(webView, 3);
            webView.CreationProperties = null;
            webView.DefaultBackgroundColor = Color.White;
            webView.Dock = DockStyle.Fill;
            webView.Location = new Point(3, 33);
            webView.Name = "webView";
            webView.Size = new Size(580, 401);
            webView.TabIndex = 2;
            webView.ZoomFactor = 1D;
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
            splitter.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)splitter).EndInit();
            splitter.ResumeLayout(false);
            tableMap.ResumeLayout(false);
            tableMap.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)webView).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menuStrip1;
        private ToolStripMenuItem menuProject;
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
        private ColorDialog colorDialog1;
        private ToolStripMenuItem menuAboutUs;
        private ToolStripMenuItem itemPlot;
        private ToolStripMenuItem menuAddSSCModel;
        private SplitContainer splitter;
        private TreeView treeProject;
        private ToolStripMenuItem menuSaveAs;
        private ToolStripMenuItem menuMapOptions;
        private ToolStripMenuItem menuAddHDModel;
        private ToolStripMenuItem menuAddMTModel;
        private TableLayoutPanel tableMap;
        private RadioButton map2D;
        private RadioButton map3D;
        private Microsoft.Web.WebView2.WinForms.WebView2 webView;
    }
}
