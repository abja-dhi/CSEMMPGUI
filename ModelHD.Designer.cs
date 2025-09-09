namespace CSEMMPGUI_v1
{
    partial class ModelHD
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
            menuNew = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
            utilitiesToolStripMenuItem = new ToolStripMenuItem();
            menuDfs22Dfsu = new ToolStripMenuItem();
            btnLoad = new Button();
            lblFile = new Label();
            txtFilePath = new TextBox();
            tableLayoutPanel1 = new TableLayoutPanel();
            lblModelName = new Label();
            txtModelName = new TextBox();
            lblUItem = new Label();
            comboUItem = new ComboBox();
            lblVItem = new Label();
            comboVItem = new ComboBox();
            menuStrip1.SuspendLayout();
            tableLayoutPanel1.SuspendLayout();
            SuspendLayout();
            // 
            // menuStrip1
            // 
            menuStrip1.Items.AddRange(new ToolStripItem[] { menuFile, utilitiesToolStripMenuItem });
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
            // utilitiesToolStripMenuItem
            // 
            utilitiesToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { menuDfs22Dfsu });
            utilitiesToolStripMenuItem.Name = "utilitiesToolStripMenuItem";
            utilitiesToolStripMenuItem.Size = new Size(61, 20);
            utilitiesToolStripMenuItem.Text = "Utilities ";
            // 
            // menuDfs22Dfsu
            // 
            menuDfs22Dfsu.Name = "menuDfs22Dfsu";
            menuDfs22Dfsu.Size = new Size(193, 22);
            menuDfs22Dfsu.Text = "Dfs2 to Dfsu Converter";
            menuDfs22Dfsu.Click += menuDfs22Dfsu_Click;
            // 
            // btnLoad
            // 
            btnLoad.Dock = DockStyle.Fill;
            btnLoad.Location = new Point(703, 33);
            btnLoad.Name = "btnLoad";
            btnLoad.Size = new Size(94, 24);
            btnLoad.TabIndex = 1;
            btnLoad.Text = "...";
            btnLoad.UseVisualStyleBackColor = true;
            btnLoad.Click += btnLoad_Click;
            // 
            // lblFile
            // 
            lblFile.AutoSize = true;
            lblFile.Dock = DockStyle.Fill;
            lblFile.Location = new Point(3, 30);
            lblFile.Name = "lblFile";
            lblFile.Size = new Size(144, 30);
            lblFile.TabIndex = 2;
            lblFile.Text = "File";
            lblFile.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtFilePath
            // 
            txtFilePath.Dock = DockStyle.Fill;
            txtFilePath.Enabled = false;
            txtFilePath.Location = new Point(153, 33);
            txtFilePath.Name = "txtFilePath";
            txtFilePath.Size = new Size(544, 23);
            txtFilePath.TabIndex = 3;
            txtFilePath.TextChanged += input_Changed;
            // 
            // tableLayoutPanel1
            // 
            tableLayoutPanel1.ColumnCount = 3;
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 150F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 100F));
            tableLayoutPanel1.Controls.Add(lblFile, 0, 1);
            tableLayoutPanel1.Controls.Add(btnLoad, 2, 1);
            tableLayoutPanel1.Controls.Add(txtFilePath, 1, 1);
            tableLayoutPanel1.Controls.Add(lblModelName, 0, 0);
            tableLayoutPanel1.Controls.Add(txtModelName, 1, 0);
            tableLayoutPanel1.Controls.Add(lblUItem, 0, 2);
            tableLayoutPanel1.Controls.Add(comboUItem, 1, 2);
            tableLayoutPanel1.Controls.Add(lblVItem, 0, 3);
            tableLayoutPanel1.Controls.Add(comboVItem, 1, 3);
            tableLayoutPanel1.Dock = DockStyle.Fill;
            tableLayoutPanel1.Location = new Point(0, 24);
            tableLayoutPanel1.Name = "tableLayoutPanel1";
            tableLayoutPanel1.RowCount = 5;
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableLayoutPanel1.Size = new Size(800, 426);
            tableLayoutPanel1.TabIndex = 4;
            // 
            // lblModelName
            // 
            lblModelName.AutoSize = true;
            lblModelName.Dock = DockStyle.Fill;
            lblModelName.Location = new Point(3, 0);
            lblModelName.Name = "lblModelName";
            lblModelName.Size = new Size(144, 30);
            lblModelName.TabIndex = 5;
            lblModelName.Text = "Model Name";
            lblModelName.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtModelName
            // 
            tableLayoutPanel1.SetColumnSpan(txtModelName, 2);
            txtModelName.Dock = DockStyle.Fill;
            txtModelName.Location = new Point(153, 3);
            txtModelName.Name = "txtModelName";
            txtModelName.Size = new Size(644, 23);
            txtModelName.TabIndex = 6;
            txtModelName.TextChanged += input_Changed;
            // 
            // lblUItem
            // 
            lblUItem.AutoSize = true;
            lblUItem.Dock = DockStyle.Fill;
            lblUItem.Location = new Point(3, 60);
            lblUItem.Name = "lblUItem";
            lblUItem.Size = new Size(144, 30);
            lblUItem.TabIndex = 7;
            lblUItem.Text = "U Item in the Model";
            lblUItem.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboUItem
            // 
            comboUItem.Dock = DockStyle.Fill;
            comboUItem.DropDownStyle = ComboBoxStyle.DropDownList;
            comboUItem.Enabled = false;
            comboUItem.FormattingEnabled = true;
            comboUItem.Location = new Point(153, 63);
            comboUItem.Name = "comboUItem";
            comboUItem.Size = new Size(544, 23);
            comboUItem.TabIndex = 8;
            comboUItem.SelectedIndexChanged += input_Changed;
            // 
            // lblVItem
            // 
            lblVItem.AutoSize = true;
            lblVItem.Dock = DockStyle.Fill;
            lblVItem.Location = new Point(3, 90);
            lblVItem.Name = "lblVItem";
            lblVItem.Size = new Size(144, 30);
            lblVItem.TabIndex = 9;
            lblVItem.Text = "V Item in the Model";
            lblVItem.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboVItem
            // 
            comboVItem.Dock = DockStyle.Fill;
            comboVItem.DropDownStyle = ComboBoxStyle.DropDownList;
            comboVItem.Enabled = false;
            comboVItem.FormattingEnabled = true;
            comboVItem.Location = new Point(153, 93);
            comboVItem.Name = "comboVItem";
            comboVItem.Size = new Size(544, 23);
            comboVItem.TabIndex = 10;
            comboVItem.SelectedIndexChanged += input_Changed;
            // 
            // ModelHD
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(800, 450);
            Controls.Add(tableLayoutPanel1);
            Controls.Add(menuStrip1);
            MainMenuStrip = menuStrip1;
            Name = "ModelHD";
            Text = "HD Model";
            FormClosing += HDModel_FormClosing;
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            tableLayoutPanel1.ResumeLayout(false);
            tableLayoutPanel1.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menuStrip1;
        private ToolStripMenuItem menuFile;
        private Button btnLoad;
        private Label lblFile;
        private TextBox txtFilePath;
        private TableLayoutPanel tableLayoutPanel1;
        private Label label5;
        private Label label4;
        private Label label3;
        private Label lblVItem;
        private ToolStripMenuItem menuSave;
        private Label lblModelName;
        private TextBox txtModelName;
        private ToolStripMenuItem menuNew;
        private ToolStripMenuItem menuExit;
        private Label lblUItem;
        private ComboBox comboUItem;
        private ToolStripMenuItem utilitiesToolStripMenuItem;
        private ToolStripMenuItem menuDfs22Dfsu;
        private ComboBox comboVItem;
    }
}