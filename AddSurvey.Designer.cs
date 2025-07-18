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
            addDataToolStripMenuItem = new ToolStripMenuItem();
            aDCPToolStripMenuItem = new ToolStripMenuItem();
            vesselMountedToolStripMenuItem = new ToolStripMenuItem();
            seabedLanderToolStripMenuItem = new ToolStripMenuItem();
            oBSToolStripMenuItem = new ToolStripMenuItem();
            waterSampleToolStripMenuItem = new ToolStripMenuItem();
            menuStrip1.SuspendLayout();
            SuspendLayout();
            // 
            // menuStrip1
            // 
            menuStrip1.Items.AddRange(new ToolStripItem[] { saveToolStripMenuItem, addDataToolStripMenuItem });
            menuStrip1.Location = new Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new Size(884, 24);
            menuStrip1.TabIndex = 0;
            menuStrip1.Text = "menuStrip1";
            // 
            // saveToolStripMenuItem
            // 
            saveToolStripMenuItem.Name = "saveToolStripMenuItem";
            saveToolStripMenuItem.Size = new Size(43, 20);
            saveToolStripMenuItem.Text = "Save";
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
            aDCPToolStripMenuItem.Size = new Size(147, 22);
            aDCPToolStripMenuItem.Text = "ADCP";
            // 
            // vesselMountedToolStripMenuItem
            // 
            vesselMountedToolStripMenuItem.Name = "vesselMountedToolStripMenuItem";
            vesselMountedToolStripMenuItem.Size = new Size(157, 22);
            vesselMountedToolStripMenuItem.Text = "Vessel Mounted";
            // 
            // seabedLanderToolStripMenuItem
            // 
            seabedLanderToolStripMenuItem.Name = "seabedLanderToolStripMenuItem";
            seabedLanderToolStripMenuItem.Size = new Size(157, 22);
            seabedLanderToolStripMenuItem.Text = "Seabed Lander";
            seabedLanderToolStripMenuItem.Click += seabedLanderToolStripMenuItem_Click;
            // 
            // oBSToolStripMenuItem
            // 
            oBSToolStripMenuItem.Name = "oBSToolStripMenuItem";
            oBSToolStripMenuItem.Size = new Size(147, 22);
            oBSToolStripMenuItem.Text = "OBS";
            // 
            // waterSampleToolStripMenuItem
            // 
            waterSampleToolStripMenuItem.Name = "waterSampleToolStripMenuItem";
            waterSampleToolStripMenuItem.Size = new Size(147, 22);
            waterSampleToolStripMenuItem.Text = "Water Sample";
            // 
            // AddSurvey
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(884, 461);
            Controls.Add(menuStrip1);
            MainMenuStrip = menuStrip1;
            Name = "AddSurvey";
            Text = "AddSurvey";
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
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
    }
}