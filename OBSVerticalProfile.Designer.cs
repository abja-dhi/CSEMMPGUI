namespace CSEMMPGUI_v1
{
    partial class OBSVerticalProfile
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(OBSVerticalProfile));
            menuStrip1 = new MenuStrip();
            fileToolStripMenuItem = new ToolStripMenuItem();
            menuNew = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
            tableMain = new TableLayoutPanel();
            tableFileInfo = new TableLayoutPanel();
            lblFilePath = new Label();
            lblName = new Label();
            txtName = new TextBox();
            txtFilePath = new TextBox();
            btnLoadPath = new Button();
            tableColumnInfo = new TableLayoutPanel();
            comboDepth = new ComboBox();
            lblDate = new Label();
            lblDepth = new Label();
            lblNTU = new Label();
            comboDate = new ComboBox();
            comboNTU = new ComboBox();
            lblSSCModel = new Label();
            comboSSCModel = new ComboBox();
            lblTime = new Label();
            comboTime = new ComboBox();
            tableMasking = new TableLayoutPanel();
            tableNTUMasking = new TableLayoutPanel();
            checkMaskingNTU = new CheckBox();
            lblMaskingMinNTU = new Label();
            lblMaskingMaxNTU = new Label();
            txtMaskingMinNTU = new TextBox();
            txtMaskingMaxNTU = new TextBox();
            tableDepthMasking = new TableLayoutPanel();
            checkMaskingDepth = new CheckBox();
            lblMaskingMinDepth = new Label();
            lblMaskingMaxDepth = new Label();
            txtMaskingMinDepth = new TextBox();
            txtMaskingMaxDepth = new TextBox();
            tableDateTimeMasking = new TableLayoutPanel();
            checkMaskingDateTime = new CheckBox();
            lblMaskingStartDateTime = new Label();
            lblMaskingEndDateTime = new Label();
            txtMaskingStartDateTime = new TextBox();
            txtMaskingEndDateTime = new TextBox();
            menuStrip1.SuspendLayout();
            tableMain.SuspendLayout();
            tableFileInfo.SuspendLayout();
            tableColumnInfo.SuspendLayout();
            tableMasking.SuspendLayout();
            tableNTUMasking.SuspendLayout();
            tableDepthMasking.SuspendLayout();
            tableDateTimeMasking.SuspendLayout();
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
            // tableMain
            // 
            tableMain.ColumnCount = 2;
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 60F));
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40F));
            tableMain.Controls.Add(tableFileInfo, 0, 0);
            tableMain.Controls.Add(tableColumnInfo, 0, 1);
            tableMain.Controls.Add(tableMasking, 1, 0);
            tableMain.Dock = DockStyle.Fill;
            tableMain.Location = new Point(0, 24);
            tableMain.Name = "tableMain";
            tableMain.RowCount = 3;
            tableMain.RowStyles.Add(new RowStyle(SizeType.Absolute, 60F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Absolute, 160F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableMain.Size = new Size(800, 336);
            tableMain.TabIndex = 1;
            // 
            // tableFileInfo
            // 
            tableFileInfo.ColumnCount = 3;
            tableFileInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 15F));
            tableFileInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70F));
            tableFileInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 15F));
            tableFileInfo.Controls.Add(lblFilePath, 0, 1);
            tableFileInfo.Controls.Add(lblName, 0, 0);
            tableFileInfo.Controls.Add(txtName, 1, 0);
            tableFileInfo.Controls.Add(txtFilePath, 1, 1);
            tableFileInfo.Controls.Add(btnLoadPath, 2, 1);
            tableFileInfo.Dock = DockStyle.Fill;
            tableFileInfo.Location = new Point(3, 3);
            tableFileInfo.Name = "tableFileInfo";
            tableFileInfo.RowCount = 3;
            tableFileInfo.RowStyles.Add(new RowStyle(SizeType.Absolute, 24F));
            tableFileInfo.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableFileInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableFileInfo.Size = new Size(474, 54);
            tableFileInfo.TabIndex = 0;
            // 
            // lblFilePath
            // 
            lblFilePath.AutoSize = true;
            lblFilePath.Dock = DockStyle.Fill;
            lblFilePath.Location = new Point(3, 24);
            lblFilePath.Name = "lblFilePath";
            lblFilePath.Size = new Size(65, 30);
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
            lblName.Size = new Size(65, 24);
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
            txtFilePath.Location = new Point(74, 27);
            txtFilePath.Name = "txtFilePath";
            txtFilePath.Size = new Size(325, 23);
            txtFilePath.TabIndex = 3;
            txtFilePath.TextChanged += input_Changed;
            // 
            // btnLoadPath
            // 
            btnLoadPath.Dock = DockStyle.Fill;
            btnLoadPath.Location = new Point(405, 27);
            btnLoadPath.Name = "btnLoadPath";
            btnLoadPath.Size = new Size(66, 24);
            btnLoadPath.TabIndex = 4;
            btnLoadPath.Text = "...";
            btnLoadPath.UseVisualStyleBackColor = true;
            btnLoadPath.Click += btnLoadPath_Click;
            // 
            // tableColumnInfo
            // 
            tableColumnInfo.ColumnCount = 2;
            tableColumnInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableColumnInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableColumnInfo.Controls.Add(comboDepth, 1, 2);
            tableColumnInfo.Controls.Add(lblDate, 0, 0);
            tableColumnInfo.Controls.Add(lblDepth, 0, 2);
            tableColumnInfo.Controls.Add(lblNTU, 0, 3);
            tableColumnInfo.Controls.Add(comboDate, 1, 0);
            tableColumnInfo.Controls.Add(comboNTU, 1, 3);
            tableColumnInfo.Controls.Add(lblSSCModel, 0, 4);
            tableColumnInfo.Controls.Add(comboSSCModel, 1, 4);
            tableColumnInfo.Controls.Add(lblTime, 0, 1);
            tableColumnInfo.Controls.Add(comboTime, 1, 1);
            tableColumnInfo.Dock = DockStyle.Fill;
            tableColumnInfo.Enabled = false;
            tableColumnInfo.Location = new Point(3, 63);
            tableColumnInfo.Name = "tableColumnInfo";
            tableColumnInfo.RowCount = 6;
            tableColumnInfo.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableColumnInfo.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableColumnInfo.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableColumnInfo.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableColumnInfo.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableColumnInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableColumnInfo.Size = new Size(474, 154);
            tableColumnInfo.TabIndex = 1;
            // 
            // comboDepth
            // 
            comboDepth.Dock = DockStyle.Fill;
            comboDepth.DropDownStyle = ComboBoxStyle.DropDownList;
            comboDepth.FormattingEnabled = true;
            comboDepth.Location = new Point(240, 63);
            comboDepth.Name = "comboDepth";
            comboDepth.Size = new Size(231, 23);
            comboDepth.TabIndex = 7;
            comboDepth.SelectedIndexChanged += input_Changed;
            // 
            // lblDate
            // 
            lblDate.AutoSize = true;
            lblDate.Dock = DockStyle.Fill;
            lblDate.Location = new Point(3, 0);
            lblDate.Name = "lblDate";
            lblDate.Size = new Size(231, 30);
            lblDate.TabIndex = 0;
            lblDate.Text = "Date";
            lblDate.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblDepth
            // 
            lblDepth.AutoSize = true;
            lblDepth.Dock = DockStyle.Fill;
            lblDepth.Location = new Point(3, 60);
            lblDepth.Name = "lblDepth";
            lblDepth.Size = new Size(231, 30);
            lblDepth.TabIndex = 1;
            lblDepth.Text = "Depth";
            lblDepth.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblNTU
            // 
            lblNTU.AutoSize = true;
            lblNTU.Dock = DockStyle.Fill;
            lblNTU.Location = new Point(3, 90);
            lblNTU.Name = "lblNTU";
            lblNTU.Size = new Size(231, 30);
            lblNTU.TabIndex = 2;
            lblNTU.Text = "NTU";
            lblNTU.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboDate
            // 
            comboDate.Dock = DockStyle.Fill;
            comboDate.DropDownStyle = ComboBoxStyle.DropDownList;
            comboDate.FormattingEnabled = true;
            comboDate.Location = new Point(240, 3);
            comboDate.Name = "comboDate";
            comboDate.Size = new Size(231, 23);
            comboDate.TabIndex = 6;
            comboDate.SelectedIndexChanged += input_Changed;
            // 
            // comboNTU
            // 
            comboNTU.Dock = DockStyle.Fill;
            comboNTU.DropDownStyle = ComboBoxStyle.DropDownList;
            comboNTU.FormattingEnabled = true;
            comboNTU.Location = new Point(240, 93);
            comboNTU.Name = "comboNTU";
            comboNTU.Size = new Size(231, 23);
            comboNTU.TabIndex = 8;
            comboNTU.SelectedIndexChanged += input_Changed;
            // 
            // lblSSCModel
            // 
            lblSSCModel.AutoSize = true;
            lblSSCModel.Dock = DockStyle.Fill;
            lblSSCModel.Enabled = false;
            lblSSCModel.Location = new Point(3, 120);
            lblSSCModel.Name = "lblSSCModel";
            lblSSCModel.Size = new Size(231, 30);
            lblSSCModel.TabIndex = 9;
            lblSSCModel.Text = "NTU to SSC Model";
            lblSSCModel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboSSCModel
            // 
            comboSSCModel.Dock = DockStyle.Fill;
            comboSSCModel.DropDownStyle = ComboBoxStyle.DropDownList;
            comboSSCModel.Enabled = false;
            comboSSCModel.FormattingEnabled = true;
            comboSSCModel.Location = new Point(240, 123);
            comboSSCModel.Name = "comboSSCModel";
            comboSSCModel.Size = new Size(231, 23);
            comboSSCModel.TabIndex = 10;
            comboSSCModel.SelectedIndexChanged += input_Changed;
            // 
            // lblTime
            // 
            lblTime.AutoSize = true;
            lblTime.Dock = DockStyle.Fill;
            lblTime.Location = new Point(3, 30);
            lblTime.Name = "lblTime";
            lblTime.Size = new Size(231, 30);
            lblTime.TabIndex = 11;
            lblTime.Text = "Time";
            lblTime.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboTime
            // 
            comboTime.Dock = DockStyle.Fill;
            comboTime.DropDownStyle = ComboBoxStyle.DropDownList;
            comboTime.FormattingEnabled = true;
            comboTime.Location = new Point(240, 33);
            comboTime.Name = "comboTime";
            comboTime.Size = new Size(231, 23);
            comboTime.TabIndex = 12;
            comboTime.SelectedIndexChanged += input_Changed;
            // 
            // tableMasking
            // 
            tableMasking.ColumnCount = 1;
            tableMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableMasking.Controls.Add(tableNTUMasking, 0, 2);
            tableMasking.Controls.Add(tableDepthMasking, 0, 1);
            tableMasking.Controls.Add(tableDateTimeMasking, 0, 0);
            tableMasking.Dock = DockStyle.Fill;
            tableMasking.Enabled = false;
            tableMasking.Location = new Point(483, 3);
            tableMasking.Name = "tableMasking";
            tableMasking.RowCount = 4;
            tableMain.SetRowSpan(tableMasking, 2);
            tableMasking.RowStyles.Add(new RowStyle(SizeType.Absolute, 70F));
            tableMasking.RowStyles.Add(new RowStyle(SizeType.Absolute, 70F));
            tableMasking.RowStyles.Add(new RowStyle(SizeType.Absolute, 70F));
            tableMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableMasking.Size = new Size(314, 214);
            tableMasking.TabIndex = 2;
            // 
            // tableNTUMasking
            // 
            tableNTUMasking.ColumnCount = 3;
            tableNTUMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 27.27273F));
            tableNTUMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tableNTUMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tableNTUMasking.Controls.Add(checkMaskingNTU, 0, 0);
            tableNTUMasking.Controls.Add(lblMaskingMinNTU, 1, 0);
            tableNTUMasking.Controls.Add(lblMaskingMaxNTU, 2, 0);
            tableNTUMasking.Controls.Add(txtMaskingMinNTU, 1, 1);
            tableNTUMasking.Controls.Add(txtMaskingMaxNTU, 2, 1);
            tableNTUMasking.Dock = DockStyle.Fill;
            tableNTUMasking.Location = new Point(3, 143);
            tableNTUMasking.Name = "tableNTUMasking";
            tableNTUMasking.RowCount = 3;
            tableNTUMasking.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableNTUMasking.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableNTUMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableNTUMasking.Size = new Size(308, 64);
            tableNTUMasking.TabIndex = 2;
            // 
            // checkMaskingNTU
            // 
            checkMaskingNTU.AutoSize = true;
            checkMaskingNTU.Dock = DockStyle.Fill;
            checkMaskingNTU.Location = new Point(3, 3);
            checkMaskingNTU.Name = "checkMaskingNTU";
            tableNTUMasking.SetRowSpan(checkMaskingNTU, 2);
            checkMaskingNTU.Size = new Size(78, 54);
            checkMaskingNTU.TabIndex = 0;
            checkMaskingNTU.Text = "NTU Masking";
            checkMaskingNTU.UseVisualStyleBackColor = true;
            checkMaskingNTU.CheckedChanged += checkMaskingNTU_CheckedChanged;
            // 
            // lblMaskingMinNTU
            // 
            lblMaskingMinNTU.AutoSize = true;
            lblMaskingMinNTU.Dock = DockStyle.Fill;
            lblMaskingMinNTU.Enabled = false;
            lblMaskingMinNTU.Location = new Point(87, 0);
            lblMaskingMinNTU.Name = "lblMaskingMinNTU";
            lblMaskingMinNTU.Size = new Size(106, 30);
            lblMaskingMinNTU.TabIndex = 1;
            lblMaskingMinNTU.Text = "Minimum";
            lblMaskingMinNTU.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // lblMaskingMaxNTU
            // 
            lblMaskingMaxNTU.AutoSize = true;
            lblMaskingMaxNTU.Dock = DockStyle.Fill;
            lblMaskingMaxNTU.Enabled = false;
            lblMaskingMaxNTU.Location = new Point(199, 0);
            lblMaskingMaxNTU.Name = "lblMaskingMaxNTU";
            lblMaskingMaxNTU.Size = new Size(106, 30);
            lblMaskingMaxNTU.TabIndex = 2;
            lblMaskingMaxNTU.Text = "Maximum";
            lblMaskingMaxNTU.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtMaskingMinNTU
            // 
            txtMaskingMinNTU.Dock = DockStyle.Fill;
            txtMaskingMinNTU.Enabled = false;
            txtMaskingMinNTU.Location = new Point(87, 33);
            txtMaskingMinNTU.Name = "txtMaskingMinNTU";
            txtMaskingMinNTU.Size = new Size(106, 23);
            txtMaskingMinNTU.TabIndex = 3;
            txtMaskingMinNTU.TextChanged += input_Changed;
            // 
            // txtMaskingMaxNTU
            // 
            txtMaskingMaxNTU.Dock = DockStyle.Fill;
            txtMaskingMaxNTU.Enabled = false;
            txtMaskingMaxNTU.Location = new Point(199, 33);
            txtMaskingMaxNTU.Name = "txtMaskingMaxNTU";
            txtMaskingMaxNTU.Size = new Size(106, 23);
            txtMaskingMaxNTU.TabIndex = 4;
            txtMaskingMaxNTU.TextChanged += input_Changed;
            // 
            // tableDepthMasking
            // 
            tableDepthMasking.ColumnCount = 3;
            tableDepthMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 27.27273F));
            tableDepthMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tableDepthMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tableDepthMasking.Controls.Add(checkMaskingDepth, 0, 0);
            tableDepthMasking.Controls.Add(lblMaskingMinDepth, 1, 0);
            tableDepthMasking.Controls.Add(lblMaskingMaxDepth, 2, 0);
            tableDepthMasking.Controls.Add(txtMaskingMinDepth, 1, 1);
            tableDepthMasking.Controls.Add(txtMaskingMaxDepth, 2, 1);
            tableDepthMasking.Dock = DockStyle.Fill;
            tableDepthMasking.Location = new Point(3, 73);
            tableDepthMasking.Name = "tableDepthMasking";
            tableDepthMasking.RowCount = 3;
            tableDepthMasking.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableDepthMasking.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableDepthMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableDepthMasking.Size = new Size(308, 64);
            tableDepthMasking.TabIndex = 1;
            // 
            // checkMaskingDepth
            // 
            checkMaskingDepth.AutoSize = true;
            checkMaskingDepth.Dock = DockStyle.Fill;
            checkMaskingDepth.Location = new Point(3, 3);
            checkMaskingDepth.Name = "checkMaskingDepth";
            tableDepthMasking.SetRowSpan(checkMaskingDepth, 2);
            checkMaskingDepth.Size = new Size(78, 54);
            checkMaskingDepth.TabIndex = 0;
            checkMaskingDepth.Text = "Depth Masking";
            checkMaskingDepth.UseVisualStyleBackColor = true;
            checkMaskingDepth.CheckedChanged += checkMaskingDepth_CheckedChanged;
            // 
            // lblMaskingMinDepth
            // 
            lblMaskingMinDepth.AutoSize = true;
            lblMaskingMinDepth.Dock = DockStyle.Fill;
            lblMaskingMinDepth.Enabled = false;
            lblMaskingMinDepth.Location = new Point(87, 0);
            lblMaskingMinDepth.Name = "lblMaskingMinDepth";
            lblMaskingMinDepth.Size = new Size(106, 30);
            lblMaskingMinDepth.TabIndex = 1;
            lblMaskingMinDepth.Text = "Minimum";
            lblMaskingMinDepth.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // lblMaskingMaxDepth
            // 
            lblMaskingMaxDepth.AutoSize = true;
            lblMaskingMaxDepth.Dock = DockStyle.Fill;
            lblMaskingMaxDepth.Enabled = false;
            lblMaskingMaxDepth.Location = new Point(199, 0);
            lblMaskingMaxDepth.Name = "lblMaskingMaxDepth";
            lblMaskingMaxDepth.Size = new Size(106, 30);
            lblMaskingMaxDepth.TabIndex = 2;
            lblMaskingMaxDepth.Text = "Maximum";
            lblMaskingMaxDepth.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtMaskingMinDepth
            // 
            txtMaskingMinDepth.Dock = DockStyle.Fill;
            txtMaskingMinDepth.Enabled = false;
            txtMaskingMinDepth.Location = new Point(87, 33);
            txtMaskingMinDepth.Name = "txtMaskingMinDepth";
            txtMaskingMinDepth.Size = new Size(106, 23);
            txtMaskingMinDepth.TabIndex = 3;
            txtMaskingMinDepth.TextChanged += input_Changed;
            // 
            // txtMaskingMaxDepth
            // 
            txtMaskingMaxDepth.Dock = DockStyle.Fill;
            txtMaskingMaxDepth.Enabled = false;
            txtMaskingMaxDepth.Location = new Point(199, 33);
            txtMaskingMaxDepth.Name = "txtMaskingMaxDepth";
            txtMaskingMaxDepth.Size = new Size(106, 23);
            txtMaskingMaxDepth.TabIndex = 4;
            txtMaskingMaxDepth.TextChanged += input_Changed;
            // 
            // tableDateTimeMasking
            // 
            tableDateTimeMasking.ColumnCount = 3;
            tableDateTimeMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 27.27273F));
            tableDateTimeMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tableDateTimeMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 36.363636F));
            tableDateTimeMasking.Controls.Add(checkMaskingDateTime, 0, 0);
            tableDateTimeMasking.Controls.Add(lblMaskingStartDateTime, 1, 0);
            tableDateTimeMasking.Controls.Add(lblMaskingEndDateTime, 2, 0);
            tableDateTimeMasking.Controls.Add(txtMaskingStartDateTime, 1, 1);
            tableDateTimeMasking.Controls.Add(txtMaskingEndDateTime, 2, 1);
            tableDateTimeMasking.Dock = DockStyle.Fill;
            tableDateTimeMasking.Location = new Point(3, 3);
            tableDateTimeMasking.Name = "tableDateTimeMasking";
            tableDateTimeMasking.RowCount = 3;
            tableDateTimeMasking.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableDateTimeMasking.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableDateTimeMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableDateTimeMasking.Size = new Size(308, 64);
            tableDateTimeMasking.TabIndex = 0;
            // 
            // checkMaskingDateTime
            // 
            checkMaskingDateTime.AutoSize = true;
            checkMaskingDateTime.Dock = DockStyle.Fill;
            checkMaskingDateTime.Location = new Point(3, 3);
            checkMaskingDateTime.Name = "checkMaskingDateTime";
            tableDateTimeMasking.SetRowSpan(checkMaskingDateTime, 2);
            checkMaskingDateTime.Size = new Size(78, 54);
            checkMaskingDateTime.TabIndex = 0;
            checkMaskingDateTime.Text = "DateTime Masking";
            checkMaskingDateTime.UseVisualStyleBackColor = true;
            checkMaskingDateTime.CheckedChanged += checkMaskingDateTime_CheckedChanged;
            // 
            // lblMaskingStartDateTime
            // 
            lblMaskingStartDateTime.AutoSize = true;
            lblMaskingStartDateTime.Dock = DockStyle.Fill;
            lblMaskingStartDateTime.Enabled = false;
            lblMaskingStartDateTime.Location = new Point(87, 0);
            lblMaskingStartDateTime.Name = "lblMaskingStartDateTime";
            lblMaskingStartDateTime.Size = new Size(106, 30);
            lblMaskingStartDateTime.TabIndex = 1;
            lblMaskingStartDateTime.Text = "Start";
            lblMaskingStartDateTime.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // lblMaskingEndDateTime
            // 
            lblMaskingEndDateTime.AutoSize = true;
            lblMaskingEndDateTime.Dock = DockStyle.Fill;
            lblMaskingEndDateTime.Enabled = false;
            lblMaskingEndDateTime.Location = new Point(199, 0);
            lblMaskingEndDateTime.Name = "lblMaskingEndDateTime";
            lblMaskingEndDateTime.Size = new Size(106, 30);
            lblMaskingEndDateTime.TabIndex = 2;
            lblMaskingEndDateTime.Text = "End";
            lblMaskingEndDateTime.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtMaskingStartDateTime
            // 
            txtMaskingStartDateTime.Dock = DockStyle.Fill;
            txtMaskingStartDateTime.Enabled = false;
            txtMaskingStartDateTime.Location = new Point(87, 33);
            txtMaskingStartDateTime.Name = "txtMaskingStartDateTime";
            txtMaskingStartDateTime.Size = new Size(106, 23);
            txtMaskingStartDateTime.TabIndex = 3;
            txtMaskingStartDateTime.TextChanged += input_Changed;
            // 
            // txtMaskingEndDateTime
            // 
            txtMaskingEndDateTime.Dock = DockStyle.Fill;
            txtMaskingEndDateTime.Enabled = false;
            txtMaskingEndDateTime.Location = new Point(199, 33);
            txtMaskingEndDateTime.Name = "txtMaskingEndDateTime";
            txtMaskingEndDateTime.Size = new Size(106, 23);
            txtMaskingEndDateTime.TabIndex = 4;
            txtMaskingEndDateTime.TextChanged += input_Changed;
            // 
            // OBSVerticalProfile
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(800, 360);
            Controls.Add(tableMain);
            Controls.Add(menuStrip1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MainMenuStrip = menuStrip1;
            Name = "OBSVerticalProfile";
            Text = "OBS Vertical Profile";
            FormClosing += OBSVerticalProfile_FormClosing;
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            tableMain.ResumeLayout(false);
            tableFileInfo.ResumeLayout(false);
            tableFileInfo.PerformLayout();
            tableColumnInfo.ResumeLayout(false);
            tableColumnInfo.PerformLayout();
            tableMasking.ResumeLayout(false);
            tableNTUMasking.ResumeLayout(false);
            tableNTUMasking.PerformLayout();
            tableDepthMasking.ResumeLayout(false);
            tableDepthMasking.PerformLayout();
            tableDateTimeMasking.ResumeLayout(false);
            tableDateTimeMasking.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menuStrip1;
        private ToolStripMenuItem fileToolStripMenuItem;
        private TableLayoutPanel tableMain;
        private TableLayoutPanel tableFileInfo;
        private Label lblFilePath;
        private TableLayoutPanel tableColumnInfo;
        private Label lblDate;
        private Label lblDepth;
        private Label lblNTU;
        private TableLayoutPanel tableMasking;
        private TableLayoutPanel tableNTUMasking;
        private CheckBox checkMaskingNTU;
        private Label lblMaskingMinNTU;
        private Label lblMaskingMaxNTU;
        private TableLayoutPanel tableDepthMasking;
        private CheckBox checkMaskingDepth;
        private Label lblMaskingMinDepth;
        private Label lblMaskingMaxDepth;
        private TableLayoutPanel tableDateTimeMasking;
        private CheckBox checkMaskingDateTime;
        private Label lblMaskingStartDateTime;
        private Label lblMaskingEndDateTime;
        private ComboBox comboDate;
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
        private Label lblSSCModel;
        private ComboBox comboSSCModel;
        private Label lblTime;
        private ComboBox comboTime;
    }
}