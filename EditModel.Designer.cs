namespace CSEMMPGUI_v1
{
    partial class EditModel
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(EditModel));
            menuStrip1 = new MenuStrip();
            menuFile = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
            btnLoad = new Button();
            lblFile = new Label();
            txtFilePath = new TextBox();
            tableLayoutPanel1 = new TableLayoutPanel();
            lblModelName = new Label();
            txtModelName = new TextBox();
            menuStrip1.SuspendLayout();
            tableLayoutPanel1.SuspendLayout();
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
            lblFile.Size = new Size(94, 30);
            lblFile.TabIndex = 2;
            lblFile.Text = "File";
            lblFile.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtFilePath
            // 
            txtFilePath.Dock = DockStyle.Fill;
            txtFilePath.Enabled = false;
            txtFilePath.Location = new Point(103, 33);
            txtFilePath.Name = "txtFilePath";
            txtFilePath.Size = new Size(594, 23);
            txtFilePath.TabIndex = 3;
            txtFilePath.TextChanged += input_Changed;
            // 
            // tableLayoutPanel1
            // 
            tableLayoutPanel1.ColumnCount = 3;
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 100F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 100F));
            tableLayoutPanel1.Controls.Add(lblFile, 0, 1);
            tableLayoutPanel1.Controls.Add(btnLoad, 2, 1);
            tableLayoutPanel1.Controls.Add(txtFilePath, 1, 1);
            tableLayoutPanel1.Controls.Add(lblModelName, 0, 0);
            tableLayoutPanel1.Controls.Add(txtModelName, 1, 0);
            tableLayoutPanel1.Dock = DockStyle.Fill;
            tableLayoutPanel1.Location = new Point(0, 24);
            tableLayoutPanel1.Name = "tableLayoutPanel1";
            tableLayoutPanel1.RowCount = 3;
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
            lblModelName.Size = new Size(94, 30);
            lblModelName.TabIndex = 5;
            lblModelName.Text = "Model Name";
            lblModelName.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtModelName
            // 
            tableLayoutPanel1.SetColumnSpan(txtModelName, 2);
            txtModelName.Dock = DockStyle.Fill;
            txtModelName.Location = new Point(103, 3);
            txtModelName.Name = "txtModelName";
            txtModelName.Size = new Size(694, 23);
            txtModelName.TabIndex = 6;
            txtModelName.TextChanged += input_Changed;
            // 
            // EditModel
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(tableLayoutPanel1);
            Controls.Add(menuStrip1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MainMenuStrip = menuStrip1;
            Name = "EditModel";
            Text = "Edit Model";
            FormClosing += EditModel_FormClosing;
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
        private Label label1;
        private ToolStripMenuItem menuSave;
        private Label lblModelName;
        private TextBox txtModelName;
        private ToolStripMenuItem menuExit;
    }
}