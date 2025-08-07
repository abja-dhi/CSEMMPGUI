namespace CSEMMPGUI_v1
{
    partial class AddOBSVerticalProfile
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(AddOBSVerticalProfile));
            menuStrip1 = new MenuStrip();
            fileToolStripMenuItem = new ToolStripMenuItem();
            menuNew = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
            tblMain = new TableLayoutPanel();
            tblFileInfo = new TableLayoutPanel();
            lblFilePath = new Label();
            lblName = new Label();
            txtName = new TextBox();
            txtFilePath = new TextBox();
            btnLoadPath = new Button();
            tblColumnInfo = new TableLayoutPanel();
            comboDepth = new ComboBox();
            lblDateTime = new Label();
            lblDepth = new Label();
            lblNTU = new Label();
            comboDateTime = new ComboBox();
            comboNTU = new ComboBox();
            tblMasking = new TableLayoutPanel();
            tblNTUMasking = new TableLayoutPanel();
            checkMaskingNTU = new CheckBox();
            lblMaskingMinNTU = new Label();
            lblMaskingMaxNTU = new Label();
            txtMaskingMinNTU = new TextBox();
            txtMaskingMaxNTU = new TextBox();
            tblDepthMasking = new TableLayoutPanel();
            checkMaskingDepth = new CheckBox();
            lblMaskingMinDepth = new Label();
            lblMaskingMaxDepth = new Label();
            txtMaskingMinDepth = new TextBox();
            txtMaskingMaxDepth = new TextBox();
            tblDateTimeMasking = new TableLayoutPanel();
            checkMaskingDateTime = new CheckBox();
            lblMaskingStartDateTime = new Label();
            lblMaskingEndDateTime = new Label();
            txtMaskingStartDateTime = new TextBox();
            txtMaskingEndDateTime = new TextBox();
            menuStrip1.SuspendLayout();
            tblMain.SuspendLayout();
            tblFileInfo.SuspendLayout();
            tblColumnInfo.SuspendLayout();
            tblMasking.SuspendLayout();
            tblNTUMasking.SuspendLayout();
            tblDepthMasking.SuspendLayout();
            tblDateTimeMasking.SuspendLayout();
            SuspendLayout();
            // 
            // menuStrip1
            // 
            menuStrip1.Items.AddRange(new ToolStripItem[] { fileToolStripMenuItem });
            menuStrip1.Location = new Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new Size(800, 24);
            menuStrip1.TabIndex = 0;
            menuStrip1.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            fileToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { menuNew, menuSave, menuExit });
            fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            fileToolStripMenuItem.Size = new Size(37, 20);
            fileToolStripMenuItem.Text = "File";
            // 
            // menuNew
            // 
            menuNew.Name = "menuNew";
            menuNew.Size = new Size(98, 22);
            menuNew.Text = "New";
            menuNew.Click += menuNew_Click;
            // 
            // menuSave
            // 
            menuSave.Name = "menuSave";
            menuSave.Size = new Size(98, 22);
            menuSave.Text = "Save";
            menuSave.Click += menuSave_Click;
            // 
            // menuExit
            // 
            menuExit.Name = "menuExit";
            menuExit.Size = new Size(98, 22);
            menuExit.Text = "Exit";
            menuExit.Click += menuExit_Click;
            // 
            // tblMain
            // 
            tblMain.ColumnCount = 2;
            tblMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 60F));
            tblMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40F));
            tblMain.Controls.Add(tblFileInfo, 0, 0);
            tblMain.Controls.Add(tblColumnInfo, 0, 1);
            tblMain.Controls.Add(tblMasking, 1, 0);
            tblMain.Dock = DockStyle.Fill;
            tblMain.Location = new Point(0, 24);
            tblMain.Name = "tblMain";
            tblMain.RowCount = 2;
            tblMain.RowStyles.Add(new RowStyle(SizeType.Percent, 22.384428F));
            tblMain.RowStyles.Add(new RowStyle(SizeType.Percent, 77.61557F));
            tblMain.Size = new Size(800, 265);
            tblMain.TabIndex = 1;
            // 
            // tblFileInfo
            // 
            tblFileInfo.ColumnCount = 3;
            tblFileInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 15F));
            tblFileInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70F));
            tblFileInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 15F));
            tblFileInfo.Controls.Add(lblFilePath, 0, 1);
            tblFileInfo.Controls.Add(lblName, 0, 0);
            tblFileInfo.Controls.Add(txtName, 1, 0);
            tblFileInfo.Controls.Add(txtFilePath, 1, 1);
            tblFileInfo.Controls.Add(btnLoadPath, 2, 1);
            tblFileInfo.Dock = DockStyle.Fill;
            tblFileInfo.Location = new Point(3, 3);
            tblFileInfo.Name = "tblFileInfo";
            tblFileInfo.RowCount = 2;
            tblFileInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tblFileInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tblFileInfo.Size = new Size(474, 53);
            tblFileInfo.TabIndex = 0;
            // 
            // lblFilePath
            // 
            lblFilePath.AutoSize = true;
            lblFilePath.Dock = DockStyle.Fill;
            lblFilePath.Location = new Point(3, 26);
            lblFilePath.Name = "lblFilePath";
            lblFilePath.Size = new Size(65, 27);
            lblFilePath.TabIndex = 0;
            lblFilePath.Text = "Data File";
            lblFilePath.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblName
            // 
            lblName.AutoSize = true;
            lblName.Dock = DockStyle.Fill;
            lblName.Location = new Point(3, 0);
            lblName.Name = "lblName";
            lblName.Size = new Size(65, 26);
            lblName.TabIndex = 1;
            lblName.Text = "Name";
            lblName.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtName
            // 
            txtName.Dock = DockStyle.Fill;
            txtName.Location = new Point(74, 3);
            txtName.Name = "txtName";
            txtName.Size = new Size(325, 23);
            txtName.TabIndex = 2;
            txtName.TextChanged += input_Changed;
            // 
            // txtFilePath
            // 
            txtFilePath.Dock = DockStyle.Fill;
            txtFilePath.Location = new Point(74, 29);
            txtFilePath.Name = "txtFilePath";
            txtFilePath.Size = new Size(325, 23);
            txtFilePath.TabIndex = 3;
            txtFilePath.TextChanged += input_Changed;
            // 
            // btnLoadPath
            // 
            btnLoadPath.Dock = DockStyle.Fill;
            btnLoadPath.Location = new Point(405, 29);
            btnLoadPath.Name = "btnLoadPath";
            btnLoadPath.Size = new Size(66, 21);
            btnLoadPath.TabIndex = 4;
            btnLoadPath.Text = "...";
            btnLoadPath.UseVisualStyleBackColor = true;
            btnLoadPath.Click += btnLoadPath_Click;
            // 
            // tblColumnInfo
            // 
            tblColumnInfo.ColumnCount = 2;
            tblColumnInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tblColumnInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tblColumnInfo.Controls.Add(comboDepth, 1, 1);
            tblColumnInfo.Controls.Add(lblDateTime, 0, 0);
            tblColumnInfo.Controls.Add(lblDepth, 0, 1);
            tblColumnInfo.Controls.Add(lblNTU, 0, 2);
            tblColumnInfo.Controls.Add(comboDateTime, 1, 0);
            tblColumnInfo.Controls.Add(comboNTU, 1, 2);
            tblColumnInfo.Dock = DockStyle.Fill;
            tblColumnInfo.Enabled = false;
            tblColumnInfo.Location = new Point(3, 62);
            tblColumnInfo.Name = "tblColumnInfo";
            tblColumnInfo.RowCount = 5;
            tblColumnInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 20F));
            tblColumnInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 20F));
            tblColumnInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 20F));
            tblColumnInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 20F));
            tblColumnInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 20F));
            tblColumnInfo.Size = new Size(474, 200);
            tblColumnInfo.TabIndex = 1;
            // 
            // comboDepth
            // 
            comboDepth.Dock = DockStyle.Fill;
            comboDepth.FormattingEnabled = true;
            comboDepth.Location = new Point(240, 43);
            comboDepth.Name = "comboDepth";
            comboDepth.Size = new Size(231, 23);
            comboDepth.TabIndex = 7;
            comboDepth.SelectedIndexChanged += input_Changed;
            // 
            // lblDateTime
            // 
            lblDateTime.AutoSize = true;
            lblDateTime.Dock = DockStyle.Fill;
            lblDateTime.Location = new Point(3, 0);
            lblDateTime.Name = "lblDateTime";
            lblDateTime.Size = new Size(231, 40);
            lblDateTime.TabIndex = 0;
            lblDateTime.Text = "DateTime";
            lblDateTime.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblDepth
            // 
            lblDepth.AutoSize = true;
            lblDepth.Dock = DockStyle.Fill;
            lblDepth.Location = new Point(3, 40);
            lblDepth.Name = "lblDepth";
            lblDepth.Size = new Size(231, 40);
            lblDepth.TabIndex = 1;
            lblDepth.Text = "Depth";
            lblDepth.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblNTU
            // 
            lblNTU.AutoSize = true;
            lblNTU.Dock = DockStyle.Fill;
            lblNTU.Location = new Point(3, 80);
            lblNTU.Name = "lblNTU";
            lblNTU.Size = new Size(231, 40);
            lblNTU.TabIndex = 2;
            lblNTU.Text = "NTU";
            lblNTU.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboDateTime
            // 
            comboDateTime.Dock = DockStyle.Fill;
            comboDateTime.FormattingEnabled = true;
            comboDateTime.Location = new Point(240, 3);
            comboDateTime.Name = "comboDateTime";
            comboDateTime.Size = new Size(231, 23);
            comboDateTime.TabIndex = 6;
            comboDateTime.SelectedIndexChanged += input_Changed;
            // 
            // comboNTU
            // 
            comboNTU.Dock = DockStyle.Fill;
            comboNTU.FormattingEnabled = true;
            comboNTU.Location = new Point(240, 83);
            comboNTU.Name = "comboNTU";
            comboNTU.Size = new Size(231, 23);
            comboNTU.TabIndex = 8;
            comboNTU.SelectedIndexChanged += input_Changed;
            // 
            // tblMasking
            // 
            tblMasking.ColumnCount = 1;
            tblMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tblMasking.Controls.Add(tblNTUMasking, 0, 2);
            tblMasking.Controls.Add(tblDepthMasking, 0, 1);
            tblMasking.Controls.Add(tblDateTimeMasking, 0, 0);
            tblMasking.Dock = DockStyle.Fill;
            tblMasking.Enabled = false;
            tblMasking.Location = new Point(483, 3);
            tblMasking.Name = "tblMasking";
            tblMasking.RowCount = 3;
            tblMain.SetRowSpan(tblMasking, 2);
            tblMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 33.33F));
            tblMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 33.33F));
            tblMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 33.34F));
            tblMasking.Size = new Size(314, 259);
            tblMasking.TabIndex = 2;
            // 
            // tblNTUMasking
            // 
            tblNTUMasking.ColumnCount = 3;
            tblNTUMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 27.272728F));
            tblNTUMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tblNTUMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tblNTUMasking.Controls.Add(checkMaskingNTU, 0, 0);
            tblNTUMasking.Controls.Add(lblMaskingMinNTU, 1, 0);
            tblNTUMasking.Controls.Add(lblMaskingMaxNTU, 2, 0);
            tblNTUMasking.Controls.Add(txtMaskingMinNTU, 1, 1);
            tblNTUMasking.Controls.Add(txtMaskingMaxNTU, 2, 1);
            tblNTUMasking.Dock = DockStyle.Fill;
            tblNTUMasking.Location = new Point(3, 175);
            tblNTUMasking.Name = "tblNTUMasking";
            tblNTUMasking.RowCount = 2;
            tblNTUMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tblNTUMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tblNTUMasking.Size = new Size(308, 81);
            tblNTUMasking.TabIndex = 2;
            // 
            // checkMaskingNTU
            // 
            checkMaskingNTU.AutoSize = true;
            checkMaskingNTU.Dock = DockStyle.Fill;
            checkMaskingNTU.Location = new Point(3, 3);
            checkMaskingNTU.Name = "checkMaskingNTU";
            tblNTUMasking.SetRowSpan(checkMaskingNTU, 2);
            checkMaskingNTU.Size = new Size(78, 75);
            checkMaskingNTU.TabIndex = 0;
            checkMaskingNTU.Text = "NTU Masking";
            checkMaskingNTU.UseVisualStyleBackColor = true;
            checkMaskingNTU.CheckedChanged += input_Changed;
            // 
            // lblMaskingMinNTU
            // 
            lblMaskingMinNTU.AutoSize = true;
            lblMaskingMinNTU.Dock = DockStyle.Fill;
            lblMaskingMinNTU.Location = new Point(87, 0);
            lblMaskingMinNTU.Name = "lblMaskingMinNTU";
            lblMaskingMinNTU.Size = new Size(106, 40);
            lblMaskingMinNTU.TabIndex = 1;
            lblMaskingMinNTU.Text = "Minimum";
            lblMaskingMinNTU.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // lblMaskingMaxNTU
            // 
            lblMaskingMaxNTU.AutoSize = true;
            lblMaskingMaxNTU.Dock = DockStyle.Fill;
            lblMaskingMaxNTU.Location = new Point(199, 0);
            lblMaskingMaxNTU.Name = "lblMaskingMaxNTU";
            lblMaskingMaxNTU.Size = new Size(106, 40);
            lblMaskingMaxNTU.TabIndex = 2;
            lblMaskingMaxNTU.Text = "Maximum";
            lblMaskingMaxNTU.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtMaskingMinNTU
            // 
            txtMaskingMinNTU.Dock = DockStyle.Fill;
            txtMaskingMinNTU.Location = new Point(87, 43);
            txtMaskingMinNTU.Name = "txtMaskingMinNTU";
            txtMaskingMinNTU.Size = new Size(106, 23);
            txtMaskingMinNTU.TabIndex = 3;
            txtMaskingMinNTU.TextChanged += input_Changed;
            // 
            // txtMaskingMaxNTU
            // 
            txtMaskingMaxNTU.Dock = DockStyle.Fill;
            txtMaskingMaxNTU.Location = new Point(199, 43);
            txtMaskingMaxNTU.Name = "txtMaskingMaxNTU";
            txtMaskingMaxNTU.Size = new Size(106, 23);
            txtMaskingMaxNTU.TabIndex = 4;
            txtMaskingMaxNTU.TextChanged += input_Changed;
            // 
            // tblDepthMasking
            // 
            tblDepthMasking.ColumnCount = 3;
            tblDepthMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 27.272728F));
            tblDepthMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tblDepthMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tblDepthMasking.Controls.Add(checkMaskingDepth, 0, 0);
            tblDepthMasking.Controls.Add(lblMaskingMinDepth, 1, 0);
            tblDepthMasking.Controls.Add(lblMaskingMaxDepth, 2, 0);
            tblDepthMasking.Controls.Add(txtMaskingMinDepth, 1, 1);
            tblDepthMasking.Controls.Add(txtMaskingMaxDepth, 2, 1);
            tblDepthMasking.Dock = DockStyle.Fill;
            tblDepthMasking.Location = new Point(3, 89);
            tblDepthMasking.Name = "tblDepthMasking";
            tblDepthMasking.RowCount = 2;
            tblDepthMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tblDepthMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tblDepthMasking.Size = new Size(308, 80);
            tblDepthMasking.TabIndex = 1;
            // 
            // checkMaskingDepth
            // 
            checkMaskingDepth.AutoSize = true;
            checkMaskingDepth.Dock = DockStyle.Fill;
            checkMaskingDepth.Location = new Point(3, 3);
            checkMaskingDepth.Name = "checkMaskingDepth";
            tblDepthMasking.SetRowSpan(checkMaskingDepth, 2);
            checkMaskingDepth.Size = new Size(78, 74);
            checkMaskingDepth.TabIndex = 0;
            checkMaskingDepth.Text = "Depth Masking";
            checkMaskingDepth.UseVisualStyleBackColor = true;
            checkMaskingDepth.CheckedChanged += input_Changed;
            // 
            // lblMaskingMinDepth
            // 
            lblMaskingMinDepth.AutoSize = true;
            lblMaskingMinDepth.Dock = DockStyle.Fill;
            lblMaskingMinDepth.Location = new Point(87, 0);
            lblMaskingMinDepth.Name = "lblMaskingMinDepth";
            lblMaskingMinDepth.Size = new Size(106, 40);
            lblMaskingMinDepth.TabIndex = 1;
            lblMaskingMinDepth.Text = "Minimum";
            lblMaskingMinDepth.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // lblMaskingMaxDepth
            // 
            lblMaskingMaxDepth.AutoSize = true;
            lblMaskingMaxDepth.Dock = DockStyle.Fill;
            lblMaskingMaxDepth.Location = new Point(199, 0);
            lblMaskingMaxDepth.Name = "lblMaskingMaxDepth";
            lblMaskingMaxDepth.Size = new Size(106, 40);
            lblMaskingMaxDepth.TabIndex = 2;
            lblMaskingMaxDepth.Text = "Maximum";
            lblMaskingMaxDepth.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtMaskingMinDepth
            // 
            txtMaskingMinDepth.Dock = DockStyle.Fill;
            txtMaskingMinDepth.Location = new Point(87, 43);
            txtMaskingMinDepth.Name = "txtMaskingMinDepth";
            txtMaskingMinDepth.Size = new Size(106, 23);
            txtMaskingMinDepth.TabIndex = 3;
            txtMaskingMinDepth.TextChanged += input_Changed;
            // 
            // txtMaskingMaxDepth
            // 
            txtMaskingMaxDepth.Dock = DockStyle.Fill;
            txtMaskingMaxDepth.Location = new Point(199, 43);
            txtMaskingMaxDepth.Name = "txtMaskingMaxDepth";
            txtMaskingMaxDepth.Size = new Size(106, 23);
            txtMaskingMaxDepth.TabIndex = 4;
            txtMaskingMaxDepth.TextChanged += input_Changed;
            // 
            // tblDateTimeMasking
            // 
            tblDateTimeMasking.ColumnCount = 3;
            tblDateTimeMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 27.27273F));
            tblDateTimeMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tblDateTimeMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tblDateTimeMasking.Controls.Add(checkMaskingDateTime, 0, 0);
            tblDateTimeMasking.Controls.Add(lblMaskingStartDateTime, 1, 0);
            tblDateTimeMasking.Controls.Add(lblMaskingEndDateTime, 2, 0);
            tblDateTimeMasking.Controls.Add(txtMaskingStartDateTime, 1, 1);
            tblDateTimeMasking.Controls.Add(txtMaskingEndDateTime, 2, 1);
            tblDateTimeMasking.Dock = DockStyle.Fill;
            tblDateTimeMasking.Location = new Point(3, 3);
            tblDateTimeMasking.Name = "tblDateTimeMasking";
            tblDateTimeMasking.RowCount = 2;
            tblDateTimeMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tblDateTimeMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tblDateTimeMasking.Size = new Size(308, 80);
            tblDateTimeMasking.TabIndex = 0;
            // 
            // checkMaskingDateTime
            // 
            checkMaskingDateTime.AutoSize = true;
            checkMaskingDateTime.Dock = DockStyle.Fill;
            checkMaskingDateTime.Location = new Point(3, 3);
            checkMaskingDateTime.Name = "checkMaskingDateTime";
            tblDateTimeMasking.SetRowSpan(checkMaskingDateTime, 2);
            checkMaskingDateTime.Size = new Size(78, 74);
            checkMaskingDateTime.TabIndex = 0;
            checkMaskingDateTime.Text = "DateTime Masking";
            checkMaskingDateTime.UseVisualStyleBackColor = true;
            checkMaskingDateTime.CheckedChanged += input_Changed;
            // 
            // lblMaskingStartDateTime
            // 
            lblMaskingStartDateTime.AutoSize = true;
            lblMaskingStartDateTime.Dock = DockStyle.Fill;
            lblMaskingStartDateTime.Location = new Point(87, 0);
            lblMaskingStartDateTime.Name = "lblMaskingStartDateTime";
            lblMaskingStartDateTime.Size = new Size(106, 40);
            lblMaskingStartDateTime.TabIndex = 1;
            lblMaskingStartDateTime.Text = "Start";
            lblMaskingStartDateTime.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // lblMaskingEndDateTime
            // 
            lblMaskingEndDateTime.AutoSize = true;
            lblMaskingEndDateTime.Dock = DockStyle.Fill;
            lblMaskingEndDateTime.Location = new Point(199, 0);
            lblMaskingEndDateTime.Name = "lblMaskingEndDateTime";
            lblMaskingEndDateTime.Size = new Size(106, 40);
            lblMaskingEndDateTime.TabIndex = 2;
            lblMaskingEndDateTime.Text = "End";
            lblMaskingEndDateTime.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtMaskingStartDateTime
            // 
            txtMaskingStartDateTime.Dock = DockStyle.Fill;
            txtMaskingStartDateTime.Location = new Point(87, 43);
            txtMaskingStartDateTime.Name = "txtMaskingStartDateTime";
            txtMaskingStartDateTime.Size = new Size(106, 23);
            txtMaskingStartDateTime.TabIndex = 3;
            txtMaskingStartDateTime.TextChanged += input_Changed;
            // 
            // txtMaskingEndDateTime
            // 
            txtMaskingEndDateTime.Dock = DockStyle.Fill;
            txtMaskingEndDateTime.Location = new Point(199, 43);
            txtMaskingEndDateTime.Name = "txtMaskingEndDateTime";
            txtMaskingEndDateTime.Size = new Size(106, 23);
            txtMaskingEndDateTime.TabIndex = 4;
            txtMaskingEndDateTime.TextChanged += input_Changed;
            // 
            // AddOBSVerticalProfile
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 289);
            Controls.Add(tblMain);
            Controls.Add(menuStrip1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MainMenuStrip = menuStrip1;
            Name = "AddOBSVerticalProfile";
            Text = "OBS Vertical Profile";
            FormClosing += AddOBSVerticalProfile_FormClosing;
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            tblMain.ResumeLayout(false);
            tblFileInfo.ResumeLayout(false);
            tblFileInfo.PerformLayout();
            tblColumnInfo.ResumeLayout(false);
            tblColumnInfo.PerformLayout();
            tblMasking.ResumeLayout(false);
            tblNTUMasking.ResumeLayout(false);
            tblNTUMasking.PerformLayout();
            tblDepthMasking.ResumeLayout(false);
            tblDepthMasking.PerformLayout();
            tblDateTimeMasking.ResumeLayout(false);
            tblDateTimeMasking.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menuStrip1;
        private ToolStripMenuItem fileToolStripMenuItem;
        private TableLayoutPanel tblMain;
        private TableLayoutPanel tblFileInfo;
        private Label lblFilePath;
        private TableLayoutPanel tblColumnInfo;
        private Label lblDateTime;
        private Label lblDepth;
        private Label lblNTU;
        private TableLayoutPanel tblMasking;
        private TableLayoutPanel tblNTUMasking;
        private CheckBox checkMaskingNTU;
        private Label lblMaskingMinNTU;
        private Label lblMaskingMaxNTU;
        private TableLayoutPanel tblDepthMasking;
        private CheckBox checkMaskingDepth;
        private Label lblMaskingMinDepth;
        private Label lblMaskingMaxDepth;
        private TableLayoutPanel tblDateTimeMasking;
        private CheckBox checkMaskingDateTime;
        private Label lblMaskingStartDateTime;
        private Label lblMaskingEndDateTime;
        private ComboBox comboDateTime;
        private ToolStripMenuItem menuNew;
        private ToolStripMenuItem menuSave;
        private ToolStripMenuItem menuExit;
        private Label lblName;
        private TextBox txtName;
        private TextBox txtFilePath;
        private Button btnLoadPath;
        private ComboBox comboDepth;
        private ComboBox comboNTU;
        private TextBox txtMaskingMinNTU;
        private TextBox txtMaskingMaxNTU;
        private TextBox txtMaskingMinDepth;
        private TextBox txtMaskingMaxDepth;
        private TextBox txtMaskingStartDateTime;
        private TextBox txtMaskingEndDateTime;
    }
}