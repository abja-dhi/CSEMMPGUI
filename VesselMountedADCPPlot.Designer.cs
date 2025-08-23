namespace CSEMMPGUI_v1
{
    partial class VesselMountedADCPPlot
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(VesselMountedADCPPlot));
            tableMain = new TableLayoutPanel();
            lblPlotType = new Label();
            comboPlotType = new ComboBox();
            btnPlot = new Button();
            boxProperties = new GroupBox();
            tableProp = new TableLayoutPanel();
            tableMain.SuspendLayout();
            boxProperties.SuspendLayout();
            SuspendLayout();
            // 
            // tableMain
            // 
            tableMain.ColumnCount = 2;
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70F));
            tableMain.Controls.Add(lblPlotType, 0, 0);
            tableMain.Controls.Add(comboPlotType, 1, 0);
            tableMain.Controls.Add(btnPlot, 0, 1);
            tableMain.Controls.Add(boxProperties, 0, 2);
            tableMain.Dock = DockStyle.Fill;
            tableMain.Location = new Point(0, 0);
            tableMain.Name = "tableMain";
            tableMain.RowCount = 3;
            tableMain.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableMain.Size = new Size(800, 450);
            tableMain.TabIndex = 0;
            // 
            // lblPlotType
            // 
            lblPlotType.AutoSize = true;
            lblPlotType.Dock = DockStyle.Fill;
            lblPlotType.Location = new Point(3, 0);
            lblPlotType.Name = "lblPlotType";
            lblPlotType.Size = new Size(234, 30);
            lblPlotType.TabIndex = 0;
            lblPlotType.Text = "Plot Type";
            lblPlotType.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboPlotType
            // 
            comboPlotType.Dock = DockStyle.Fill;
            comboPlotType.DropDownStyle = ComboBoxStyle.DropDownList;
            comboPlotType.FormattingEnabled = true;
            comboPlotType.Items.AddRange(new object[] { "Platform Orientation", "Four Beam Flood Plot", "Single Beam Flood Plot", "Plot Transect Velocities", "Beam Geometry Animation", "Transect Animation" });
            comboPlotType.Location = new Point(243, 3);
            comboPlotType.Name = "comboPlotType";
            comboPlotType.Size = new Size(554, 23);
            comboPlotType.TabIndex = 1;
            comboPlotType.SelectedIndexChanged += comboPlotType_SelectedIndexChanged;
            // 
            // btnPlot
            // 
            btnPlot.Dock = DockStyle.Fill;
            btnPlot.Location = new Point(3, 33);
            btnPlot.Name = "btnPlot";
            btnPlot.Size = new Size(234, 24);
            btnPlot.TabIndex = 2;
            btnPlot.Text = "Plot";
            btnPlot.UseVisualStyleBackColor = true;
            btnPlot.Click += btnPlot_Click;
            // 
            // boxProperties
            // 
            tableMain.SetColumnSpan(boxProperties, 2);
            boxProperties.Controls.Add(tableProp);
            boxProperties.Dock = DockStyle.Fill;
            boxProperties.Location = new Point(3, 63);
            boxProperties.Name = "boxProperties";
            boxProperties.Size = new Size(794, 384);
            boxProperties.TabIndex = 3;
            boxProperties.TabStop = false;
            boxProperties.Text = "Properties";
            // 
            // tableProp
            // 
            tableProp.ColumnCount = 3;
            tableProp.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            tableProp.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40F));
            tableProp.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            tableProp.Dock = DockStyle.Fill;
            tableProp.Location = new Point(3, 19);
            tableProp.Name = "tableProp";
            tableProp.RowCount = 2;
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableProp.Size = new Size(788, 362);
            tableProp.TabIndex = 0;
            // 
            // VesselMountedADCPPlot
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(tableMain);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "VesselMountedADCPPlot";
            Text = "Plot Vessel Mounted ADCP";
            tableMain.ResumeLayout(false);
            tableMain.PerformLayout();
            boxProperties.ResumeLayout(false);
            ResumeLayout(false);
        }

        #endregion

        private TableLayoutPanel tableMain;
        private Label lblPlotType;
        private ComboBox comboPlotType;
        private Button btnPlot;
        private GroupBox boxProperties;
        private TableLayoutPanel tableProp;
    }
}