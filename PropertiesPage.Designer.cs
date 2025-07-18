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
            label1 = new Label();
            label2 = new Label();
            label3 = new Label();
            txtProjectDir = new TextBox();
            txtProjectName = new TextBox();
            button1 = new Button();
            textBox1 = new TextBox();
            label4 = new Label();
            SuspendLayout();
            // 
            // txtProjectEPSG
            // 
            txtProjectEPSG.Location = new Point(150, 84);
            txtProjectEPSG.Name = "txtProjectEPSG";
            txtProjectEPSG.Size = new Size(297, 23);
            txtProjectEPSG.TabIndex = 0;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(33, 87);
            label1.Name = "label1";
            label1.Size = new Size(34, 15);
            label1.TabIndex = 1;
            label1.Text = "EPSG";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(33, 30);
            label2.Name = "label2";
            label2.Size = new Size(95, 15);
            label2.TabIndex = 2;
            label2.Text = "Project Directory";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(33, 57);
            label3.Name = "label3";
            label3.Size = new Size(79, 15);
            label3.TabIndex = 3;
            label3.Text = "Project Name";
            // 
            // txtProjectDir
            // 
            txtProjectDir.Location = new Point(150, 31);
            txtProjectDir.Name = "txtProjectDir";
            txtProjectDir.Size = new Size(297, 23);
            txtProjectDir.TabIndex = 4;
            // 
            // txtProjectName
            // 
            txtProjectName.Location = new Point(150, 57);
            txtProjectName.Name = "txtProjectName";
            txtProjectName.Size = new Size(297, 23);
            txtProjectName.TabIndex = 5;
            // 
            // button1
            // 
            button1.Location = new Point(453, 31);
            button1.Name = "button1";
            button1.Size = new Size(75, 23);
            button1.TabIndex = 6;
            button1.Text = "...";
            button1.UseVisualStyleBackColor = true;
            // 
            // textBox1
            // 
            textBox1.Location = new Point(150, 122);
            textBox1.Multiline = true;
            textBox1.Name = "textBox1";
            textBox1.Size = new Size(297, 210);
            textBox1.TabIndex = 8;
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new Point(33, 125);
            label4.Name = "label4";
            label4.Size = new Size(107, 15);
            label4.TabIndex = 7;
            label4.Text = "Project Description";
            // 
            // PropertiesPage
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(textBox1);
            Controls.Add(label4);
            Controls.Add(button1);
            Controls.Add(txtProjectName);
            Controls.Add(txtProjectDir);
            Controls.Add(label3);
            Controls.Add(label2);
            Controls.Add(label1);
            Controls.Add(txtProjectEPSG);
            Name = "PropertiesPage";
            Text = "Project Properties";
            FormClosed += PropertiesPage_FormClosed;
            Load += PropertiesPage_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private TextBox txtProjectEPSG;
        private Label label1;
        private Label label2;
        private Label label3;
        private TextBox txtProjectDir;
        private TextBox txtProjectName;
        private Button button1;
        private TextBox textBox1;
        private Label label4;
    }
}