namespace CSEMMPGUI_v1
{
    partial class EditWaterSample
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
            DataGridViewCellStyle dataGridViewCellStyle1 = new DataGridViewCellStyle();
            menu = new MenuStrip();
            menuFile = new ToolStripMenuItem();
            menuSave = new ToolStripMenuItem();
            menuExit = new ToolStripMenuItem();
            utilitiesToolStripMenuItem = new ToolStripMenuItem();
            exportToCSVToolStripMenuItem = new ToolStripMenuItem();
            gridData = new DataGridView();
            colSampleName = new DataGridViewTextBoxColumn();
            colDateTime = new DataGridViewTextBoxColumn();
            colX = new DataGridViewTextBoxColumn();
            colY = new DataGridViewTextBoxColumn();
            colDepth = new DataGridViewTextBoxColumn();
            colSSC = new DataGridViewTextBoxColumn();
            colNotes = new DataGridViewTextBoxColumn();
            tableMain = new TableLayoutPanel();
            lblName = new Label();
            txtName = new TextBox();
            menu.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)gridData).BeginInit();
            tableMain.SuspendLayout();
            SuspendLayout();
            // 
            // menu
            // 
            menu.Items.AddRange(new ToolStripItem[] { menuFile, utilitiesToolStripMenuItem });
            menu.Location = new Point(0, 0);
            menu.Name = "menu";
            menu.Size = new Size(800, 24);
            menu.TabIndex = 0;
            menu.Text = "menuStrip1";
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
            // utilitiesToolStripMenuItem
            // 
            utilitiesToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { exportToCSVToolStripMenuItem });
            utilitiesToolStripMenuItem.Name = "utilitiesToolStripMenuItem";
            utilitiesToolStripMenuItem.Size = new Size(58, 20);
            utilitiesToolStripMenuItem.Text = "Utilities";
            // 
            // exportToCSVToolStripMenuItem
            // 
            exportToCSVToolStripMenuItem.Name = "exportToCSVToolStripMenuItem";
            exportToCSVToolStripMenuItem.Size = new Size(146, 22);
            exportToCSVToolStripMenuItem.Text = "Export to CSV";
            // 
            // gridData
            // 
            dataGridViewCellStyle1.WrapMode = DataGridViewTriState.True;
            gridData.AlternatingRowsDefaultCellStyle = dataGridViewCellStyle1;
            gridData.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            gridData.Columns.AddRange(new DataGridViewColumn[] { colSampleName, colDateTime, colX, colY, colDepth, colSSC, colNotes });
            tableMain.SetColumnSpan(gridData, 2);
            gridData.Dock = DockStyle.Fill;
            gridData.Location = new Point(3, 28);
            gridData.Name = "gridData";
            gridData.Size = new Size(794, 395);
            gridData.TabIndex = 2;
            gridData.CellValueChanged += gridData_CellValueChanged;
            gridData.EditingControlShowing += gridData_EditingControlShowing;
            // 
            // colSampleName
            // 
            colSampleName.HeaderText = "Sample Name";
            colSampleName.Name = "colSampleName";
            colSampleName.Width = 150;
            // 
            // colDateTime
            // 
            colDateTime.HeaderText = "DateTime";
            colDateTime.Name = "colDateTime";
            colDateTime.Width = 150;
            // 
            // colX
            // 
            colX.HeaderText = "X";
            colX.Name = "colX";
            colX.Width = 70;
            // 
            // colY
            // 
            colY.HeaderText = "Y";
            colY.Name = "colY";
            colY.Width = 70;
            // 
            // colDepth
            // 
            colDepth.HeaderText = "Depth";
            colDepth.Name = "colDepth";
            colDepth.Width = 70;
            // 
            // colSSC
            // 
            colSSC.HeaderText = "SSC (mg/L)";
            colSSC.Name = "colSSC";
            colSSC.Width = 70;
            // 
            // colNotes
            // 
            colNotes.HeaderText = "Notes";
            colNotes.Name = "colNotes";
            colNotes.Width = 300;
            // 
            // tableMain
            // 
            tableMain.ColumnCount = 2;
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            tableMain.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 80F));
            tableMain.Controls.Add(gridData, 0, 1);
            tableMain.Controls.Add(lblName, 0, 0);
            tableMain.Controls.Add(txtName, 1, 0);
            tableMain.Dock = DockStyle.Fill;
            tableMain.Location = new Point(0, 24);
            tableMain.Name = "tableMain";
            tableMain.RowCount = 2;
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 6F));
            tableMain.RowStyles.Add(new RowStyle(SizeType.Percent, 94F));
            tableMain.Size = new Size(800, 426);
            tableMain.TabIndex = 3;
            // 
            // lblName
            // 
            lblName.AutoSize = true;
            lblName.Dock = DockStyle.Fill;
            lblName.Location = new Point(3, 0);
            lblName.Name = "lblName";
            lblName.Size = new Size(154, 25);
            lblName.TabIndex = 3;
            lblName.Text = "Water Sample Name";
            lblName.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtName
            // 
            txtName.Dock = DockStyle.Fill;
            txtName.Location = new Point(163, 3);
            txtName.Name = "txtName";
            txtName.Size = new Size(634, 23);
            txtName.TabIndex = 4;
            txtName.TextChanged += txtName_TextChanged;
            // 
            // EditWaterSample
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(tableMain);
            Controls.Add(menu);
            MainMenuStrip = menu;
            Name = "EditWaterSample";
            Text = "WaterSample";
            FormClosing += AddWaterSample_FormClosing;
            menu.ResumeLayout(false);
            menu.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)gridData).EndInit();
            tableMain.ResumeLayout(false);
            tableMain.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private MenuStrip menu;
        private ToolStripMenuItem menuFile;
        private ToolStripMenuItem menuSave;
        private DataGridView gridData;
        private ToolStripMenuItem menuExit;
        private DataGridViewTextBoxColumn colSampleName;
        private DataGridViewTextBoxColumn colDateTime;
        private DataGridViewTextBoxColumn colX;
        private DataGridViewTextBoxColumn colY;
        private DataGridViewTextBoxColumn colDepth;
        private DataGridViewTextBoxColumn colSSC;
        private DataGridViewTextBoxColumn colNotes;
        private TableLayoutPanel tableMain;
        private Label lblName;
        private TextBox txtName;
        private ToolStripMenuItem utilitiesToolStripMenuItem;
        private ToolStripMenuItem exportToCSVToolStripMenuItem;
    }
}