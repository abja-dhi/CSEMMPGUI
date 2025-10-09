namespace CSEMMPGUI_v1
{
    partial class Survey
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
            components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Survey));
            menuStrip1 = new MenuStrip();
            menuFile = new ToolStripMenuItem();
            menuNew = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
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
            menuViSeaExtern2CSVSingle = new ToolStripMenuItem();
            menuViSeaExtern2CSVBatch = new ToolStripMenuItem();
            txtSurveyName = new TextBox();
            lblSurveyName = new Label();
            panel1 = new Panel();
            treeSurvey = new TreeView();
            tableLayoutPanel1 = new TableLayoutPanel();
            boxWater = new GroupBox();
            tableWater = new TableLayoutPanel();
            lblDensity = new Label();
            lblSalinity = new Label();
            lblTemperature = new Label();
            lblPH = new Label();
            txtDensity = new TextBox();
            txtSalinity = new TextBox();
            txtTemperature = new TextBox();
            txtPH = new TextBox();
            boxSediment = new GroupBox();
            tableSediment = new TableLayoutPanel();
            lblSedimentDiameter = new Label();
            lblSedimentDensity = new Label();
            txtSedimentDiameter = new TextBox();
            txtSedimentDensity = new TextBox();
            cmenuNode = new ContextMenuStrip(components);
            itemOpen = new ToolStripMenuItem();
            itemPlot = new ToolStripMenuItem();
            itemDelete = new ToolStripMenuItem();
            menuStrip1.SuspendLayout();
            panel1.SuspendLayout();
            tableLayoutPanel1.SuspendLayout();
            boxWater.SuspendLayout();
            tableWater.SuspendLayout();
            boxSediment.SuspendLayout();
            tableSediment.SuspendLayout();
            cmenuNode.SuspendLayout();
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
            menuFile.DropDownItems.AddRange(new ToolStripItem[] { menuNew, menuSave, menuExit });
            menuFile.Name = "menuFile";
            menuFile.Size = new Size(37, 20);
            menuFile.Text = "File";
            // 
            // menuNew
            // 
            menuNew.Name = "menuNew";
            menuNew.Size = new Size(107, 22);
            menuNew.Text = "New...";
            menuNew.Click += menuNew_Click;
            // 
            // menuSave
            // 
            menuSave.Name = "menuSave";
            menuSave.Size = new Size(107, 22);
            menuSave.Text = "Save...";
            menuSave.Click += menuSave_Click;
            // 
            // menuExit
            // 
            menuExit.Name = "menuExit";
            menuExit.Size = new Size(107, 22);
            menuExit.Text = "Exit";
            menuExit.Click += menuExit_Click;
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
            menuViSeaExtern2CSV.DropDownItems.AddRange(new ToolStripItem[] { menuViSeaExtern2CSVSingle, menuViSeaExtern2CSVBatch });
            menuViSeaExtern2CSV.Name = "menuViSeaExtern2CSV";
            menuViSeaExtern2CSV.Size = new Size(196, 22);
            menuViSeaExtern2CSV.Text = "ViSea Extern.dat to CSV";
            // 
            // menuViSeaExtern2CSVSingle
            // 
            menuViSeaExtern2CSVSingle.Name = "menuViSeaExtern2CSVSingle";
            menuViSeaExtern2CSVSingle.Size = new Size(167, 22);
            menuViSeaExtern2CSVSingle.Text = "Single File";
            // 
            // menuViSeaExtern2CSVBatch
            // 
            menuViSeaExtern2CSVBatch.Name = "menuViSeaExtern2CSVBatch";
            menuViSeaExtern2CSVBatch.Size = new Size(167, 22);
            menuViSeaExtern2CSVBatch.Text = "Batch Conversion";
            // 
            // txtSurveyName
            // 
            txtSurveyName.Dock = DockStyle.Top;
            txtSurveyName.Location = new Point(139, 3);
            txtSurveyName.Name = "txtSurveyName";
            txtSurveyName.Size = new Size(542, 23);
            txtSurveyName.TabIndex = 1;
            txtSurveyName.TextChanged += input_Changed;
            // 
            // lblSurveyName
            // 
            lblSurveyName.AutoSize = true;
            lblSurveyName.Dock = DockStyle.Fill;
            lblSurveyName.Location = new Point(3, 0);
            lblSurveyName.Name = "lblSurveyName";
            lblSurveyName.Size = new Size(130, 28);
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
            treeSurvey.NodeMouseClick += treeSurvey_NodeMouseClick;
            treeSurvey.NodeMouseDoubleClick += treeSurvey_NodeMouseDoubleClick;
            // 
            // tableLayoutPanel1
            // 
            tableLayoutPanel1.ColumnCount = 2;
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 80F));
            tableLayoutPanel1.Controls.Add(txtSurveyName, 1, 0);
            tableLayoutPanel1.Controls.Add(lblSurveyName, 0, 0);
            tableLayoutPanel1.Controls.Add(boxWater, 0, 1);
            tableLayoutPanel1.Controls.Add(boxSediment, 0, 2);
            tableLayoutPanel1.Dock = DockStyle.Fill;
            tableLayoutPanel1.Location = new Point(200, 24);
            tableLayoutPanel1.Name = "tableLayoutPanel1";
            tableLayoutPanel1.RowCount = 4;
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Absolute, 28F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Absolute, 140F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Absolute, 84F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableLayoutPanel1.Size = new Size(684, 437);
            tableLayoutPanel1.TabIndex = 5;
            // 
            // boxWater
            // 
            tableLayoutPanel1.SetColumnSpan(boxWater, 2);
            boxWater.Controls.Add(tableWater);
            boxWater.Dock = DockStyle.Fill;
            boxWater.Location = new Point(3, 31);
            boxWater.Name = "boxWater";
            boxWater.Size = new Size(678, 134);
            boxWater.TabIndex = 3;
            boxWater.TabStop = false;
            boxWater.Text = "Water Properties";
            boxWater.Visible = false;
            // 
            // tableWater
            // 
            tableWater.ColumnCount = 2;
            tableWater.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            tableWater.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 80F));
            tableWater.Controls.Add(lblDensity, 0, 0);
            tableWater.Controls.Add(lblSalinity, 0, 1);
            tableWater.Controls.Add(lblTemperature, 0, 2);
            tableWater.Controls.Add(lblPH, 0, 3);
            tableWater.Controls.Add(txtDensity, 1, 0);
            tableWater.Controls.Add(txtSalinity, 1, 1);
            tableWater.Controls.Add(txtTemperature, 1, 2);
            tableWater.Controls.Add(txtPH, 1, 3);
            tableWater.Dock = DockStyle.Fill;
            tableWater.Location = new Point(3, 19);
            tableWater.Name = "tableWater";
            tableWater.RowCount = 4;
            tableWater.RowStyles.Add(new RowStyle(SizeType.Absolute, 28F));
            tableWater.RowStyles.Add(new RowStyle(SizeType.Absolute, 28F));
            tableWater.RowStyles.Add(new RowStyle(SizeType.Absolute, 28F));
            tableWater.RowStyles.Add(new RowStyle(SizeType.Absolute, 28F));
            tableWater.Size = new Size(672, 112);
            tableWater.TabIndex = 0;
            // 
            // lblDensity
            // 
            lblDensity.AutoSize = true;
            lblDensity.Dock = DockStyle.Fill;
            lblDensity.Location = new Point(3, 0);
            lblDensity.Name = "lblDensity";
            lblDensity.Size = new Size(128, 28);
            lblDensity.TabIndex = 0;
            lblDensity.Text = "Density";
            lblDensity.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblSalinity
            // 
            lblSalinity.AutoSize = true;
            lblSalinity.Dock = DockStyle.Fill;
            lblSalinity.Location = new Point(3, 28);
            lblSalinity.Name = "lblSalinity";
            lblSalinity.Size = new Size(128, 28);
            lblSalinity.TabIndex = 1;
            lblSalinity.Text = "Salinity";
            lblSalinity.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblTemperature
            // 
            lblTemperature.AutoSize = true;
            lblTemperature.Dock = DockStyle.Fill;
            lblTemperature.Location = new Point(3, 56);
            lblTemperature.Name = "lblTemperature";
            lblTemperature.Size = new Size(128, 28);
            lblTemperature.TabIndex = 2;
            lblTemperature.Text = "Temperature";
            lblTemperature.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblPH
            // 
            lblPH.AutoSize = true;
            lblPH.Dock = DockStyle.Fill;
            lblPH.Location = new Point(3, 84);
            lblPH.Name = "lblPH";
            lblPH.Size = new Size(128, 28);
            lblPH.TabIndex = 3;
            lblPH.Text = "pH";
            lblPH.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtDensity
            // 
            txtDensity.Dock = DockStyle.Fill;
            txtDensity.Location = new Point(137, 3);
            txtDensity.Name = "txtDensity";
            txtDensity.Size = new Size(532, 23);
            txtDensity.TabIndex = 4;
            txtDensity.Text = "1023";
            txtDensity.TextChanged += input_Changed;
            // 
            // txtSalinity
            // 
            txtSalinity.Dock = DockStyle.Fill;
            txtSalinity.Location = new Point(137, 31);
            txtSalinity.Name = "txtSalinity";
            txtSalinity.Size = new Size(532, 23);
            txtSalinity.TabIndex = 5;
            txtSalinity.Text = "32";
            txtSalinity.TextChanged += input_Changed;
            // 
            // txtTemperature
            // 
            txtTemperature.Dock = DockStyle.Fill;
            txtTemperature.Location = new Point(137, 59);
            txtTemperature.Name = "txtTemperature";
            txtTemperature.Size = new Size(532, 23);
            txtTemperature.TabIndex = 6;
            txtTemperature.TextChanged += input_Changed;
            // 
            // txtPH
            // 
            txtPH.Dock = DockStyle.Fill;
            txtPH.Location = new Point(137, 87);
            txtPH.Name = "txtPH";
            txtPH.Size = new Size(532, 23);
            txtPH.TabIndex = 7;
            txtPH.Text = "8.1";
            txtPH.TextChanged += input_Changed;
            // 
            // boxSediment
            // 
            tableLayoutPanel1.SetColumnSpan(boxSediment, 2);
            boxSediment.Controls.Add(tableSediment);
            boxSediment.Dock = DockStyle.Fill;
            boxSediment.Location = new Point(3, 171);
            boxSediment.Name = "boxSediment";
            boxSediment.Size = new Size(678, 78);
            boxSediment.TabIndex = 4;
            boxSediment.TabStop = false;
            boxSediment.Text = "Sediment Properties";
            boxSediment.Visible = false;
            // 
            // tableSediment
            // 
            tableSediment.ColumnCount = 2;
            tableSediment.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            tableSediment.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 80F));
            tableSediment.Controls.Add(lblSedimentDiameter, 0, 0);
            tableSediment.Controls.Add(lblSedimentDensity, 0, 1);
            tableSediment.Controls.Add(txtSedimentDiameter, 1, 0);
            tableSediment.Controls.Add(txtSedimentDensity, 1, 1);
            tableSediment.Dock = DockStyle.Fill;
            tableSediment.Location = new Point(3, 19);
            tableSediment.Name = "tableSediment";
            tableSediment.RowCount = 2;
            tableSediment.RowStyles.Add(new RowStyle(SizeType.Absolute, 28F));
            tableSediment.RowStyles.Add(new RowStyle(SizeType.Absolute, 28F));
            tableSediment.Size = new Size(672, 56);
            tableSediment.TabIndex = 0;
            // 
            // lblSedimentDiameter
            // 
            lblSedimentDiameter.AutoSize = true;
            lblSedimentDiameter.Dock = DockStyle.Fill;
            lblSedimentDiameter.Location = new Point(3, 0);
            lblSedimentDiameter.Name = "lblSedimentDiameter";
            lblSedimentDiameter.Size = new Size(128, 28);
            lblSedimentDiameter.TabIndex = 0;
            lblSedimentDiameter.Text = "Particle Diameter";
            lblSedimentDiameter.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblSedimentDensity
            // 
            lblSedimentDensity.AutoSize = true;
            lblSedimentDensity.Dock = DockStyle.Fill;
            lblSedimentDensity.Location = new Point(3, 28);
            lblSedimentDensity.Name = "lblSedimentDensity";
            lblSedimentDensity.Size = new Size(128, 28);
            lblSedimentDensity.TabIndex = 1;
            lblSedimentDensity.Text = "Particle Density";
            lblSedimentDensity.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtSedimentDiameter
            // 
            txtSedimentDiameter.Dock = DockStyle.Fill;
            txtSedimentDiameter.Location = new Point(137, 3);
            txtSedimentDiameter.Name = "txtSedimentDiameter";
            txtSedimentDiameter.Size = new Size(532, 23);
            txtSedimentDiameter.TabIndex = 2;
            txtSedimentDiameter.Text = "2.5e-4";
            txtSedimentDiameter.TextChanged += input_Changed;
            // 
            // txtSedimentDensity
            // 
            txtSedimentDensity.Dock = DockStyle.Fill;
            txtSedimentDensity.Location = new Point(137, 31);
            txtSedimentDensity.Name = "txtSedimentDensity";
            txtSedimentDensity.Size = new Size(532, 23);
            txtSedimentDensity.TabIndex = 3;
            txtSedimentDensity.Text = "2650";
            txtSedimentDensity.TextChanged += input_Changed;
            // 
            // cmenuNode
            // 
            cmenuNode.Items.AddRange(new ToolStripItem[] { itemOpen, itemPlot, itemDelete });
            cmenuNode.Name = "cmenuNode";
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
            // Survey
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(884, 461);
            Controls.Add(tableLayoutPanel1);
            Controls.Add(panel1);
            Controls.Add(menuStrip1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MainMenuStrip = menuStrip1;
            Name = "Survey";
            Text = "Survey";
            Activated += Survey_Activated;
            FormClosing += Survey_FormClosing;
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            panel1.ResumeLayout(false);
            tableLayoutPanel1.ResumeLayout(false);
            tableLayoutPanel1.PerformLayout();
            boxWater.ResumeLayout(false);
            tableWater.ResumeLayout(false);
            tableWater.PerformLayout();
            boxSediment.ResumeLayout(false);
            tableSediment.ResumeLayout(false);
            tableSediment.PerformLayout();
            cmenuNode.ResumeLayout(false);
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
        private ToolStripMenuItem menuViSeaExtern2CSVSingle;
        private ToolStripMenuItem menuViSeaExtern2CSVBatch;
        private ToolStripMenuItem menuExit;
        private ContextMenuStrip cmenuNode;
        private ToolStripMenuItem itemOpen;
        private ToolStripMenuItem itemPlot;
        private ToolStripMenuItem itemDelete;
        private GroupBox boxWater;
        private TableLayoutPanel tableWater;
        private GroupBox boxSediment;
        private TableLayoutPanel tableSediment;
        private Label lblDensity;
        private Label lblSalinity;
        private Label lblTemperature;
        private Label lblPH;
        private TextBox txtDensity;
        private TextBox txtSalinity;
        private TextBox txtTemperature;
        private TextBox txtPH;
        private Label lblSedimentDiameter;
        private Label lblSedimentDensity;
        private TextBox txtSedimentDiameter;
        private TextBox txtSedimentDensity;
    }
}