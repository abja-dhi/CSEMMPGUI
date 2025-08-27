namespace CSEMMPGUI_v1
{
    partial class SSCModel
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(SSCModel));
            menuStrip1 = new MenuStrip();
            menuFile = new ToolStripMenuItem();
            menuNew = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
            tableMain = new TableLayoutPanel();
            tableModelMode = new TableLayoutPanel();
            rbManual = new RadioButton();
            rbAuto = new RadioButton();
            comboFits = new ComboBox();
            tableManual = new TableLayoutPanel();
            lblParamName = new Label();
            lblParamValue = new Label();
            lblA = new Label();
            lblB = new Label();
            lblC = new Label();
            txtA = new TextBox();
            txtB = new TextBox();
            txtC = new TextBox();
            tableModelName = new TableLayoutPanel();
            lblModelName = new Label();
            txtModelName = new TextBox();
            tableTrees = new TableLayoutPanel();
            treeItems = new TreeView();
            menuStrip1.SuspendLayout();
            tableMain.SuspendLayout();
            tableModelMode.SuspendLayout();
            tableManual.SuspendLayout();
            tableModelName.SuspendLayout();
            tableTrees.SuspendLayout();
            SuspendLayout();
            // 
            // menuStrip1
            // 
            menuStrip1.Items.AddRange(new ToolStripItem[] { menuFile });
            menuStrip1.Location = new Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new Size(800, 24);
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
            tableMain.ColumnCount = 4;
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            tableMain.Controls.Add(tableModelMode, 0, 1);
            tableMain.Controls.Add(tableManual, 0, 2);
            tableMain.Controls.Add(tableModelName, 0, 0);
            tableMain.Controls.Add(tableTrees, 2, 2);
            tableMain.Dock = DockStyle.Fill;
            tableMain.Location = new Point(0, 24);
            tableMain.Name = "tableMain";
            tableMain.RowCount = 3;
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 80F));
            tableMain.Size = new Size(800, 426);
            tableMain.TabIndex = 1;
            // 
            // tableModelMode
            // 
            tableModelMode.ColumnCount = 3;
            tableMain.SetColumnSpan(tableModelMode, 3);
            tableModelMode.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableModelMode.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33F));
            tableModelMode.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 34F));
            tableModelMode.Controls.Add(rbManual, 0, 0);
            tableModelMode.Controls.Add(rbAuto, 1, 0);
            tableModelMode.Controls.Add(comboFits, 2, 0);
            tableModelMode.Dock = DockStyle.Fill;
            tableModelMode.Location = new Point(3, 45);
            tableModelMode.Name = "tableModelMode";
            tableModelMode.RowCount = 1;
            tableModelMode.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableModelMode.Size = new Size(594, 36);
            tableModelMode.TabIndex = 1;
            // 
            // rbManual
            // 
            rbManual.AutoSize = true;
            rbManual.Dock = DockStyle.Fill;
            rbManual.Location = new Point(3, 3);
            rbManual.Name = "rbManual";
            rbManual.Size = new Size(190, 30);
            rbManual.TabIndex = 0;
            rbManual.Text = "Manual";
            rbManual.UseVisualStyleBackColor = true;
            rbManual.CheckedChanged += rbManual_CheckedChanged;
            // 
            // rbAuto
            // 
            rbAuto.AutoSize = true;
            rbAuto.Checked = true;
            rbAuto.Dock = DockStyle.Fill;
            rbAuto.Location = new Point(199, 3);
            rbAuto.Name = "rbAuto";
            rbAuto.Size = new Size(190, 30);
            rbAuto.TabIndex = 1;
            rbAuto.TabStop = true;
            rbAuto.Text = "Automatic";
            rbAuto.UseVisualStyleBackColor = true;
            // 
            // comboFits
            // 
            comboFits.Dock = DockStyle.Fill;
            comboFits.DropDownStyle = ComboBoxStyle.DropDownList;
            comboFits.FormattingEnabled = true;
            comboFits.Items.AddRange(new object[] { "Linear", "Log-Linear", "Exponential" });
            comboFits.Location = new Point(395, 3);
            comboFits.Name = "comboFits";
            comboFits.Size = new Size(196, 23);
            comboFits.TabIndex = 2;
            comboFits.SelectedIndexChanged += input_Changed;
            // 
            // tableManual
            // 
            tableManual.ColumnCount = 2;
            tableMain.SetColumnSpan(tableManual, 2);
            tableManual.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableManual.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableManual.Controls.Add(lblParamName, 0, 0);
            tableManual.Controls.Add(lblParamValue, 1, 0);
            tableManual.Controls.Add(lblA, 0, 1);
            tableManual.Controls.Add(lblB, 0, 2);
            tableManual.Controls.Add(lblC, 0, 3);
            tableManual.Controls.Add(txtA, 1, 1);
            tableManual.Controls.Add(txtB, 1, 2);
            tableManual.Controls.Add(txtC, 1, 3);
            tableManual.Dock = DockStyle.Fill;
            tableManual.Enabled = false;
            tableManual.Location = new Point(3, 87);
            tableManual.Name = "tableManual";
            tableManual.RowCount = 10;
            tableManual.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableManual.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableManual.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableManual.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableManual.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableManual.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableManual.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableManual.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableManual.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableManual.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableManual.Size = new Size(394, 336);
            tableManual.TabIndex = 2;
            // 
            // lblParamName
            // 
            lblParamName.AutoSize = true;
            lblParamName.Dock = DockStyle.Fill;
            lblParamName.Location = new Point(3, 0);
            lblParamName.Name = "lblParamName";
            lblParamName.Size = new Size(191, 33);
            lblParamName.TabIndex = 0;
            lblParamName.Text = "Parameter";
            lblParamName.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblParamValue
            // 
            lblParamValue.AutoSize = true;
            lblParamValue.Dock = DockStyle.Fill;
            lblParamValue.Location = new Point(200, 0);
            lblParamValue.Name = "lblParamValue";
            lblParamValue.Size = new Size(191, 33);
            lblParamValue.TabIndex = 1;
            lblParamValue.Text = "Value";
            lblParamValue.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblA
            // 
            lblA.AutoSize = true;
            lblA.Dock = DockStyle.Fill;
            lblA.Location = new Point(3, 33);
            lblA.Name = "lblA";
            lblA.Size = new Size(191, 33);
            lblA.TabIndex = 2;
            lblA.Text = "A";
            lblA.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblB
            // 
            lblB.AutoSize = true;
            lblB.Dock = DockStyle.Fill;
            lblB.Location = new Point(3, 66);
            lblB.Name = "lblB";
            lblB.Size = new Size(191, 33);
            lblB.TabIndex = 3;
            lblB.Text = "B";
            lblB.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblC
            // 
            lblC.AutoSize = true;
            lblC.Dock = DockStyle.Fill;
            lblC.Location = new Point(3, 99);
            lblC.Name = "lblC";
            lblC.Size = new Size(191, 33);
            lblC.TabIndex = 4;
            lblC.Text = "C";
            lblC.TextAlign = ContentAlignment.MiddleLeft;
            lblC.Visible = false;
            // 
            // txtA
            // 
            txtA.Dock = DockStyle.Fill;
            txtA.Location = new Point(200, 36);
            txtA.Name = "txtA";
            txtA.Size = new Size(191, 23);
            txtA.TabIndex = 5;
            txtA.TextChanged += input_Changed;
            // 
            // txtB
            // 
            txtB.Dock = DockStyle.Fill;
            txtB.Location = new Point(200, 69);
            txtB.Name = "txtB";
            txtB.Size = new Size(191, 23);
            txtB.TabIndex = 6;
            txtB.TextChanged += input_Changed;
            // 
            // txtC
            // 
            txtC.Dock = DockStyle.Fill;
            txtC.Location = new Point(200, 102);
            txtC.Name = "txtC";
            txtC.Size = new Size(191, 23);
            txtC.TabIndex = 7;
            txtC.Visible = false;
            txtC.TextChanged += input_Changed;
            // 
            // tableModelName
            // 
            tableModelName.ColumnCount = 2;
            tableMain.SetColumnSpan(tableModelName, 2);
            tableModelName.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            tableModelName.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70F));
            tableModelName.Controls.Add(lblModelName, 0, 0);
            tableModelName.Controls.Add(txtModelName, 1, 0);
            tableModelName.Dock = DockStyle.Fill;
            tableModelName.Location = new Point(3, 3);
            tableModelName.Name = "tableModelName";
            tableModelName.RowCount = 1;
            tableModelName.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableModelName.Size = new Size(394, 36);
            tableModelName.TabIndex = 4;
            // 
            // lblModelName
            // 
            lblModelName.AutoSize = true;
            lblModelName.Dock = DockStyle.Fill;
            lblModelName.Location = new Point(3, 0);
            lblModelName.Name = "lblModelName";
            lblModelName.Size = new Size(112, 36);
            lblModelName.TabIndex = 0;
            lblModelName.Text = "Model Name";
            lblModelName.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtModelName
            // 
            txtModelName.Dock = DockStyle.Fill;
            txtModelName.Location = new Point(121, 3);
            txtModelName.Name = "txtModelName";
            txtModelName.Size = new Size(270, 23);
            txtModelName.TabIndex = 1;
            txtModelName.TextChanged += input_Changed;
            // 
            // tableTrees
            // 
            tableTrees.ColumnCount = 2;
            tableMain.SetColumnSpan(tableTrees, 2);
            tableTrees.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableTrees.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableTrees.Controls.Add(treeItems, 0, 0);
            tableTrees.Dock = DockStyle.Fill;
            tableTrees.Location = new Point(403, 87);
            tableTrees.Name = "tableTrees";
            tableTrees.RowCount = 1;
            tableTrees.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            tableTrees.Size = new Size(394, 336);
            tableTrees.TabIndex = 6;
            // 
            // treeItems
            // 
            tableTrees.SetColumnSpan(treeItems, 2);
            treeItems.Dock = DockStyle.Fill;
            treeItems.Location = new Point(3, 3);
            treeItems.Name = "treeItems";
            treeItems.Size = new Size(388, 330);
            treeItems.TabIndex = 3;
            // 
            // SSCModel
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(tableMain);
            Controls.Add(menuStrip1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MainMenuStrip = menuStrip1;
            Name = "SSCModel";
            Text = "SSC Model";
            FormClosing += SSCModel_FormClosing;
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            tableMain.ResumeLayout(false);
            tableModelMode.ResumeLayout(false);
            tableModelMode.PerformLayout();
            tableManual.ResumeLayout(false);
            tableManual.PerformLayout();
            tableModelName.ResumeLayout(false);
            tableModelName.PerformLayout();
            tableTrees.ResumeLayout(false);
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menuStrip1;
        private ToolStripMenuItem menuFile;
        private ToolStripMenuItem menuNew;
        private ToolStripMenuItem menuSave;
        private ToolStripMenuItem menuExit;
        private TableLayoutPanel tableMain;
        private TableLayoutPanel tableModelMode;
        private RadioButton rbManual;
        private RadioButton rbAuto;
        private ComboBox comboFits;
        private TableLayoutPanel tableManual;
        private Label lblParamName;
        private Label lblParamValue;
        private Label lblA;
        private Label lblB;
        private TextBox txtA;
        private TextBox txtB;
        private TreeView treeItems;
        private TableLayoutPanel tableModelName;
        private Label lblModelName;
        private TextBox txtModelName;
        private TableLayoutPanel tableTrees;
        private Label lblC;
        private TextBox txtC;
    }
}