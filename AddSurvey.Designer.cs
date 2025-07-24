namespace CSEMMPGUI_v1
{
    partial class AddSurvey
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(AddSurvey));
            menuStrip1 = new MenuStrip();
            menuFile = new ToolStripMenuItem();
            menuNew = new ToolStripMenuItem();
            menuOpen = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuAddData = new ToolStripMenuItem();
            menuADCP = new ToolStripMenuItem();
            menuADCPVesselMounted = new ToolStripMenuItem();
            menuADCPSeabedLander = new ToolStripMenuItem();
            menuOBS = new ToolStripMenuItem();
            menuOBSVerticalProfile = new ToolStripMenuItem();
            menuOBSTransect = new ToolStripMenuItem();
            menuWaterSample = new ToolStripMenuItem();
            menuUtilities = new ToolStripMenuItem();
            menuViSeaExtern2CSV = new ToolStripMenuItem();
            txtSurveyName = new TextBox();
            lblSurveyName = new Label();
            panel1 = new Panel();
            treeSurvey = new TreeView();
            tableLayoutPanel1 = new TableLayoutPanel();
            menuStrip1.SuspendLayout();
            panel1.SuspendLayout();
            tableLayoutPanel1.SuspendLayout();
            SuspendLayout();
            // 
            // menuStrip1
            // 
            menuStrip1.Items.AddRange(new ToolStripItem[] { menuFile, menuAddData, menuUtilities });
            menuStrip1.Location = new Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new Size(884, 24);
            menuStrip1.TabIndex = 0;
            menuStrip1.Text = "menuStrip1";
            // 
            // menuFile
            // 
            menuFile.DropDownItems.AddRange(new ToolStripItem[] { menuNew, menuOpen, menuSave });
            menuFile.Name = "menuFile";
            menuFile.Size = new Size(37, 20);
            menuFile.Text = "File";
            // 
            // menuNew
            // 
            menuNew.Name = "menuNew";
            menuNew.Size = new Size(112, 22);
            menuNew.Text = "New...";
            menuNew.Click += menuNew_Click;
            // 
            // menuOpen
            // 
            menuOpen.Name = "menuOpen";
            menuOpen.Size = new Size(112, 22);
            menuOpen.Text = "Open...";
            menuOpen.Click += menuOpen_Click;
            // 
            // menuSave
            // 
            menuSave.Name = "menuSave";
            menuSave.Size = new Size(112, 22);
            menuSave.Text = "Save...";
            menuSave.Click += menuSave_Click;
            // 
            // menuAddData
            // 
            menuAddData.DropDownItems.AddRange(new ToolStripItem[] { menuADCP, menuOBS, menuWaterSample });
            menuAddData.Name = "menuAddData";
            menuAddData.Size = new Size(68, 20);
            menuAddData.Text = "Add Data";
            // 
            // menuADCP
            // 
            menuADCP.DropDownItems.AddRange(new ToolStripItem[] { menuADCPVesselMounted, menuADCPSeabedLander });
            menuADCP.Name = "menuADCP";
            menuADCP.Size = new Size(147, 22);
            menuADCP.Text = "ADCP";
            // 
            // menuADCPVesselMounted
            // 
            menuADCPVesselMounted.Name = "menuADCPVesselMounted";
            menuADCPVesselMounted.Size = new Size(157, 22);
            menuADCPVesselMounted.Text = "Vessel Mounted";
            menuADCPVesselMounted.Click += menuADCPVesselMounted_Click;
            // 
            // menuADCPSeabedLander
            // 
            menuADCPSeabedLander.Name = "menuADCPSeabedLander";
            menuADCPSeabedLander.Size = new Size(157, 22);
            menuADCPSeabedLander.Text = "Seabed Lander";
            menuADCPSeabedLander.Click += menuADCPSeabedLander_Click;
            // 
            // menuOBS
            // 
            menuOBS.DropDownItems.AddRange(new ToolStripItem[] { menuOBSVerticalProfile, menuOBSTransect });
            menuOBS.Name = "menuOBS";
            menuOBS.Size = new Size(147, 22);
            menuOBS.Text = "OBS";
            // 
            // menuOBSVerticalProfile
            // 
            menuOBSVerticalProfile.Name = "menuOBSVerticalProfile";
            menuOBSVerticalProfile.Size = new Size(149, 22);
            menuOBSVerticalProfile.Text = "Vertical Profile";
            menuOBSVerticalProfile.Click += menuOBSVerticalProfile_Click;
            // 
            // menuOBSTransect
            // 
            menuOBSTransect.Name = "menuOBSTransect";
            menuOBSTransect.Size = new Size(149, 22);
            menuOBSTransect.Text = "Transect";
            menuOBSTransect.Click += menuOBSTransect_Click;
            // 
            // menuWaterSample
            // 
            menuWaterSample.Name = "menuWaterSample";
            menuWaterSample.Size = new Size(147, 22);
            menuWaterSample.Text = "Water Sample";
            menuWaterSample.Click += menuWaterSample_Click;
            // 
            // menuUtilities
            // 
            menuUtilities.DropDownItems.AddRange(new ToolStripItem[] { menuViSeaExtern2CSV });
            menuUtilities.Name = "menuUtilities";
            menuUtilities.Size = new Size(58, 20);
            menuUtilities.Text = "Utilities";
            // 
            // menuViSeaExtern2CSV
            // 
            menuViSeaExtern2CSV.Name = "menuViSeaExtern2CSV";
            menuViSeaExtern2CSV.Size = new Size(196, 22);
            menuViSeaExtern2CSV.Text = "ViSea Extern.dat to CSV";
            menuViSeaExtern2CSV.Click += menuViSeaExtern2CSV_Click;
            // 
            // txtSurveyName
            // 
            txtSurveyName.Dock = DockStyle.Top;
            txtSurveyName.Location = new Point(139, 3);
            txtSurveyName.Name = "txtSurveyName";
            txtSurveyName.Size = new Size(542, 23);
            txtSurveyName.TabIndex = 1;
            txtSurveyName.Leave += txtSurveyName_Leave;
            // 
            // lblSurveyName
            // 
            lblSurveyName.AutoSize = true;
            lblSurveyName.Dock = DockStyle.Top;
            lblSurveyName.Location = new Point(3, 0);
            lblSurveyName.Name = "lblSurveyName";
            lblSurveyName.Size = new Size(130, 15);
            lblSurveyName.TabIndex = 2;
            lblSurveyName.Text = "Survey Name";
            lblSurveyName.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // panel1
            // 
            panel1.Controls.Add(treeSurvey);
            panel1.Dock = DockStyle.Left;
            panel1.Location = new Point(0, 24);
            panel1.Name = "panel1";
            panel1.Size = new Size(200, 437);
            panel1.TabIndex = 4;
            // 
            // treeSurvey
            // 
            treeSurvey.Dock = DockStyle.Fill;
            treeSurvey.Location = new Point(0, 0);
            treeSurvey.Name = "treeSurvey";
            treeSurvey.Size = new Size(200, 437);
            treeSurvey.TabIndex = 0;
            // 
            // tableLayoutPanel1
            // 
            tableLayoutPanel1.ColumnCount = 2;
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 80F));
            tableLayoutPanel1.Controls.Add(txtSurveyName, 1, 0);
            tableLayoutPanel1.Controls.Add(lblSurveyName, 0, 0);
            tableLayoutPanel1.Dock = DockStyle.Fill;
            tableLayoutPanel1.Location = new Point(200, 24);
            tableLayoutPanel1.Name = "tableLayoutPanel1";
            tableLayoutPanel1.RowCount = 1;
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableLayoutPanel1.Size = new Size(684, 437);
            tableLayoutPanel1.TabIndex = 5;
            // 
            // AddSurvey
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(884, 461);
            Controls.Add(tableLayoutPanel1);
            Controls.Add(panel1);
            Controls.Add(menuStrip1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MainMenuStrip = menuStrip1;
            Name = "AddSurvey";
            Text = "AddSurvey";
            Activated += AddSurvey_Activated;
            FormClosing += AddSurvey_FormClosing;
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            panel1.ResumeLayout(false);
            tableLayoutPanel1.ResumeLayout(false);
            tableLayoutPanel1.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menuStrip1;
        private ToolStripMenuItem menuFile;
        private ToolStripMenuItem menuAddData;
        private ToolStripMenuItem menuADCP;
        private ToolStripMenuItem menuADCPVesselMounted;
        private ToolStripMenuItem menuADCPSeabedLander;
        private ToolStripMenuItem menuOBS;
        private ToolStripMenuItem menuWaterSample;
        private TextBox txtSurveyName;
        private Label lblSurveyName;
        private ToolStripMenuItem menuSave;
        private Panel panel1;
        private TreeView treeSurvey;
        private ToolStripMenuItem menuUtilities;
        private ToolStripMenuItem menuViSeaExtern2CSV;
        private ToolStripMenuItem menuOBSVerticalProfile;
        private ToolStripMenuItem menuOBSTransect;
        private TableLayoutPanel tableLayoutPanel1;
        private ToolStripMenuItem menuNew;
        private ToolStripMenuItem menuOpen;
    }
}