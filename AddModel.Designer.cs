namespace CSEMMPGUI_v1
{
    partial class AddModel
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
            menuSave = new ToolStripMenuItem();
            btnLoad = new Button();
            lblFilePath = new Label();
            txtFilePath = new TextBox();
            tableLayoutPanel1 = new TableLayoutPanel();
            tableFileInfo = new TableLayoutPanel();
            lblStartingTime = new Label();
            lblNumberOfNodes = new Label();
            lblNumberOfElements = new Label();
            lblGeometryType = new Label();
            lbl5 = new Label();
            lbl4 = new Label();
            lbl3 = new Label();
            lbl2 = new Label();
            lbl1 = new Label();
            menuStrip1.SuspendLayout();
            tableLayoutPanel1.SuspendLayout();
            tableFileInfo.SuspendLayout();
            SuspendLayout();
            // 
            // menuStrip1
            // 
            menuStrip1.Items.AddRange(new ToolStripItem[] { menuSave });
            menuStrip1.Location = new Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new Size(800, 24);
            menuStrip1.TabIndex = 0;
            menuStrip1.Text = "menuStrip1";
            // 
            // menuSave
            // 
            menuSave.Name = "menuSave";
            menuSave.Size = new Size(43, 20);
            menuSave.Text = "Save";
            menuSave.Click += menuSave_Click;
            // 
            // btnLoad
            // 
            btnLoad.Dock = DockStyle.Fill;
            btnLoad.Location = new Point(706, 3);
            btnLoad.Name = "btnLoad";
            btnLoad.Size = new Size(91, 23);
            btnLoad.TabIndex = 1;
            btnLoad.Text = "...";
            btnLoad.UseVisualStyleBackColor = true;
            btnLoad.Click += btnLoad_Click;
            // 
            // lblFilePath
            // 
            lblFilePath.AutoSize = true;
            lblFilePath.Dock = DockStyle.Fill;
            lblFilePath.Location = new Point(3, 0);
            lblFilePath.Name = "lblFilePath";
            lblFilePath.Size = new Size(66, 29);
            lblFilePath.TabIndex = 2;
            lblFilePath.Text = "File";
            lblFilePath.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // txtFilePath
            // 
            txtFilePath.Dock = DockStyle.Fill;
            txtFilePath.Location = new Point(75, 3);
            txtFilePath.Name = "txtFilePath";
            txtFilePath.Size = new Size(625, 23);
            txtFilePath.TabIndex = 3;
            txtFilePath.Leave += txtFilePath_Leave;
            // 
            // tableLayoutPanel1
            // 
            tableLayoutPanel1.ColumnCount = 3;
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 10.2941179F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 89.70588F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 96F));
            tableLayoutPanel1.Controls.Add(lblFilePath, 0, 0);
            tableLayoutPanel1.Controls.Add(btnLoad, 2, 0);
            tableLayoutPanel1.Controls.Add(txtFilePath, 1, 0);
            tableLayoutPanel1.Controls.Add(tableFileInfo, 1, 1);
            tableLayoutPanel1.Dock = DockStyle.Fill;
            tableLayoutPanel1.Location = new Point(0, 24);
            tableLayoutPanel1.Name = "tableLayoutPanel1";
            tableLayoutPanel1.RowCount = 3;
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 7.160494F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 92.83951F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Absolute, 20F));
            tableLayoutPanel1.Size = new Size(800, 426);
            tableLayoutPanel1.TabIndex = 4;
            // 
            // tableFileInfo
            // 
            tableFileInfo.ColumnCount = 2;
            tableFileInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableFileInfo.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableFileInfo.Controls.Add(lblStartingTime, 1, 4);
            tableFileInfo.Controls.Add(lblNumberOfNodes, 1, 3);
            tableFileInfo.Controls.Add(lblNumberOfElements, 1, 2);
            tableFileInfo.Controls.Add(lblGeometryType, 1, 1);
            tableFileInfo.Controls.Add(lbl5, 0, 4);
            tableFileInfo.Controls.Add(lbl4, 0, 3);
            tableFileInfo.Controls.Add(lbl3, 0, 2);
            tableFileInfo.Controls.Add(lbl2, 0, 1);
            tableFileInfo.Controls.Add(lbl1, 0, 0);
            tableFileInfo.Dock = DockStyle.Fill;
            tableFileInfo.Location = new Point(75, 32);
            tableFileInfo.Name = "tableFileInfo";
            tableFileInfo.RowCount = 6;
            tableFileInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 7F));
            tableFileInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 7F));
            tableFileInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 7F));
            tableFileInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 7F));
            tableFileInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 7F));
            tableFileInfo.RowStyles.Add(new RowStyle(SizeType.Percent, 65F));
            tableFileInfo.Size = new Size(625, 370);
            tableFileInfo.TabIndex = 4;
            tableFileInfo.Visible = false;
            // 
            // lblStartingTime
            // 
            lblStartingTime.AutoSize = true;
            lblStartingTime.Dock = DockStyle.Fill;
            lblStartingTime.Location = new Point(315, 100);
            lblStartingTime.Name = "lblStartingTime";
            lblStartingTime.Size = new Size(307, 25);
            lblStartingTime.TabIndex = 15;
            lblStartingTime.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblNumberOfNodes
            // 
            lblNumberOfNodes.AutoSize = true;
            lblNumberOfNodes.Dock = DockStyle.Fill;
            lblNumberOfNodes.Location = new Point(315, 75);
            lblNumberOfNodes.Name = "lblNumberOfNodes";
            lblNumberOfNodes.Size = new Size(307, 25);
            lblNumberOfNodes.TabIndex = 14;
            lblNumberOfNodes.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblNumberOfElements
            // 
            lblNumberOfElements.AutoSize = true;
            lblNumberOfElements.Dock = DockStyle.Fill;
            lblNumberOfElements.Location = new Point(315, 50);
            lblNumberOfElements.Name = "lblNumberOfElements";
            lblNumberOfElements.Size = new Size(307, 25);
            lblNumberOfElements.TabIndex = 13;
            lblNumberOfElements.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lblGeometryType
            // 
            lblGeometryType.AutoSize = true;
            lblGeometryType.Dock = DockStyle.Fill;
            lblGeometryType.Location = new Point(315, 25);
            lblGeometryType.Name = "lblGeometryType";
            lblGeometryType.Size = new Size(307, 25);
            lblGeometryType.TabIndex = 12;
            lblGeometryType.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lbl5
            // 
            lbl5.AutoSize = true;
            lbl5.Dock = DockStyle.Fill;
            lbl5.Location = new Point(3, 100);
            lbl5.Name = "lbl5";
            lbl5.Size = new Size(306, 25);
            lbl5.TabIndex = 10;
            lbl5.Text = "Starting Time";
            lbl5.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lbl4
            // 
            lbl4.AutoSize = true;
            lbl4.Dock = DockStyle.Fill;
            lbl4.Location = new Point(3, 75);
            lbl4.Name = "lbl4";
            lbl4.Size = new Size(306, 25);
            lbl4.TabIndex = 8;
            lbl4.Text = "Number of Nodes";
            lbl4.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lbl3
            // 
            lbl3.AutoSize = true;
            lbl3.Dock = DockStyle.Fill;
            lbl3.Location = new Point(3, 50);
            lbl3.Name = "lbl3";
            lbl3.Size = new Size(306, 25);
            lbl3.TabIndex = 4;
            lbl3.Text = "Number of Elements";
            lbl3.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lbl2
            // 
            lbl2.AutoSize = true;
            lbl2.Dock = DockStyle.Fill;
            lbl2.Location = new Point(3, 25);
            lbl2.Name = "lbl2";
            lbl2.Size = new Size(306, 25);
            lbl2.TabIndex = 2;
            lbl2.Text = "File Geometry Type";
            lbl2.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // lbl1
            // 
            lbl1.AutoSize = true;
            lbl1.Dock = DockStyle.Fill;
            lbl1.Location = new Point(3, 0);
            lbl1.Name = "lbl1";
            lbl1.Size = new Size(306, 25);
            lbl1.TabIndex = 0;
            lbl1.Text = "File Information";
            lbl1.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // AddModel
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(tableLayoutPanel1);
            Controls.Add(menuStrip1);
            MainMenuStrip = menuStrip1;
            Name = "AddModel";
            Text = "AddModel";
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            tableLayoutPanel1.ResumeLayout(false);
            tableLayoutPanel1.PerformLayout();
            tableFileInfo.ResumeLayout(false);
            tableFileInfo.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menuStrip1;
        private ToolStripMenuItem menuSave;
        private Button btnLoad;
        private Label lblFilePath;
        private TextBox txtFilePath;
        private TableLayoutPanel tableLayoutPanel1;
        private TableLayoutPanel tableFileInfo;
        private Label label5;
        private Label label4;
        private Label label3;
        private Label lblGeometryType;
        private Label label1;
        private Label lblStartingTime;
        private Label lblNumberOfNodes;
        private Label lblNumberOfElements;
        private Label lbl5;
        private Label lbl4;
        private Label lbl3;
        private Label lbl2;
        private Label lbl1;
    }
}