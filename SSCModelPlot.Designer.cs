namespace CSEMMPGUI_v1
{
    partial class SSCModelPlot
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(SSCModelPlot));
            tableMain = new TableLayoutPanel();
            boxProperties = new GroupBox();
            tableProp = new TableLayoutPanel();
            tablePlotButton = new TableLayoutPanel();
            btnPlot = new Button();
            tableInitialSetup = new TableLayoutPanel();
            comboPlotType = new ComboBox();
            lblPlotType = new Label();
            tableMain.SuspendLayout();
            boxProperties.SuspendLayout();
            tablePlotButton.SuspendLayout();
            tableInitialSetup.SuspendLayout();
            SuspendLayout();
            // 
            // tableMain
            // 
            tableMain.ColumnCount = 2;
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70F));
            tableMain.Controls.Add(boxProperties, 0, 2);
            tableMain.Controls.Add(tablePlotButton, 0, 1);
            tableMain.Controls.Add(tableInitialSetup, 0, 0);
            tableMain.Dock = DockStyle.Fill;
            tableMain.Location = new Point(0, 0);
            tableMain.Name = "tableMain";
            tableMain.RowCount = 3;
            tableMain.RowStyles.Add(new RowStyle(SizeType.Absolute, 40F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Absolute, 40F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableMain.Size = new Size(800, 450);
            tableMain.TabIndex = 0;
            // 
            // boxProperties
            // 
            tableMain.SetColumnSpan(boxProperties, 2);
            boxProperties.Controls.Add(tableProp);
            boxProperties.Dock = DockStyle.Fill;
            boxProperties.Location = new Point(3, 83);
            boxProperties.Name = "boxProperties";
            boxProperties.Size = new Size(794, 364);
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
            tableProp.Size = new Size(788, 342);
            tableProp.TabIndex = 0;
            // 
            // tablePlotButton
            // 
            tablePlotButton.ColumnCount = 2;
            tablePlotButton.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tablePlotButton.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tablePlotButton.Controls.Add(btnPlot, 0, 0);
            tablePlotButton.Dock = DockStyle.Fill;
            tablePlotButton.Location = new Point(3, 43);
            tablePlotButton.Name = "tablePlotButton";
            tablePlotButton.RowCount = 1;
            tablePlotButton.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tablePlotButton.Size = new Size(234, 34);
            tablePlotButton.TabIndex = 4;
            // 
            // btnPlot
            // 
            btnPlot.Dock = DockStyle.Fill;
            btnPlot.Location = new Point(3, 3);
            btnPlot.Name = "btnPlot";
            btnPlot.Size = new Size(111, 28);
            btnPlot.TabIndex = 2;
            btnPlot.Text = "Plot";
            btnPlot.UseVisualStyleBackColor = true;
            btnPlot.Click += btnPlot_Click;
            // 
            // tableInitialSetup
            // 
            tableInitialSetup.ColumnCount = 2;
            tableMain.SetColumnSpan(tableInitialSetup, 3);
            tableInitialSetup.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            tableInitialSetup.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70F));
            tableInitialSetup.Controls.Add(comboPlotType, 1, 0);
            tableInitialSetup.Controls.Add(lblPlotType, 0, 0);
            tableInitialSetup.Dock = DockStyle.Fill;
            tableInitialSetup.Location = new Point(3, 3);
            tableInitialSetup.Name = "tableInitialSetup";
            tableInitialSetup.RowCount = 1;
            tableInitialSetup.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableInitialSetup.Size = new Size(794, 34);
            tableInitialSetup.TabIndex = 5;
            // 
            // comboPlotType
            // 
            comboPlotType.Dock = DockStyle.Fill;
            comboPlotType.DropDownStyle = ComboBoxStyle.DropDownList;
            comboPlotType.FormattingEnabled = true;
            comboPlotType.Items.AddRange(new object[] { "Regression Plot" });
            comboPlotType.Location = new Point(241, 3);
            comboPlotType.Name = "comboPlotType";
            comboPlotType.Size = new Size(550, 23);
            comboPlotType.TabIndex = 1;
            comboPlotType.SelectedIndexChanged += comboPlotType_SelectedIndexChanged;
            // 
            // lblPlotType
            // 
            lblPlotType.AutoSize = true;
            lblPlotType.Dock = DockStyle.Fill;
            lblPlotType.Location = new Point(3, 0);
            lblPlotType.Name = "lblPlotType";
            lblPlotType.Size = new Size(232, 34);
            lblPlotType.TabIndex = 0;
            lblPlotType.Text = "Plot Type";
            lblPlotType.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // SSCModelPlot
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(tableMain);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "SSCModelPlot";
            Text = "Plot SSC Model";
            tableMain.ResumeLayout(false);
            boxProperties.ResumeLayout(false);
            tablePlotButton.ResumeLayout(false);
            tableInitialSetup.ResumeLayout(false);
            tableInitialSetup.PerformLayout();
            ResumeLayout(false);
        }

        #endregion

        private TableLayoutPanel tableMain;
        private Label lblPlotType;
        private ComboBox comboPlotType;
        private Button btnPlot;
        private GroupBox boxProperties;
        private TableLayoutPanel tableProp;
        private TableLayoutPanel tablePlotButton;
        private TableLayoutPanel tableInitialSetup;
    }
}