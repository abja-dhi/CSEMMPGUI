namespace CSEMMPGUI_v1
{
    partial class AddSurvey
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
            saveToolStripMenuItem = new ToolStripMenuItem();
            openToolStripMenuItem = new ToolStripMenuItem();
            saveToolStripMenuItem1 = new ToolStripMenuItem();
            addDataToolStripMenuItem = new ToolStripMenuItem();
            aDCPToolStripMenuItem = new ToolStripMenuItem();
            vesselMountedToolStripMenuItem = new ToolStripMenuItem();
            seabedLanderToolStripMenuItem = new ToolStripMenuItem();
            oBSToolStripMenuItem = new ToolStripMenuItem();
            waterSampleToolStripMenuItem = new ToolStripMenuItem();
            textBox1 = new TextBox();
            label1 = new Label();
            panel1 = new Panel();
            treeView1 = new TreeView();
            utilitiesToolStripMenuItem = new ToolStripMenuItem();
            viseaExterndatToCSVToolStripMenuItem = new ToolStripMenuItem();
            verticalProfileToolStripMenuItem = new ToolStripMenuItem();
            transectToolStripMenuItem = new ToolStripMenuItem();
            menuStrip1.SuspendLayout();
            panel1.SuspendLayout();
            SuspendLayout();
            // 
            // menuStrip1
            // 
            menuStrip1.Items.AddRange(new ToolStripItem[] { saveToolStripMenuItem, addDataToolStripMenuItem, utilitiesToolStripMenuItem });
            menuStrip1.Location = new Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new Size(884, 24);
            menuStrip1.TabIndex = 0;
            menuStrip1.Text = "menuStrip1";
            // 
            // saveToolStripMenuItem
            // 
            saveToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { openToolStripMenuItem, saveToolStripMenuItem1 });
            saveToolStripMenuItem.Name = "saveToolStripMenuItem";
            saveToolStripMenuItem.Size = new Size(37, 20);
            saveToolStripMenuItem.Text = "File";
            // 
            // openToolStripMenuItem
            // 
            openToolStripMenuItem.Name = "openToolStripMenuItem";
            openToolStripMenuItem.Size = new Size(112, 22);
            openToolStripMenuItem.Text = "Open...";
            // 
            // saveToolStripMenuItem1
            // 
            saveToolStripMenuItem1.Name = "saveToolStripMenuItem1";
            saveToolStripMenuItem1.Size = new Size(112, 22);
            saveToolStripMenuItem1.Text = "Save...";
            // 
            // addDataToolStripMenuItem
            // 
            addDataToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { aDCPToolStripMenuItem, oBSToolStripMenuItem, waterSampleToolStripMenuItem });
            addDataToolStripMenuItem.Name = "addDataToolStripMenuItem";
            addDataToolStripMenuItem.Size = new Size(68, 20);
            addDataToolStripMenuItem.Text = "Add Data";
            // 
            // aDCPToolStripMenuItem
            // 
            aDCPToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { vesselMountedToolStripMenuItem, seabedLanderToolStripMenuItem });
            aDCPToolStripMenuItem.Name = "aDCPToolStripMenuItem";
            aDCPToolStripMenuItem.Size = new Size(180, 22);
            aDCPToolStripMenuItem.Text = "ADCP";
            // 
            // vesselMountedToolStripMenuItem
            // 
            vesselMountedToolStripMenuItem.Name = "vesselMountedToolStripMenuItem";
            vesselMountedToolStripMenuItem.Size = new Size(180, 22);
            vesselMountedToolStripMenuItem.Text = "Vessel Mounted";
            // 
            // seabedLanderToolStripMenuItem
            // 
            seabedLanderToolStripMenuItem.Name = "seabedLanderToolStripMenuItem";
            seabedLanderToolStripMenuItem.Size = new Size(180, 22);
            seabedLanderToolStripMenuItem.Text = "Seabed Lander";
            seabedLanderToolStripMenuItem.Click += seabedLanderToolStripMenuItem_Click;
            // 
            // oBSToolStripMenuItem
            // 
            oBSToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { verticalProfileToolStripMenuItem, transectToolStripMenuItem });
            oBSToolStripMenuItem.Name = "oBSToolStripMenuItem";
            oBSToolStripMenuItem.Size = new Size(180, 22);
            oBSToolStripMenuItem.Text = "OBS";
            // 
            // waterSampleToolStripMenuItem
            // 
            waterSampleToolStripMenuItem.Name = "waterSampleToolStripMenuItem";
            waterSampleToolStripMenuItem.Size = new Size(180, 22);
            waterSampleToolStripMenuItem.Text = "Water Sample";
            // 
            // textBox1
            // 
            textBox1.Location = new Point(514, 112);
            textBox1.Name = "textBox1";
            textBox1.Size = new Size(100, 23);
            textBox1.TabIndex = 1;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(514, 74);
            label1.Name = "label1";
            label1.Size = new Size(77, 15);
            label1.TabIndex = 2;
            label1.Text = "Survey Name";
            // 
            // panel1
            // 
            panel1.Controls.Add(treeView1);
            panel1.Dock = DockStyle.Left;
            panel1.Location = new Point(0, 24);
            panel1.Name = "panel1";
            panel1.Size = new Size(200, 437);
            panel1.TabIndex = 4;
            // 
            // treeView1
            // 
            treeView1.Dock = DockStyle.Fill;
            treeView1.Location = new Point(0, 0);
            treeView1.Name = "treeView1";
            treeView1.Size = new Size(200, 437);
            treeView1.TabIndex = 0;
            // 
            // utilitiesToolStripMenuItem
            // 
            utilitiesToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { viseaExterndatToCSVToolStripMenuItem });
            utilitiesToolStripMenuItem.Name = "utilitiesToolStripMenuItem";
            utilitiesToolStripMenuItem.Size = new Size(58, 20);
            utilitiesToolStripMenuItem.Text = "Utilities";
            // 
            // viseaExterndatToCSVToolStripMenuItem
            // 
            viseaExterndatToCSVToolStripMenuItem.Name = "viseaExterndatToCSVToolStripMenuItem";
            viseaExterndatToCSVToolStripMenuItem.Size = new Size(196, 22);
            viseaExterndatToCSVToolStripMenuItem.Text = "ViSea Extern.dat to CSV";
            // 
            // verticalProfileToolStripMenuItem
            // 
            verticalProfileToolStripMenuItem.Name = "verticalProfileToolStripMenuItem";
            verticalProfileToolStripMenuItem.Size = new Size(180, 22);
            verticalProfileToolStripMenuItem.Text = "Vertical Profile";
            // 
            // transectToolStripMenuItem
            // 
            transectToolStripMenuItem.Name = "transectToolStripMenuItem";
            transectToolStripMenuItem.Size = new Size(180, 22);
            transectToolStripMenuItem.Text = "Transect";
            // 
            // AddSurvey
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(884, 461);
            Controls.Add(panel1);
            Controls.Add(label1);
            Controls.Add(textBox1);
            Controls.Add(menuStrip1);
            MainMenuStrip = menuStrip1;
            Name = "AddSurvey";
            Text = "AddSurvey";
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            panel1.ResumeLayout(false);
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menuStrip1;
        private ToolStripMenuItem saveToolStripMenuItem;
        private ToolStripMenuItem addDataToolStripMenuItem;
        private ToolStripMenuItem aDCPToolStripMenuItem;
        private ToolStripMenuItem vesselMountedToolStripMenuItem;
        private ToolStripMenuItem seabedLanderToolStripMenuItem;
        private ToolStripMenuItem oBSToolStripMenuItem;
        private ToolStripMenuItem waterSampleToolStripMenuItem;
        private TextBox textBox1;
        private Label label1;
        private ToolStripMenuItem openToolStripMenuItem;
        private ToolStripMenuItem saveToolStripMenuItem1;
        private Panel panel1;
        private TreeView treeView1;
        private ToolStripMenuItem utilitiesToolStripMenuItem;
        private ToolStripMenuItem viseaExterndatToCSVToolStripMenuItem;
        private ToolStripMenuItem verticalProfileToolStripMenuItem;
        private ToolStripMenuItem transectToolStripMenuItem;
    }
}