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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(PropertiesPage));
            txtProjectEPSG = new TextBox();
            lblProjectEPSG = new Label();
            txtProjectDescription = new TextBox();
            lblProjectDescription = new Label();
            tableOrganizer = new TableLayoutPanel();
            menuMain = new MenuStrip();
            menuFile = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
            tableOrganizer.SuspendLayout();
            menuMain.SuspendLayout();
            SuspendLayout();
            // 
            // txtProjectEPSG
            // 
            txtProjectEPSG.Dock = DockStyle.Fill;
            txtProjectEPSG.Location = new Point(156, 3);
            txtProjectEPSG.Name = "txtProjectEPSG";
            txtProjectEPSG.Size = new Size(354, 23);
            txtProjectEPSG.TabIndex = 3;
            txtProjectEPSG.TextChanged += inputChanged;
            // 
            // lblProjectEPSG
            // 
            lblProjectEPSG.AutoSize = true;
            lblProjectEPSG.Dock = DockStyle.Fill;
            lblProjectEPSG.Location = new Point(3, 0);
            lblProjectEPSG.Name = "lblProjectEPSG";
            lblProjectEPSG.Size = new Size(147, 30);
            lblProjectEPSG.TabIndex = 1;
            lblProjectEPSG.Text = "EPSG";
            // 
            // txtProjectDescription
            // 
            txtProjectDescription.Dock = DockStyle.Fill;
            txtProjectDescription.Location = new Point(156, 33);
            txtProjectDescription.Multiline = true;
            txtProjectDescription.Name = "txtProjectDescription";
            txtProjectDescription.Size = new Size(354, 253);
            txtProjectDescription.TabIndex = 4;
            txtProjectDescription.TextChanged += inputChanged;
            // 
            // lblProjectDescription
            // 
            lblProjectDescription.AutoSize = true;
            lblProjectDescription.Dock = DockStyle.Fill;
            lblProjectDescription.Location = new Point(3, 30);
            lblProjectDescription.Name = "lblProjectDescription";
            lblProjectDescription.Size = new Size(147, 259);
            lblProjectDescription.TabIndex = 7;
            lblProjectDescription.Text = "Project Description";
            // 
            // tableOrganizer
            // 
            tableOrganizer.ColumnCount = 2;
            tableOrganizer.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            tableOrganizer.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70F));
            tableOrganizer.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 20F));
            tableOrganizer.Controls.Add(txtProjectDescription, 1, 1);
            tableOrganizer.Controls.Add(lblProjectDescription, 0, 1);
            tableOrganizer.Controls.Add(txtProjectEPSG, 1, 0);
            tableOrganizer.Controls.Add(lblProjectEPSG, 0, 0);
            tableOrganizer.Dock = DockStyle.Fill;
            tableOrganizer.Location = new Point(0, 24);
            tableOrganizer.Name = "tableOrganizer";
            tableOrganizer.RowCount = 2;
            tableOrganizer.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableOrganizer.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
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
            menuFile.DropDownItems.AddRange(new ToolStripItem[] { menuSave, menuExit });
            menuFile.Name = "menuFile";
            menuFile.Size = new Size(37, 20);
            menuFile.Text = "File";
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
            // PropertiesPage
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(513, 313);
            Controls.Add(tableOrganizer);
            Controls.Add(menuMain);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MainMenuStrip = menuMain;
            Name = "PropertiesPage";
            Text = "Project Properties";
            FormClosing += PropertiesPage_FormClosing;
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
        private TextBox txtProjectDescription;
        private Label lblProjectDescription;
        private TableLayoutPanel tableOrganizer;
        private MenuStrip menuMain;
        private ToolStripMenuItem menuFile;
        private ToolStripMenuItem menuSave;
        private ToolStripMenuItem menuExit;
    }
}