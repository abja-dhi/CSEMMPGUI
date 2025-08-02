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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(VesselMountedADCPPrintConfig));
            txtConfig = new TextBox();
            SuspendLayout();
            // 
            // txtConfig
            // 
            txtConfig.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            txtConfig.Location = new Point(0, 0);
            txtConfig.Multiline = true;
            txtConfig.Name = "txtConfig";
            txtConfig.ScrollBars = ScrollBars.Both;
            txtConfig.Size = new Size(712, 427);
            txtConfig.TabIndex = 2;
            // 
            // VesselMountedADCPPrintConfig
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(712, 427);
            Controls.Add(txtConfig);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "VesselMountedADCPPrintConfig";
            Text = "Vessel Mounted ADCP Config";
            Load += VesselMountedADCPPrintConfig_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion
        private TextBox txtConfig;
    }
}