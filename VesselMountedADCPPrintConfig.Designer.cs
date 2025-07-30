namespace CSEMMPGUI_v1
{
    partial class VesselMountedADCPPrintConfig
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
            vScrollBar1 = new VScrollBar();
            hScrollBar1 = new HScrollBar();
            txtConfig = new TextBox();
            SuspendLayout();
            // 
            // vScrollBar1
            // 
            vScrollBar1.Dock = DockStyle.Right;
            vScrollBar1.Location = new Point(682, 0);
            vScrollBar1.Name = "vScrollBar1";
            vScrollBar1.Size = new Size(30, 427);
            vScrollBar1.TabIndex = 0;
            // 
            // hScrollBar1
            // 
            hScrollBar1.Dock = DockStyle.Bottom;
            hScrollBar1.Location = new Point(0, 410);
            hScrollBar1.Name = "hScrollBar1";
            hScrollBar1.Size = new Size(682, 17);
            hScrollBar1.TabIndex = 1;
            // 
            // txtConfig
            // 
            txtConfig.Dock = DockStyle.Fill;
            txtConfig.Location = new Point(0, 0);
            txtConfig.Multiline = true;
            txtConfig.Name = "txtConfig";
            txtConfig.Size = new Size(682, 410);
            txtConfig.TabIndex = 2;
            // 
            // VesselMountedADCPPrintConfig
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(712, 427);
            Controls.Add(txtConfig);
            Controls.Add(hScrollBar1);
            Controls.Add(vScrollBar1);
            Name = "VesselMountedADCPPrintConfig";
            Text = "Vessel Mounted ADCP Config";
            Load += VesselMountedADCPPrintConfig_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private VScrollBar vScrollBar1;
        private HScrollBar hScrollBar1;
        private TextBox txtConfig;
    }
}