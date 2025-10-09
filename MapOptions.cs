using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using NetTopologySuite.IO;

namespace CSEMMPGUI_v1
{
    public partial class MapOptions : Form
    {
        bool isSaved;
        public _ClassConfigurationManager _project = new();
        public XmlElement mapSettings;
        public XmlElement mapSettings2D;
        public XmlElement mapSettings3D;
        public XmlElement mapShapefiles;
        public int currentShapefileIndex;
        public Dictionary<string, XmlElement> shapefileSettings = new Dictionary<string, XmlElement>();
        public List<TextBox> shpPathTextBoxes;
        public List<TextBox> shpTypeTextBoxes;
        public List<Panel> shpColorPanels;
        public List<Button> shpColorButtons;
        public List<TextBox> shpSizeTextBoxes;

        private TableLayoutPanel tableShpPoint;
        private Label lblShpPointPath;
        private TextBox txtShpPointPath;
        private Label lblShpPointType;
        private TextBox txtShpPointType;
        private Label lblShpPointColor;
        private Panel pnlShpPointColor;
        private Button btnShpPointColor;
        private Label lblShpPointMarker;
        private ComboBox comboShpPointMarker;
        private Label lblShpPointMarkerSize;
        private NumericUpDown numShpPointMarkerSize;
        private Label lblShpPointMarkerAlpha;
        private NumericUpDown numShpPointMarkerAlpha;

        private TableLayoutPanel tableShpLine;
        private Label lblShpLinePath;
        private TextBox txtShpLinePath;
        private Label lblShpLineType;
        private TextBox txtShpLineType;
        private Label lblShpLineColor;
        private Panel pnlShpLineColor;
        private Button btnShpLineColor;
        private Label lblShpLineLineWidth;
        private TextBox txtShpLineLineWidth;
        private Label lblShpLineAlpha;
        private NumericUpDown numShpLineAlpha;

        private TableLayoutPanel tableShpPoly;
        private Label lblShpPolyPath;
        private TextBox txtShpPolyPath;
        private Label lblShpPolyType;
        private TextBox txtShpPolyType;
        private Label lblShpPolyEdgeColor;
        private Panel pnlShpPolyEdgeColor;
        private Button btnShpPolyEdgeColor;
        private Label lblShpPolyLineWidth;
        private TextBox txtShpPolyLineWidth;
        private Label lblShpPolyFaceColor;
        private Panel pnlShpPolyFaceColor;
        private Button btnShpPolyFaceColor;
        private Label lblShpPolyAlpha;
        private NumericUpDown numShpPolyAlpha;

        private Label lblShpLabelText;
        private TextBox txtShpLabelText;
        private Label lblShpLabelFontSize;
        private NumericUpDown numShpLabelFontSize;
        private Label lblShpLabelColor;
        private Panel pnlShpLabelColor;
        private Button btnShpLabelColor;
        private Label lblShpLabelHA;
        private ComboBox comboShpLabelHA;
        private Label lblShpLabelVA;
        private ComboBox comboShpLabelVA;
        private Label lblShpLabelOffsetPointsX;
        private TextBox txtShpLabelOffsetPointsX;
        private Label lblShpLabelOffsetPointsY;
        private TextBox txtShpLabelOffsetPointsY;
        private Label lblShpLabelOffsetDataX;
        private TextBox txtShpLabelOffsetDataX;
        private Label lblShpLabelOffsetDataY;
        private TextBox txtShpLabelOffsetDataY;

        private void InitializeShpTab()
        {
            InitializeShpProperties();
            CreateShpPointComponenets();
            CreateShpLineComponents();
            CreateShpPolyComponents();
            CreateShpLabelComponents();
            BuildTableShpPoint();
            BuildTableShpLine();
            BuildTableShpPoly();
        }

        private void InitializeShpProperties()
        {
            tableShpPoint = new TableLayoutPanel();
            lblShpPointPath = new Label();
            txtShpPointPath = new TextBox();
            lblShpPointType = new Label();
            txtShpPointType = new TextBox();
            lblShpPointColor = new Label();
            pnlShpPointColor = new Panel();
            btnShpPointColor = new Button();
            lblShpPointMarker = new Label();
            comboShpPointMarker = new ComboBox();
            lblShpPointMarkerSize = new Label();
            numShpPointMarkerSize = new NumericUpDown();
            lblShpPointMarkerAlpha = new Label();
            numShpPointMarkerAlpha = new NumericUpDown();


            tableShpLine = new TableLayoutPanel();
            lblShpLinePath = new Label();
            txtShpLinePath = new TextBox();
            lblShpLineType = new Label();
            txtShpLineType = new TextBox();
            lblShpLineColor = new Label();
            pnlShpLineColor = new Panel();
            btnShpLineColor = new Button();
            lblShpLineLineWidth = new Label();
            txtShpLineLineWidth = new TextBox();
            lblShpLineAlpha = new Label();
            numShpLineAlpha = new NumericUpDown();

            tableShpPoly = new TableLayoutPanel();
            lblShpPolyPath = new Label();
            txtShpPolyPath = new TextBox();
            lblShpPolyType = new Label();
            txtShpPolyType = new TextBox();
            lblShpPolyEdgeColor = new Label();
            pnlShpPolyEdgeColor = new Panel();
            btnShpPolyEdgeColor = new Button();
            lblShpPolyLineWidth = new Label();
            txtShpPolyLineWidth = new TextBox();
            lblShpPolyFaceColor = new Label();
            pnlShpPolyFaceColor = new Panel();
            btnShpPolyFaceColor = new Button();
            lblShpPolyAlpha = new Label();
            numShpPolyAlpha = new NumericUpDown();

            lblShpLabelText = new Label();
            txtShpLabelText = new TextBox();
            lblShpLabelFontSize = new Label();
            numShpLabelFontSize = new NumericUpDown();
            lblShpLabelColor = new Label();
            pnlShpLabelColor = new Panel();
            btnShpLabelColor = new Button();
            lblShpLabelHA = new Label();
            comboShpLabelHA = new ComboBox();
            lblShpLabelVA = new Label();
            comboShpLabelVA = new ComboBox();
            lblShpLabelOffsetPointsX = new Label();
            txtShpLabelOffsetPointsX = new TextBox();
            lblShpLabelOffsetPointsY = new Label();
            txtShpLabelOffsetPointsY = new TextBox();
            lblShpLabelOffsetDataX = new Label();
            txtShpLabelOffsetDataX = new TextBox();
            lblShpLabelOffsetDataY = new Label();
            txtShpLabelOffsetDataY = new TextBox();

        }

        private void CreateShpPointComponenets()
        {
            // 
            // lblShpPointPath
            // 
            lblShpPointPath.AutoSize = true;
            lblShpPointPath.Dock = DockStyle.Fill;
            lblShpPointPath.Name = "lblShpPointPath";
            lblShpPointPath.TabIndex = 0;
            lblShpPointPath.Text = "Path";
            lblShpPointPath.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtShpPointPath
            // 
            txtShpPointPath.Dock = DockStyle.Fill;
            txtShpPointPath.Enabled = false;
            txtShpPointPath.Name = "txtShpPointPath";
            txtShpPointPath.TabIndex = 2;
            lblShpPointPath.TextChanged += txtShp_TextChanged;
            // 
            // lblShpPointType
            // 
            lblShpPointType.AutoSize = true;
            lblShpPointType.Dock = DockStyle.Fill;
            lblShpPointType.Name = "lblShpPointType";
            lblShpPointType.TabIndex = 1;
            lblShpPointType.Text = "Shapefile Type";
            lblShpPointType.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtShpPointType
            // 
            txtShpPointType.Dock = DockStyle.Fill;
            txtShpPointType.Enabled = false;
            txtShpPointType.Name = "txtShpPointType";
            txtShpPointType.TabIndex = 3;
            txtShpPointType.TextChanged += txtShp_TextChanged;
            // 
            // lblShpPointColor
            // 
            lblShpPointColor.AutoSize = true;
            lblShpPointColor.Dock = DockStyle.Fill;
            lblShpPointColor.Name = "lblShpPointColor";
            lblShpPointColor.TabIndex = 4;
            lblShpPointColor.Text = "Point Color";
            lblShpPointColor.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // pnlShpPointColor
            // 
            pnlShpPointColor.Dock = DockStyle.Fill;
            pnlShpPointColor.Name = "pnlShpPointColor";
            pnlShpPointColor.BackColor = Color.Black;
            pnlShpPointColor.TabIndex = 5;
            pnlShpPointColor.BackColorChanged += pnlBackColor_Changed;
            // 
            // btnShpPointColor
            // 
            btnShpPointColor.Dock = DockStyle.Fill;
            btnShpPointColor.Name = "btnShpPointColor";
            btnShpPointColor.TabIndex = 6;
            btnShpPointColor.Text = "...";
            btnShpPointColor.UseVisualStyleBackColor = true;
            btnShpPointColor.Click += colorButton_Click;
            // 
            // lblShpPointMarker
            // 
            lblShpPointMarker.AutoSize = true;
            lblShpPointMarker.Dock = DockStyle.Fill;
            lblShpPointMarker.Name = "lblShpPointMarker";
            lblShpPointMarker.TabIndex = 7;
            lblShpPointMarker.Text = "Marker";
            lblShpPointMarker.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboShpPointMarker
            // 
            comboShpPointMarker.Dock = DockStyle.Fill;
            comboShpPointMarker.DropDownStyle = ComboBoxStyle.DropDownList;
            comboShpPointMarker.FormattingEnabled = true;
            comboShpPointMarker.Items.AddRange(new object[] { "o", "*", "^", "x" });
            comboShpPointMarker.Name = "comboShpPointMarker";
            comboShpPointMarker.TabIndex = 15;
            comboShpPointMarker.SelectedIndex = 0;
            comboShpPointMarker.SelectedIndexChanged += comboShp_SelectedIndexChanged;
            // 
            // lblShpPointMarkerSize
            // 
            lblShpPointMarkerSize.AutoSize = true;
            lblShpPointMarkerSize.Dock = DockStyle.Fill;
            lblShpPointMarkerSize.Name = "lblShpPointMarkerSize";
            lblShpPointMarkerSize.TabIndex = 8;
            lblShpPointMarkerSize.Text = "Marker Size";
            lblShpPointMarkerSize.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // numShpPointMarkerSize
            // 
            numShpPointMarkerSize.Dock = DockStyle.Fill;
            numShpPointMarkerSize.Maximum = new decimal(new int[] { 30, 0, 0, 0 });
            numShpPointMarkerSize.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            numShpPointMarkerSize.Name = "numShpPointMarkerSize";
            numShpPointMarkerSize.TabIndex = 16;
            numShpPointMarkerSize.Value = new decimal(new int[] { 12, 0, 0, 0 });
            numShpPointMarkerSize.ValueChanged += numShp_ValueChanged;
            // 
            // lblShpPointMarkerAlpha
            // 
            lblShpPointMarkerAlpha.AutoSize = true;
            lblShpPointMarkerAlpha.Dock = DockStyle.Fill;
            lblShpPointMarkerAlpha.Name = "lblShpPointMarkerAlpha";
            lblShpPointMarkerAlpha.TabIndex = 9;
            lblShpPointMarkerAlpha.Text = "Transparency";
            lblShpPointMarkerAlpha.TextAlign = ContentAlignment.MiddleLeft;
            toolTip1.SetToolTip(lblShpPointMarkerAlpha, "0 = Fully Transparent, 1 = Fully Opaque");
            // 
            // numShpPointMarkerAlpha
            // 
            numShpPointMarkerAlpha.Dock = DockStyle.Fill;
            numShpPointMarkerAlpha.Minimum = 0;
            numShpPointMarkerAlpha.Increment = 0.05M;
            numShpPointMarkerAlpha.Maximum = 1;
            numShpPointMarkerAlpha.Value = 1;
            numShpPointMarkerAlpha.DecimalPlaces = 2;
            numShpPointMarkerAlpha.Name = "numShpPointMarkerAlpha";
            numShpPointMarkerAlpha.TabIndex = 17;
            numShpPointMarkerAlpha.ValueChanged += numShp_ValueChanged;
        }

        private void CreateShpLineComponents()
        {
            // 
            // lblShpLinePath
            // 
            lblShpLinePath.AutoSize = true;
            lblShpLinePath.Dock = DockStyle.Fill;
            lblShpLinePath.Name = "lblShpLinePath";
            lblShpLinePath.TabIndex = 0;
            lblShpLinePath.Text = "Path";
            lblShpLinePath.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtShpLinePath
            // 
            txtShpLinePath.Dock = DockStyle.Fill;
            txtShpLinePath.Enabled = false;
            txtShpLinePath.Name = "txtShpLinePath";
            txtShpLinePath.TabIndex = 2;
            txtShpLinePath.TextChanged += txtShp_TextChanged;
            // 
            // lblShpLineType
            // 
            lblShpLineType.AutoSize = true;
            lblShpLineType.Dock = DockStyle.Fill;
            lblShpLineType.Name = "lblShpLineType";
            lblShpLineType.TabIndex = 1;
            lblShpLineType.Text = "Shapefile Type";
            lblShpLineType.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtShpLineType
            // 
            txtShpLineType.Dock = DockStyle.Fill;
            txtShpLineType.Enabled = false;
            txtShpLineType.Name = "txtShpLineType";
            txtShpLineType.TabIndex = 3;
            txtShpLineType.TextChanged += txtShp_TextChanged;
            //
            // lblShpLineColor
            //
            lblShpLineColor.AutoSize = true;
            lblShpLineColor.Dock = DockStyle.Fill;
            lblShpLineColor.Name = "lblShpLineColor";
            lblShpLineColor.TabIndex = 4;
            lblShpLineColor.Text = "Line Color";
            lblShpLineColor.TextAlign = ContentAlignment.MiddleLeft;
            //
            // pnlShpLineColor
            //
            pnlShpLineColor.Dock = DockStyle.Fill;
            pnlShpLineColor.Name = "pnlShpLineColor";
            pnlShpLineColor.BackColor = Color.Black;
            pnlShpLineColor.TabIndex = 5;
            pnlShpLineColor.BackColorChanged += pnlBackColor_Changed;
            //
            // btnShpLineColor
            //
            btnShpLineColor.Dock = DockStyle.Fill;
            btnShpLineColor.Name = "btnShpLineColor";
            btnShpLineColor.TabIndex = 6;
            btnShpLineColor.Text = "...";
            btnShpLineColor.UseVisualStyleBackColor = true;
            btnShpLineColor.Click += colorButton_Click;
            //
            // lblShpLineLineWidth
            //
            lblShpLineLineWidth.AutoSize = true;
            lblShpLineLineWidth.Dock = DockStyle.Fill;
            lblShpLineLineWidth.Name = "lblShpLineLineWidth";
            lblShpLineLineWidth.TabIndex = 7;
            lblShpLineLineWidth.Text = "Line Width";
            lblShpLineLineWidth.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtShpLineLineWidth
            //
            txtShpLineLineWidth.Dock = DockStyle.Fill;
            txtShpLineLineWidth.Name = "txtShpLineLineWidth";
            txtShpLineLineWidth.TabIndex = 15;
            txtShpLineLineWidth.Text = "1.0";
            txtShpLineLineWidth.TextChanged += txtShp_TextChanged;
            //
            // lblShpLineAlpha
            //
            lblShpLineAlpha.AutoSize = true;
            lblShpLineAlpha.Dock = DockStyle.Fill;
            lblShpLineAlpha.Name = "lblShpLineAlpha";
            lblShpLineAlpha.TabIndex = 8;
            lblShpLineAlpha.Text = "Transparency";
            lblShpLineAlpha.TextAlign = ContentAlignment.MiddleLeft;
            toolTip1.SetToolTip(lblShpLineAlpha, "0 = Fully Transparent, 1 = Fully Opaque");
            //
            // numShpLineAlpha
            //
            numShpLineAlpha.Dock = DockStyle.Fill;
            numShpLineAlpha.Minimum = 0;
            numShpLineAlpha.Increment = 0.05M;
            numShpLineAlpha.Maximum = 1;
            numShpLineAlpha.Value = 1;
            numShpLineAlpha.DecimalPlaces = 2;
            numShpLineAlpha.Name = "numShpLineAlpha";
            numShpLineAlpha.TabIndex = 16;
            numShpLineAlpha.ValueChanged += numShp_ValueChanged;

        }

        private void CreateShpPolyComponents()
        {
            //
            // lblShpPolyPath
            //
            lblShpPolyPath.AutoSize = true;
            lblShpPolyPath.Dock = DockStyle.Fill;
            lblShpPolyPath.Name = "lblShpPolyPath";
            lblShpPolyPath.TabIndex = 0;
            lblShpPolyPath.Text = "Path";
            lblShpPolyPath.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtShpPolyPath
            //
            txtShpPolyPath.Dock = DockStyle.Fill;
            txtShpPolyPath.Enabled = false;
            txtShpPolyPath.Name = "txtShpPolyPath";
            txtShpPolyPath.TabIndex = 2;
            txtShpPolyPath.TextChanged += txtShp_TextChanged;
            //
            // lblShpPolyType
            //
            lblShpPolyType.AutoSize = true;
            lblShpPolyType.Dock = DockStyle.Fill;
            lblShpPolyType.Name = "lblShpPolyType";
            lblShpPolyType.TabIndex = 1;
            lblShpPolyType.Text = "Shapefile Type";
            lblShpPolyType.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtShpPolyType
            //
            txtShpPolyType.Dock = DockStyle.Fill;
            txtShpPolyType.Enabled = false;
            txtShpPolyType.Name = "txtShpPolyType";
            txtShpPolyType.TabIndex = 3;
            txtShpPolyType.TextChanged += txtShp_TextChanged;
            //
            // lblShpPolyEdgeColor
            //
            lblShpPolyEdgeColor.AutoSize = true;
            lblShpPolyEdgeColor.Dock = DockStyle.Fill;
            lblShpPolyEdgeColor.Name = "lblShpPolyEdgeColor";
            lblShpPolyEdgeColor.TabIndex = 4;
            lblShpPolyEdgeColor.Text = "Edge Color";
            lblShpPolyEdgeColor.TextAlign = ContentAlignment.MiddleLeft;
            //
            // pnlShpPolyEdgeColor
            //
            pnlShpPolyEdgeColor.Dock = DockStyle.Fill;
            pnlShpPolyEdgeColor.Name = "pnlShpPolyEdgeColor";
            pnlShpPolyEdgeColor.BackColor = Color.Black;
            pnlShpPolyEdgeColor.TabIndex = 5;
            pnlShpPolyEdgeColor.BackColorChanged += pnlBackColor_Changed;
            //
            // btnShpPolyEdgeColor
            //
            btnShpPolyEdgeColor.Dock = DockStyle.Fill;
            btnShpPolyEdgeColor.Name = "btnShpPolyEdgeColor";
            btnShpPolyEdgeColor.TabIndex = 6;
            btnShpPolyEdgeColor.Text = "...";
            btnShpPolyEdgeColor.UseVisualStyleBackColor = true;
            btnShpPolyEdgeColor.Click += colorButton_Click;
            //
            // lblShpPolyLineWidth
            //
            lblShpPolyLineWidth.AutoSize = true;
            lblShpPolyLineWidth.Dock = DockStyle.Fill;
            lblShpPolyLineWidth.Name = "lblShpPolyLineWidth";
            lblShpPolyLineWidth.TabIndex = 7;
            lblShpPolyLineWidth.Text = "Line Width";
            lblShpPolyLineWidth.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtShpPolyLineWidth
            //
            txtShpPolyLineWidth.Dock = DockStyle.Fill;
            txtShpPolyLineWidth.Name = "txtShpPolyLineWidth";
            txtShpPolyLineWidth.TabIndex = 15;
            txtShpPolyLineWidth.Text = "0.8";
            txtShpPolyLineWidth.TextChanged += txtShp_TextChanged;
            //
            // lblShpPolyFaceColor
            //
            lblShpPolyFaceColor.AutoSize = true;
            lblShpPolyFaceColor.Dock = DockStyle.Fill;
            lblShpPolyFaceColor.Name = "lblShpPolyFaceColor";
            lblShpPolyFaceColor.TabIndex = 8;
            lblShpPolyFaceColor.Text = "Face Color";
            lblShpPolyFaceColor.TextAlign = ContentAlignment.MiddleLeft;
            //
            // pnlShpPolyFaceColor
            //
            pnlShpPolyFaceColor.Dock = DockStyle.Fill;
            pnlShpPolyFaceColor.Name = "pnlShpPolyFaceColor";
            pnlShpPolyFaceColor.BackColor = Color.Black;
            pnlShpPolyFaceColor.TabIndex = 9;
            pnlShpPolyFaceColor.BackColorChanged += pnlBackColor_Changed;
            //
            // btnShpPolyFaceColor
            btnShpPolyFaceColor.Dock = DockStyle.Fill;
            btnShpPolyFaceColor.Name = "btnShpPolyFaceColor";
            btnShpPolyFaceColor.TabIndex = 10;
            btnShpPolyFaceColor.Text = "...";
            btnShpPolyFaceColor.UseVisualStyleBackColor = true;
            btnShpPolyFaceColor.Click += colorButton_Click;
            //
            // lblShpPolyAlpha
            lblShpPolyAlpha.AutoSize = true;
            lblShpPolyAlpha.Dock = DockStyle.Fill;
            lblShpPolyAlpha.Name = "lblShpPolyAlpha";
            lblShpPolyAlpha.TabIndex = 11;
            lblShpPolyAlpha.Text = "Transparency";
            lblShpPolyAlpha.TextAlign = ContentAlignment.MiddleLeft;
            toolTip1.SetToolTip(lblShpPolyAlpha, "0 = Fully Transparent, 1 = Fully Opaque");
            //
            // numShpPolyAlpha
            numShpPolyAlpha.Dock = DockStyle.Fill;
            numShpPolyAlpha.Minimum = 0;
            numShpPolyAlpha.Increment = 0.05M;
            numShpPolyAlpha.Maximum = 1;
            numShpPolyAlpha.Value = 1;
            numShpPolyAlpha.DecimalPlaces = 2;
            numShpPolyAlpha.Name = "numShpPolyAlpha";
            numShpPolyAlpha.TabIndex = 17;
            numShpPolyAlpha.ValueChanged += numShp_ValueChanged;

        }

        private void CreateShpLabelComponents()
        {
            //
            // lblShpLabelText
            //
            lblShpLabelText.AutoSize = true;
            lblShpLabelText.Dock = DockStyle.Fill;
            lblShpLabelText.Name = "lblShpLabelText";
            lblShpLabelText.TabIndex = 10;
            lblShpLabelText.Text = "Label Text";
            lblShpLabelText.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtShpLabelText
            //
            txtShpLabelText.Dock = DockStyle.Fill;
            txtShpLabelText.Name = "txtShpLabelText";
            txtShpLabelText.TabIndex = 18;
            txtShpLabelText.TextChanged += txtShp_TextChanged;
            //
            // lblShpLabelFontSize
            //
            lblShpLabelFontSize.AutoSize = true;
            lblShpLabelFontSize.Dock = DockStyle.Fill;
            lblShpLabelFontSize.Name = "lblShpLabelFontSize";
            lblShpLabelFontSize.TabIndex = 11;
            lblShpLabelFontSize.Text = "Font Size";
            lblShpLabelFontSize.TextAlign = ContentAlignment.MiddleLeft;
            //
            // numShpLabelFontSize
            //
            numShpLabelFontSize.Dock = DockStyle.Fill;
            numShpLabelFontSize.Maximum = new decimal(new int[] { 30, 0, 0, 0 });
            numShpLabelFontSize.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            numShpLabelFontSize.Name = "numShpLabelFontSize";
            numShpLabelFontSize.TabIndex = 19;
            numShpLabelFontSize.Value = new decimal(new int[] { 8, 0, 0, 0 });
            numShpLabelFontSize.ValueChanged += numShp_ValueChanged;
            //
            // lblShpLabelColor
            //
            lblShpLabelColor.AutoSize = true;
            lblShpLabelColor.Dock = DockStyle.Fill;
            lblShpLabelColor.Name = "lblShpLabelColor";
            lblShpLabelColor.TabIndex = 12;
            lblShpLabelColor.Text = "Label Color";
            lblShpLabelColor.TextAlign = ContentAlignment.MiddleLeft;
            //
            // pnlShpLabelColor
            //
            pnlShpLabelColor.Dock = DockStyle.Fill;
            pnlShpLabelColor.Name = "pnlShpLabelColor";
            pnlShpLabelColor.BackColor = Color.Black;
            pnlShpLabelColor.TabIndex = 13;
            pnlShpLabelColor.BackColorChanged += pnlBackColor_Changed;
            //
            // btnShpLabelColor
            //
            btnShpLabelColor.Dock = DockStyle.Fill;
            btnShpLabelColor.Name = "btnShpLabelColor";
            btnShpLabelColor.TabIndex = 14;
            btnShpLabelColor.Text = "...";
            btnShpLabelColor.UseVisualStyleBackColor = true;
            btnShpLabelColor.Click += colorButton_Click;
            //
            // lblShpLabelHA
            //
            lblShpLabelHA.AutoSize = true;
            lblShpLabelHA.Dock = DockStyle.Fill;
            lblShpLabelHA.Name = "lblShpLabelHA";
            lblShpLabelHA.TabIndex = 13;
            lblShpLabelHA.Text = "Horizontal Alignment";
            lblShpLabelHA.TextAlign = ContentAlignment.MiddleLeft;
            //
            // comboShpLabelHA
            //
            comboShpLabelHA.Dock = DockStyle.Fill;
            comboShpLabelHA.DropDownStyle = ComboBoxStyle.DropDownList;
            comboShpLabelHA.FormattingEnabled = true;
            comboShpLabelHA.Items.AddRange(new object[] { "Left", "Center", "Right" });
            comboShpLabelHA.Name = "comboShpLabelHA";
            comboShpLabelHA.TabIndex = 20;
            comboShpLabelHA.SelectedIndex = 0;
            comboShpLabelHA.SelectedIndexChanged += comboShp_SelectedIndexChanged;
            //
            // lblShpLabelVA
            //
            lblShpLabelVA.AutoSize = true;
            lblShpLabelVA.Dock = DockStyle.Fill;
            lblShpLabelVA.Name = "lblShpLabelVA";
            lblShpLabelVA.TabIndex = 14;
            lblShpLabelVA.Text = "Vertical Alignment";
            lblShpLabelVA.TextAlign = ContentAlignment.MiddleLeft;
            //
            // comboShpLabelVA
            //
            comboShpLabelVA.Dock = DockStyle.Fill;
            comboShpLabelVA.DropDownStyle = ComboBoxStyle.DropDownList;
            comboShpLabelVA.FormattingEnabled = true;
            comboShpLabelVA.Items.AddRange(new object[] { "Top", "Center", "Bottom" });
            comboShpLabelVA.Name = "comboShpLabelVA";
            comboShpLabelVA.TabIndex = 21;
            comboShpLabelVA.SelectedIndex = 1;
            comboShpLabelVA.SelectedIndexChanged += comboShp_SelectedIndexChanged;
            //
            // lblShpLabelOffsetPointsX
            //
            lblShpLabelOffsetPointsX.AutoSize = true;
            lblShpLabelOffsetPointsX.Dock = DockStyle.Fill;
            lblShpLabelOffsetPointsX.Name = "lblShpLabelOffsetPointsX";
            lblShpLabelOffsetPointsX.TabIndex = 15;
            lblShpLabelOffsetPointsX.Text = "Offset Points X";
            lblShpLabelOffsetPointsX.TextAlign = ContentAlignment.MiddleLeft;
            toolTip1.SetToolTip(lblShpLabelOffsetPointsX, "Offset in points (1/72 inch) in the X direction");
            //
            // txtShpLabelOffsetPointsX
            //
            txtShpLabelOffsetPointsX.Dock = DockStyle.Fill;
            txtShpLabelOffsetPointsX.Name = "txtShpLabelOffsetPointsX";
            txtShpLabelOffsetPointsX.TabIndex = 22;
            txtShpLabelOffsetPointsX.Text = "0";
            txtShpLabelOffsetPointsX.TextChanged += txtShp_TextChanged;
            //
            // lblShpLabelOffsetPointsY
            //
            lblShpLabelOffsetPointsY.AutoSize = true;
            lblShpLabelOffsetPointsY.Dock = DockStyle.Fill;
            lblShpLabelOffsetPointsY.Name = "lblShpLabelOffsetPointsY";
            lblShpLabelOffsetPointsY.TabIndex = 16;
            lblShpLabelOffsetPointsY.Text = "Offset Points Y";
            lblShpLabelOffsetPointsY.TextAlign = ContentAlignment.MiddleLeft;
            toolTip1.SetToolTip(lblShpLabelOffsetPointsY, "Offset in points (1/72 inch) in the Y direction");
            //
            // txtShpLabelOffsetPointsY
            //
            txtShpLabelOffsetPointsY.Dock = DockStyle.Fill;
            txtShpLabelOffsetPointsY.Name = "txtShpLabelOffsetPointsY";
            txtShpLabelOffsetPointsY.TabIndex = 23;
            txtShpLabelOffsetPointsY.Text = "0";
            txtShpLabelOffsetPointsY.TextChanged += txtShp_TextChanged;
            //
            // lblShpLabelOffsetDataX
            //
            lblShpLabelOffsetDataX.AutoSize = true;
            lblShpLabelOffsetDataX.Dock = DockStyle.Fill;
            lblShpLabelOffsetDataX.Name = "lblShpLabelOffsetDataX";
            lblShpLabelOffsetDataX.TabIndex = 17;
            lblShpLabelOffsetDataX.Text = "Offset Data X";
            lblShpLabelOffsetDataX.TextAlign = ContentAlignment.MiddleLeft;
            toolTip1.SetToolTip(lblShpLabelOffsetDataX, "Offset in data units in the X direction");
            //
            // txtShpLabelOffsetDataX
            //
            txtShpLabelOffsetDataX.Dock = DockStyle.Fill;
            txtShpLabelOffsetDataX.Name = "txtShpLabelOffsetDataX";
            txtShpLabelOffsetDataX.TabIndex = 24;
            txtShpLabelOffsetDataX.Text = "0";
            txtShpLabelOffsetDataX.TextChanged += txtShp_TextChanged;
            //
            // lblShpLabelOffsetDataY
            //
            lblShpLabelOffsetDataY.AutoSize = true;
            lblShpLabelOffsetDataY.Dock = DockStyle.Fill;
            lblShpLabelOffsetDataY.Name = "lblShpLabelOffsetDataY";
            lblShpLabelOffsetDataY.TabIndex = 18;
            lblShpLabelOffsetDataY.Text = "Offset Data Y";
            lblShpLabelOffsetDataY.TextAlign = ContentAlignment.MiddleLeft;
            toolTip1.SetToolTip(lblShpLabelOffsetDataY, "Offset in data units in the Y direction");
            //
            // txtShpLabelOffsetDataY
            //
            txtShpLabelOffsetDataY.Dock = DockStyle.Fill;
            txtShpLabelOffsetDataY.Name = "txtShpLabelOffsetDataY";
            txtShpLabelOffsetDataY.TabIndex = 25;
            txtShpLabelOffsetDataY.Text = "0";
            txtShpLabelOffsetDataY.TextChanged += txtShp_TextChanged;

        }

        private void BuildTableShpPoint()
        {
            // 
            // tableShpPoint
            // 
            tableShpPoint.ColumnCount = 3;
            tableShpPoint.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 170F));
            tableShpPoint.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableShpPoint.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 70F));
            tableShpPoint.Dock = DockStyle.Fill;
            tableShpPoint.Location = new Point(0, 0);
            tableShpPoint.Name = "tableShpPoint";
            tableShpPoint.RowCount = 16;
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoint.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableShpPoint.Size = new Size(520, 707);
            tableShpPoint.TabIndex = 0;
            tableShpPoint.Controls.Add(lblShpPointPath, 0, 0);
            tableShpPoint.Controls.Add(lblShpPointType, 0, 1);
            tableShpPoint.Controls.Add(txtShpPointPath, 1, 0);
            tableShpPoint.Controls.Add(txtShpPointType, 1, 1);
            tableShpPoint.Controls.Add(lblShpPointColor, 0, 2);
            tableShpPoint.Controls.Add(pnlShpPointColor, 1, 2);
            tableShpPoint.Controls.Add(btnShpPointColor, 2, 2);
            tableShpPoint.Controls.Add(lblShpPointMarker, 0, 3);
            tableShpPoint.Controls.Add(lblShpPointMarkerSize, 0, 4);
            tableShpPoint.Controls.Add(lblShpPointMarkerAlpha, 0, 5);
            tableShpPoint.Controls.Add(comboShpPointMarker, 1, 3);
            tableShpPoint.Controls.Add(numShpPointMarkerSize, 1, 4);
            tableShpPoint.Controls.Add(numShpPointMarkerAlpha, 1, 5);
            AddLabelComponentsToTable(tableShpPoint, 6);
        }

        private void BuildTableShpLine()
        {
            // 
            // tableShpLine
            // 
            tableShpLine.ColumnCount = 3;
            tableShpLine.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 170F));
            tableShpLine.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableShpLine.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 70F));
            tableShpLine.Dock = DockStyle.Fill;
            tableShpLine.Location = new Point(0, 0);
            tableShpLine.Name = "tableShpLine";
            tableShpLine.RowCount = 15;
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpLine.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableShpLine.Size = new Size(520, 707);
            tableShpLine.TabIndex = 0;
            tableShpLine.Controls.Add(lblShpLinePath, 0, 0);
            tableShpLine.Controls.Add(lblShpLineType, 0, 1);
            tableShpLine.Controls.Add(txtShpLinePath, 1, 0);
            tableShpLine.Controls.Add(txtShpLineType, 1, 1);
            tableShpLine.Controls.Add(lblShpLineColor, 0, 2);
            tableShpLine.Controls.Add(pnlShpLineColor, 1, 2);
            tableShpLine.Controls.Add(btnShpLineColor, 2, 2);
            tableShpLine.Controls.Add(lblShpLineLineWidth, 0, 3);
            tableShpLine.Controls.Add(txtShpLineLineWidth, 1, 3);
            tableShpLine.Controls.Add(lblShpLineAlpha, 0, 4);
            tableShpLine.Controls.Add(numShpLineAlpha, 1, 4);
            AddLabelComponentsToTable(tableShpLine, 5);
        }

        private void BuildTableShpPoly()
        {
            // 
            // tableShpPoly
            // 
            tableShpPoly.ColumnCount = 3;
            tableShpPoly.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 170F));
            tableShpPoly.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableShpPoly.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 70F));
            tableShpPoly.Dock = DockStyle.Fill;
            tableShpPoly.Location = new Point(0, 0);
            tableShpPoly.Name = "tableShpPoly";
            tableShpPoly.RowCount = 16;
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableShpPoly.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableShpPoly.Size = new Size(520, 707);
            tableShpPoly.TabIndex = 0;
            tableShpPoly.Controls.Add(lblShpPolyPath, 0, 0);
            tableShpPoly.Controls.Add(lblShpPolyType, 0, 1);
            tableShpPoly.Controls.Add(txtShpPolyPath, 1, 0);
            tableShpPoly.Controls.Add(txtShpPolyType, 1, 1);
            tableShpPoly.Controls.Add(lblShpPolyEdgeColor, 0, 2);
            tableShpPoly.Controls.Add(pnlShpPolyEdgeColor, 1, 2);
            tableShpPoly.Controls.Add(btnShpPolyEdgeColor, 2, 2);
            tableShpPoly.Controls.Add(lblShpPolyLineWidth, 0, 3);
            tableShpPoly.Controls.Add(txtShpPolyLineWidth, 1, 3);
            tableShpPoly.Controls.Add(lblShpPolyFaceColor, 0, 4);
            tableShpPoly.Controls.Add(pnlShpPolyFaceColor, 1, 4);
            tableShpPoly.Controls.Add(btnShpPolyFaceColor, 2, 4);
            tableShpPoly.Controls.Add(lblShpPolyAlpha, 0, 5);
            tableShpPoly.Controls.Add(numShpPolyAlpha, 1, 5);
            AddLabelComponentsToTable(tableShpPoly, 6);
        }

        private void AddLabelComponentsToTable(TableLayoutPanel table, int startingRow)
        {
            table.Controls.Add(lblShpLabelText, 0, startingRow);
            table.Controls.Add(txtShpLabelText, 1, startingRow);
            table.Controls.Add(lblShpLabelFontSize, 0, startingRow + 1);
            table.Controls.Add(numShpLabelFontSize, 1, startingRow + 1);
            table.Controls.Add(lblShpLabelColor, 0, startingRow + 2);
            table.Controls.Add(pnlShpLabelColor, 1, startingRow + 2);
            table.Controls.Add(btnShpLabelColor, 2, startingRow + 2);
            table.Controls.Add(lblShpLabelHA, 0, startingRow + 3);
            table.Controls.Add(comboShpLabelHA, 1, startingRow + 3);
            table.Controls.Add(lblShpLabelVA, 0, startingRow + 4);
            table.Controls.Add(comboShpLabelVA, 1, startingRow + 4);
            table.Controls.Add(lblShpLabelOffsetPointsX, 0, startingRow + 5);
            table.Controls.Add(txtShpLabelOffsetPointsX, 1, startingRow + 5);
            table.Controls.Add(lblShpLabelOffsetPointsY, 0, startingRow + 6);
            table.Controls.Add(txtShpLabelOffsetPointsY, 1, startingRow + 6);
            table.Controls.Add(lblShpLabelOffsetDataX, 0, startingRow + 7);
            table.Controls.Add(txtShpLabelOffsetDataX, 1, startingRow + 7);
            table.Controls.Add(lblShpLabelOffsetDataY, 0, startingRow + 8);
            table.Controls.Add(txtShpLabelOffsetDataY, 1, startingRow + 8);
        }

        private string GetShapeType(string filePath)
        {
            // Example using NetTopologySuite
            using (var reader = new ShapefileDataReader(filePath, new NetTopologySuite.Geometries.GeometryFactory()))
            {
                var geomType = reader.ShapeHeader.ShapeType.ToString();
                MessageBox.Show(geomType);
                if (geomType.Contains("Point")) return "Point";
                if (geomType.Contains("Polygon")) return "Polygon";
                if (geomType.Contains("Line")) return "Line";

                return "The shapefile type " + geomType + " is not supported.";
            }
        }

        private void InitializeWidgets()
        {
            foreach (var file in Directory.GetFiles(_Globals.CMapsPath, "*.png"))
            {
                string name = Path.GetFileNameWithoutExtension(file);
                combo2Dcmap.Items.Add(new ColormapItem(name, Image.FromFile(file)));
                combo3Dcmap.Items.Add(new ColormapItem(name, Image.FromFile(file)));
            }
            combo2Dcmap.DrawItem += (s, e) =>
            {
                if (e.Index < 0) return;

                e.DrawBackground();
                var item = (ColormapItem)combo2Dcmap.Items[e.Index];

                int textColumnWidth = 100;  // fixed width reserved for text

                // Draw text (always in the same aligned column)
                using (Brush brush = new SolidBrush(e.ForeColor))
                {
                    e.Graphics.DrawString(
                        item.Name,
                        e.Font,
                        brush,
                        e.Bounds.Left + 2,
                        e.Bounds.Top + (e.Bounds.Height - e.Font.Height) / 2
                    );
                }

                // Draw preview aligned to the same start point
                if (item.Preview != null)
                {
                    int imageX = e.Bounds.Left + textColumnWidth;
                    int imageWidth = e.Bounds.Right - imageX - 2;
                    int imageHeight = e.Bounds.Height - 4;

                    var imageRect = new Rectangle(imageX, e.Bounds.Top + 2, imageWidth, imageHeight);
                    e.Graphics.DrawImage(item.Preview, imageRect);
                }

                e.DrawFocusRectangle();
            };
            combo3Dcmap.DrawItem += (s, e) =>
            {
                if (e.Index < 0) return;

                e.DrawBackground();
                var item = (ColormapItem)combo3Dcmap.Items[e.Index];

                int textColumnWidth = 100;  // fixed width reserved for text

                // Draw text (always in the same aligned column)
                using (Brush brush = new SolidBrush(e.ForeColor))
                {
                    e.Graphics.DrawString(
                        item.Name,
                        e.Font,
                        brush,
                        e.Bounds.Left + 2,
                        e.Bounds.Top + (e.Bounds.Height - e.Font.Height) / 2
                    );
                }

                // Draw preview aligned to the same start point
                if (item.Preview != null)
                {
                    int imageX = e.Bounds.Left + textColumnWidth;
                    int imageWidth = e.Bounds.Right - imageX - 2;
                    int imageHeight = e.Bounds.Height - 4;

                    var imageRect = new Rectangle(imageX, e.Bounds.Top + 2, imageWidth, imageHeight);
                    e.Graphics.DrawImage(item.Preview, imageRect);
                }

                e.DrawFocusRectangle();
            };
        }

        private void selectComboByValue(ComboBox combo, string value)
        {
            for (int i = 0; i < combo.Items.Count; i++)
            {
                if (combo.Items[i].ToString() == value)
                {
                    combo.SelectedIndex = i;
                    return;
                }
            }
            // If we reach here, the value was not found
            if (combo.Items.Count > 0)
            {
                combo.SelectedIndex = 0; // Select the first item as a fallback
            }
        }

        private string getValueByIndex(ComboBox combo, int index)
        {
            if (index >= 0 && index < combo.Items.Count)
            {
                return combo.Items[index].ToString();
            }
            return string.Empty; // or throw an exception, or return null, based on your needs
        }

        private void FillSurveyTree(TreeView tree)
        {
            tree.Nodes.Clear();
            foreach (XmlElement survey in _project.GetObjects("Survey"))
            {
                string surveyName = survey.GetAttribute("name");
                TreeNode nodeElement = new TreeNode(surveyName);
                nodeElement.Tag = survey;
                tree.Nodes.Add(nodeElement);
            }
        }

        private void SetSurveyCheck(TreeView tree, XmlElement settingElement)
        {
            XmlElement? surveysElement = settingElement.SelectSingleNode("Surveys") as XmlElement;
            XmlNodeList surveys = surveysElement.SelectNodes("Survey");
            List<string> surveyIds = new List<string>();
            foreach (XmlNode s in surveys)
            {
                if (s is XmlElement surveyElem)
                {
                    string ID = surveyElem.SelectSingleNode("ID")?.InnerText;
                    surveyIds.Add(ID);
                }
            }
            foreach (TreeNode surveyNode in tree.Nodes)
            {
                XmlNode? node = surveyNode.Tag as XmlNode;
                if (node is XmlElement elem)
                {
                    string id = elem.GetAttribute("id");
                    if (surveyIds.Contains(id))
                    {
                        surveyNode.Checked = true;
                    }
                    else
                    {
                        surveyNode.Checked = false;
                    }
                }
            }
        }

        private void populateTextBox(TextBox textBox, XmlNode? node, string defaultValue)
        {
            if (node != null)
            {
                if (!String.IsNullOrEmpty(node.InnerText))
                    textBox.Text = node.InnerText;
                else
                    textBox.Text = defaultValue;
            }
            else
                textBox.Text = defaultValue;
        }

        private void populateComboBox(ComboBox comboBox, XmlNode? node)
        {
            if (node != null)
            {
                if (!String.IsNullOrEmpty(node.InnerText))
                    selectComboByValue(comboBox, node.InnerText);
                else
                    comboBox.SelectedIndex = 0;
            }
            else
                comboBox.SelectedIndex = 0;
        }

        private void populateCMapCombo(ComboBox comboBox, XmlNode? node)
        {
            if (node != null)
            {
                comboBox.SelectedItem = comboBox.Items
                    .Cast<ColormapItem>()
                    .FirstOrDefault(i => i.Name.Equals(node.InnerText ?? "jet", StringComparison.OrdinalIgnoreCase));
            }
            else
                comboBox.SelectedIndex = 0;
        }

        private void populatePanelColor(Panel panel, XmlNode? node, string defaultColor)
        {
            if (node != null)
            {
                if (!String.IsNullOrEmpty(node.InnerText))
                    panel.BackColor = ColorTranslator.FromHtml(node.InnerText);
                else
                    panel.BackColor = ColorTranslator.FromHtml(defaultColor);
            }
            else
                panel.BackColor = ColorTranslator.FromHtml(defaultColor);
        }

        private void populateNumericUpDown(NumericUpDown numericUpDown, XmlNode? node, decimal defaultValue)
        {
            if (node != null)
            {
                if (decimal.TryParse(node.InnerText, out decimal value))
                    numericUpDown.Value = value;
                else
                    numericUpDown.Value = defaultValue;
            }
            else
                numericUpDown.Value = defaultValue;
        }

        private void populate2DMapSetting()
        {
            XmlNode? bkgColorNode = mapSettings2D.SelectSingleNode("BackgroundColor");
            populatePanelColor(pnl2DBackColor, bkgColorNode, "#000000");
            XmlNode? fielNameNode = mapSettings2D.SelectSingleNode("FieldName");
            populateComboBox(combo2DFieldName, fielNameNode);
            XmlNode? cmapNode = mapSettings2D.SelectSingleNode("Colormap");
            populateCMapCombo(combo2Dcmap, cmapNode);
            XmlNode? vminNode = mapSettings2D.SelectSingleNode("vmin");
            populateTextBox(txt2Dvmin, vminNode, "");
            XmlNode? vmaxNode = mapSettings2D.SelectSingleNode("vmax");
            populateTextBox(txt2Dvmax, vmaxNode, "");
            XmlNode? paddingNode = mapSettings2D.SelectSingleNode("Padding");
            populateTextBox(txt2DPagDeg, paddingNode, "0.1");
            XmlNode? nGridLinesNode = mapSettings2D.SelectSingleNode("NGridLines");
            populateNumericUpDown(num2DNGridLines, nGridLinesNode, 10);
            XmlNode? gridOpacityNode = mapSettings2D.SelectSingleNode("GridOpacity");
            populateTextBox(txt2DGridOpacity, gridOpacityNode, "0.35");
            XmlNode? gridColorNode = mapSettings2D.SelectSingleNode("GridColor");
            populatePanelColor(pnl2DGridColor, gridColorNode, "#333333");
            XmlNode? gridWidthNode = mapSettings2D.SelectSingleNode("GridWidth");
            populateTextBox(txt2DGridWidth, gridWidthNode, "1");
            XmlNode? nAxisTicksNode = mapSettings2D.SelectSingleNode("NAxisTicks");
            populateNumericUpDown(num2DNAxisTicks, nAxisTicksNode, 7);
            XmlNode? tickFontSizeNode = mapSettings2D.SelectSingleNode("TickFontSize");
            populateNumericUpDown(num2DTickFontSize, tickFontSizeNode, 10);
            XmlNode? tickNDecimalsNode = mapSettings2D.SelectSingleNode("TickNDecimals");
            populateNumericUpDown(num2DNTicksDecimals, tickNDecimalsNode, 4);
            XmlNode? axisLabelFontSizeNode = mapSettings2D.SelectSingleNode("AxisLabelFontSize");
            populateNumericUpDown(num2DAxisLabelFontSize, axisLabelFontSizeNode, 12);
            XmlNode? axisLabelColorNode = mapSettings2D.SelectSingleNode("AxisLabelColor");
            populatePanelColor(pnl2DAxisLabelColor, axisLabelColorNode, "#cccccc");
            XmlNode? hoverFontSizeNode = mapSettings2D.SelectSingleNode("HoverFontSize");
            populateNumericUpDown(num2DHoverFontSize, hoverFontSizeNode, 9);
            XmlNode? transectLineWidthNode = mapSettings2D.SelectSingleNode("TransectLineWidth");
            populateTextBox(txt2DTransectLineWidth, transectLineWidthNode, "3");
            XmlNode? verticalAggBinItemNode = mapSettings2D.SelectSingleNode("VerticalAggBinItem");
            populateComboBox(combo2DBins, verticalAggBinItemNode);
            if (combo2DBins.SelectedItem.ToString() == "Bin")
            {
                num2DBins.Visible = true;
                txt2DDepth.Visible = false;
            }
            else
            {
                num2DBins.Visible = false;
                txt2DDepth.Visible = true;
            }
            XmlNode? verticalAggBinTargetNode = mapSettings2D.SelectSingleNode("VerticalAggBinTarget");
            if (verticalAggBinTargetNode != null)
            {
                string? target = verticalAggBinTargetNode.InnerText;
                if (target != null)
                {
                    if (target == "Mean")
                    {
                        num2DBins.Enabled = false;
                        check2DBins.Checked = true;
                    }
                    else
                    {
                        num2DBins.Enabled = true;
                        check2DBins.Checked = false;
                        if (int.TryParse(target, out int value))
                            num2DBins.Value = value;
                        else
                            num2DBins.Value = 1;
                    }
                }
                else
                {
                    num2DBins.Enabled = true;
                    check2DBins.Checked = false;
                    num2DBins.Value = 1;
                }
            }
            else
            {
                num2DBins.Enabled = true;
                check2DBins.Checked = false;
                num2DBins.Value = 1;
            }
            XmlNode? verticalAggBeamNode = mapSettings2D.SelectSingleNode("VerticalAggBeam");
            if (verticalAggBeamNode != null)
            {
                string? beam = verticalAggBeamNode.InnerText;
                if (beam != null)
                {
                    if (beam == "Mean")
                    {
                        num2DBeams.Enabled = false;
                        check2DBeams.Checked = true;
                    }
                    else
                    {
                        num2DBeams.Enabled = true;
                        check2DBeams.Checked = false;
                        if (int.TryParse(beam, out int value))
                            num2DBeams.Value = value;
                        else
                            num2DBeams.Value = 1;
                    }
                }
                else
                {
                    num2DBeams.Enabled = true;
                    check2DBeams.Checked = false;
                    num2DBeams.Value = 1;
                }
            }
            else
            {
                num2DBeams.Enabled = true;
                check2DBeams.Checked = false;
                num2DBeams.Value = 1;
            }
            FillSurveyTree(treeSurveys2D);
            SetSurveyCheck(treeSurveys2D, mapSettings2D);
        }

        private void populate3DMapSetting()
        {
            XmlNode? bkgColorNode = mapSettings3D.SelectSingleNode("BackgroundColor");
            populatePanelColor(pnl3DBackColor, bkgColorNode, "#000000");
            XmlNode? fielNameNode = mapSettings3D.SelectSingleNode("FieldName");
            populateComboBox(combo3DFieldName, fielNameNode);
            XmlNode? cmapNode = mapSettings3D.SelectSingleNode("Colormap");
            populateCMapCombo(combo3Dcmap, cmapNode);
            XmlNode? vminNode = mapSettings3D.SelectSingleNode("vmin");
            populateTextBox(txt3Dvmin, vminNode, "");
            XmlNode? vmaxNode = mapSettings3D.SelectSingleNode("vmax");
            populateTextBox(txt3Dvmax, vmaxNode, "");
            XmlNode? paddingNode = mapSettings3D.SelectSingleNode("Padding");
            populateTextBox(txt3DPagDeg, paddingNode, "0.1");
            XmlNode? nGridLinesNode = mapSettings3D.SelectSingleNode("NGridLines");
            populateNumericUpDown(num3DNGridLines, nGridLinesNode, 10);
            XmlNode? gridOpacityNode = mapSettings3D.SelectSingleNode("GridOpacity");
            populateTextBox(txt3DGridOpacity, gridOpacityNode, "0.35");
            XmlNode? gridColorNode = mapSettings3D.SelectSingleNode("GridColor");
            populatePanelColor(pnl3DGridColor, gridColorNode, "#333333");
            XmlNode? gridWidthNode = mapSettings3D.SelectSingleNode("GridWidth");
            populateTextBox(txt3DGridWidth, gridWidthNode, "1");
            XmlNode? nAxisTicksNode = mapSettings3D.SelectSingleNode("NAxisTicks");
            populateNumericUpDown(num3DNAxisTicks, nAxisTicksNode, 7);
            XmlNode? tickFontSizeNode = mapSettings3D.SelectSingleNode("TickFontSize");
            populateNumericUpDown(num3DTickFontSize, tickFontSizeNode, 10);
            XmlNode? tickNDecimalsNode = mapSettings3D.SelectSingleNode("TickNDecimals");
            populateNumericUpDown(num3DNTicksDecimals, tickNDecimalsNode, 4);
            XmlNode? axisLabelFontSizeNode = mapSettings3D.SelectSingleNode("AxisLabelFontSize");
            populateNumericUpDown(num3DAxisLabelFontSize, axisLabelFontSizeNode, 12);
            XmlNode? axisLabelColorNode = mapSettings3D.SelectSingleNode("AxisLabelColor");
            populatePanelColor(pnl3DAxisLabelColor, axisLabelColorNode, "#cccccc");
            XmlNode? hoverFontSizeNode = mapSettings3D.SelectSingleNode("HoverFontSize");
            populateNumericUpDown(num3DHoverFontSize, hoverFontSizeNode, 9);
            XmlNode? zScaleNode = mapSettings3D.SelectSingleNode("ZScale");
            populateTextBox(txt3DZScale, zScaleNode, "3.0");
            FillSurveyTree(treeSurveys3D);
            SetSurveyCheck(treeSurveys3D, mapSettings3D);
        }

        private void PopulateShapefileSetting()
        {
            treeShapefiles.Nodes.Clear();
            XmlNodeList shapefiles = mapShapefiles.SelectNodes("Shapefile");
            if (shapefiles.Count == 0)
                return;
            foreach (XmlNode shpNode in shapefiles)
            {
                XmlElement? shp = shpNode as XmlElement;
                if (shp == null)
                    continue;
                XmlNode? nameNode = shp.SelectSingleNode("Name");
                string name = nameNode != null ? nameNode.InnerText : "Unnamed";
                XmlNode? pathNode = shp.SelectSingleNode("Path");
                string path = pathNode != null ? pathNode.InnerText : "";
                XmlNode? kindNode = shp.SelectSingleNode("Kind");
                string kind = kindNode != null ? kindNode.InnerText : "Point";
                ShapeFile shapeFile = new ShapeFile(name: name, path: path, kind: kind);
                if (shapeFile.Kind == "Point")
                {
                    XmlNode? pointColorNode = shp.SelectSingleNode("PointColor");
                    shapeFile.PointColor = pointColorNode != null ? pointColorNode.InnerText : "#000000";
                    XmlNode? pointMarkerNode = shp.SelectSingleNode("PointMarker");
                    shapeFile.PointMarker = pointMarkerNode != null ? pointMarkerNode.InnerText : "o";
                    XmlNode? pointMarkerSizeNode = shp.SelectSingleNode("PointMarkerSize");
                    shapeFile.PointMarkerSize = pointMarkerSizeNode != null ? pointMarkerSizeNode.InnerText : "12";
                    XmlNode? pointAlphaNode = shp.SelectSingleNode("PointAlpha");
                    shapeFile.PointAlpha = pointAlphaNode != null ? pointAlphaNode.InnerText : "1.0";
                }
                else if (shapeFile.Kind == "Line")
                {
                    XmlNode? lineColorNode = shp.SelectSingleNode("LineColor");
                    shapeFile.LineColor = lineColorNode != null ? lineColorNode.InnerText : "#000000";
                    XmlNode? lineLineWidthNode = shp.SelectSingleNode("LineLineWidth");
                    shapeFile.LineLineWidth = lineLineWidthNode != null ? lineLineWidthNode.InnerText : "1";
                    XmlNode? lineAlphaNode = shp.SelectSingleNode("LineAlpha");
                    shapeFile.LineAlpha = lineAlphaNode != null ? lineAlphaNode.InnerText : "1.0";
                }
                else if (shapeFile.Kind == "Polygon")
                {
                    XmlNode? polyEdgeColorNode = shp.SelectSingleNode("PolyEdgeColor");
                    shapeFile.PolyEdgeColor = polyEdgeColorNode != null ? polyEdgeColorNode.InnerText : "#000000";
                    XmlNode? polyLineWidthNode = shp.SelectSingleNode("PolyLineWidth");
                    shapeFile.PolyLineWidth = polyLineWidthNode != null ? polyLineWidthNode.InnerText : "0.8";
                    XmlNode? polyFaceColorNode = shp.SelectSingleNode("PolyFaceColor");
                    shapeFile.PolyFaceColor = polyFaceColorNode != null ? polyFaceColorNode.InnerText : "#000000";
                    XmlNode? polyAlphaNode = shp.SelectSingleNode("PolyAlpha");
                    shapeFile.PolyAlpha = polyAlphaNode != null ? polyAlphaNode.InnerText : "1.0";
                }
                XmlNode? labelTextNode = shp.SelectSingleNode("LabelText");
                shapeFile.LabelText = labelTextNode != null ? labelTextNode.InnerText : "";
                XmlNode? labelFontSizeNode = shp.SelectSingleNode("LabelFontSize");
                shapeFile.LabelFontSize = labelFontSizeNode != null ? labelFontSizeNode.InnerText : "8";
                XmlNode? labelColorNode = shp.SelectSingleNode("LabelColor");
                shapeFile.LabelColor = labelColorNode != null ? labelColorNode.InnerText : "#000000";
                XmlNode? labelHANode = shp.SelectSingleNode("LabelHA");
                shapeFile.LabelHA = labelHANode != null ? labelHANode.InnerText : "Left";
                XmlNode? labelVANode = shp.SelectSingleNode("LabelVA");
                shapeFile.LabelVA = labelVANode != null ? labelVANode.InnerText : "Center";
                XmlNode? labelOffsetPointsXNode = shp.SelectSingleNode("LabelOffsetPointsX");
                shapeFile.LabelOffsetPointsX = labelOffsetPointsXNode != null ? labelOffsetPointsXNode.InnerText : "0";
                XmlNode? labelOffsetPointsYNode = shp.SelectSingleNode("LabelOffsetPointsY");
                shapeFile.LabelOffsetPointsY = labelOffsetPointsYNode != null ? labelOffsetPointsYNode.InnerText : "0";
                XmlNode? labelOffsetDataXNode = shp.SelectSingleNode("LabelOffsetDataX");
                shapeFile.LabelOffsetDataX = labelOffsetDataXNode != null ? labelOffsetDataXNode.InnerText : "0";
                XmlNode? labelOffsetDataYNode = shp.SelectSingleNode("LabelOffsetDataY");
                shapeFile.LabelOffsetDataY = labelOffsetDataYNode != null ? labelOffsetDataYNode.InnerText : "0";
                bool isChecked = shp.GetAttribute("visible") == "true";
                AddShapeFileToTree(shapeFile, isChecked);
            }
        }

        private void PopulateFields()
        {
            populate2DMapSetting();
            populate3DMapSetting();
            PopulateShapefileSetting();
            isSaved = true; // Initially, fields are populated and considered saved
        }

        public MapOptions()
        {
            InitializeComponent();
            InitializeWidgets();
            InitializeShpTab();
            mapSettings = _project.GetObject("MapSettings", "2");
            mapSettings2D = mapSettings.SelectSingleNode("Map2D") as XmlElement;
            mapSettings3D = mapSettings.SelectSingleNode("Map3D") as XmlElement;
            mapShapefiles = mapSettings.SelectSingleNode("MapShapefiles") as XmlElement;
            treeSurveys2D.CheckBoxes = true;
            treeSurveys3D.CheckBoxes = true;
            treeShapefiles.CheckBoxes = true;
            PopulateFields();
        }

        private void menuSave_Click(object sender, EventArgs e)
        {
            SaveSettings();
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            if (!isSaved)
            {
                DialogResult result = MessageBox.Show(
                    text: "You have unsaved changes. Do you want to save before exiting?",
                    caption: "Confirm Exit",
                    buttons: MessageBoxButtons.YesNoCancel,
                    icon: MessageBoxIcon.Warning);
                if (result == DialogResult.Yes)
                {
                    SaveSettings();
                    this.Close();
                    return;

                }
                else if (result == DialogResult.Cancel)
                {
                    return; // User chose to cancel
                }
                else
                {
                    this.Close(); // User chose not to save, proceed with exit  
                }
            }
            else
            {
                this.Close(); // Close the form if there are no unsaved changes
            }
        }

        private void combo2DBins_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (combo2DBins.SelectedIndex == 0)
            {
                num2DBins.Visible = true;
                txt2DDepth.Visible = false;
                num2DBins.Enabled = !check2DBins.Checked;
            }
            else
            {
                num2DBins.Visible = false;
                txt2DDepth.Visible = true;
                txt2DDepth.Enabled = !check2DBins.Checked;
            }
            isSaved = false;
        }

        private void check2DBins_CheckedChanged(object sender, EventArgs e)
        {
            if (check2DBins.Checked)
            {
                num2DBins.Enabled = false;
                txt2DDepth.Enabled = false;
            }
            else
            {
                num2DBins.Enabled = true;
                txt2DDepth.Enabled = true;
            }
            isSaved = false;
        }

        private void check2DBeams_CheckedChanged(object sender, EventArgs e)
        {
            if (check2DBins.Checked)
            {
                num2DBeams.Enabled = false;
            }
            else
            {
                num2DBeams.Enabled = true;
            }
            isSaved = false;
        }

        private void SaveSettings2D()
        {
            XmlNode? bkgColorNode = mapSettings2D.SelectSingleNode("BackgroundColor");
            if (bkgColorNode == null)
            {
                bkgColorNode = _Globals.Config.CreateElement("BackgroundColor");
                mapSettings2D.AppendChild(bkgColorNode);
            }
            bkgColorNode.InnerText = ColorTranslator.ToHtml(pnl2DBackColor.BackColor);

            XmlNode? fieldNameNode = mapSettings2D.SelectSingleNode("FieldName");
            if (fieldNameNode == null)
            {
                fieldNameNode = _Globals.Config.CreateElement("FieldName");
                mapSettings2D.AppendChild(fieldNameNode);
            }
            fieldNameNode.InnerText = getValueByIndex(combo2DFieldName, combo2DFieldName.SelectedIndex);

            XmlNode? cmapNode = mapSettings2D.SelectSingleNode("Colormap");
            if (cmapNode == null)
            {
                cmapNode = _Globals.Config.CreateElement("Colormap");
                mapSettings2D.AppendChild(cmapNode);
            }
            cmapNode.InnerText = ((ColormapItem)combo2Dcmap.SelectedItem).Name;

            XmlNode? vminNode = mapSettings2D.SelectSingleNode("vmin");
            if (vminNode == null)
            {
                vminNode = _Globals.Config.CreateElement("vmin");
                mapSettings2D.AppendChild(vminNode);
            }
            vminNode.InnerText = txt2Dvmin.Text;

            XmlNode? vmaxNode = mapSettings2D.SelectSingleNode("vmax");
            if (vmaxNode == null)
            {
                vmaxNode = _Globals.Config.CreateElement("vmax");
                mapSettings2D.AppendChild(vmaxNode);
            }
            vmaxNode.InnerText = txt2Dvmax.Text;

            XmlNode? paddingNode = mapSettings2D.SelectSingleNode("Padding");
            if (paddingNode == null)
            {
                paddingNode = _Globals.Config.CreateElement("Padding");
                mapSettings2D.AppendChild(paddingNode);
            }
            paddingNode.InnerText = txt2DPagDeg.Text;

            XmlNode? nGridLinesNode = mapSettings2D.SelectSingleNode("NGridLines");
            if (nGridLinesNode == null)
            {
                nGridLinesNode = _Globals.Config.CreateElement("NGridLines");
                mapSettings2D.AppendChild(nGridLinesNode);
            }
            nGridLinesNode.InnerText = num2DNGridLines.Value.ToString();

            XmlNode? gridOpacityNode = mapSettings2D.SelectSingleNode("GridOpacity");
            if (gridOpacityNode == null)
            {
                gridOpacityNode = _Globals.Config.CreateElement("GridOpacity");
                mapSettings2D.AppendChild(gridOpacityNode);
            }
            gridOpacityNode.InnerText = txt2DGridOpacity.Text;

            XmlNode? gridColorNode = mapSettings2D.SelectSingleNode("GridColor");
            if (gridColorNode == null)
            {
                gridColorNode = _Globals.Config.CreateElement("GridColor");
                mapSettings2D.AppendChild(gridColorNode);
            }
            gridColorNode.InnerText = ColorTranslator.ToHtml(pnl2DGridColor.BackColor);

            XmlNode? gridWidthNode = mapSettings2D.SelectSingleNode("GridWidth");
            if (gridWidthNode == null)
            {
                gridWidthNode = _Globals.Config.CreateElement("GridWidth");
                mapSettings2D.AppendChild(gridWidthNode);
            }
            gridWidthNode.InnerText = txt2DGridWidth.Text;

            XmlNode? nAxisTicksNode = mapSettings2D.SelectSingleNode("NAxisTicks");
            if (nAxisTicksNode == null)
            {
                nAxisTicksNode = _Globals.Config.CreateElement("NAxisTicks");
                mapSettings2D.AppendChild(nAxisTicksNode);
            }
            nAxisTicksNode.InnerText = num2DNAxisTicks.Value.ToString();

            XmlNode? tickFontSizeNode = mapSettings2D.SelectSingleNode("TickFontSize");
            if (tickFontSizeNode == null)
            {
                tickFontSizeNode = _Globals.Config.CreateElement("TickFontSize");
                mapSettings2D.AppendChild(tickFontSizeNode);
            }
            tickFontSizeNode.InnerText = num2DTickFontSize.Value.ToString();

            XmlNode? tickNDecimalsNode = mapSettings2D.SelectSingleNode("TickNDecimals");
            if (tickNDecimalsNode == null)
            {
                tickNDecimalsNode = _Globals.Config.CreateElement("TickNDecimals");
                mapSettings2D.AppendChild(tickNDecimalsNode);
            }
            tickNDecimalsNode.InnerText = num2DNTicksDecimals.Value.ToString();

            XmlNode? axisLabelFontSizeNode = mapSettings2D.SelectSingleNode("AxisLabelFontSize");
            if (axisLabelFontSizeNode == null)
            {
                axisLabelFontSizeNode = _Globals.Config.CreateElement("AxisLabelFontSize");
                mapSettings2D.AppendChild(axisLabelFontSizeNode);
            }
            axisLabelFontSizeNode.InnerText = num2DAxisLabelFontSize.Value.ToString();

            XmlNode? axisLabelColorNode = mapSettings2D.SelectSingleNode("AxisLabelColor");
            if (axisLabelColorNode == null)
            {
                axisLabelColorNode = _Globals.Config.CreateElement("AxisLabelColor");
                mapSettings2D.AppendChild(axisLabelColorNode);
            }
            axisLabelColorNode.InnerText = ColorTranslator.ToHtml(pnl2DAxisLabelColor.BackColor);

            XmlNode? hoverFontSizeNode = mapSettings2D.SelectSingleNode("HoverFontSize");
            if (hoverFontSizeNode == null)
            {
                hoverFontSizeNode = _Globals.Config.CreateElement("HoverFontSize");
                mapSettings2D.AppendChild(hoverFontSizeNode);
            }
            hoverFontSizeNode.InnerText = num2DHoverFontSize.Value.ToString();

            XmlNode? transectLineWidthNode = mapSettings2D.SelectSingleNode("TransectLineWidth");
            if (transectLineWidthNode == null)
            {
                transectLineWidthNode = _Globals.Config.CreateElement("TransectLineWidth");
                mapSettings2D.AppendChild(transectLineWidthNode);
            }
            transectLineWidthNode.InnerText = txt2DTransectLineWidth.Text;

            XmlNode? verticalAggBinItemNode = mapSettings2D.SelectSingleNode("VerticalAggBinItem");
            if (verticalAggBinItemNode == null)
            {
                verticalAggBinItemNode = _Globals.Config.CreateElement("VerticalAggBinItem");
                mapSettings2D.AppendChild(verticalAggBinItemNode);
            }
            verticalAggBinItemNode.InnerText = getValueByIndex(combo2DBins, combo2DBins.SelectedIndex);

            XmlNode? verticalAggBinTargetNode = mapSettings2D.SelectSingleNode("VerticalAggBinTarget");
            if (verticalAggBinTargetNode == null)
            {
                verticalAggBinTargetNode = _Globals.Config.CreateElement("VerticalAggBinTarget");
                mapSettings2D.AppendChild(verticalAggBinTargetNode);
            }
            if (check2DBins.Checked)
                verticalAggBinTargetNode.InnerText = "Mean";
            else
            {
                if (combo2DBins.SelectedIndex == 0)
                    verticalAggBinTargetNode.InnerText = num2DBins.Value.ToString();
                else
                    verticalAggBinTargetNode.InnerText = txt2DDepth.Text;
            }

            XmlNode? verticalAggBeamNode = mapSettings2D.SelectSingleNode("VerticalAggBeam");
            if (verticalAggBeamNode == null)
            {
                verticalAggBeamNode = _Globals.Config.CreateElement("VerticalAggBeam");
                mapSettings2D.AppendChild(verticalAggBeamNode);
            }
            if (check2DBeams.Checked)
                verticalAggBeamNode.InnerText = "Mean";
            else
                verticalAggBeamNode.InnerText = num2DBeams.Value.ToString();
            // Surveys
            XmlNode? surveysNode = mapSettings2D.SelectSingleNode("Surveys");
            if (surveysNode != null)
            {
                XmlNodeList surveys = surveysNode.SelectNodes("Survey");
                foreach (XmlNode s in surveys)
                {
                    surveysNode.RemoveChild(s);
                }
            }
            else
            {
                surveysNode = _Globals.Config.CreateElement("Surveys");
                mapSettings2D.AppendChild(surveysNode);
            }
            foreach (TreeNode surveyNode in treeSurveys2D.Nodes)
            {
                if (surveyNode.Checked)
                {
                    XmlElement? surveyElem = surveyNode.Tag as XmlElement;
                    if (surveyElem != null)
                    {
                        string id = surveyElem.GetAttribute("id");
                        XmlElement newSurveyNode = _Globals.Config.CreateElement("Survey");
                        XmlElement idNode = _Globals.Config.CreateElement("ID");
                        idNode.InnerText = id;
                        newSurveyNode.AppendChild(idNode);
                        surveysNode.AppendChild(newSurveyNode);
                    }
                }
            }
        }

        private void SaveSettings3D()
        {
            XmlNode? bkgColorNode = mapSettings3D.SelectSingleNode("BackgroundColor");
            if (bkgColorNode == null)
            {
                bkgColorNode = _Globals.Config.CreateElement("BackgroundColor");
                mapSettings3D.AppendChild(bkgColorNode);
            }
            bkgColorNode.InnerText = ColorTranslator.ToHtml(pnl3DBackColor.BackColor);

            XmlNode? fieldNameNode = mapSettings3D.SelectSingleNode("FieldName");
            if (fieldNameNode == null)
            {
                fieldNameNode = _Globals.Config.CreateElement("FieldName");
                mapSettings3D.AppendChild(fieldNameNode);
            }
            fieldNameNode.InnerText = getValueByIndex(combo3DFieldName, combo3DFieldName.SelectedIndex);

            XmlNode? cmapNode = mapSettings3D.SelectSingleNode("Colormap");
            if (cmapNode == null)
            {
                cmapNode = _Globals.Config.CreateElement("Colormap");
                mapSettings3D.AppendChild(cmapNode);
            }
            cmapNode.InnerText = ((ColormapItem)combo3Dcmap.SelectedItem).Name;

            XmlNode? vminNode = mapSettings3D.SelectSingleNode("vmin");
            if (vminNode == null)
            {
                vminNode = _Globals.Config.CreateElement("vmin");
                mapSettings3D.AppendChild(vminNode);
            }
            vminNode.InnerText = txt3Dvmin.Text;

            XmlNode? vmaxNode = mapSettings3D.SelectSingleNode("vmax");
            if (vmaxNode == null)
            {
                vmaxNode = _Globals.Config.CreateElement("vmax");
                mapSettings3D.AppendChild(vmaxNode);
            }
            vmaxNode.InnerText = txt3Dvmax.Text;

            XmlNode? paddingNode = mapSettings3D.SelectSingleNode("Padding");
            if (paddingNode == null)
            {
                paddingNode = _Globals.Config.CreateElement("Padding");
                mapSettings3D.AppendChild(paddingNode);
            }
            paddingNode.InnerText = txt3DPagDeg.Text;

            XmlNode? nGridLinesNode = mapSettings3D.SelectSingleNode("NGridLines");
            if (nGridLinesNode == null)
            {
                nGridLinesNode = _Globals.Config.CreateElement("NGridLines");
                mapSettings3D.AppendChild(nGridLinesNode);
            }
            nGridLinesNode.InnerText = num3DNGridLines.Value.ToString();

            XmlNode? gridOpacityNode = mapSettings3D.SelectSingleNode("GridOpacity");
            if (gridOpacityNode == null)
            {
                gridOpacityNode = _Globals.Config.CreateElement("GridOpacity");
                mapSettings3D.AppendChild(gridOpacityNode);
            }
            gridOpacityNode.InnerText = txt3DGridOpacity.Text;

            XmlNode? gridColorNode = mapSettings3D.SelectSingleNode("GridColor");
            if (gridColorNode == null)
            {
                gridColorNode = _Globals.Config.CreateElement("GridColor");
                mapSettings3D.AppendChild(gridColorNode);
            }
            gridColorNode.InnerText = ColorTranslator.ToHtml(pnl3DGridColor.BackColor);

            XmlNode? gridWidthNode = mapSettings3D.SelectSingleNode("GridWidth");
            if (gridWidthNode == null)
            {
                gridWidthNode = _Globals.Config.CreateElement("GridWidth");
                mapSettings3D.AppendChild(gridWidthNode);
            }
            gridWidthNode.InnerText = txt3DGridWidth.Text;

            XmlNode? nAxisTicksNode = mapSettings3D.SelectSingleNode("NAxisTicks");
            if (nAxisTicksNode == null)
            {
                nAxisTicksNode = _Globals.Config.CreateElement("NAxisTicks");
                mapSettings3D.AppendChild(nAxisTicksNode);
            }
            nAxisTicksNode.InnerText = num3DNAxisTicks.Value.ToString();

            XmlNode? tickFontSizeNode = mapSettings3D.SelectSingleNode("TickFontSize");
            if (tickFontSizeNode == null)
            {
                tickFontSizeNode = _Globals.Config.CreateElement("TickFontSize");
                mapSettings3D.AppendChild(tickFontSizeNode);
            }
            tickFontSizeNode.InnerText = num3DTickFontSize.Value.ToString();

            XmlNode? tickNDecimalsNode = mapSettings3D.SelectSingleNode("TickNDecimals");
            if (tickNDecimalsNode == null)
            {
                tickNDecimalsNode = _Globals.Config.CreateElement("TickNDecimals");
                mapSettings3D.AppendChild(tickNDecimalsNode);
            }
            tickNDecimalsNode.InnerText = num3DNTicksDecimals.Value.ToString();

            XmlNode? axisLabelFontSizeNode = mapSettings3D.SelectSingleNode("AxisLabelFontSize");
            if (axisLabelFontSizeNode == null)
            {
                axisLabelFontSizeNode = _Globals.Config.CreateElement("AxisLabelFontSize");
                mapSettings3D.AppendChild(axisLabelFontSizeNode);
            }
            axisLabelFontSizeNode.InnerText = num3DAxisLabelFontSize.Value.ToString();

            XmlNode? axisLabelColorNode = mapSettings3D.SelectSingleNode("AxisLabelColor");
            if (axisLabelColorNode == null)
            {
                axisLabelColorNode = _Globals.Config.CreateElement("AxisLabelColor");
                mapSettings3D.AppendChild(axisLabelColorNode);
            }
            axisLabelColorNode.InnerText = ColorTranslator.ToHtml(pnl3DAxisLabelColor.BackColor);

            XmlNode? hoverFontSizeNode = mapSettings3D.SelectSingleNode("HoverFontSize");
            if (hoverFontSizeNode == null)
            {
                hoverFontSizeNode = _Globals.Config.CreateElement("HoverFontSize");
                mapSettings3D.AppendChild(hoverFontSizeNode);
            }
            hoverFontSizeNode.InnerText = num3DHoverFontSize.Value.ToString();

            XmlNode? zScaleNode = mapSettings3D.SelectSingleNode("ZScale");
            if (zScaleNode == null)
            {
                zScaleNode = _Globals.Config.CreateElement("ZScale");
                mapSettings3D.AppendChild(zScaleNode);
            }
            zScaleNode.InnerText = txt3DZScale.Text;

            // Surveys
            XmlNode? surveysNode = mapSettings3D.SelectSingleNode("Surveys");
            if (surveysNode != null)
            {
                XmlNodeList surveys = surveysNode.SelectNodes("Survey");
                foreach (XmlNode s in surveys)
                {
                    surveysNode.RemoveChild(s);
                }
            }
            else
            {
                surveysNode = _Globals.Config.CreateElement("Surveys");
                mapSettings3D.AppendChild(surveysNode);
            }
            foreach (TreeNode surveyNode in treeSurveys3D.Nodes)
            {
                if (surveyNode.Checked)
                {
                    XmlElement? surveyElem = surveyNode.Tag as XmlElement;
                    if (surveyElem != null)
                    {
                        string id = surveyElem.GetAttribute("id");
                        XmlElement newSurveyNode = _Globals.Config.CreateElement("Survey");
                        XmlElement idNode = _Globals.Config.CreateElement("ID");
                        idNode.InnerText = id;
                        newSurveyNode.AppendChild(idNode);
                        surveysNode.AppendChild(newSurveyNode);
                    }
                }
            }
        }

        private void SaveSettingsShp()
        {
            // Shapefiles
            XmlNodeList? shapefilesNode = mapShapefiles.SelectNodes("Shapefile");
            if (shapefilesNode != null)
            {
                foreach (XmlNode shpNode in shapefilesNode)
                {
                    mapShapefiles.RemoveChild(shpNode);
                }
            }
            foreach (TreeNode shpNode in treeShapefiles.Nodes)
            {
                ShapeFile? shp = shpNode.Tag as ShapeFile;
                if (shp != null)
                {
                    XmlElement newShpNode = _Globals.Config.CreateElement("Shapefile");
                    newShpNode.SetAttribute("visible", shpNode.Checked ? "true" : "false");
                    XmlElement nameNode = _Globals.Config.CreateElement("Name");
                    nameNode.InnerText = shp.Name;
                    newShpNode.AppendChild(nameNode);
                    XmlElement pathNode = _Globals.Config.CreateElement("Path");
                    pathNode.InnerText = shp.Path;
                    newShpNode.AppendChild(pathNode);
                    XmlElement kindNode = _Globals.Config.CreateElement("Kind");
                    kindNode.InnerText = shp.Kind;
                    newShpNode.AppendChild(kindNode);
                    if (shp.Kind == "Point")
                    {
                        XmlElement pointColorNode = _Globals.Config.CreateElement("PointColor");
                        pointColorNode.InnerText = shp.PointColor;
                        newShpNode.AppendChild(pointColorNode);
                        XmlElement pointMarkerNode = _Globals.Config.CreateElement("PointMarker");
                        pointMarkerNode.InnerText = shp.PointMarker;
                        newShpNode.AppendChild(pointMarkerNode);
                        XmlElement pointMarkerSizeNode = _Globals.Config.CreateElement("PointMarkerSize");
                        pointMarkerSizeNode.InnerText = shp.PointMarkerSize;
                        newShpNode.AppendChild(pointMarkerSizeNode);
                        XmlElement pointAlphaNode = _Globals.Config.CreateElement("PointAlpha");
                        pointAlphaNode.InnerText = shp.PointAlpha;
                        newShpNode.AppendChild(pointAlphaNode);
                    }
                    else if (shp.Kind == "Line")
                    {
                        XmlElement lineColorNode = _Globals.Config.CreateElement("LineColor");
                        lineColorNode.InnerText = shp.LineColor;
                        newShpNode.AppendChild(lineColorNode);
                        XmlElement lineLineWidthNode = _Globals.Config.CreateElement("LineLineWidth");
                        lineLineWidthNode.InnerText = shp.LineLineWidth;
                        newShpNode.AppendChild(lineLineWidthNode);
                        XmlElement lineAlphaNode = _Globals.Config.CreateElement("LineAlpha");
                        lineAlphaNode.InnerText = shp.LineAlpha;
                        newShpNode.AppendChild(lineAlphaNode);
                    }
                    else if (shp.Kind == "Polygon")
                    {
                        XmlElement polyEdgeColorNode = _Globals.Config.CreateElement("PolyEdgeColor");
                        polyEdgeColorNode.InnerText = shp.PolyEdgeColor;
                        newShpNode.AppendChild(polyEdgeColorNode);
                        XmlElement polyLineWidthNode = _Globals.Config.CreateElement("PolyLineWidth");
                        polyLineWidthNode.InnerText = shp.PolyLineWidth;
                        newShpNode.AppendChild(polyLineWidthNode);
                        XmlElement polyFaceColorNode = _Globals.Config.CreateElement("PolyFaceColor");
                        polyFaceColorNode.InnerText = shp.PolyFaceColor;
                        newShpNode.AppendChild(polyFaceColorNode);
                        XmlElement polyAlphaNode = _Globals.Config.CreateElement("PolyAlpha");
                        polyAlphaNode.InnerText = shp.PolyAlpha;
                        newShpNode.AppendChild(polyAlphaNode);
                    }
                    XmlElement labelTextNode = _Globals.Config.CreateElement("LabelText");
                    labelTextNode.InnerText = shp.LabelText;
                    newShpNode.AppendChild(labelTextNode);
                    XmlElement labelFontSizeNode = _Globals.Config.CreateElement("LabelFontSize");
                    labelFontSizeNode.InnerText = shp.LabelFontSize;
                    newShpNode.AppendChild(labelFontSizeNode);
                    XmlElement labelColorNode = _Globals.Config.CreateElement("LabelColor");
                    labelColorNode.InnerText = shp.LabelColor;
                    newShpNode.AppendChild(labelColorNode);
                    XmlElement labelHANode = _Globals.Config.CreateElement("LabelHA");
                    labelHANode.InnerText = shp.LabelHA;
                    newShpNode.AppendChild(labelHANode);
                    XmlElement labelVANode = _Globals.Config.CreateElement("LabelVA");
                    labelVANode.InnerText = shp.LabelVA;
                    newShpNode.AppendChild(labelVANode);
                    XmlElement labelOffsetPointsXNode = _Globals.Config.CreateElement("LabelOffsetPointsX");
                    labelOffsetPointsXNode.InnerText = shp.LabelOffsetPointsX;
                    newShpNode.AppendChild(labelOffsetPointsXNode);
                    XmlElement labelOffsetPointsYNode = _Globals.Config.CreateElement("LabelOffsetPointsY");
                    labelOffsetPointsYNode.InnerText = shp.LabelOffsetPointsY;
                    newShpNode.AppendChild(labelOffsetPointsYNode);
                    XmlElement labelOffsetDataXNode = _Globals.Config.CreateElement("LabelOffsetDataX");
                    labelOffsetDataXNode.InnerText = shp.LabelOffsetDataX;
                    newShpNode.AppendChild(labelOffsetDataXNode);
                    XmlElement labelOffsetDataYNode = _Globals.Config.CreateElement("LabelOffsetDataY");
                    labelOffsetDataYNode.InnerText = shp.LabelOffsetDataY;
                    newShpNode.AppendChild(labelOffsetDataYNode);
                    mapShapefiles.AppendChild(newShpNode);
                }
            }
        }

        private void SaveSettings()
        {
            SaveSettings2D();
            SaveSettings3D();
            SaveSettingsShp();
            string name = _project.GetSetting("Name");
            string mapViewer2DPath = Path.Combine(_Globals.dataPath, "PlumeTrack", $"MapViewer2D_{name}.html");
            string mapViewer3DPath = Path.Combine(_Globals.dataPath, "PlumeTrack", $"MapViewer3D_{name}.html");
            if (File.Exists(mapViewer2DPath))
                File.Delete(mapViewer2DPath);
            if (File.Exists(mapViewer3DPath))
                File.Delete(mapViewer3DPath);
            isSaved = true;
            _project.SaveConfig(saveMode: 1);
        }

        private void AddShapeFileToTree(ShapeFile shp, bool Checked)
        {
            TreeNode nodeElement = new TreeNode(shp.Name);
            nodeElement.Tag = shp;
            treeShapefiles.Nodes.Add(nodeElement);
            nodeElement.Checked = Checked;
            AddShapeFileTable(shp);
        }

        private int AddShapeFileTable(ShapeFile shp)
        {
            splitShp.Panel2.Controls.Clear();
            if (shp.Kind == "Point")
            {
                splitShp.Panel2.Controls.Add(tableShpPoint);
                txtShpPointPath.Text = shp.Path;
                txtShpPointType.Text = shp.Kind;
                pnlShpPointColor.BackColor = ColorTranslator.FromHtml(shp.PointColor);
                selectComboByValue(comboShpPointMarker, shp.PointMarker);
                numShpPointMarkerSize.Value = int.Parse(shp.PointMarkerSize);
                numShpPointMarkerAlpha.Value = decimal.Parse(shp.PointAlpha);
            }
            else if (shp.Kind == "Line")
            {
                splitShp.Panel2.Controls.Add(tableShpLine);
                txtShpLinePath.Text = shp.Path;
                txtShpLineType.Text = shp.Kind;
                pnlShpLineColor.BackColor = ColorTranslator.FromHtml(shp.LineColor);
                txtShpLineLineWidth.Text = shp.LineLineWidth;
                numShpLineAlpha.Value = decimal.Parse(shp.LineAlpha);
            }

            else if (shp.Kind == "Polygon")
            {
                splitShp.Panel2.Controls.Add(tableShpPoly);
                txtShpPolyPath.Text = shp.Path;
                txtShpPolyType.Text = shp.Kind;
                pnlShpPolyEdgeColor.BackColor = ColorTranslator.FromHtml(shp.PolyEdgeColor);
                txtShpPolyLineWidth.Text = shp.PolyLineWidth;
                pnlShpPolyFaceColor.BackColor = ColorTranslator.FromHtml(shp.PolyFaceColor);
                numShpPolyAlpha.Value = decimal.Parse(shp.PolyAlpha);
            }
            else
            {
                MessageBox.Show("The shapefile type " + shp.Kind + " is not supported.");
                return 0;
            }
            txtShpLabelText.Text = shp.LabelText;
            numShpLabelFontSize.Value = int.Parse(shp.LabelFontSize);
            pnlShpLabelColor.BackColor = ColorTranslator.FromHtml(shp.LabelColor);
            selectComboByValue(comboShpLabelHA, shp.LabelHA);
            selectComboByValue(comboShpLabelVA, shp.LabelVA);
            txtShpLabelOffsetPointsX.Text = shp.LabelOffsetPointsX;
            txtShpLabelOffsetPointsY.Text = shp.LabelOffsetPointsY;
            txtShpLabelOffsetDataX.Text = shp.LabelOffsetDataX;
            txtShpLabelOffsetDataY.Text = shp.LabelOffsetDataY;
            return 1;
        }

        private void btnShpAddShapefile_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog
            {
                Title = "Select Shapefile",
                Filter = "Shapefiles (*.shp)|*.shp",
                Multiselect = false,
                InitialDirectory = _project.GetSetting("Directory")
            };
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                string selectedPath = ofd.FileName;
                string selectedType = GetShapeType(selectedPath);
                string selectedName = Path.GetFileNameWithoutExtension(selectedPath);
                ShapeFile shp = new ShapeFile(name: selectedName, path: selectedPath, kind: selectedType);
                AddShapeFileToTree(shp, true);
            }
        }

        private void colorButton_Click(object sender, EventArgs e)
        {
            Button? btn = sender as Button;
            if (btn == null) return;
            Panel? pnl;
            if (btn.Name == "btn2DBackColor")
                pnl = pnl2DBackColor;
            else if (btn.Name == "btn2DGridColor")
                pnl = pnl2DGridColor;
            else if (btn.Name == "btn2DAxisLabelColor")
                pnl = pnl2DAxisLabelColor;
            else if (btn.Name == "btn3DBackColor")
                pnl = pnl3DBackColor;
            else if (btn.Name == "btn3DGridColor")
                pnl = pnl3DGridColor;
            else if (btn.Name == "btn3DAxisLabelColor")
                pnl = pnl3DAxisLabelColor;
            else if (btn.Name == "btnShpPointColor")
                pnl = pnlShpPointColor;
            else if (btn.Name == "btnShpLabelColor")
                pnl = pnlShpLabelColor;
            else if (btn.Name == "btnShpLineColor")
                pnl = pnlShpLineColor;
            else if (btn.Name == "btnShpPolyEdgeColor")
                pnl = pnlShpPolyEdgeColor;
            else if (btn.Name == "btnShpPolyFaceColor")
                pnl = pnlShpPolyFaceColor;
            else
                return;
            ColorDialog colorDialog = new ColorDialog
            {
                AllowFullOpen = true,
                AnyColor = true,
                FullOpen = true,
                Color = pnl.BackColor,
            };
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                pnl.BackColor = colorDialog.Color;
            }
        }

        private void pnlBackColor_Changed(object sender, EventArgs e)
        {
            Panel? panel = sender as Panel;
            if (panel == null) return;
            if (panel.Name.Contains("Shp"))
            {
                ShapeFile? shp = treeShapefiles.SelectedNode?.Tag as ShapeFile;
                if (shp == null) return;
                if (panel.Name == "pnlShpPointColor")
                    shp.PointColor = ColorTranslator.ToHtml(panel.BackColor);
                else if (panel.Name == "pnlShpLabelColor")
                    shp.LabelColor = ColorTranslator.ToHtml(panel.BackColor);
                else if (panel.Name == "pnlShpLineColor")
                    shp.LineColor = ColorTranslator.ToHtml(panel.BackColor);
                else if (panel.Name == "pnlShpPolyEdgeColor")
                    shp.PolyEdgeColor = ColorTranslator.ToHtml(panel.BackColor);
                else if (panel.Name == "pnlShpPolyFaceColor")
                    shp.PolyFaceColor = ColorTranslator.ToHtml(panel.BackColor);
            }
            isSaved = false;
        }

        private void treeShapefiles_NodeMouseClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            ShapeFile? shp = e.Node.Tag as ShapeFile;
            if (shp == null) return;
            AddShapeFileTable(shp);
        }

        private void input_Changed(object sender, EventArgs e)
        {
            isSaved = false;
        }

        private void txtShp_TextChanged(object sender, EventArgs e)
        {
            TextBox? txt = sender as TextBox;
            if (txt == null) return;
            ShapeFile? shp = treeShapefiles.SelectedNode?.Tag as ShapeFile;
            if (shp == null) return;
            if (txt.Name == "txtShpPointPath" || txt.Name == "txtShpLinePath" || txt.Name == "txtShpPolyPath")
                shp.Path = txt.Text;
            else if (txt.Name == "txtShpPointType" || txt.Name == "txtShpLineType" || txt.Name == "txtShpPolyType")
                shp.Kind = txt.Text;
            else if (txt.Name == "txtShpLineLineWidth")
                shp.LineLineWidth = txt.Text;
            else if (txt.Name == "txtShpPolyLineWidth")
                shp.PolyLineWidth = txt.Text;
            else if (txt.Name == "txtShpLabelText")
                shp.LabelText = txt.Text;
            else if (txt.Name == "txtShpLabelOffsetPointsX")
                shp.LabelOffsetPointsX = txt.Text;
            else if (txt.Name == "txtShpLabelOffsetPointsY")
                shp.LabelOffsetPointsY = txt.Text;
            else if (txt.Name == "txtShpLabelOffsetDataX")
                shp.LabelOffsetDataX = txt.Text;
            else if (txt.Name == "txtShpLabelOffsetDataY")
                shp.LabelOffsetDataY = txt.Text;
            isSaved = false;
        }

        private void comboShp_SelectedIndexChanged(object sender, EventArgs e)
        {
            ComboBox? combo = sender as ComboBox;
            if (combo == null) return;
            ShapeFile? shp = treeShapefiles.SelectedNode?.Tag as ShapeFile;
            if (shp == null) return;
            if (combo.Name == "comboShpPointMarker")
                shp.PointMarker = combo.SelectedItem.ToString();
            else if (combo.Name == "comboShpLabelHA")
                shp.LabelHA = combo.SelectedItem.ToString();
            else if (combo.Name == "comboShpLabelVA")
                shp.LabelVA = combo.SelectedItem.ToString();
            isSaved = false;
        }

        private void numShp_ValueChanged(object sender, EventArgs e)
        {
            NumericUpDown? num = sender as NumericUpDown;
            if (num == null) return;
            ShapeFile? shp = treeShapefiles.SelectedNode?.Tag as ShapeFile;
            if (shp == null) return;
            if (num.Name == "numShpPointMarkerSize")
                shp.PointMarkerSize = num.Value.ToString();
            else if (num.Name == "numShpPointMarkerAlpha")
                shp.PointAlpha = num.Value.ToString();
            else if (num.Name == "numShpLineAlpha")
                shp.LineAlpha = num.Value.ToString();
            else if (num.Name == "numShpPolyAlpha")
                shp.PolyAlpha = num.Value.ToString();
            else if (num.Name == "numShpLabelFontSize")
                shp.LabelFontSize = num.Value.ToString();
            isSaved = false;
        }

        private void treeShapefiles_AfterSelect(object sender, TreeViewEventArgs e)
        {
            if (treeShapefiles.SelectedNode != null)
            {
                ShapeFile? shp = treeShapefiles.SelectedNode.Tag as ShapeFile;
                if (shp != null)
                {
                    AddShapeFileTable(shp);
                }
            }
            else
            {
                splitShp.Panel2.Controls.Clear();
            }
        }
    }
}
