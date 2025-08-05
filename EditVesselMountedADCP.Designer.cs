namespace CSEMMPGUI_v1
{
    partial class EditVesselMountedADCP
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
            menuStrip1 = new MenuStrip();
            menuFile = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
            lblPD0File = new Label();
            lblPositionFile = new Label();
            txtPD0Path = new TextBox();
            txtPositionPath = new TextBox();
            btnLoadPD0 = new Button();
            btnLoadPosition = new Button();
            tableConfig = new TableLayoutPanel();
            lblCRPOffsets = new Label();
            lblRotationAngle = new Label();
            lblUTCOffset = new Label();
            lblMagneticDeclination = new Label();
            lblName = new Label();
            tableCRPOffsets = new TableLayoutPanel();
            lblCRPZ = new Label();
            lblCRPY = new Label();
            lblCRPX = new Label();
            txtCRPX = new TextBox();
            txtCRPY = new TextBox();
            txtCRPZ = new TextBox();
            lblRSSICoefficients = new Label();
            tableRSSI = new TableLayoutPanel();
            lblRSSI1 = new Label();
            txtRSSI1 = new TextBox();
            txtRSSI2 = new TextBox();
            txtRSSI3 = new TextBox();
            txtRSSI4 = new TextBox();
            lblRSSI2 = new Label();
            lblRSSI3 = new Label();
            lblRSSI4 = new Label();
            txtName = new TextBox();
            txtMagneticDeclination = new TextBox();
            txtUTCOffset = new TextBox();
            txtRotationAngle = new TextBox();
            lblFirstEnsemble = new Label();
            txtFirstEnsemble = new NumericUpDown();
            lblLastEnsemble = new Label();
            txtLastEnsemble = new NumericUpDown();
            tablePosition = new TableLayoutPanel();
            lblYColumn = new Label();
            lblXColumn = new Label();
            comboX = new ComboBox();
            lblDateTimeColumn = new Label();
            comboDateTime = new ComboBox();
            lblHeadingColumn = new Label();
            comboHeading = new ComboBox();
            comboY = new ComboBox();
            btnPrintConfig = new Button();
            tableInputs = new TableLayoutPanel();
            tableMain = new TableLayoutPanel();
            boxFileInfo = new GroupBox();
            boxPosition = new GroupBox();
            boxConfiguration = new GroupBox();
            boxMasking = new GroupBox();
            tableMasking = new TableLayoutPanel();
            tableMaskingErrorVelocity = new TableLayoutPanel();
            lblMaxErrorVelocity = new Label();
            checkMaskingErrorVelocity = new CheckBox();
            lblMinErrorVelocity = new Label();
            txtMinErrorVelocity = new TextBox();
            txtMaxErrorVelocity = new TextBox();
            tableMaskingCorrelationMagnitude = new TableLayoutPanel();
            lblMaxCorrelationMagnitude = new Label();
            checkMaskCorrelationMagnitude = new CheckBox();
            lblMinCorrelationMagnitude = new Label();
            txtMinCorrelationMagnitude = new TextBox();
            txtMaxCorrelationMagnitude = new TextBox();
            tableMaskingVelocity = new TableLayoutPanel();
            lblMaxVelocity = new Label();
            checkMaskingVelocity = new CheckBox();
            lblMinVelocity = new Label();
            txtMinVelocity = new TextBox();
            txtMaxVelocity = new TextBox();
            tableMaskingPercentGood = new TableLayoutPanel();
            checkMaskPercentGood = new CheckBox();
            lblMinPercentGood = new Label();
            txtMinPercentGood = new TextBox();
            tableMaskingEchoIntensity = new TableLayoutPanel();
            lblMaxEchoIntensity = new Label();
            checkMaskEchoIntensity = new CheckBox();
            lblMinEchoIntensity = new Label();
            txtMinEchoIntensity = new TextBox();
            txtMaxEchoIntensity = new TextBox();
            tableMaskingEnsembles = new TableLayoutPanel();
            menuStrip1.SuspendLayout();
            tableConfig.SuspendLayout();
            tableCRPOffsets.SuspendLayout();
            tableRSSI.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)txtFirstEnsemble).BeginInit();
            ((System.ComponentModel.ISupportInitialize)txtLastEnsemble).BeginInit();
            tablePosition.SuspendLayout();
            tableInputs.SuspendLayout();
            tableMain.SuspendLayout();
            boxFileInfo.SuspendLayout();
            boxPosition.SuspendLayout();
            boxConfiguration.SuspendLayout();
            boxMasking.SuspendLayout();
            tableMasking.SuspendLayout();
            tableMaskingErrorVelocity.SuspendLayout();
            tableMaskingCorrelationMagnitude.SuspendLayout();
            tableMaskingVelocity.SuspendLayout();
            tableMaskingPercentGood.SuspendLayout();
            tableMaskingEchoIntensity.SuspendLayout();
            tableMaskingEnsembles.SuspendLayout();
            SuspendLayout();
            // 
            // menuStrip1
            // 
            menuStrip1.Items.AddRange(new ToolStripItem[] { menuFile });
            menuStrip1.Location = new Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new Size(1094, 24);
            menuStrip1.TabIndex = 0;
            menuStrip1.Text = "menuStrip1";
            // 
            // menuFile
            // 
            menuFile.DropDownItems.AddRange(new ToolStripItem[] { menuSave, menuExit });
            menuFile.Name = "menuFile";
            menuFile.Size = new Size(37, 20);
            menuFile.Text = "File";
            // 
            // menuSave
            // 
            menuSave.Name = "menuSave";
            menuSave.Size = new Size(180, 22);
            menuSave.Text = "Save...";
            menuSave.Click += menuSave_Click;
            // 
            // menuExit
            // 
            menuExit.Name = "menuExit";
            menuExit.Size = new Size(180, 22);
            menuExit.Text = "Exit";
            menuExit.Click += menuExit_Click;
            // 
            // lblPD0File
            // 
            lblPD0File.AutoSize = true;
            lblPD0File.Dock = DockStyle.Fill;
            lblPD0File.Location = new Point(3, 0);
            lblPD0File.Name = "lblPD0File";
            lblPD0File.Size = new Size(78, 27);
            lblPD0File.TabIndex = 1;
            lblPD0File.Text = ".000 File";
            lblPD0File.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // lblPositionFile
            // 
            lblPositionFile.AutoSize = true;
            lblPositionFile.Dock = DockStyle.Fill;
            lblPositionFile.Location = new Point(3, 27);
            lblPositionFile.Name = "lblPositionFile";
            lblPositionFile.Size = new Size(78, 28);
            lblPositionFile.TabIndex = 2;
            lblPositionFile.Text = "Position File";
            lblPositionFile.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtPD0Path
            // 
            txtPD0Path.Dock = DockStyle.Fill;
            txtPD0Path.Location = new Point(87, 3);
            txtPD0Path.Name = "txtPD0Path";
            txtPD0Path.Size = new Size(290, 23);
            txtPD0Path.TabIndex = 3;
            txtPD0Path.TextChanged += input_Changed;
            // 
            // txtPositionPath
            // 
            txtPositionPath.Dock = DockStyle.Fill;
            txtPositionPath.Location = new Point(87, 30);
            txtPositionPath.Name = "txtPositionPath";
            txtPositionPath.Size = new Size(290, 23);
            txtPositionPath.TabIndex = 4;
            txtPositionPath.TextChanged += input_Changed;
            // 
            // btnLoadPD0
            // 
            btnLoadPD0.Dock = DockStyle.Fill;
            btnLoadPD0.Location = new Point(383, 3);
            btnLoadPD0.Name = "btnLoadPD0";
            btnLoadPD0.Size = new Size(38, 21);
            btnLoadPD0.TabIndex = 5;
            btnLoadPD0.Text = "...";
            btnLoadPD0.UseVisualStyleBackColor = true;
            btnLoadPD0.Click += btnLoadPD0_Click;
            // 
            // btnLoadPosition
            // 
            btnLoadPosition.Dock = DockStyle.Fill;
            btnLoadPosition.Location = new Point(383, 30);
            btnLoadPosition.Name = "btnLoadPosition";
            btnLoadPosition.Size = new Size(38, 22);
            btnLoadPosition.TabIndex = 6;
            btnLoadPosition.Text = "...";
            btnLoadPosition.UseVisualStyleBackColor = true;
            btnLoadPosition.Click += btnLoadPosition_Click;
            // 
            // tableConfig
            // 
            tableConfig.ColumnCount = 2;
            tableConfig.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableConfig.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableConfig.Controls.Add(lblCRPOffsets, 0, 4);
            tableConfig.Controls.Add(lblRotationAngle, 0, 3);
            tableConfig.Controls.Add(lblUTCOffset, 0, 2);
            tableConfig.Controls.Add(lblMagneticDeclination, 0, 1);
            tableConfig.Controls.Add(lblName, 0, 0);
            tableConfig.Controls.Add(tableCRPOffsets, 1, 4);
            tableConfig.Controls.Add(lblRSSICoefficients, 0, 5);
            tableConfig.Controls.Add(tableRSSI, 1, 5);
            tableConfig.Controls.Add(txtName, 1, 0);
            tableConfig.Controls.Add(txtMagneticDeclination, 1, 1);
            tableConfig.Controls.Add(txtUTCOffset, 1, 2);
            tableConfig.Controls.Add(txtRotationAngle, 1, 3);
            tableConfig.Dock = DockStyle.Fill;
            tableConfig.Location = new Point(3, 19);
            tableConfig.Name = "tableConfig";
            tableConfig.RowCount = 9;
            tableConfig.RowStyles.Add(new RowStyle(SizeType.Percent, 8F));
            tableConfig.RowStyles.Add(new RowStyle(SizeType.Percent, 8F));
            tableConfig.RowStyles.Add(new RowStyle(SizeType.Percent, 8F));
            tableConfig.RowStyles.Add(new RowStyle(SizeType.Percent, 8F));
            tableConfig.RowStyles.Add(new RowStyle(SizeType.Percent, 22F));
            tableConfig.RowStyles.Add(new RowStyle(SizeType.Percent, 31F));
            tableConfig.RowStyles.Add(new RowStyle(SizeType.Percent, 5F));
            tableConfig.RowStyles.Add(new RowStyle(SizeType.Percent, 5F));
            tableConfig.RowStyles.Add(new RowStyle(SizeType.Percent, 5F));
            tableConfig.Size = new Size(315, 396);
            tableConfig.TabIndex = 7;
            // 
            // lblCRPOffsets
            // 
            lblCRPOffsets.AutoSize = true;
            lblCRPOffsets.Dock = DockStyle.Fill;
            lblCRPOffsets.Location = new Point(3, 124);
            lblCRPOffsets.Name = "lblCRPOffsets";
            lblCRPOffsets.Size = new Size(151, 87);
            lblCRPOffsets.TabIndex = 8;
            lblCRPOffsets.Text = "CRP Offsets (m)";
            lblCRPOffsets.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblRotationAngle
            // 
            lblRotationAngle.AutoSize = true;
            lblRotationAngle.Dock = DockStyle.Fill;
            lblRotationAngle.Location = new Point(3, 93);
            lblRotationAngle.Name = "lblRotationAngle";
            lblRotationAngle.Size = new Size(151, 31);
            lblRotationAngle.TabIndex = 7;
            lblRotationAngle.Text = "Rotation Angle (deg Clockwise)";
            lblRotationAngle.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblUTCOffset
            // 
            lblUTCOffset.AutoSize = true;
            lblUTCOffset.Dock = DockStyle.Fill;
            lblUTCOffset.Location = new Point(3, 62);
            lblUTCOffset.Name = "lblUTCOffset";
            lblUTCOffset.Size = new Size(151, 31);
            lblUTCOffset.TabIndex = 4;
            lblUTCOffset.Text = "UTC Offset (hour)";
            lblUTCOffset.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblMagneticDeclination
            // 
            lblMagneticDeclination.AutoSize = true;
            lblMagneticDeclination.Dock = DockStyle.Fill;
            lblMagneticDeclination.Location = new Point(3, 31);
            lblMagneticDeclination.Name = "lblMagneticDeclination";
            lblMagneticDeclination.Size = new Size(151, 31);
            lblMagneticDeclination.TabIndex = 2;
            lblMagneticDeclination.Text = "Magnetic Declination (deg From N)";
            lblMagneticDeclination.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblName
            // 
            lblName.AutoSize = true;
            lblName.Dock = DockStyle.Fill;
            lblName.Location = new Point(3, 0);
            lblName.Name = "lblName";
            lblName.Size = new Size(151, 31);
            lblName.TabIndex = 0;
            lblName.Text = "Name";
            lblName.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // tableCRPOffsets
            // 
            tableCRPOffsets.ColumnCount = 2;
            tableCRPOffsets.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableCRPOffsets.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableCRPOffsets.Controls.Add(lblCRPZ, 0, 2);
            tableCRPOffsets.Controls.Add(lblCRPY, 0, 1);
            tableCRPOffsets.Controls.Add(lblCRPX, 0, 0);
            tableCRPOffsets.Controls.Add(txtCRPX, 1, 0);
            tableCRPOffsets.Controls.Add(txtCRPY, 1, 1);
            tableCRPOffsets.Controls.Add(txtCRPZ, 1, 2);
            tableCRPOffsets.Dock = DockStyle.Fill;
            tableCRPOffsets.Location = new Point(160, 127);
            tableCRPOffsets.Name = "tableCRPOffsets";
            tableCRPOffsets.RowCount = 3;
            tableCRPOffsets.RowStyles.Add(new RowStyle(SizeType.Percent, 33F));
            tableCRPOffsets.RowStyles.Add(new RowStyle(SizeType.Percent, 33F));
            tableCRPOffsets.RowStyles.Add(new RowStyle(SizeType.Percent, 34F));
            tableCRPOffsets.Size = new Size(152, 81);
            tableCRPOffsets.TabIndex = 9;
            // 
            // lblCRPZ
            // 
            lblCRPZ.AutoSize = true;
            lblCRPZ.Dock = DockStyle.Fill;
            lblCRPZ.Location = new Point(3, 52);
            lblCRPZ.Name = "lblCRPZ";
            lblCRPZ.Size = new Size(70, 29);
            lblCRPZ.TabIndex = 4;
            lblCRPZ.Text = "+Z";
            lblCRPZ.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblCRPY
            // 
            lblCRPY.AutoSize = true;
            lblCRPY.Dock = DockStyle.Fill;
            lblCRPY.Location = new Point(3, 26);
            lblCRPY.Name = "lblCRPY";
            lblCRPY.Size = new Size(70, 26);
            lblCRPY.TabIndex = 2;
            lblCRPY.Text = "+Y";
            lblCRPY.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblCRPX
            // 
            lblCRPX.AutoSize = true;
            lblCRPX.Dock = DockStyle.Fill;
            lblCRPX.Location = new Point(3, 0);
            lblCRPX.Name = "lblCRPX";
            lblCRPX.Size = new Size(70, 26);
            lblCRPX.TabIndex = 0;
            lblCRPX.Text = "+X";
            lblCRPX.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtCRPX
            // 
            txtCRPX.Dock = DockStyle.Fill;
            txtCRPX.Location = new Point(79, 3);
            txtCRPX.Name = "txtCRPX";
            txtCRPX.Size = new Size(70, 23);
            txtCRPX.TabIndex = 5;
            txtCRPX.Text = "0";
            txtCRPX.TextChanged += input_Changed;
            // 
            // txtCRPY
            // 
            txtCRPY.Dock = DockStyle.Fill;
            txtCRPY.Location = new Point(79, 29);
            txtCRPY.Name = "txtCRPY";
            txtCRPY.Size = new Size(70, 23);
            txtCRPY.TabIndex = 6;
            txtCRPY.Text = "0";
            txtCRPY.TextChanged += input_Changed;
            // 
            // txtCRPZ
            // 
            txtCRPZ.Dock = DockStyle.Fill;
            txtCRPZ.Location = new Point(79, 55);
            txtCRPZ.Name = "txtCRPZ";
            txtCRPZ.Size = new Size(70, 23);
            txtCRPZ.TabIndex = 7;
            txtCRPZ.Text = "0";
            txtCRPZ.TextChanged += input_Changed;
            // 
            // lblRSSICoefficients
            // 
            lblRSSICoefficients.AutoSize = true;
            lblRSSICoefficients.Dock = DockStyle.Fill;
            lblRSSICoefficients.Location = new Point(3, 211);
            lblRSSICoefficients.Name = "lblRSSICoefficients";
            lblRSSICoefficients.Size = new Size(151, 122);
            lblRSSICoefficients.TabIndex = 10;
            lblRSSICoefficients.Text = "RSSI Coefficients";
            lblRSSICoefficients.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // tableRSSI
            // 
            tableRSSI.ColumnCount = 2;
            tableRSSI.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableRSSI.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableRSSI.Controls.Add(lblRSSI1, 0, 0);
            tableRSSI.Controls.Add(txtRSSI1, 1, 0);
            tableRSSI.Controls.Add(txtRSSI2, 1, 1);
            tableRSSI.Controls.Add(txtRSSI3, 1, 2);
            tableRSSI.Controls.Add(txtRSSI4, 1, 3);
            tableRSSI.Controls.Add(lblRSSI2, 0, 1);
            tableRSSI.Controls.Add(lblRSSI3, 0, 2);
            tableRSSI.Controls.Add(lblRSSI4, 0, 3);
            tableRSSI.Dock = DockStyle.Fill;
            tableRSSI.Location = new Point(160, 214);
            tableRSSI.Name = "tableRSSI";
            tableRSSI.RowCount = 4;
            tableRSSI.RowStyles.Add(new RowStyle(SizeType.Percent, 25F));
            tableRSSI.RowStyles.Add(new RowStyle(SizeType.Percent, 25F));
            tableRSSI.RowStyles.Add(new RowStyle(SizeType.Percent, 25F));
            tableRSSI.RowStyles.Add(new RowStyle(SizeType.Percent, 25F));
            tableRSSI.Size = new Size(152, 116);
            tableRSSI.TabIndex = 11;
            // 
            // lblRSSI1
            // 
            lblRSSI1.AutoSize = true;
            lblRSSI1.Dock = DockStyle.Fill;
            lblRSSI1.Location = new Point(3, 0);
            lblRSSI1.Name = "lblRSSI1";
            lblRSSI1.Size = new Size(70, 29);
            lblRSSI1.TabIndex = 0;
            lblRSSI1.Text = "Beam 1";
            lblRSSI1.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtRSSI1
            // 
            txtRSSI1.Dock = DockStyle.Fill;
            txtRSSI1.Location = new Point(79, 3);
            txtRSSI1.Name = "txtRSSI1";
            txtRSSI1.Size = new Size(70, 23);
            txtRSSI1.TabIndex = 1;
            txtRSSI1.TextChanged += input_Changed;
            // 
            // txtRSSI2
            // 
            txtRSSI2.Dock = DockStyle.Fill;
            txtRSSI2.Location = new Point(79, 32);
            txtRSSI2.Name = "txtRSSI2";
            txtRSSI2.Size = new Size(70, 23);
            txtRSSI2.TabIndex = 2;
            txtRSSI2.TextChanged += input_Changed;
            // 
            // txtRSSI3
            // 
            txtRSSI3.Dock = DockStyle.Fill;
            txtRSSI3.Location = new Point(79, 61);
            txtRSSI3.Name = "txtRSSI3";
            txtRSSI3.Size = new Size(70, 23);
            txtRSSI3.TabIndex = 3;
            txtRSSI3.TextChanged += input_Changed;
            // 
            // txtRSSI4
            // 
            txtRSSI4.Dock = DockStyle.Fill;
            txtRSSI4.Location = new Point(79, 90);
            txtRSSI4.Name = "txtRSSI4";
            txtRSSI4.Size = new Size(70, 23);
            txtRSSI4.TabIndex = 4;
            txtRSSI4.TextChanged += input_Changed;
            // 
            // lblRSSI2
            // 
            lblRSSI2.AutoSize = true;
            lblRSSI2.Dock = DockStyle.Fill;
            lblRSSI2.Location = new Point(3, 29);
            lblRSSI2.Name = "lblRSSI2";
            lblRSSI2.Size = new Size(70, 29);
            lblRSSI2.TabIndex = 5;
            lblRSSI2.Text = "Beam 2";
            lblRSSI2.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblRSSI3
            // 
            lblRSSI3.AutoSize = true;
            lblRSSI3.Dock = DockStyle.Fill;
            lblRSSI3.Location = new Point(3, 58);
            lblRSSI3.Name = "lblRSSI3";
            lblRSSI3.Size = new Size(70, 29);
            lblRSSI3.TabIndex = 6;
            lblRSSI3.Text = "Beam 3";
            lblRSSI3.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblRSSI4
            // 
            lblRSSI4.AutoSize = true;
            lblRSSI4.Dock = DockStyle.Fill;
            lblRSSI4.Location = new Point(3, 87);
            lblRSSI4.Name = "lblRSSI4";
            lblRSSI4.Size = new Size(70, 29);
            lblRSSI4.TabIndex = 7;
            lblRSSI4.Text = "Beam 4";
            lblRSSI4.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtName
            // 
            txtName.Dock = DockStyle.Fill;
            txtName.Location = new Point(160, 3);
            txtName.Name = "txtName";
            txtName.Size = new Size(152, 23);
            txtName.TabIndex = 12;
            txtName.TextChanged += input_Changed;
            // 
            // txtMagneticDeclination
            // 
            txtMagneticDeclination.Dock = DockStyle.Fill;
            txtMagneticDeclination.Location = new Point(160, 34);
            txtMagneticDeclination.Name = "txtMagneticDeclination";
            txtMagneticDeclination.Size = new Size(152, 23);
            txtMagneticDeclination.TabIndex = 13;
            txtMagneticDeclination.Text = "0";
            txtMagneticDeclination.TextChanged += input_Changed;
            // 
            // txtUTCOffset
            // 
            txtUTCOffset.Dock = DockStyle.Fill;
            txtUTCOffset.Location = new Point(160, 65);
            txtUTCOffset.Name = "txtUTCOffset";
            txtUTCOffset.Size = new Size(152, 23);
            txtUTCOffset.TabIndex = 14;
            txtUTCOffset.Text = "0";
            txtUTCOffset.TextChanged += input_Changed;
            // 
            // txtRotationAngle
            // 
            txtRotationAngle.Dock = DockStyle.Fill;
            txtRotationAngle.Location = new Point(160, 96);
            txtRotationAngle.Name = "txtRotationAngle";
            txtRotationAngle.Size = new Size(152, 23);
            txtRotationAngle.TabIndex = 15;
            txtRotationAngle.Text = "0";
            txtRotationAngle.TextChanged += input_Changed;
            // 
            // lblFirstEnsemble
            // 
            lblFirstEnsemble.AutoSize = true;
            lblFirstEnsemble.Dock = DockStyle.Fill;
            lblFirstEnsemble.Location = new Point(3, 0);
            lblFirstEnsemble.Name = "lblFirstEnsemble";
            lblFirstEnsemble.Size = new Size(148, 28);
            lblFirstEnsemble.TabIndex = 12;
            lblFirstEnsemble.Text = "First Ensemble";
            lblFirstEnsemble.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtFirstEnsemble
            // 
            txtFirstEnsemble.Dock = DockStyle.Fill;
            txtFirstEnsemble.Location = new Point(157, 3);
            txtFirstEnsemble.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            txtFirstEnsemble.Name = "txtFirstEnsemble";
            txtFirstEnsemble.Size = new Size(149, 23);
            txtFirstEnsemble.TabIndex = 13;
            txtFirstEnsemble.Value = new decimal(new int[] { 1, 0, 0, 0 });
            txtFirstEnsemble.ValueChanged += input_Changed;
            // 
            // lblLastEnsemble
            // 
            lblLastEnsemble.AutoSize = true;
            lblLastEnsemble.Dock = DockStyle.Fill;
            lblLastEnsemble.Location = new Point(3, 28);
            lblLastEnsemble.Name = "lblLastEnsemble";
            lblLastEnsemble.Size = new Size(148, 29);
            lblLastEnsemble.TabIndex = 14;
            lblLastEnsemble.Text = "Last Ensemble";
            lblLastEnsemble.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtLastEnsemble
            // 
            txtLastEnsemble.Dock = DockStyle.Fill;
            txtLastEnsemble.Location = new Point(157, 31);
            txtLastEnsemble.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            txtLastEnsemble.Name = "txtLastEnsemble";
            txtLastEnsemble.Size = new Size(149, 23);
            txtLastEnsemble.TabIndex = 15;
            txtLastEnsemble.Value = new decimal(new int[] { 1, 0, 0, 0 });
            txtLastEnsemble.ValueChanged += input_Changed;
            // 
            // tablePosition
            // 
            tablePosition.ColumnCount = 2;
            tablePosition.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tablePosition.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tablePosition.Controls.Add(lblYColumn, 0, 2);
            tablePosition.Controls.Add(lblXColumn, 0, 1);
            tablePosition.Controls.Add(comboX, 1, 1);
            tablePosition.Controls.Add(lblDateTimeColumn, 0, 0);
            tablePosition.Controls.Add(comboDateTime, 1, 0);
            tablePosition.Controls.Add(lblHeadingColumn, 0, 3);
            tablePosition.Controls.Add(comboHeading, 1, 3);
            tablePosition.Controls.Add(comboY, 1, 2);
            tablePosition.Dock = DockStyle.Fill;
            tablePosition.Location = new Point(3, 19);
            tablePosition.Name = "tablePosition";
            tablePosition.RowCount = 10;
            tablePosition.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tablePosition.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tablePosition.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tablePosition.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tablePosition.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tablePosition.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tablePosition.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tablePosition.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tablePosition.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tablePosition.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tablePosition.Size = new Size(424, 312);
            tablePosition.TabIndex = 8;
            // 
            // lblYColumn
            // 
            lblYColumn.AutoSize = true;
            lblYColumn.Dock = DockStyle.Fill;
            lblYColumn.Location = new Point(3, 62);
            lblYColumn.Name = "lblYColumn";
            lblYColumn.Size = new Size(206, 31);
            lblYColumn.TabIndex = 4;
            lblYColumn.Text = "Y";
            lblYColumn.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblXColumn
            // 
            lblXColumn.AutoSize = true;
            lblXColumn.Dock = DockStyle.Fill;
            lblXColumn.Location = new Point(3, 31);
            lblXColumn.Name = "lblXColumn";
            lblXColumn.Size = new Size(206, 31);
            lblXColumn.TabIndex = 2;
            lblXColumn.Text = "X";
            lblXColumn.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboX
            // 
            comboX.Dock = DockStyle.Fill;
            comboX.DropDownStyle = ComboBoxStyle.DropDownList;
            comboX.FormattingEnabled = true;
            comboX.Location = new Point(215, 34);
            comboX.Name = "comboX";
            comboX.Size = new Size(206, 23);
            comboX.TabIndex = 3;
            comboX.SelectedIndexChanged += input_Changed;
            // 
            // lblDateTimeColumn
            // 
            lblDateTimeColumn.AutoSize = true;
            lblDateTimeColumn.Dock = DockStyle.Fill;
            lblDateTimeColumn.Location = new Point(3, 0);
            lblDateTimeColumn.Name = "lblDateTimeColumn";
            lblDateTimeColumn.Size = new Size(206, 31);
            lblDateTimeColumn.TabIndex = 0;
            lblDateTimeColumn.Text = "DateTime";
            lblDateTimeColumn.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboDateTime
            // 
            comboDateTime.Dock = DockStyle.Fill;
            comboDateTime.DropDownStyle = ComboBoxStyle.DropDownList;
            comboDateTime.FormattingEnabled = true;
            comboDateTime.Location = new Point(215, 3);
            comboDateTime.Name = "comboDateTime";
            comboDateTime.Size = new Size(206, 23);
            comboDateTime.TabIndex = 1;
            comboDateTime.SelectedIndexChanged += input_Changed;
            // 
            // lblHeadingColumn
            // 
            lblHeadingColumn.AutoSize = true;
            lblHeadingColumn.Dock = DockStyle.Fill;
            lblHeadingColumn.Location = new Point(3, 93);
            lblHeadingColumn.Name = "lblHeadingColumn";
            lblHeadingColumn.Size = new Size(206, 31);
            lblHeadingColumn.TabIndex = 6;
            lblHeadingColumn.Text = "Heading";
            lblHeadingColumn.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboHeading
            // 
            comboHeading.Dock = DockStyle.Fill;
            comboHeading.DropDownStyle = ComboBoxStyle.DropDownList;
            comboHeading.FormattingEnabled = true;
            comboHeading.Location = new Point(215, 96);
            comboHeading.Name = "comboHeading";
            comboHeading.Size = new Size(206, 23);
            comboHeading.TabIndex = 7;
            comboHeading.SelectedIndexChanged += input_Changed;
            // 
            // comboY
            // 
            comboY.Dock = DockStyle.Fill;
            comboY.DropDownStyle = ComboBoxStyle.DropDownList;
            comboY.FormattingEnabled = true;
            comboY.Location = new Point(215, 65);
            comboY.Name = "comboY";
            comboY.Size = new Size(206, 23);
            comboY.TabIndex = 5;
            comboY.SelectedIndexChanged += input_Changed;
            // 
            // btnPrintConfig
            // 
            btnPrintConfig.Dock = DockStyle.Fill;
            btnPrintConfig.Enabled = false;
            btnPrintConfig.Location = new Point(441, 429);
            btnPrintConfig.Name = "btnPrintConfig";
            btnPrintConfig.Size = new Size(321, 43);
            btnPrintConfig.TabIndex = 9;
            btnPrintConfig.Text = "View Instrument Config";
            btnPrintConfig.UseVisualStyleBackColor = true;
            btnPrintConfig.Click += btnPrintConfig_Click;
            // 
            // tableInputs
            // 
            tableInputs.ColumnCount = 3;
            tableInputs.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            tableInputs.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70F));
            tableInputs.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 10F));
            tableInputs.Controls.Add(lblPD0File, 0, 0);
            tableInputs.Controls.Add(lblPositionFile, 0, 1);
            tableInputs.Controls.Add(txtPD0Path, 1, 0);
            tableInputs.Controls.Add(txtPositionPath, 1, 1);
            tableInputs.Controls.Add(btnLoadPosition, 2, 1);
            tableInputs.Controls.Add(btnLoadPD0, 2, 0);
            tableInputs.Dock = DockStyle.Fill;
            tableInputs.Location = new Point(3, 19);
            tableInputs.Name = "tableInputs";
            tableInputs.RowCount = 2;
            tableInputs.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableInputs.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableInputs.Size = new Size(424, 55);
            tableInputs.TabIndex = 10;
            // 
            // tableMain
            // 
            tableMain.CellBorderStyle = TableLayoutPanelCellBorderStyle.Single;
            tableMain.ColumnCount = 3;
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40F));
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            tableMain.Controls.Add(boxFileInfo, 0, 0);
            tableMain.Controls.Add(boxPosition, 0, 1);
            tableMain.Controls.Add(btnPrintConfig, 1, 2);
            tableMain.Controls.Add(boxConfiguration, 1, 0);
            tableMain.Controls.Add(boxMasking, 2, 0);
            tableMain.Dock = DockStyle.Fill;
            tableMain.Location = new Point(0, 24);
            tableMain.Name = "tableMain";
            tableMain.RowCount = 3;
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 17.787159F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 72.1636047F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 10.049242F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Absolute, 20F));
            tableMain.Size = new Size(1094, 476);
            tableMain.TabIndex = 11;
            // 
            // boxFileInfo
            // 
            boxFileInfo.Controls.Add(tableInputs);
            boxFileInfo.Dock = DockStyle.Fill;
            boxFileInfo.Location = new Point(4, 4);
            boxFileInfo.Name = "boxFileInfo";
            boxFileInfo.Size = new Size(430, 77);
            boxFileInfo.TabIndex = 12;
            boxFileInfo.TabStop = false;
            boxFileInfo.Text = "File Information";
            // 
            // boxPosition
            // 
            boxPosition.Controls.Add(tablePosition);
            boxPosition.Dock = DockStyle.Fill;
            boxPosition.Enabled = false;
            boxPosition.Location = new Point(4, 88);
            boxPosition.Name = "boxPosition";
            boxPosition.Size = new Size(430, 334);
            boxPosition.TabIndex = 13;
            boxPosition.TabStop = false;
            boxPosition.Text = "Position Information";
            // 
            // boxConfiguration
            // 
            boxConfiguration.Controls.Add(tableConfig);
            boxConfiguration.Dock = DockStyle.Fill;
            boxConfiguration.Enabled = false;
            boxConfiguration.Location = new Point(441, 4);
            boxConfiguration.Name = "boxConfiguration";
            tableMain.SetRowSpan(boxConfiguration, 2);
            boxConfiguration.Size = new Size(321, 418);
            boxConfiguration.TabIndex = 14;
            boxConfiguration.TabStop = false;
            boxConfiguration.Text = "Configurations";
            // 
            // boxMasking
            // 
            boxMasking.Controls.Add(tableMasking);
            boxMasking.Dock = DockStyle.Fill;
            boxMasking.Enabled = false;
            boxMasking.Location = new Point(769, 4);
            boxMasking.Name = "boxMasking";
            tableMain.SetRowSpan(boxMasking, 2);
            boxMasking.Size = new Size(321, 418);
            boxMasking.TabIndex = 15;
            boxMasking.TabStop = false;
            boxMasking.Text = "Masking";
            // 
            // tableMasking
            // 
            tableMasking.ColumnCount = 1;
            tableMasking.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableMasking.Controls.Add(tableMaskingErrorVelocity, 0, 5);
            tableMasking.Controls.Add(tableMaskingCorrelationMagnitude, 0, 3);
            tableMasking.Controls.Add(tableMaskingVelocity, 0, 3);
            tableMasking.Controls.Add(tableMaskingPercentGood, 0, 2);
            tableMasking.Controls.Add(tableMaskingEchoIntensity, 0, 1);
            tableMasking.Controls.Add(tableMaskingEnsembles, 0, 0);
            tableMasking.Dock = DockStyle.Fill;
            tableMasking.Location = new Point(3, 19);
            tableMasking.Name = "tableMasking";
            tableMasking.RowCount = 7;
            tableMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 16F));
            tableMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 16F));
            tableMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 16F));
            tableMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 16F));
            tableMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 16F));
            tableMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 16F));
            tableMasking.RowStyles.Add(new RowStyle(SizeType.Percent, 4F));
            tableMasking.Size = new Size(315, 396);
            tableMasking.TabIndex = 11;
            tableMasking.Tag = "";
            // 
            // tableMaskingErrorVelocity
            // 
            tableMaskingErrorVelocity.ColumnCount = 3;
            tableMaskingErrorVelocity.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 34F));
            tableMaskingErrorVelocity.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableMaskingErrorVelocity.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableMaskingErrorVelocity.Controls.Add(lblMaxErrorVelocity, 2, 0);
            tableMaskingErrorVelocity.Controls.Add(checkMaskingErrorVelocity, 0, 0);
            tableMaskingErrorVelocity.Controls.Add(lblMinErrorVelocity, 1, 0);
            tableMaskingErrorVelocity.Controls.Add(txtMinErrorVelocity, 1, 1);
            tableMaskingErrorVelocity.Controls.Add(txtMaxErrorVelocity, 2, 1);
            tableMaskingErrorVelocity.Dock = DockStyle.Fill;
            tableMaskingErrorVelocity.Location = new Point(3, 318);
            tableMaskingErrorVelocity.Name = "tableMaskingErrorVelocity";
            tableMaskingErrorVelocity.RowCount = 2;
            tableMaskingErrorVelocity.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingErrorVelocity.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingErrorVelocity.Size = new Size(309, 57);
            tableMaskingErrorVelocity.TabIndex = 5;
            // 
            // lblMaxErrorVelocity
            // 
            lblMaxErrorVelocity.AutoSize = true;
            lblMaxErrorVelocity.Dock = DockStyle.Fill;
            lblMaxErrorVelocity.Enabled = false;
            lblMaxErrorVelocity.Location = new Point(209, 0);
            lblMaxErrorVelocity.Name = "lblMaxErrorVelocity";
            lblMaxErrorVelocity.Size = new Size(97, 28);
            lblMaxErrorVelocity.TabIndex = 2;
            lblMaxErrorVelocity.Text = "Maximum";
            lblMaxErrorVelocity.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // checkMaskingErrorVelocity
            // 
            checkMaskingErrorVelocity.AutoSize = true;
            checkMaskingErrorVelocity.Dock = DockStyle.Fill;
            checkMaskingErrorVelocity.Location = new Point(3, 3);
            checkMaskingErrorVelocity.Name = "checkMaskingErrorVelocity";
            tableMaskingErrorVelocity.SetRowSpan(checkMaskingErrorVelocity, 2);
            checkMaskingErrorVelocity.Size = new Size(99, 51);
            checkMaskingErrorVelocity.TabIndex = 0;
            checkMaskingErrorVelocity.Text = "Mask Error Velocity (m/s)";
            checkMaskingErrorVelocity.TextAlign = ContentAlignment.MiddleCenter;
            checkMaskingErrorVelocity.UseVisualStyleBackColor = true;
            checkMaskingErrorVelocity.CheckedChanged += input_Changed;
            // 
            // lblMinErrorVelocity
            // 
            lblMinErrorVelocity.AutoSize = true;
            lblMinErrorVelocity.Dock = DockStyle.Fill;
            lblMinErrorVelocity.Enabled = false;
            lblMinErrorVelocity.Location = new Point(108, 0);
            lblMinErrorVelocity.Name = "lblMinErrorVelocity";
            lblMinErrorVelocity.Size = new Size(95, 28);
            lblMinErrorVelocity.TabIndex = 1;
            lblMinErrorVelocity.Text = "Minimum";
            lblMinErrorVelocity.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtMinErrorVelocity
            // 
            txtMinErrorVelocity.Dock = DockStyle.Fill;
            txtMinErrorVelocity.Enabled = false;
            txtMinErrorVelocity.Location = new Point(108, 31);
            txtMinErrorVelocity.Name = "txtMinErrorVelocity";
            txtMinErrorVelocity.Size = new Size(95, 23);
            txtMinErrorVelocity.TabIndex = 3;
            txtMinErrorVelocity.TextChanged += input_Changed;
            // 
            // txtMaxErrorVelocity
            // 
            txtMaxErrorVelocity.Dock = DockStyle.Fill;
            txtMaxErrorVelocity.Enabled = false;
            txtMaxErrorVelocity.Location = new Point(209, 31);
            txtMaxErrorVelocity.Name = "txtMaxErrorVelocity";
            txtMaxErrorVelocity.Size = new Size(97, 23);
            txtMaxErrorVelocity.TabIndex = 4;
            txtMaxErrorVelocity.TextChanged += input_Changed;
            // 
            // tableMaskingCorrelationMagnitude
            // 
            tableMaskingCorrelationMagnitude.ColumnCount = 3;
            tableMaskingCorrelationMagnitude.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 34F));
            tableMaskingCorrelationMagnitude.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableMaskingCorrelationMagnitude.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableMaskingCorrelationMagnitude.Controls.Add(lblMaxCorrelationMagnitude, 2, 0);
            tableMaskingCorrelationMagnitude.Controls.Add(checkMaskCorrelationMagnitude, 0, 0);
            tableMaskingCorrelationMagnitude.Controls.Add(lblMinCorrelationMagnitude, 1, 0);
            tableMaskingCorrelationMagnitude.Controls.Add(txtMinCorrelationMagnitude, 1, 1);
            tableMaskingCorrelationMagnitude.Controls.Add(txtMaxCorrelationMagnitude, 2, 1);
            tableMaskingCorrelationMagnitude.Dock = DockStyle.Fill;
            tableMaskingCorrelationMagnitude.Location = new Point(3, 192);
            tableMaskingCorrelationMagnitude.Name = "tableMaskingCorrelationMagnitude";
            tableMaskingCorrelationMagnitude.RowCount = 2;
            tableMaskingCorrelationMagnitude.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingCorrelationMagnitude.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingCorrelationMagnitude.Size = new Size(309, 57);
            tableMaskingCorrelationMagnitude.TabIndex = 4;
            // 
            // lblMaxCorrelationMagnitude
            // 
            lblMaxCorrelationMagnitude.AutoSize = true;
            lblMaxCorrelationMagnitude.Dock = DockStyle.Fill;
            lblMaxCorrelationMagnitude.Enabled = false;
            lblMaxCorrelationMagnitude.Location = new Point(209, 0);
            lblMaxCorrelationMagnitude.Name = "lblMaxCorrelationMagnitude";
            lblMaxCorrelationMagnitude.Size = new Size(97, 28);
            lblMaxCorrelationMagnitude.TabIndex = 2;
            lblMaxCorrelationMagnitude.Text = "Maximum";
            lblMaxCorrelationMagnitude.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // checkMaskCorrelationMagnitude
            // 
            checkMaskCorrelationMagnitude.AutoSize = true;
            checkMaskCorrelationMagnitude.Dock = DockStyle.Fill;
            checkMaskCorrelationMagnitude.Location = new Point(3, 3);
            checkMaskCorrelationMagnitude.Name = "checkMaskCorrelationMagnitude";
            tableMaskingCorrelationMagnitude.SetRowSpan(checkMaskCorrelationMagnitude, 2);
            checkMaskCorrelationMagnitude.Size = new Size(99, 51);
            checkMaskCorrelationMagnitude.TabIndex = 0;
            checkMaskCorrelationMagnitude.Text = "Mask Correlation Magnitude (-)";
            checkMaskCorrelationMagnitude.TextAlign = ContentAlignment.MiddleCenter;
            checkMaskCorrelationMagnitude.UseVisualStyleBackColor = true;
            checkMaskCorrelationMagnitude.CheckedChanged += input_Changed;
            // 
            // lblMinCorrelationMagnitude
            // 
            lblMinCorrelationMagnitude.AutoSize = true;
            lblMinCorrelationMagnitude.Dock = DockStyle.Fill;
            lblMinCorrelationMagnitude.Enabled = false;
            lblMinCorrelationMagnitude.Location = new Point(108, 0);
            lblMinCorrelationMagnitude.Name = "lblMinCorrelationMagnitude";
            lblMinCorrelationMagnitude.Size = new Size(95, 28);
            lblMinCorrelationMagnitude.TabIndex = 1;
            lblMinCorrelationMagnitude.Text = "Minimum";
            lblMinCorrelationMagnitude.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtMinCorrelationMagnitude
            // 
            txtMinCorrelationMagnitude.Dock = DockStyle.Fill;
            txtMinCorrelationMagnitude.Enabled = false;
            txtMinCorrelationMagnitude.Location = new Point(108, 31);
            txtMinCorrelationMagnitude.Name = "txtMinCorrelationMagnitude";
            txtMinCorrelationMagnitude.Size = new Size(95, 23);
            txtMinCorrelationMagnitude.TabIndex = 3;
            txtMinCorrelationMagnitude.Text = "0";
            txtMinCorrelationMagnitude.TextChanged += input_Changed;
            // 
            // txtMaxCorrelationMagnitude
            // 
            txtMaxCorrelationMagnitude.Dock = DockStyle.Fill;
            txtMaxCorrelationMagnitude.Enabled = false;
            txtMaxCorrelationMagnitude.Location = new Point(209, 31);
            txtMaxCorrelationMagnitude.Name = "txtMaxCorrelationMagnitude";
            txtMaxCorrelationMagnitude.Size = new Size(97, 23);
            txtMaxCorrelationMagnitude.TabIndex = 4;
            txtMaxCorrelationMagnitude.Text = "255";
            txtMaxCorrelationMagnitude.TextChanged += input_Changed;
            // 
            // tableMaskingVelocity
            // 
            tableMaskingVelocity.ColumnCount = 3;
            tableMaskingVelocity.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 34F));
            tableMaskingVelocity.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableMaskingVelocity.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableMaskingVelocity.Controls.Add(lblMaxVelocity, 2, 0);
            tableMaskingVelocity.Controls.Add(checkMaskingVelocity, 0, 0);
            tableMaskingVelocity.Controls.Add(lblMinVelocity, 1, 0);
            tableMaskingVelocity.Controls.Add(txtMinVelocity, 1, 1);
            tableMaskingVelocity.Controls.Add(txtMaxVelocity, 2, 1);
            tableMaskingVelocity.Dock = DockStyle.Fill;
            tableMaskingVelocity.Location = new Point(3, 255);
            tableMaskingVelocity.Name = "tableMaskingVelocity";
            tableMaskingVelocity.RowCount = 2;
            tableMaskingVelocity.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingVelocity.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingVelocity.Size = new Size(309, 57);
            tableMaskingVelocity.TabIndex = 3;
            // 
            // lblMaxVelocity
            // 
            lblMaxVelocity.AutoSize = true;
            lblMaxVelocity.Dock = DockStyle.Fill;
            lblMaxVelocity.Enabled = false;
            lblMaxVelocity.Location = new Point(209, 0);
            lblMaxVelocity.Name = "lblMaxVelocity";
            lblMaxVelocity.Size = new Size(97, 28);
            lblMaxVelocity.TabIndex = 2;
            lblMaxVelocity.Text = "Maximum";
            lblMaxVelocity.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // checkMaskingVelocity
            // 
            checkMaskingVelocity.AutoSize = true;
            checkMaskingVelocity.Dock = DockStyle.Fill;
            checkMaskingVelocity.Location = new Point(3, 3);
            checkMaskingVelocity.Name = "checkMaskingVelocity";
            tableMaskingVelocity.SetRowSpan(checkMaskingVelocity, 2);
            checkMaskingVelocity.Size = new Size(99, 51);
            checkMaskingVelocity.TabIndex = 0;
            checkMaskingVelocity.Text = "Mask Current Speed on XY Plane (m/s)";
            checkMaskingVelocity.TextAlign = ContentAlignment.MiddleCenter;
            checkMaskingVelocity.UseVisualStyleBackColor = true;
            checkMaskingVelocity.CheckedChanged += input_Changed;
            // 
            // lblMinVelocity
            // 
            lblMinVelocity.AutoSize = true;
            lblMinVelocity.Dock = DockStyle.Fill;
            lblMinVelocity.Enabled = false;
            lblMinVelocity.Location = new Point(108, 0);
            lblMinVelocity.Name = "lblMinVelocity";
            lblMinVelocity.Size = new Size(95, 28);
            lblMinVelocity.TabIndex = 1;
            lblMinVelocity.Text = "Minimum";
            lblMinVelocity.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtMinVelocity
            // 
            txtMinVelocity.Dock = DockStyle.Fill;
            txtMinVelocity.Enabled = false;
            txtMinVelocity.Location = new Point(108, 31);
            txtMinVelocity.Name = "txtMinVelocity";
            txtMinVelocity.Size = new Size(95, 23);
            txtMinVelocity.TabIndex = 3;
            txtMinVelocity.TextChanged += input_Changed;
            // 
            // txtMaxVelocity
            // 
            txtMaxVelocity.Dock = DockStyle.Fill;
            txtMaxVelocity.Enabled = false;
            txtMaxVelocity.Location = new Point(209, 31);
            txtMaxVelocity.Name = "txtMaxVelocity";
            txtMaxVelocity.Size = new Size(97, 23);
            txtMaxVelocity.TabIndex = 4;
            txtMaxVelocity.TextChanged += input_Changed;
            // 
            // tableMaskingPercentGood
            // 
            tableMaskingPercentGood.ColumnCount = 3;
            tableMaskingPercentGood.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 34F));
            tableMaskingPercentGood.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableMaskingPercentGood.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableMaskingPercentGood.Controls.Add(checkMaskPercentGood, 0, 0);
            tableMaskingPercentGood.Controls.Add(lblMinPercentGood, 1, 0);
            tableMaskingPercentGood.Controls.Add(txtMinPercentGood, 1, 1);
            tableMaskingPercentGood.Dock = DockStyle.Fill;
            tableMaskingPercentGood.Location = new Point(3, 129);
            tableMaskingPercentGood.Name = "tableMaskingPercentGood";
            tableMaskingPercentGood.RowCount = 2;
            tableMaskingPercentGood.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingPercentGood.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingPercentGood.Size = new Size(309, 57);
            tableMaskingPercentGood.TabIndex = 2;
            // 
            // checkMaskPercentGood
            // 
            checkMaskPercentGood.AutoSize = true;
            checkMaskPercentGood.Dock = DockStyle.Fill;
            checkMaskPercentGood.Location = new Point(3, 3);
            checkMaskPercentGood.Name = "checkMaskPercentGood";
            tableMaskingPercentGood.SetRowSpan(checkMaskPercentGood, 2);
            checkMaskPercentGood.Size = new Size(99, 51);
            checkMaskPercentGood.TabIndex = 0;
            checkMaskPercentGood.Text = "Mask Percent Good (%)";
            checkMaskPercentGood.TextAlign = ContentAlignment.MiddleCenter;
            checkMaskPercentGood.UseVisualStyleBackColor = true;
            checkMaskPercentGood.CheckedChanged += input_Changed;
            // 
            // lblMinPercentGood
            // 
            lblMinPercentGood.AutoSize = true;
            lblMinPercentGood.Dock = DockStyle.Fill;
            lblMinPercentGood.Enabled = false;
            lblMinPercentGood.Location = new Point(108, 0);
            lblMinPercentGood.Name = "lblMinPercentGood";
            lblMinPercentGood.Size = new Size(95, 28);
            lblMinPercentGood.TabIndex = 1;
            lblMinPercentGood.Text = "Minimum";
            lblMinPercentGood.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtMinPercentGood
            // 
            txtMinPercentGood.Dock = DockStyle.Fill;
            txtMinPercentGood.Enabled = false;
            txtMinPercentGood.Location = new Point(108, 31);
            txtMinPercentGood.Name = "txtMinPercentGood";
            txtMinPercentGood.Size = new Size(95, 23);
            txtMinPercentGood.TabIndex = 3;
            txtMinPercentGood.Text = "0";
            txtMinPercentGood.TextChanged += input_Changed;
            // 
            // tableMaskingEchoIntensity
            // 
            tableMaskingEchoIntensity.ColumnCount = 3;
            tableMaskingEchoIntensity.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 34F));
            tableMaskingEchoIntensity.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableMaskingEchoIntensity.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableMaskingEchoIntensity.Controls.Add(lblMaxEchoIntensity, 2, 0);
            tableMaskingEchoIntensity.Controls.Add(checkMaskEchoIntensity, 0, 0);
            tableMaskingEchoIntensity.Controls.Add(lblMinEchoIntensity, 1, 0);
            tableMaskingEchoIntensity.Controls.Add(txtMinEchoIntensity, 1, 1);
            tableMaskingEchoIntensity.Controls.Add(txtMaxEchoIntensity, 2, 1);
            tableMaskingEchoIntensity.Dock = DockStyle.Fill;
            tableMaskingEchoIntensity.Location = new Point(3, 66);
            tableMaskingEchoIntensity.Name = "tableMaskingEchoIntensity";
            tableMaskingEchoIntensity.RowCount = 2;
            tableMaskingEchoIntensity.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingEchoIntensity.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingEchoIntensity.Size = new Size(309, 57);
            tableMaskingEchoIntensity.TabIndex = 0;
            // 
            // lblMaxEchoIntensity
            // 
            lblMaxEchoIntensity.AutoSize = true;
            lblMaxEchoIntensity.Dock = DockStyle.Fill;
            lblMaxEchoIntensity.Enabled = false;
            lblMaxEchoIntensity.Location = new Point(209, 0);
            lblMaxEchoIntensity.Name = "lblMaxEchoIntensity";
            lblMaxEchoIntensity.Size = new Size(97, 28);
            lblMaxEchoIntensity.TabIndex = 2;
            lblMaxEchoIntensity.Text = "Maximum";
            lblMaxEchoIntensity.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // checkMaskEchoIntensity
            // 
            checkMaskEchoIntensity.AutoSize = true;
            checkMaskEchoIntensity.Dock = DockStyle.Fill;
            checkMaskEchoIntensity.Location = new Point(3, 3);
            checkMaskEchoIntensity.Name = "checkMaskEchoIntensity";
            tableMaskingEchoIntensity.SetRowSpan(checkMaskEchoIntensity, 2);
            checkMaskEchoIntensity.Size = new Size(99, 51);
            checkMaskEchoIntensity.TabIndex = 0;
            checkMaskEchoIntensity.Text = "Mask Echo Intensity (Counts)";
            checkMaskEchoIntensity.TextAlign = ContentAlignment.MiddleCenter;
            checkMaskEchoIntensity.UseVisualStyleBackColor = true;
            checkMaskEchoIntensity.CheckedChanged += input_Changed;
            // 
            // lblMinEchoIntensity
            // 
            lblMinEchoIntensity.AutoSize = true;
            lblMinEchoIntensity.Dock = DockStyle.Fill;
            lblMinEchoIntensity.Enabled = false;
            lblMinEchoIntensity.Location = new Point(108, 0);
            lblMinEchoIntensity.Name = "lblMinEchoIntensity";
            lblMinEchoIntensity.Size = new Size(95, 28);
            lblMinEchoIntensity.TabIndex = 1;
            lblMinEchoIntensity.Text = "Minimum";
            lblMinEchoIntensity.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtMinEchoIntensity
            // 
            txtMinEchoIntensity.Dock = DockStyle.Fill;
            txtMinEchoIntensity.Enabled = false;
            txtMinEchoIntensity.Location = new Point(108, 31);
            txtMinEchoIntensity.Name = "txtMinEchoIntensity";
            txtMinEchoIntensity.Size = new Size(95, 23);
            txtMinEchoIntensity.TabIndex = 3;
            txtMinEchoIntensity.Text = "0";
            txtMinEchoIntensity.TextChanged += input_Changed;
            // 
            // txtMaxEchoIntensity
            // 
            txtMaxEchoIntensity.Dock = DockStyle.Fill;
            txtMaxEchoIntensity.Enabled = false;
            txtMaxEchoIntensity.Location = new Point(209, 31);
            txtMaxEchoIntensity.Name = "txtMaxEchoIntensity";
            txtMaxEchoIntensity.Size = new Size(97, 23);
            txtMaxEchoIntensity.TabIndex = 4;
            txtMaxEchoIntensity.Text = "255";
            txtMaxEchoIntensity.TextChanged += input_Changed;
            // 
            // tableMaskingEnsembles
            // 
            tableMaskingEnsembles.ColumnCount = 2;
            tableMaskingEnsembles.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableMaskingEnsembles.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableMaskingEnsembles.Controls.Add(lblFirstEnsemble, 0, 0);
            tableMaskingEnsembles.Controls.Add(lblLastEnsemble, 0, 1);
            tableMaskingEnsembles.Controls.Add(txtFirstEnsemble, 1, 0);
            tableMaskingEnsembles.Controls.Add(txtLastEnsemble, 1, 1);
            tableMaskingEnsembles.Dock = DockStyle.Fill;
            tableMaskingEnsembles.Location = new Point(3, 3);
            tableMaskingEnsembles.Name = "tableMaskingEnsembles";
            tableMaskingEnsembles.RowCount = 2;
            tableMaskingEnsembles.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingEnsembles.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableMaskingEnsembles.Size = new Size(309, 57);
            tableMaskingEnsembles.TabIndex = 1;
            // 
            // EditVesselMountedADCP
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1094, 500);
            Controls.Add(tableMain);
            Controls.Add(menuStrip1);
            MainMenuStrip = menuStrip1;
            Name = "EditVesselMountedADCP";
            Text = "Vessel Mounted ADCP";
            FormClosing += EditVesselMountedADCP_FormClosing;
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            tableConfig.ResumeLayout(false);
            tableConfig.PerformLayout();
            tableCRPOffsets.ResumeLayout(false);
            tableCRPOffsets.PerformLayout();
            tableRSSI.ResumeLayout(false);
            tableRSSI.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)txtFirstEnsemble).EndInit();
            ((System.ComponentModel.ISupportInitialize)txtLastEnsemble).EndInit();
            tablePosition.ResumeLayout(false);
            tablePosition.PerformLayout();
            tableInputs.ResumeLayout(false);
            tableInputs.PerformLayout();
            tableMain.ResumeLayout(false);
            boxFileInfo.ResumeLayout(false);
            boxPosition.ResumeLayout(false);
            boxConfiguration.ResumeLayout(false);
            boxMasking.ResumeLayout(false);
            tableMasking.ResumeLayout(false);
            tableMaskingErrorVelocity.ResumeLayout(false);
            tableMaskingErrorVelocity.PerformLayout();
            tableMaskingCorrelationMagnitude.ResumeLayout(false);
            tableMaskingCorrelationMagnitude.PerformLayout();
            tableMaskingVelocity.ResumeLayout(false);
            tableMaskingVelocity.PerformLayout();
            tableMaskingPercentGood.ResumeLayout(false);
            tableMaskingPercentGood.PerformLayout();
            tableMaskingEchoIntensity.ResumeLayout(false);
            tableMaskingEchoIntensity.PerformLayout();
            tableMaskingEnsembles.ResumeLayout(false);
            tableMaskingEnsembles.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menuStrip1;
        private ToolStripMenuItem menuFile;
        private ToolStripMenuItem menuSave;
        private Label lblPD0File;
        private Label lblPositionFile;
        private TextBox txtPD0Path;
        private TextBox txtPositionPath;
        private Button btnLoadPD0;
        private Button btnLoadPosition;
        private TableLayoutPanel tableConfig;
        private TableLayoutPanel tablePosition;
        private Label lblXColumn;
        private ComboBox comboX;
        private Label lblDateTimeColumn;
        private ComboBox comboDateTime;
        private Label lblCRPOffsets;
        private Label lblRotationAngle;
        private Label lblUTCOffset;
        private Label lblMagneticDeclination;
        private Label lblName;
        private TableLayoutPanel tableCRPOffsets;
        private Label lblCRPX;
        private Label lblYColumn;
        private ComboBox comboY;
        private Label lblCRPZ;
        private Label lblCRPY;
        private TextBox txtCRPX;
        private Label lblRSSICoefficients;
        private TableLayoutPanel tableRSSI;
        private Label lblRSSI1;
        private Label lblFirstEnsemble;
        private NumericUpDown txtFirstEnsemble;
        private Label lblLastEnsemble;
        private NumericUpDown txtLastEnsemble;
        private Button btnPrintConfig;
        private TableLayoutPanel tableInputs;
        private TableLayoutPanel tableMain;
        private TableLayoutPanel tableMasking;
        private TableLayoutPanel tableMaskingEchoIntensity;
        private Label lblMaxEchoIntensity;
        private CheckBox checkMaskEchoIntensity;
        private Label lblMinEchoIntensity;
        private TextBox txtMinEchoIntensity;
        private TextBox txtMaxEchoIntensity;
        private Label lblHeadingColumn;
        private ComboBox comboHeading;
        private GroupBox boxFileInfo;
        private GroupBox boxPosition;
        private GroupBox boxConfiguration;
        private GroupBox boxMasking;
        private TextBox txtCRPY;
        private TextBox txtCRPZ;
        private TextBox txtRSSI1;
        private TextBox txtRSSI2;
        private TextBox txtRSSI3;
        private TextBox txtRSSI4;
        private Label lblRSSI2;
        private TextBox txtName;
        private TextBox txtMagneticDeclination;
        private TextBox txtUTCOffset;
        private TextBox txtRotationAngle;
        private TableLayoutPanel tableMaskingEnsembles;
        private Label lblRSSI3;
        private Label lblRSSI4;
        private TableLayoutPanel tableMaskingCorrelationMagnitude;
        private CheckBox checkMaskCorrelationMagnitude;
        private Label lblMaxCorrelationMagnitude;
        private Label lblMinCorrelationMagnitude;
        private TextBox txtMaxCorrelationMagnitude;
        private TextBox txtMinCorrelationMagnitude;
        private TableLayoutPanel tableMaskingPercentGood;
        private CheckBox checkMaskPercentGood;
        private Label lblMinPercentGood;
        private TextBox txtMinPercentGood;
        private TableLayoutPanel tableMaskingVelocity;
        private CheckBox checkMaskingVelocity;
        private Label lblMinVelocity;
        private Label lblMaxVelocity;
        private TextBox txtMinVelocity;
        private TextBox txtMaxVelocity;
        private TableLayoutPanel tableMaskingErrorVelocity;
        private CheckBox checkMaskingErrorVelocity;

        private Label label3;
        private Label lblMinErrorVelocity;
        private Label lblMaxErrorVelocity;
        private TextBox txtMinErrorVelocity;
        private TextBox txtMaxErrorVelocity;
        private ToolStripMenuItem menuExit;
    }
}