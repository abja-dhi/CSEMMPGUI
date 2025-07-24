namespace CSEMMPGUI_v1
{
    partial class PropertiesPage
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
            txtProjectEPSG = new TextBox();
            lblProjectEPSG = new Label();
            lblProjectDir = new Label();
            lblProjectName = new Label();
            txtProjectDir = new TextBox();
            txtProjectName = new TextBox();
            btnProjectDir = new Button();
            txtProjectDescription = new TextBox();
            lblProjectDescription = new Label();
            tableOrganizer = new TableLayoutPanel();
            menuMain = new MenuStrip();
            menuFile = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            tableOrganizer.SuspendLayout();
            menuMain.SuspendLayout();
            SuspendLayout();
            // 
            // txtProjectEPSG
            // 
            txtProjectEPSG.Dock = DockStyle.Fill;
            txtProjectEPSG.Location = new Point(105, 59);
            txtProjectEPSG.Name = "txtProjectEPSG";
            txtProjectEPSG.Size = new Size(327, 23);
            txtProjectEPSG.TabIndex = 3;
            txtProjectEPSG.TextChanged += saveStatus;
            // 
            // lblProjectEPSG
            // 
            lblProjectEPSG.AutoSize = true;
            lblProjectEPSG.Dock = DockStyle.Fill;
            lblProjectEPSG.Location = new Point(3, 56);
            lblProjectEPSG.Name = "lblProjectEPSG";
            lblProjectEPSG.Size = new Size(96, 28);
            lblProjectEPSG.TabIndex = 1;
            lblProjectEPSG.Text = "EPSG";
            // 
            // lblProjectDir
            // 
            lblProjectDir.AutoSize = true;
            lblProjectDir.Dock = DockStyle.Fill;
            lblProjectDir.Location = new Point(3, 28);
            lblProjectDir.Name = "lblProjectDir";
            lblProjectDir.Size = new Size(96, 28);
            lblProjectDir.TabIndex = 2;
            lblProjectDir.Text = "Project Directory";
            // 
            // lblProjectName
            // 
            lblProjectName.AutoSize = true;
            lblProjectName.Dock = DockStyle.Fill;
            lblProjectName.Location = new Point(3, 0);
            lblProjectName.Name = "lblProjectName";
            lblProjectName.Size = new Size(96, 28);
            lblProjectName.TabIndex = 3;
            lblProjectName.Text = "Project Name";
            // 
            // txtProjectDir
            // 
            txtProjectDir.Dock = DockStyle.Fill;
            txtProjectDir.Location = new Point(105, 31);
            txtProjectDir.Name = "txtProjectDir";
            txtProjectDir.Size = new Size(327, 23);
            txtProjectDir.TabIndex = 1;
            txtProjectDir.TextChanged += saveStatus;
            // 
            // txtProjectName
            // 
            txtProjectName.Dock = DockStyle.Fill;
            txtProjectName.Location = new Point(105, 3);
            txtProjectName.Name = "txtProjectName";
            txtProjectName.Size = new Size(327, 23);
            txtProjectName.TabIndex = 0;
            txtProjectName.TextChanged += saveStatus;
            // 
            // btnProjectDir
            // 
            btnProjectDir.Dock = DockStyle.Fill;
            btnProjectDir.Location = new Point(438, 31);
            btnProjectDir.Name = "btnProjectDir";
            btnProjectDir.Size = new Size(72, 22);
            btnProjectDir.TabIndex = 2;
            btnProjectDir.Text = "...";
            btnProjectDir.UseVisualStyleBackColor = true;
            btnProjectDir.Click += btnProjectDir_Click;
            // 
            // txtProjectDescription
            // 
            txtProjectDescription.Dock = DockStyle.Fill;
            txtProjectDescription.Location = new Point(105, 87);
            txtProjectDescription.Multiline = true;
            txtProjectDescription.Name = "txtProjectDescription";
            txtProjectDescription.Size = new Size(327, 199);
            txtProjectDescription.TabIndex = 4;
            txtProjectDescription.TextChanged += saveStatus;
            // 
            // lblProjectDescription
            // 
            lblProjectDescription.AutoSize = true;
            lblProjectDescription.Dock = DockStyle.Fill;
            lblProjectDescription.Location = new Point(3, 84);
            lblProjectDescription.Name = "lblProjectDescription";
            lblProjectDescription.Size = new Size(96, 205);
            lblProjectDescription.TabIndex = 7;
            lblProjectDescription.Text = "Project Description";
            // 
            // tableOrganizer
            // 
            tableOrganizer.ColumnCount = 3;
            tableOrganizer.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            tableOrganizer.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 65F));
            tableOrganizer.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 15F));
            tableOrganizer.Controls.Add(lblProjectDir, 0, 1);
            tableOrganizer.Controls.Add(txtProjectDescription, 1, 3);
            tableOrganizer.Controls.Add(txtProjectDir, 1, 1);
            tableOrganizer.Controls.Add(lblProjectDescription, 0, 3);
            tableOrganizer.Controls.Add(btnProjectDir, 2, 1);
            tableOrganizer.Controls.Add(txtProjectEPSG, 1, 2);
            tableOrganizer.Controls.Add(lblProjectEPSG, 0, 2);
            tableOrganizer.Controls.Add(txtProjectName, 1, 0);
            tableOrganizer.Controls.Add(lblProjectName, 0, 0);
            tableOrganizer.Dock = DockStyle.Fill;
            tableOrganizer.Location = new Point(0, 24);
            tableOrganizer.Name = "tableOrganizer";
            tableOrganizer.RowCount = 4;
            tableOrganizer.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableOrganizer.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableOrganizer.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
            tableOrganizer.RowStyles.Add(new RowStyle(SizeType.Percent, 70F));
            tableOrganizer.Size = new Size(513, 289);
            tableOrganizer.TabIndex = 9;
            // 
            // menuMain
            // 
            menuMain.Items.AddRange(new ToolStripItem[] { menuFile });
            menuMain.Location = new Point(0, 0);
            menuMain.Name = "menuMain";
            menuMain.Size = new Size(513, 24);
            menuMain.TabIndex = 10;
            menuMain.Text = "menuStrip1";
            // 
            // menuFile
            // 
            menuFile.DropDownItems.AddRange(new ToolStripItem[] { menuSave });
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
            // PropertiesPage
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(513, 313);
            Controls.Add(tableOrganizer);
            Controls.Add(menuMain);
            MainMenuStrip = menuMain;
            Name = "PropertiesPage";
            Text = "Project Properties";
            FormClosing += PropertiesPage_FormClosing;
            Load += PropertiesPage_Load;
            tableOrganizer.ResumeLayout(false);
            tableOrganizer.PerformLayout();
            menuMain.ResumeLayout(false);
            menuMain.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private TextBox txtProjectEPSG;
        private Label lblProjectEPSG;
        private Label lblProjectDir;
        private Label lblProjectName;
        private TextBox txtProjectDir;
        private TextBox txtProjectName;
        private Button btnProjectDir;
        private TextBox txtProjectDescription;
        private Label lblProjectDescription;
        private TableLayoutPanel tableOrganizer;
        private MenuStrip menuMain;
        private ToolStripMenuItem menuFile;
        private ToolStripMenuItem menuSave;
    }
}