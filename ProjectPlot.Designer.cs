namespace CSEMMPGUI_v1
{
    partial class ProjectPlot
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
            tableMain = new TableLayoutPanel();
            tablePlotButton = new TableLayoutPanel();
            btnPlot = new Button();
            tableInitialSetup = new TableLayoutPanel();
            lblPlotType = new Label();
            comboPlotType = new ComboBox();
            panelProp = new Panel();
            tableProp = new TableLayoutPanel();
            tableMain.SuspendLayout();
            tablePlotButton.SuspendLayout();
            tableInitialSetup.SuspendLayout();
            panelProp.SuspendLayout();
            SuspendLayout();
            // 
            // tableMain
            // 
            tableMain.ColumnCount = 2;
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70F));
            tableMain.Controls.Add(tablePlotButton, 0, 1);
            tableMain.Controls.Add(tableInitialSetup, 0, 0);
            tableMain.Controls.Add(panelProp, 0, 2);
            tableMain.Dock = DockStyle.Fill;
            tableMain.Location = new Point(0, 0);
            tableMain.Name = "tableMain";
            tableMain.RowCount = 3;
            tableMain.RowStyles.Add(new RowStyle(SizeType.Absolute, 40F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Absolute, 40F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Absolute, 20F));
            tableMain.Size = new Size(800, 767);
            tableMain.TabIndex = 0;
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
            tableInitialSetup.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 20F));
            tableInitialSetup.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 20F));
            tableInitialSetup.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 20F));
            tableInitialSetup.Controls.Add(lblPlotType, 0, 0);
            tableInitialSetup.Controls.Add(comboPlotType, 1, 0);
            tableInitialSetup.Dock = DockStyle.Fill;
            tableInitialSetup.Location = new Point(3, 3);
            tableInitialSetup.Name = "tableInitialSetup";
            tableInitialSetup.RowCount = 2;
            tableInitialSetup.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableInitialSetup.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableInitialSetup.Size = new Size(794, 34);
            tableInitialSetup.TabIndex = 5;
            // 
            // lblPlotType
            // 
            lblPlotType.AutoSize = true;
            lblPlotType.Dock = DockStyle.Fill;
            lblPlotType.Location = new Point(3, 0);
            lblPlotType.Name = "lblPlotType";
            lblPlotType.Size = new Size(232, 30);
            lblPlotType.TabIndex = 0;
            lblPlotType.Text = "Model";
            lblPlotType.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboPlotType
            // 
            comboPlotType.Dock = DockStyle.Fill;
            comboPlotType.DropDownStyle = ComboBoxStyle.DropDownList;
            comboPlotType.FormattingEnabled = true;
            comboPlotType.Items.AddRange(new object[] { "HD Comparison", "MT Comparison", "MT and HD Comparison", "MT and HD Comparison Animation" });
            comboPlotType.Location = new Point(241, 3);
            comboPlotType.Name = "comboPlotType";
            comboPlotType.Size = new Size(550, 23);
            comboPlotType.TabIndex = 2;
            comboPlotType.SelectedIndexChanged += comboPlotType_SelectedIndexChanged;
            // 
            // panelProp
            // 
            panelProp.AutoScroll = true;
            tableMain.SetColumnSpan(panelProp, 2);
            panelProp.Controls.Add(tableProp);
            panelProp.Dock = DockStyle.Fill;
            panelProp.Location = new Point(3, 83);
            panelProp.Name = "panelProp";
            panelProp.Size = new Size(794, 681);
            panelProp.TabIndex = 6;
            // 
            // tableProp
            // 
            tableProp.AutoScroll = true;
            tableProp.ColumnCount = 1;
            tableProp.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableProp.Dock = DockStyle.Fill;
            tableProp.Location = new Point(0, 0);
            tableProp.Name = "tableProp";
            tableProp.RowCount = 1;
            tableProp.RowStyles.Add(new RowStyle(SizeType.Percent, 33.3333321F));
            tableProp.Size = new Size(794, 681);
            tableProp.TabIndex = 0;
            // 
            // ProjectPlot
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 767);
            Controls.Add(tableMain);
            Name = "ProjectPlot";
            Text = "Plot Project";
            tableMain.ResumeLayout(false);
            tablePlotButton.ResumeLayout(false);
            tableInitialSetup.ResumeLayout(false);
            tableInitialSetup.PerformLayout();
            panelProp.ResumeLayout(false);
            ResumeLayout(false);
        }

        #endregion

        private TableLayoutPanel tableMain;
        private Button btnPlot;
        private TableLayoutPanel tableProp;
        private TableLayoutPanel tablePlotButton;
        private TableLayoutPanel tableInitialSetup;
        private Label lblPlotType;
        private ComboBox comboPlotType;
        private Panel panelProp;
    }
}