namespace CSEMMPGUI_v1
{
    partial class UtilsCSVImportOptions
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(UtilsCSVImportOptions));
            tableLayoutPanel1 = new TableLayoutPanel();
            rbTab = new RadioButton();
            rbWhiteSpaces = new RadioButton();
            rbSemiColon = new RadioButton();
            lblSeparator = new Label();
            rbComma = new RadioButton();
            tableLayoutPanel2 = new TableLayoutPanel();
            rbCustom = new RadioButton();
            txtCustom = new TextBox();
            lblHeader = new Label();
            txtHeader = new NumericUpDown();
            btnOK = new Button();
            tableLayoutPanel1.SuspendLayout();
            tableLayoutPanel2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)txtHeader).BeginInit();
            SuspendLayout();
            // 
            // tableLayoutPanel1
            // 
            tableLayoutPanel1.ColumnCount = 6;
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 22.98851F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 14.9425287F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 14.9425287F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 14.9425287F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 14.9425287F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 17.2413788F));
            tableLayoutPanel1.Controls.Add(rbTab, 4, 0);
            tableLayoutPanel1.Controls.Add(rbWhiteSpaces, 3, 0);
            tableLayoutPanel1.Controls.Add(rbSemiColon, 2, 0);
            tableLayoutPanel1.Controls.Add(lblSeparator, 0, 0);
            tableLayoutPanel1.Controls.Add(rbComma, 1, 0);
            tableLayoutPanel1.Controls.Add(tableLayoutPanel2, 5, 0);
            tableLayoutPanel1.Controls.Add(lblHeader, 0, 1);
            tableLayoutPanel1.Controls.Add(txtHeader, 3, 1);
            tableLayoutPanel1.Controls.Add(btnOK, 2, 2);
            tableLayoutPanel1.Dock = DockStyle.Fill;
            tableLayoutPanel1.Location = new Point(0, 0);
            tableLayoutPanel1.Name = "tableLayoutPanel1";
            tableLayoutPanel1.RowCount = 3;
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 25F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 25F));
            tableLayoutPanel1.Size = new Size(464, 123);
            tableLayoutPanel1.TabIndex = 0;
            // 
            // rbTab
            // 
            rbTab.AutoSize = true;
            rbTab.Dock = DockStyle.Fill;
            rbTab.Location = new Point(316, 3);
            rbTab.Name = "rbTab";
            rbTab.Size = new Size(63, 55);
            rbTab.TabIndex = 4;
            rbTab.Text = "Tab";
            rbTab.UseVisualStyleBackColor = true;
            // 
            // rbWhiteSpaces
            // 
            rbWhiteSpaces.AutoSize = true;
            rbWhiteSpaces.Dock = DockStyle.Fill;
            rbWhiteSpaces.Location = new Point(247, 3);
            rbWhiteSpaces.Name = "rbWhiteSpaces";
            rbWhiteSpaces.Size = new Size(63, 55);
            rbWhiteSpaces.TabIndex = 3;
            rbWhiteSpaces.Text = "Spaces";
            rbWhiteSpaces.UseVisualStyleBackColor = true;
            // 
            // rbSemiColon
            // 
            rbSemiColon.AutoSize = true;
            rbSemiColon.Dock = DockStyle.Fill;
            rbSemiColon.Location = new Point(178, 3);
            rbSemiColon.Name = "rbSemiColon";
            rbSemiColon.Size = new Size(63, 55);
            rbSemiColon.TabIndex = 2;
            rbSemiColon.Text = ";";
            rbSemiColon.UseVisualStyleBackColor = true;
            // 
            // lblSeparator
            // 
            lblSeparator.AutoSize = true;
            lblSeparator.Dock = DockStyle.Fill;
            lblSeparator.Location = new Point(3, 0);
            lblSeparator.Name = "lblSeparator";
            lblSeparator.Size = new Size(100, 61);
            lblSeparator.TabIndex = 0;
            lblSeparator.Text = "Separator";
            lblSeparator.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // rbComma
            // 
            rbComma.AutoSize = true;
            rbComma.Checked = true;
            rbComma.Dock = DockStyle.Fill;
            rbComma.Location = new Point(109, 3);
            rbComma.Name = "rbComma";
            rbComma.Size = new Size(63, 55);
            rbComma.TabIndex = 1;
            rbComma.TabStop = true;
            rbComma.Text = ",";
            rbComma.UseVisualStyleBackColor = true;
            // 
            // tableLayoutPanel2
            // 
            tableLayoutPanel2.ColumnCount = 1;
            tableLayoutPanel2.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableLayoutPanel2.Controls.Add(rbCustom, 0, 0);
            tableLayoutPanel2.Controls.Add(txtCustom, 0, 1);
            tableLayoutPanel2.Dock = DockStyle.Fill;
            tableLayoutPanel2.Location = new Point(385, 3);
            tableLayoutPanel2.Name = "tableLayoutPanel2";
            tableLayoutPanel2.RowCount = 2;
            tableLayoutPanel2.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableLayoutPanel2.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableLayoutPanel2.Size = new Size(76, 55);
            tableLayoutPanel2.TabIndex = 5;
            // 
            // rbCustom
            // 
            rbCustom.AutoSize = true;
            tableLayoutPanel2.SetColumnSpan(rbCustom, 2);
            rbCustom.Dock = DockStyle.Fill;
            rbCustom.Location = new Point(3, 3);
            rbCustom.Name = "rbCustom";
            rbCustom.Size = new Size(70, 21);
            rbCustom.TabIndex = 0;
            rbCustom.TabStop = true;
            rbCustom.Text = "Custom";
            rbCustom.UseVisualStyleBackColor = true;
            rbCustom.CheckedChanged += rbCustom_CheckedChanged;
            // 
            // txtCustom
            // 
            txtCustom.Dock = DockStyle.Fill;
            txtCustom.Location = new Point(3, 30);
            txtCustom.Name = "txtCustom";
            txtCustom.Size = new Size(70, 23);
            txtCustom.TabIndex = 1;
            // 
            // lblHeader
            // 
            lblHeader.AutoSize = true;
            tableLayoutPanel1.SetColumnSpan(lblHeader, 3);
            lblHeader.Dock = DockStyle.Fill;
            lblHeader.Location = new Point(3, 61);
            lblHeader.Name = "lblHeader";
            lblHeader.Size = new Size(238, 30);
            lblHeader.TabIndex = 6;
            lblHeader.Text = "Line number of the header row";
            lblHeader.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtHeader
            // 
            txtHeader.Dock = DockStyle.Fill;
            txtHeader.Location = new Point(247, 64);
            txtHeader.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            txtHeader.Name = "txtHeader";
            txtHeader.Size = new Size(63, 23);
            txtHeader.TabIndex = 7;
            txtHeader.Value = new decimal(new int[] { 1, 0, 0, 0 });
            // 
            // btnOK
            // 
            tableLayoutPanel1.SetColumnSpan(btnOK, 2);
            btnOK.Dock = DockStyle.Fill;
            btnOK.Location = new Point(178, 94);
            btnOK.Name = "btnOK";
            btnOK.Size = new Size(132, 26);
            btnOK.TabIndex = 8;
            btnOK.Text = "OK";
            btnOK.UseVisualStyleBackColor = true;
            btnOK.Click += btnOK_Click;
            // 
            // UtilsCSVImportOptions
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(464, 123);
            Controls.Add(tableLayoutPanel1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MaximizeBox = false;
            Name = "UtilsCSVImportOptions";
            Text = "CSV Import Options";
            tableLayoutPanel1.ResumeLayout(false);
            tableLayoutPanel1.PerformLayout();
            tableLayoutPanel2.ResumeLayout(false);
            tableLayoutPanel2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)txtHeader).EndInit();
            ResumeLayout(false);
        }

        #endregion

        private TableLayoutPanel tableLayoutPanel1;
        private Label lblSeparator;
        private RadioButton rbTab;
        private RadioButton rbWhiteSpaces;
        private RadioButton rbSemiColon;
        private RadioButton rbComma;
        private TableLayoutPanel tableLayoutPanel2;
        private RadioButton rbCustom;
        private TextBox txtCustom;
        private Label lblHeader;
        private NumericUpDown txtHeader;
        private Button btnOK;
    }
}