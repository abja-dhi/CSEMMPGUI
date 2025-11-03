using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net.NetworkInformation;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using DHI.Generic.MikeZero;
using DHI.Generic.MikeZero.DFS;
using DHI.Generic.MikeZero.DFS.dfs123;
using DHI.Generic.MikeZero.DFS.dfsu;
using DHI.Generic.MikeZero.DFS.mesh;
using DHI.Math.Expression.Operations;

namespace CSEMMPGUI_v1
{
    public partial class ProjectPlot : Form
    {
        public XmlNodeList? hdModels;
        public XmlElement? hdModel;
        public XmlNodeList? mtModels;
        public XmlElement? mtModel;
        public XmlNodeList? adcps;
        public XmlElement? adcp;
        public _ClassConfigurationManager _project = new();

        public static Label MakeLabel(string name, string text)
        {
            Label lbl = new Label();
            lbl.Name = name;
            lbl.Text = text;
            lbl.Dock = DockStyle.Fill;
            lbl.TextAlign = ContentAlignment.MiddleLeft;
            return lbl;
        }

        public static ComboBox MakeCombo(string name, string[] items)
        {
            ComboBox combo = new ComboBox();
            combo.Name = name;
            combo.Dock = DockStyle.Fill;
            combo.DropDownStyle = ComboBoxStyle.DropDownList;
            combo.FormattingEnabled = true;
            combo.Items.AddRange(items);
            if (items.Length > 0)
                combo.SelectedIndex = 0;
            return combo;
        }

        public static ComboBox MakeComboCmap(string name)
        {
            ComboBox combocmap = new ComboBox();
            combocmap.Dock = DockStyle.Fill;
            combocmap.DropDownStyle = ComboBoxStyle.DropDownList;
            combocmap.FormattingEnabled = true;
            combocmap.Name = name;
            combocmap.DrawMode = DrawMode.OwnerDrawFixed;
            combocmap.ItemHeight = 24; // more room for image
            string[] pngs = Directory.GetFiles(_Globals.CMapsPath, "*.png");
            foreach (string png in pngs) {
                string cmapName = Path.GetFileNameWithoutExtension(png);
                combocmap.Items.Add(new ColormapItem(cmapName, Image.FromFile(png)));
            }
            combocmap.SelectedIndex = 0;
            combocmap.DrawItem += (s, e) =>
            {
                if (e.Index < 0) return;

                e.DrawBackground();
                var item = (ColormapItem)combocmap.Items[e.Index];

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
            return combocmap;
        }

        public static TextBox MakeTextBox(string name, string text)
        {
            TextBox txt = new TextBox();
            txt.Name = name;
            txt.Dock = DockStyle.Fill;
            txt.Text = text;
            return txt;
        }

        public static NumericUpDown MakeNumericUpDown(string name, decimal min, decimal max, decimal value)
        {
            NumericUpDown num = new NumericUpDown();
            num.Name = name;
            num.Dock = DockStyle.Fill;
            num.Minimum = min;
            num.Maximum = max;
            num.Value = value;
            return num;
        }

        public static Button MakeButton(string name, string text)
        {
            Button btn = new Button();
            btn.Name = name;
            btn.Text = text;
            btn.Dock = DockStyle.Fill;
            return btn;
        }

        public static Panel MakePanel(string name, Color color)
        {
            Panel pnl = new Panel();
            pnl.Name = name;
            pnl.BackColor = color;
            pnl.BorderStyle = BorderStyle.FixedSingle;
            pnl.Dock = DockStyle.Fill;
            return pnl;
        }

        public static CheckBox MakeCheckBox(string name, string text, bool isChecked)
        {
            CheckBox chk = new CheckBox();
            chk.Name = name;
            chk.Text = text;
            chk.Dock = DockStyle.Fill;
            chk.Checked = isChecked;
            chk.TextAlign = ContentAlignment.MiddleCenter;
            return chk;
        }

        public static GroupBox MakeGroupBox(string name, string text)
        {
            GroupBox grp = new GroupBox();
            grp.Name = name;
            grp.Text = text;
            grp.Dock = DockStyle.Fill;
            return grp;
        }

        public static TableLayoutPanel MakeTable(string name)
        {
            TableLayoutPanel table = new TableLayoutPanel();
            table.Name = name;
            table.Dock = DockStyle.Fill;
            table.ColumnCount = 3;
            table.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            table.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40F));
            table.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 10F));
            return table;
        }

        public GroupBox? grpRequired = MakeGroupBox(name: "grpRequired", text: "Required Inputs");
        public GroupBox? grpMT = MakeGroupBox(name: "grpMT", text: "MT Inputs");
        public GroupBox? grpHD = MakeGroupBox(name: "grpHD", text: "HD Inputs");
        public GroupBox? grpADCP = MakeGroupBox(name: "grpADCP", text: "ADCP Inputs");
        public GroupBox? grpLayout = MakeGroupBox(name: "grpLayout", text: "Layout");
        public GroupBox? grpAnimation = MakeGroupBox(name: "grpAnimation", text: "Animation");
        public TableLayoutPanel? tableRequired = MakeTable(name: "tableRequired");
        public TableLayoutPanel? tableMT = MakeTable(name: "tableMT");
        public TableLayoutPanel? tableHD = MakeTable(name: "tableHD");
        public TableLayoutPanel? tableADCP = MakeTable(name: "tableADCP");
        public TableLayoutPanel? tableLayout = MakeTable(name: "tableLayout");
        public TableLayoutPanel? tableAnimation = MakeTable(name: "tableAnimation");

        // Required Inputs
        public Label? lblHDModel = MakeLabel(name: "lblHDModel", text: "HD Model");
        public ComboBox? comboHDModel = MakeCombo(name: "comboHDModel", items: Array.Empty<string>());
        public Label? lblMTModel = MakeLabel(name: "lblMTModel", text: "MT Model");
        public ComboBox? comboMTModel = MakeCombo(name: "comboMTModel", items: Array.Empty<string>());
        public Label? lblADCP = MakeLabel(name: "lblADCP", text: "ADCP");
        public ComboBox? comboADCP = MakeCombo(name: "comboADCP", items: Array.Empty<string>());
        // MT Inputs
        public Label? lblSSCScale = MakeLabel(name: "lblSSCScale", text: "SSC Scale");
        public ComboBox? comboSSCScale = MakeCombo(name: "comboSSCScale", items: new string[] { "Normal", "Logarithmic" });
        public Label? lblSSCLevels = MakeLabel(name: "lblSSCLevels", text: "SSC Levels");
        public TextBox? txtSSCLevels = MakeTextBox(name: "txtSSCLevels", text: "0.01,0.1,1.0,10.0");
        public Label? lblSSCvmin = MakeLabel(name: "lblSSCvmin", text: "vmin");
        public TextBox? txtSSCvmin = MakeTextBox(name: "txtSSCvmin", text: "");
        public Label? lblSSCvmax = MakeLabel(name: "lblSSCvmax", text: "vmax");
        public TextBox? txtSSCvmax = MakeTextBox(name: "txtSSCvmax", text: "");
        public Label? lblSSCCmap = MakeLabel(name: "lblSSCCmap", text: "SSC Colormap");
        public ComboBox? comboSSCcmap = MakeComboCmap(name: "comboSSCcmap");
        public Label? lblSSCBottomThreshold = MakeLabel(name: "lblSSCBottomThreshold", text: "SSC Bottom Threshold");
        public TextBox? txtSSCBottomThreshold = MakeTextBox(name: "txtSSCBottomThreshold", text: "");
        public Label? lblSSCPixelSizeM = MakeLabel(name: "lblSSCPixelSizeM", text: "SSC Pixel Size (m)");
        public TextBox? txtSSCPixelSizeM = MakeTextBox(name: "txtSSCPixelSizeM", text: "10");
        // HD Inputs
        public Label? lblModelFieldPixelSizeM = MakeLabel(name: "lblModelFieldPixelSizeM", text: "Model Field Pixel Size (m)");
        public TextBox? txtModelFieldPixelSizeM = MakeTextBox(name: "txtModelFieldPixelSizeM", text: "100");
        public Label? lblModelFieldQuiverStrideN = MakeLabel(name: "lblModelFieldQuiverStrideN", text: "Model Field Quiver Stride N");
        public NumericUpDown? numModelFieldQuiverStrideN = MakeNumericUpDown(name: "numModelFieldQuiverStrideN", min: 1, max: 20, value: 3);
        public Label? lblModelQuiverMode = MakeLabel(name: "lblModelQuiverMode", text: "Model Quiver Mode");
        public ComboBox? comboModelQuiverMode = MakeCombo(name: "comboModelQuiverMode", items: new string[] { "Field", "Transect" });
        public Label? lblModelQuiverScale = MakeLabel(name: "lblModelQuiverScale", text: "Model Quiver Scale");
        public TextBox? txtModelQuiverScale = MakeTextBox(name: "txtModelQuiverScale", text: "3");
        public Label? lblModelQuiverWidth = MakeLabel(name: "lblModelQuiverWidth", text: "Model Quiver Width");
        public TextBox? txtModelQuiverWidth = MakeTextBox(name: "txtModelQuiverWidth", text: "0.002");
        public Label? lblModelQuiverHeadWidth = MakeLabel(name: "lblModelQuiverHeadWidth", text: "Model Quiver Head Width");
        public TextBox? txtModelQuiverHeadWidth = MakeTextBox(name: "txtModelQuiverHeadWidth", text: "2");
        public Label? lblModelQuiverHeadLength = MakeLabel(name: "lblModelQuiverHeadLength", text: "Model Quiver Head Length");
        public TextBox? txtModelQuiverHeadLength = MakeTextBox(name: "txtModelQuiverHeadLength", text: "2.5");
        public Label? lblModelQuiverColor = MakeLabel(name: "lblModelQuiverColor", text: "Model Quiver Color");
        public Panel? pnlModelQuiverColor = MakePanel(name: "pnlModelQuiverColor", color: Color.Blue);
        public Button? btnModelQuiverColor = MakeButton(name: "btnModelQuiverColor", text: "...");
        public Label? lblModelLevels = MakeLabel(name: "lblModelLevels", text: "Model Velocity Levels");
        public TextBox? txtModelLevels = MakeTextBox(name: "txtModelLevels", text: "0.0,0.1,0.2,0.3,0.4,0.5");
        public Label? lblModelvmin = MakeLabel(name: "lblModelvmin", text: "vmin");
        public TextBox? txtModelvmin = MakeTextBox(name: "txtModelvmin", text: "");
        public Label? lblModelvmax = MakeLabel(name: "lblModelvmax", text: "vmax");
        public TextBox? txtModelvmax = MakeTextBox(name: "txtModelvmax", text: "");
        public Label? lblModelCmap = MakeLabel(name: "lblModelCmap", text: "Model Colormap");
        public ComboBox? comboModelCmap = MakeComboCmap(name: "comboModelCmap");
        public Label? lblModelCmapBottomThreshold = MakeLabel(name: "lblModelCmapBottomThreshold", text: "Model Colormap Bottom Threshold");
        public TextBox? txtModelCmapBottomThreshold = MakeTextBox(name: "txtModelCmapBottomThreshold", text: "");
        // ADCP
        public Label? lblADCPSeriesMode = MakeLabel(name: "lblADCPSeriesMode", text: "ADCP Series Mode");
        public ComboBox? comboADCPSeriesMode = MakeCombo(name: "comboADCPSeriesMode", items: new string[] { "Bin", "Depth" });
        public Label? lblADCPSeriesTarget = MakeLabel(name: "lblADCPSeriesTarget", text: "ADCP Series Target");
        public NumericUpDown? numADCPSeriesTarget = MakeNumericUpDown(name: "numADCPSeriesTarget", min: 1, max: 100, value: 10);
        public TextBox? txtADCPSeriesTarget = MakeTextBox(name: "txtADCPSeriesTarget", text: "10");
        public CheckBox? checkADCPSeriesTarget = MakeCheckBox(name: "checkADCPSeriesTarget", text: "Mean", isChecked: false);
        public Label? lblADCPQuiverScale = MakeLabel(name: "lblADCPQuiverScale", text: "ADCP Quiver Scale");
        public TextBox? txtADCPQuiverScale = MakeTextBox(name: "txtADCPQuiverScale", text: "3");
        public Label? lblADCPQuiverWidth = MakeLabel(name: "lblADCPQuiverWidth", text: "ADCP Quiver Width");
        public TextBox? txtADCPQuiverWidth = MakeTextBox(name: "txtADCPQuiverWidth", text: "0.002");
        public Label? lblADCPQuiverHeadWidth = MakeLabel(name: "lblADCPQuiverHeadWidth", text: "ADCP Quiver Head Width");
        public TextBox? txtADCPQuiverHeadWidth = MakeTextBox(name: "txtADCPQuiverHeadWidth", text: "2");
        public Label? lblADCPQuiverHeadLength = MakeLabel(name: "lblADCPQuiverHeadLength", text: "ADCP Quiver Head Length");
        public TextBox? txtADCPQuiverHeadLength = MakeTextBox(name: "txtADCPQuiverHeadLength", text: "2.5");
        public Label? lblADCPQuiverColor = MakeLabel(name: "lblADCPQuiverColor", text: "ADCP Quiver Color");
        public Panel? pnlADCPQuiverColor = MakePanel(name: "pnlADCPQuiverColor", color: Color.Red);
        public Button? btnADCPQuiverColor = MakeButton(name: "btnADCPQuiverColor", text: "...");
        public Label? lblADCPTransectColor = MakeLabel(name: "lblADCPTransectColor", text: "ADCP Transect Color");
        public Panel? pnlADCPTransectColor = MakePanel(name: "pnlADCPTransectColor", color: Color.Green);
        public Button? btnADCPTransectColor = MakeButton(name: "btnADCPTransectColor", text: "...");
        public Label? lblADCPQuiverEveryN = MakeLabel(name: "lblADCPQuiverEveryN", text: "ADCP Quiver Every N");
        public NumericUpDown? numADCPQuiverEveryN = MakeNumericUpDown(name: "numADCPQuiverEveryN", min: 1, max: 20, value: 1);
        public Label? lblADCPTransectWidth = MakeLabel(name: "lblADCPTransectWidth", text: "ADCP Transect Line Width");
        public TextBox? txtADCPTransectWidth = MakeTextBox(name: "txtADCPTransectWidth", text: "2");
        // Layout
        public Label? lblLayoutCbarTickDecimals = MakeLabel(name: "lblLayoutCbarTickDecimals", text: "Color Bar Tick Decimals");
        public NumericUpDown? numLayoutCbarTickDecimals = MakeNumericUpDown(name: "numLayoutCbarTickDecimals", min: 0, max: 5, value: 2);
        public Label? lblLayoutAxisTickDecimals = MakeLabel(name: "lblLayoutAxisTickDecimals", text: "Axis Tick Decimals");
        public NumericUpDown? numLayoutAxisTickDecimals = MakeNumericUpDown(name: "numLayoutAxisTickDecimals", min: 0, max: 5, value: 2);
        public Label? lblLayoutPadM = MakeLabel(name: "lblLayoutPadM", text: "Padding (m)");
        public TextBox? txtLayoutPadM = MakeTextBox(name: "txtLayoutPadM", text: "2000");
        public Label? lblLayoutDistanceBinM = MakeLabel(name: "lblLayoutDistanceBinM", text: "Distance Bin (m)");
        public TextBox? txtLayoutDistanceBinM = MakeTextBox(name: "txtLayoutDistanceBinM", text: "50");
        public Label? lblLayoutBarWidthScale = MakeLabel(name: "lblLayoutBarWidthScale", text: "Bar Chart Width Scale");
        public TextBox? txtLayoutBarWidthScale = MakeTextBox(name: "txtLayoutBarWidthScale", text: "0.15");
        // Animation
        public Label? lblAnimationStartIndex = MakeLabel(name: "lblAnimationStartIndex", text: "First Timestep");
        public NumericUpDown? numAnimationStartIndex = MakeNumericUpDown(name: "numAnimationStartIndex", min: 0, max: 10000, value: 0);
        public CheckBox? checkAnimationUseStart = MakeCheckBox(name: "checkAnimationUseStart", text: "Use First Timestep", isChecked: true);
        public Label? lblAnimationEndIndex = MakeLabel(name: "lblAnimationEndIndex", text: "Last Timestep");
        public NumericUpDown? numAnimationEndIndex = MakeNumericUpDown(name: "numAnimationEndIndex", min: 0, max: 10000, value: 10);
        public CheckBox? checkAnimationUseEnd = MakeCheckBox(name: "checkAnimationUseEnd", text: "Use Last Timestep", isChecked: true);
        public Label? lblAnimationTimeStep = MakeLabel(name: "lblAnimationTimeStep", text: "Time Step");
        public NumericUpDown? numAnimationTimeStep = MakeNumericUpDown(name: "numAnimationTimeStep", min: 1, max: 1000, value: 1);
        public Label? lblAnimationInterval = MakeLabel(name: "lblAnimationInterval", text: "Interval (ms)");
        public NumericUpDown? numAnimationInterval = MakeNumericUpDown(name: "numAnimationInterval", min: 100, max: 10000, value: 500);
        public Label? lblAnimationBBox = MakeLabel(name: "lblAnimationBBox", text: "Bounding Box");
        public TextBox? txtAnimationBBox = MakeTextBox(name: "txtAnimationBBox", text: "");
        public Button? btnAnimationBBox = MakeButton(name: "btnAnimationBBox", text: "...");
        public Label? lblAnimationOutputFile = MakeLabel(name: "lblAnimationOutputFile", text: "Output File");
        public TextBox? txtAnimationOutputFile = MakeTextBox(name: "txtAnimationOutputFile", text: "");
        public Button? btnAnimationOutputFile = MakeButton(name: "btnAnimationOutputFile", text: "...");

        private void PropHDModelComparison()
        {
            tableProp.Controls.Clear();
            tableProp.RowStyles.Clear();

            // Required Inputs
            XmlNodeList? hdModels = _project.GetObjects("HDModel");
            foreach (XmlNode node in hdModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboHDModel.Items.Add(item);
            }
            if (comboHDModel.Items.Count > 0)
                comboHDModel.SelectedIndex = 0;
            XmlNodeList adcps = _project.GetObjects("VesselMountedADCP");
            foreach (XmlNode node in adcps)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboADCP.Items.Add(item);
            }
            if (comboADCP.Items.Count > 0)
                comboADCP.SelectedIndex = 0;
            tableRequired.Controls.Clear();
            tableRequired.RowStyles.Clear();
            tableRequired.RowCount = 3;
            tableRequired.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableRequired.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableRequired.Controls.Add(lblHDModel, 0, 0);
            tableRequired.Controls.Add(comboHDModel, 1, 0);
            tableRequired.Controls.Add(lblADCP, 0, 1);
            tableRequired.Controls.Add(comboADCP, 1, 1);
            grpRequired.Controls.Add(tableRequired);

            // ADCP Inputs
            tableADCP.Controls.Clear();
            tableADCP.RowStyles.Clear();

            tableADCP.RowCount = 9;
            for (int i = 0; i < 9; i++)
            {
                tableADCP.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableADCP.Controls.Add(lblADCPSeriesMode, 0, 0);
            tableADCP.Controls.Add(comboADCPSeriesMode, 1, 0);
            tableADCP.Controls.Add(lblADCPSeriesTarget, 0, 1);
            tableADCP.Controls.Add(numADCPSeriesTarget, 1, 1);
            tableADCP.Controls.Add(txtADCPSeriesTarget, 1, 1);
            tableADCP.Controls.Add(checkADCPSeriesTarget, 2, 1);
            tableADCP.Controls.Add(lblADCPQuiverScale, 0, 2);
            tableADCP.Controls.Add(txtADCPQuiverScale, 1, 2);
            tableADCP.Controls.Add(lblADCPQuiverWidth, 0, 3);
            tableADCP.Controls.Add(txtADCPQuiverWidth, 1, 3);
            tableADCP.Controls.Add(lblADCPQuiverHeadWidth, 0, 4);
            tableADCP.Controls.Add(txtADCPQuiverHeadWidth, 1, 4);
            tableADCP.Controls.Add(lblADCPQuiverHeadLength, 0, 5);
            tableADCP.Controls.Add(txtADCPQuiverHeadLength, 1, 5);
            tableADCP.Controls.Add(lblADCPQuiverColor, 0, 6);
            tableADCP.Controls.Add(pnlADCPQuiverColor, 1, 6);
            tableADCP.Controls.Add(btnADCPQuiverColor, 2, 6);
            tableADCP.Controls.Add(lblADCPTransectColor, 0, 7);
            tableADCP.Controls.Add(pnlADCPTransectColor, 1, 7);
            tableADCP.Controls.Add(btnADCPTransectColor, 2, 7);
            grpADCP.Controls.Add(tableADCP);

            comboADCPSeriesMode.SelectedIndex = 0;
            txtADCPSeriesTarget.Visible = false;
            checkADCPSeriesTarget.Checked = false;

            // HD Inputs
            tableHD.Controls.Clear();
            tableHD.RowStyles.Clear();
            tableHD.RowCount = 14;
            for (int i = 0; i < 14; i++)
            {
                if (i == 13)
                    tableHD.RowStyles.Add(new RowStyle(SizeType.Absolute, 35F));
                else
                    tableHD.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableHD.Controls.Add(lblModelFieldPixelSizeM, 0, 0);
            tableHD.Controls.Add(txtModelFieldPixelSizeM, 1, 0);
            tableHD.Controls.Add(lblModelFieldQuiverStrideN, 0, 1);
            tableHD.Controls.Add(numModelFieldQuiverStrideN, 1, 1);
            tableHD.Controls.Add(lblModelQuiverMode, 0, 2);
            tableHD.Controls.Add(comboModelQuiverMode, 1, 2);
            tableHD.Controls.Add(lblModelQuiverScale, 0, 3);
            tableHD.Controls.Add(txtModelQuiverScale, 1, 3);
            tableHD.Controls.Add(lblModelQuiverWidth, 0, 4);
            tableHD.Controls.Add(txtModelQuiverWidth, 1, 4);
            tableHD.Controls.Add(lblModelQuiverHeadWidth, 0, 5);
            tableHD.Controls.Add(txtModelQuiverHeadWidth, 1, 5);
            tableHD.Controls.Add(lblModelQuiverHeadLength, 0, 6);
            tableHD.Controls.Add(txtModelQuiverHeadLength, 1, 6);
            tableHD.Controls.Add(lblModelQuiverColor, 0, 7);
            tableHD.Controls.Add(pnlModelQuiverColor, 1, 7);
            tableHD.Controls.Add(btnModelQuiverColor, 2, 7);
            tableHD.Controls.Add(lblModelLevels, 0, 8);
            tableHD.Controls.Add(txtModelLevels, 1, 8);
            tableHD.Controls.Add(lblModelvmin, 0, 9);
            tableHD.Controls.Add(txtModelvmin, 1, 9);
            tableHD.Controls.Add(lblModelvmax, 0, 10);
            tableHD.Controls.Add(txtModelvmax, 1, 10);
            tableHD.Controls.Add(lblModelCmap, 0, 11);
            tableHD.Controls.Add(comboModelCmap, 1, 11);
            tableHD.Controls.Add(lblModelCmapBottomThreshold, 0, 12);
            tableHD.Controls.Add(txtModelCmapBottomThreshold, 1, 12);
            grpHD.Controls.Add(tableHD);

            // Layout
            tableLayout.Controls.Clear();
            tableLayout.RowStyles.Clear();
            tableLayout.RowCount = 6;
            for (int i = 0; i < 6; i++)
            {
                tableLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableLayout.Controls.Add(lblLayoutCbarTickDecimals, 0, 0);
            tableLayout.Controls.Add(numLayoutCbarTickDecimals, 1, 0);
            tableLayout.Controls.Add(lblLayoutAxisTickDecimals, 0, 1);
            tableLayout.Controls.Add(numLayoutAxisTickDecimals, 1, 1);
            tableLayout.Controls.Add(lblLayoutPadM, 0, 2);
            tableLayout.Controls.Add(txtLayoutPadM, 1, 2);
            tableLayout.Controls.Add(lblLayoutDistanceBinM, 0, 3);
            tableLayout.Controls.Add(txtLayoutDistanceBinM, 1, 3);
            tableLayout.Controls.Add(lblLayoutBarWidthScale, 0, 4);
            tableLayout.Controls.Add(txtLayoutBarWidthScale, 1, 4);
            grpLayout.Controls.Add(tableLayout);

            tableProp.RowCount = 4;
            float requiredHeight = tableRequired.RowCount * 30F;
            float adcpHeight = tableADCP.RowCount * 30F;
            float hdHeight = tableHD.RowCount * 30F + 5F;
            float layoutHeight = tableLayout.RowCount * 30F;
            tableProp.Height = (int)(requiredHeight + adcpHeight + hdHeight + layoutHeight) + 40;
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, requiredHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, adcpHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, hdHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, layoutHeight));
            tableProp.Controls.Add(grpRequired, 0, 0);
            tableProp.Controls.Add(grpADCP, 0, 1);
            tableProp.Controls.Add(grpHD, 0, 2);
            tableProp.Controls.Add(grpLayout, 0, 3);
        }

        private void PropMTModelComparison()
        {
            tableProp.Controls.Clear();
            tableProp.RowStyles.Clear();
            // Required Inputs
            XmlNodeList? mtModels = _project.GetObjects("MTModel");
            foreach (XmlNode node in mtModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboMTModel.Items.Add(item);
            }
            if (comboMTModel.Items.Count > 0)
                comboMTModel.SelectedIndex = 0;
            XmlNodeList? adcps = _project.GetObjects("VesselMountedADCP");
            foreach (XmlNode node in adcps)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboADCP.Items.Add(item);
            }
            if (comboADCP.Items.Count > 0)
                comboADCP.SelectedIndex = 0;
            tableRequired.Controls.Clear();
            tableRequired.RowStyles.Clear();
            tableRequired.RowCount = 3;
            tableRequired.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableRequired.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableRequired.Controls.Add(lblMTModel, 0, 0);
            tableRequired.Controls.Add(comboMTModel, 1, 0);
            tableRequired.Controls.Add(lblADCP, 0, 1);
            tableRequired.Controls.Add(comboADCP, 1, 1);
            grpRequired.Controls.Add(tableRequired);
            // ADCP Inputs
            tableADCP.Controls.Clear();
            tableADCP.RowStyles.Clear();
            tableADCP.RowCount = 4;
            for (int i = 0; i < 4; i++)
            {
                tableADCP.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableADCP.Controls.Add(lblADCPSeriesMode, 0, 0);
            tableADCP.Controls.Add(comboADCPSeriesMode, 1, 0);
            tableADCP.Controls.Add(lblADCPSeriesTarget, 0, 1);
            tableADCP.Controls.Add(numADCPSeriesTarget, 1, 1);
            tableADCP.Controls.Add(txtADCPSeriesTarget, 1, 1);
            tableADCP.Controls.Add(checkADCPSeriesTarget, 2, 1);
            tableADCP.Controls.Add(lblADCPTransectColor, 0, 2);
            tableADCP.Controls.Add(pnlADCPTransectColor, 1, 2);
            tableADCP.Controls.Add(btnADCPTransectColor, 2, 2);
            grpADCP.Controls.Add(tableADCP);

            comboADCPSeriesMode.SelectedIndex = 0;
            txtADCPSeriesTarget.Visible = false;
            checkADCPSeriesTarget.Checked = false;
            // MT Inputs
            tableMT.Controls.Clear();
            tableMT.RowStyles.Clear();
            tableMT.RowCount = 8;
            for (int i = 0; i < 8; i++)
            {
                if (i == 4)
                    tableMT.RowStyles.Add(new RowStyle(SizeType.Absolute, 35F));
                else
                    tableMT.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableMT.Controls.Add(lblSSCScale, 0, 0);
            tableMT.Controls.Add(comboSSCScale, 1, 0);
            tableMT.Controls.Add(lblSSCLevels, 0, 1);
            tableMT.Controls.Add(txtSSCLevels, 1, 1);
            tableMT.Controls.Add(lblSSCvmin, 0, 2);
            tableMT.Controls.Add(txtSSCvmin, 1, 2);
            tableMT.Controls.Add(lblSSCvmax, 0, 3);
            tableMT.Controls.Add(txtSSCvmax, 1, 3);
            tableMT.Controls.Add(lblSSCCmap, 0, 4);
            tableMT.Controls.Add(comboSSCcmap, 1, 4);
            tableMT.Controls.Add(lblSSCBottomThreshold, 0, 5);
            tableMT.Controls.Add(txtSSCBottomThreshold, 1, 5);
            tableMT.Controls.Add(lblSSCPixelSizeM, 0, 6);
            tableMT.Controls.Add(txtSSCPixelSizeM, 1, 6);
            grpMT.Controls.Add(tableMT);
            // Layout
            tableLayout.Controls.Clear();
            tableLayout.RowStyles.Clear();
            tableLayout.RowCount = 6;
            for (int i = 0; i < 6; i++)
            {
                tableLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableLayout.Controls.Add(lblLayoutCbarTickDecimals, 0, 0);
            tableLayout.Controls.Add(numLayoutCbarTickDecimals, 1, 0);
            tableLayout.Controls.Add(lblLayoutAxisTickDecimals, 0, 1);
            tableLayout.Controls.Add(numLayoutAxisTickDecimals, 1, 1);
            tableLayout.Controls.Add(lblLayoutPadM, 0, 2);
            tableLayout.Controls.Add(txtLayoutPadM, 1, 2);
            tableLayout.Controls.Add(lblLayoutDistanceBinM, 0, 3);
            tableLayout.Controls.Add(txtLayoutDistanceBinM, 1, 3);
            tableLayout.Controls.Add(lblLayoutBarWidthScale, 0, 4);
            tableLayout.Controls.Add(txtLayoutBarWidthScale, 1, 4);
            grpLayout.Controls.Add(tableLayout);

            tableProp.RowCount = 4;
            float requiredHeight = tableRequired.RowCount * 30F;
            float adcpHeight = tableADCP.RowCount * 30F;
            float mtHeight = tableMT.RowCount * 30F + 5F;
            float layoutHeight = tableLayout.RowCount * 30F;
            tableProp.Height = (int)(requiredHeight + adcpHeight + mtHeight + layoutHeight) + 40;
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, requiredHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, adcpHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, mtHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, layoutHeight));
            tableProp.Controls.Add(grpRequired, 0, 0);
            tableProp.Controls.Add(grpADCP, 0, 1);
            tableProp.Controls.Add(grpMT, 0, 2);
            tableProp.Controls.Add(grpLayout, 0, 3);

        }

        private void PropHDMTModelComparison()
        {
            tableProp.Controls.Clear();
            tableProp.RowStyles.Clear();
            // Required Inputs
            XmlNodeList? hdModels = _project.GetObjects("HDModel");
            foreach (XmlNode node in hdModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboHDModel.Items.Add(item);
            }
            if (comboHDModel.Items.Count > 0)
                comboHDModel.SelectedIndex = 0;
            XmlNodeList? mtModels = _project.GetObjects("MTModel");
            foreach (XmlNode node in mtModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboMTModel.Items.Add(item);
            }
            if (comboMTModel.Items.Count > 0)
                comboMTModel.SelectedIndex = 0;
            XmlNodeList? adcps = _project.GetObjects("VesselMountedADCP");
            foreach (XmlNode node in adcps)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboADCP.Items.Add(item);
            }
            if (comboADCP.Items.Count > 0)
                comboADCP.SelectedIndex = 0;
            tableRequired.Controls.Clear();
            tableRequired.RowStyles.Clear();
            tableRequired.RowCount = 4;
            tableRequired.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableRequired.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableRequired.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableRequired.Controls.Add(lblHDModel, 0, 0);
            tableRequired.Controls.Add(comboHDModel, 1, 0);
            tableRequired.Controls.Add(lblMTModel, 0, 1);
            tableRequired.Controls.Add(comboMTModel, 1, 1);
            tableRequired.Controls.Add(lblADCP, 0, 2);
            tableRequired.Controls.Add(comboADCP, 1, 2);
            grpRequired.Controls.Add(tableRequired);
            // ADCP Inputs
            tableADCP.Controls.Clear();
            tableADCP.RowStyles.Clear();
            tableADCP.RowCount = 9;
            for (int i = 0; i < 9; i++)
            {
                tableADCP.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableADCP.Controls.Add(lblADCPSeriesMode, 0, 0);
            tableADCP.Controls.Add(comboADCPSeriesMode, 1, 0);
            tableADCP.Controls.Add(lblADCPSeriesTarget, 0, 1);
            tableADCP.Controls.Add(numADCPSeriesTarget, 1, 1);
            tableADCP.Controls.Add(txtADCPSeriesTarget, 1, 1);
            tableADCP.Controls.Add(checkADCPSeriesTarget, 2, 1);
            tableADCP.Controls.Add(lblADCPQuiverScale, 0, 2);
            tableADCP.Controls.Add(txtADCPQuiverScale, 1, 2);
            tableADCP.Controls.Add(lblADCPQuiverWidth, 0, 3);
            tableADCP.Controls.Add(txtADCPQuiverWidth, 1, 3);
            tableADCP.Controls.Add(lblADCPQuiverHeadWidth, 0, 4);
            tableADCP.Controls.Add(txtADCPQuiverHeadWidth, 1, 4);
            tableADCP.Controls.Add(lblADCPQuiverHeadLength, 0, 5);
            tableADCP.Controls.Add(txtADCPQuiverHeadLength, 1, 5);
            tableADCP.Controls.Add(lblADCPQuiverEveryN, 0, 6);
            tableADCP.Controls.Add(numADCPQuiverEveryN, 1, 6);
            tableADCP.Controls.Add(lblADCPTransectWidth, 0, 7);
            tableADCP.Controls.Add(txtADCPTransectWidth, 1, 7);
            grpADCP.Controls.Add(tableADCP);
            
            comboADCPSeriesMode.SelectedIndex = 0;
            txtADCPSeriesTarget.Visible = false;
            checkADCPSeriesTarget.Checked = false;
            // HD Inputs
            tableHD.Controls.Clear();
            tableHD.RowStyles.Clear();
            tableHD.RowCount = 9;
            for (int i = 0; i < 9; i++)
            {
                tableHD.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableHD.Controls.Add(lblModelFieldPixelSizeM, 0, 0);
            tableHD.Controls.Add(txtModelFieldPixelSizeM, 1, 0);
            tableHD.Controls.Add(lblModelFieldQuiverStrideN, 0, 1);
            tableHD.Controls.Add(numModelFieldQuiverStrideN, 1, 1);
            tableHD.Controls.Add(lblModelQuiverMode, 0, 2);
            tableHD.Controls.Add(comboModelQuiverMode, 1, 2);
            tableHD.Controls.Add(lblModelQuiverScale, 0, 3);
            tableHD.Controls.Add(txtModelQuiverScale, 1, 3);
            tableHD.Controls.Add(lblModelQuiverWidth, 0, 4);
            tableHD.Controls.Add(txtModelQuiverWidth, 1, 4);
            tableHD.Controls.Add(lblModelQuiverHeadWidth, 0, 5);
            tableHD.Controls.Add(txtModelQuiverHeadWidth, 1, 5);
            tableHD.Controls.Add(lblModelQuiverHeadLength, 0, 6);
            tableHD.Controls.Add(txtModelQuiverHeadLength, 1, 6);
            tableHD.Controls.Add(lblModelQuiverColor, 0, 7);
            tableHD.Controls.Add(pnlModelQuiverColor, 1, 7);
            tableHD.Controls.Add(btnModelQuiverColor, 2, 7);
            grpHD.Controls.Add(tableHD);
            // MT Inputs
            tableMT.Controls.Clear();
            tableMT.RowStyles.Clear();
            tableMT.RowCount = 8;
            for (int i = 0; i < 8; i++)
            {
                if (i == 4)
                    tableMT.RowStyles.Add(new RowStyle(SizeType.Absolute, 35F));
                else
                    tableMT.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableMT.Controls.Add(lblSSCScale, 0, 0);
            tableMT.Controls.Add(comboSSCScale, 1, 0);
            tableMT.Controls.Add(lblSSCLevels, 0, 1);
            tableMT.Controls.Add(txtSSCLevels, 1, 1);
            tableMT.Controls.Add(lblSSCvmin, 0, 2);
            tableMT.Controls.Add(txtSSCvmin, 1, 2);
            tableMT.Controls.Add(lblSSCvmax, 0, 3);
            tableMT.Controls.Add(txtSSCvmax, 1, 3);
            tableMT.Controls.Add(lblSSCCmap, 0, 4);
            tableMT.Controls.Add(comboSSCcmap, 1, 4);
            tableMT.Controls.Add(lblSSCBottomThreshold, 0, 5);
            tableMT.Controls.Add(txtSSCBottomThreshold, 1, 5);
            tableMT.Controls.Add(lblSSCPixelSizeM, 0, 6);
            tableMT.Controls.Add(txtSSCPixelSizeM, 1, 6);
            grpMT.Controls.Add(tableMT);
            // Layout
            tableLayout.Controls.Clear();
            tableLayout.RowStyles.Clear();
            tableLayout.RowCount = 4;
            for (int i = 0; i < 4; i++)
            {
                tableLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableLayout.Controls.Add(lblLayoutCbarTickDecimals, 0, 0);
            tableLayout.Controls.Add(numLayoutCbarTickDecimals, 1, 0);
            tableLayout.Controls.Add(lblLayoutAxisTickDecimals, 0, 1);
            tableLayout.Controls.Add(numLayoutAxisTickDecimals, 1, 1);
            tableLayout.Controls.Add(lblLayoutPadM, 0, 2);
            tableLayout.Controls.Add(txtLayoutPadM, 1, 2);
            grpLayout.Controls.Add(tableLayout);

            tableProp.RowCount = 5;
            float requiredHeight = tableRequired.RowCount * 30F;
            float adcpHeight = tableADCP.RowCount * 30F;
            float hdHeight = tableHD.RowCount * 30F;
            float mtHeight = tableMT.RowCount * 30F + 5F;
            float layoutHeight = tableLayout.RowCount * 30F;
            tableProp.Height = (int)(requiredHeight + adcpHeight + hdHeight + mtHeight + layoutHeight) + 40;
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, requiredHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, adcpHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, hdHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, mtHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, layoutHeight));
            tableProp.Controls.Add(grpRequired, 0, 0);
            tableProp.Controls.Add(grpADCP, 0, 1);
            tableProp.Controls.Add(grpHD, 0, 2);
            tableProp.Controls.Add(grpMT, 0, 3);
            tableProp.Controls.Add(grpLayout, 0, 4);
        }

        private void PropHDMTModelAnimation()
        {
            tableProp.Controls.Clear();
            tableProp.RowStyles.Clear();
            // Required Inputs
            XmlNodeList? hdModels = _project.GetObjects("HDModel");
            foreach (XmlNode node in hdModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboHDModel.Items.Add(item);
            }
            if (comboHDModel.Items.Count > 0)
                comboHDModel.SelectedIndex = 0;
            XmlNodeList? mtModels = _project.GetObjects("MTModel");
            foreach (XmlNode node in mtModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboMTModel.Items.Add(item);
            }
            if (comboMTModel.Items.Count > 0)
                comboMTModel.SelectedIndex = 0;
            tableRequired.Controls.Clear();
            tableRequired.RowStyles.Clear();
            tableRequired.RowCount = 3;
            tableRequired.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableRequired.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableRequired.Controls.Add(lblHDModel, 0, 0);
            tableRequired.Controls.Add(comboHDModel, 1, 0);
            tableRequired.Controls.Add(lblMTModel, 0, 1);
            tableRequired.Controls.Add(comboMTModel, 1, 1);
            grpRequired.Controls.Add(tableRequired);
            // HD Inputs
            tableHD.Controls.Clear();
            tableHD.RowStyles.Clear();
            tableHD.RowCount = 8;
            for (int i = 0; i < 8; i++)
            {
                tableHD.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableHD.Controls.Add(lblModelFieldPixelSizeM, 0, 0);
            tableHD.Controls.Add(txtModelFieldPixelSizeM, 1, 0);
            tableHD.Controls.Add(lblModelFieldQuiverStrideN, 0, 1);
            tableHD.Controls.Add(numModelFieldQuiverStrideN, 1, 1);
            tableHD.Controls.Add(lblModelQuiverScale, 0, 2);
            tableHD.Controls.Add(txtModelQuiverScale, 1, 2);
            tableHD.Controls.Add(lblModelQuiverWidth, 0, 3);
            tableHD.Controls.Add(txtModelQuiverWidth, 1, 3);
            tableHD.Controls.Add(lblModelQuiverHeadWidth, 0, 4);
            tableHD.Controls.Add(txtModelQuiverHeadWidth, 1, 4);
            tableHD.Controls.Add(lblModelQuiverHeadLength, 0, 5);
            tableHD.Controls.Add(txtModelQuiverHeadLength, 1, 5);
            tableHD.Controls.Add(lblModelQuiverColor, 0, 6);
            tableHD.Controls.Add(pnlModelQuiverColor, 1, 6);
            tableHD.Controls.Add(btnModelQuiverColor, 2, 6);
            grpHD.Controls.Add(tableHD);
            // MT Inputs
            tableMT.Controls.Clear();
            tableMT.RowStyles.Clear();
            tableMT.RowCount = 8;
            for (int i = 0; i < 8; i++)
            {
                if (i == 4)
                    tableMT.RowStyles.Add(new RowStyle(SizeType.Absolute, 35F));
                else
                    tableMT.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableMT.Controls.Add(lblSSCScale, 0, 0);
            tableMT.Controls.Add(comboSSCScale, 1, 0);
            tableMT.Controls.Add(lblSSCLevels, 0, 1);
            tableMT.Controls.Add(txtSSCLevels, 1, 1);
            tableMT.Controls.Add(lblSSCvmin, 0, 2);
            tableMT.Controls.Add(txtSSCvmin, 1, 2);
            tableMT.Controls.Add(lblSSCvmax, 0, 3);
            tableMT.Controls.Add(txtSSCvmax, 1, 3);
            tableMT.Controls.Add(lblSSCCmap, 0, 4);
            tableMT.Controls.Add(comboSSCcmap, 1, 4);
            tableMT.Controls.Add(lblSSCBottomThreshold, 0, 5);
            tableMT.Controls.Add(txtSSCBottomThreshold, 1, 5);
            tableMT.Controls.Add(lblSSCPixelSizeM, 0, 6);
            tableMT.Controls.Add(txtSSCPixelSizeM, 1, 6);
            grpMT.Controls.Add(tableMT);
            // Layout
            tableLayout.Controls.Clear();
            tableLayout.RowStyles.Clear();
            tableLayout.RowCount = 3;
            for (int i = 0; i < 3; i++)
            {
                tableLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableLayout.Controls.Add(lblLayoutCbarTickDecimals, 0, 0);
            tableLayout.Controls.Add(numLayoutCbarTickDecimals, 1, 0);
            tableLayout.Controls.Add(lblLayoutAxisTickDecimals, 0, 1);
            tableLayout.Controls.Add(numLayoutAxisTickDecimals, 1, 1);
            grpLayout.Controls.Add(tableLayout);
            // Animation
            tableAnimation.Controls.Clear();
            tableAnimation.RowStyles.Clear();
            tableAnimation.RowCount = 7;
            for (int i = 0; i < 7; i++)
            {
                tableAnimation.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            }
            tableAnimation.Controls.Add(lblAnimationStartIndex, 0, 0);
            tableAnimation.Controls.Add(numAnimationStartIndex, 1, 0);
            tableAnimation.Controls.Add(checkAnimationUseStart, 2, 0);
            tableAnimation.Controls.Add(lblAnimationEndIndex, 0, 1);
            tableAnimation.Controls.Add(numAnimationEndIndex, 1, 1);
            tableAnimation.Controls.Add(checkAnimationUseEnd, 2, 1);
            tableAnimation.Controls.Add(lblAnimationTimeStep, 0, 2);
            tableAnimation.Controls.Add(numAnimationTimeStep, 1, 2);
            tableAnimation.Controls.Add(lblAnimationInterval, 0, 3);
            tableAnimation.Controls.Add(numAnimationInterval, 1, 3);
            tableAnimation.Controls.Add(lblAnimationBBox, 0, 4);
            tableAnimation.Controls.Add(txtAnimationBBox, 1, 4);
            tableAnimation.Controls.Add(btnAnimationBBox, 2, 4);
            tableAnimation.Controls.Add(lblAnimationOutputFile, 0, 5);
            tableAnimation.Controls.Add(txtAnimationOutputFile, 1, 5);
            tableAnimation.Controls.Add(btnAnimationOutputFile, 2, 5);

            grpAnimation.Controls.Add(tableAnimation);
            // Final Layout
            tableProp.RowCount = 5;
            float requiredHeight = tableRequired.RowCount * 30F;
            float hdHeight = tableHD.RowCount * 30F;
            float mtHeight = tableMT.RowCount * 30F + 5F;
            float layoutHeight = tableLayout.RowCount * 30F;
            float animationHeight = tableAnimation.RowCount * 30F;
            tableProp.Height = (int)(requiredHeight + hdHeight + mtHeight + layoutHeight + animationHeight) + 40;
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, requiredHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, hdHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, mtHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, layoutHeight));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, animationHeight));
            tableProp.Controls.Add(grpRequired, 0, 0);
            tableProp.Controls.Add(grpHD, 0, 1);
            tableProp.Controls.Add(grpMT, 0, 2);
            tableProp.Controls.Add(grpLayout, 0, 3);
            tableProp.Controls.Add(grpAnimation, 0, 4);

        }

        private void InitializeWidgets()
        {
            comboHDModel.DisplayMember = "name";
            comboHDModel.ValueMember = "id";
            comboMTModel.DisplayMember = "name";
            comboMTModel.ValueMember = "id";
            comboADCP.DisplayMember = "name";
            comboADCP.ValueMember = "id";
            comboPlotType.SelectedIndex = 0;
            checkADCPSeriesTarget.CheckedChanged += checkADCPSeriesTarget_CheckedChanged;
            comboSSCScale.SelectedIndex = 1;
            // Set comboSSCcmap to "turbo" if available
            for (int i = 0; i < comboSSCcmap.Items.Count; i++)
            {
                if (comboSSCcmap.Items[i] is ColormapItem item && item.Name.Equals("turbo", StringComparison.OrdinalIgnoreCase))
                {
                    comboSSCcmap.SelectedIndex = i;
                    break;
                }
            }
            // Set comboModelCmap to "turbo" if available
            for (int i = 0; i < comboModelCmap.Items.Count; i++)
            {
                if (comboModelCmap.Items[i] is ColormapItem item && item.Name.Equals("turbo", StringComparison.OrdinalIgnoreCase))
                {
                    comboModelCmap.SelectedIndex = i;
                    break;
                }
            }
            comboModelQuiverMode.SelectedIndex = 0;
            btnModelQuiverColor.Click += btnChangeColor_Click;
            btnADCPQuiverColor.Click += btnChangeColor_Click;
            btnADCPTransectColor.Click += btnChangeColor_Click;
            checkAnimationUseStart.CheckedChanged += checkAnimationUseStart_CheckedChanged;
            checkAnimationUseEnd.CheckedChanged += checkAnimationUseEnd_CheckedChanged;
            btnAnimationBBox.Click += btnAnimatiobBBox_Click;
            btnAnimationOutputFile.Click += btnAnimationOutputFile_Click;
            numAnimationStartIndex.Enabled = false;
            numAnimationEndIndex.Enabled = false;
        }

        public ProjectPlot()
        {
            InitializeComponent();
            InitializeWidgets();
        }

        private bool ValidInputs(string type)
        {
            if (type == "HD")
            {

                return true;
            }
            else if (type == "MT")
            {
                return true;
            }
            else if (type == "HDMT")
            {
                return true;
            }
            else if (type == "Animation")
            {
                return true;
            }
            return true;
        }

        private void btnPlot_Click(object sender, EventArgs e)
        {
            Dictionary<string, string> inputs = null;
            if (comboPlotType.SelectedItem.ToString() == "HD Comparison")
            {
                if (ValidInputs(type: "HD"))
                {
                    var selectedHDModel = comboHDModel.SelectedItem as ComboBoxItem;
                    var selectedADCP = comboADCP.SelectedItem as ComboBoxItem;
                    string adcpSeriesTarget;
                    if (comboADCPSeriesMode.SelectedItem.ToString().Equals("Bin", StringComparison.OrdinalIgnoreCase))
                        adcpSeriesTarget = numADCPSeriesTarget.Value.ToString();
                    else
                        adcpSeriesTarget = txtADCPSeriesTarget.Text;
                    inputs = new Dictionary<string, string>
                    {
                        { "Task", "HDComparison" },
                        { "Project", _Globals.Config.OuterXml.ToString() },
                        { "ModelID", selectedHDModel.ID},
                        { "ADCPID", selectedADCP.ID},
                        { "ADCPSeriesMode", comboADCPSeriesMode.SelectedItem.ToString() },
                        { "ADCPSeriesTarget", adcpSeriesTarget },
                        { "UseMean", checkADCPSeriesTarget.Checked ? "Yes":"No" },
                        { "ADCPTransectColor", ColorTranslator.ToHtml(pnlADCPTransectColor.BackColor) },
                        { "ADCPQuiverScale", txtADCPQuiverScale.Text },
                        { "ADCPQuiverWidth", txtADCPQuiverWidth.Text },
                        { "ADCPQuiverHeadWidth", txtADCPQuiverHeadWidth.Text },
                        { "ADCPQuiverHeadLength", txtADCPQuiverHeadLength.Text },
                        { "ADCPQuiverColor", ColorTranslator.ToHtml(pnlADCPQuiverColor.BackColor) },
                        { "ModelFieldPixelSizeM", txtModelFieldPixelSizeM.Text },
                        { "ModelFieldQuiverStrideN", numModelFieldQuiverStrideN.Value.ToString() },
                        { "ModelQuiverScale", txtModelQuiverScale.Text },
                        { "ModelQuiverWidth", txtModelQuiverWidth.Text },
                        { "ModelQuiverHeadWidth", txtModelQuiverHeadWidth.Text },
                        { "ModelQuiverHeadLength", txtModelQuiverHeadLength.Text },
                        { "ModelQuiverColor", ColorTranslator.ToHtml(pnlModelQuiverColor.BackColor) },
                        { "ModelQuiverMode", comboModelQuiverMode.SelectedItem.ToString() },
                        { "ModelLevels", txtModelLevels.Text },
                        { "Modelvmin", txtModelvmin.Text },
                        { "Modelvmax", txtModelvmax.Text },
                        { "ModelCmapName", comboModelCmap.SelectedItem.ToString() },
                        { "ModelBottomThreshold", txtModelCmapBottomThreshold.Text },
                        { "LayoutCbarTickDecimals", numLayoutCbarTickDecimals.Value.ToString() },
                        { "LayoutAxisTickDecimals", numLayoutAxisTickDecimals.Value.ToString() },
                        { "LayoutPadM", txtLayoutPadM.Text },
                        { "LayoutDistanceBinM", txtLayoutDistanceBinM.Text },
                        { "LayoutBarWidthScale", txtLayoutBarWidthScale.Text }
                    };
                }
                else
                {
                    MessageBox.Show("Worng Input! Please check the inputs and try again!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
            }
            else if (comboPlotType.SelectedItem.ToString() == "MT Comparison")
            {
                if (ValidInputs(type: "MT"))
                {
                    var selectedMTModel = comboMTModel.SelectedItem as ComboBoxItem;
                    var selectedADCP = comboADCP.SelectedItem as ComboBoxItem;
                    string adcpSeriesTarget;
                    if (comboADCPSeriesMode.SelectedItem.ToString().Equals("Bin", StringComparison.OrdinalIgnoreCase))
                        adcpSeriesTarget = numADCPSeriesTarget.Value.ToString();
                    else
                        adcpSeriesTarget = txtADCPSeriesTarget.Text;
                    inputs = new Dictionary<string, string>
                    {
                        { "Task", "MTComparison" },
                        { "Project", _Globals.Config.OuterXml.ToString() },
                        { "ModelID", selectedMTModel.ID },
                        { "ADCPID", selectedADCP.ID },
                        { "ADCPSeriesMode", comboADCPSeriesMode.SelectedItem.ToString() },
                        { "ADCPSeriesTarget", adcpSeriesTarget },
                        { "UseMean", checkADCPSeriesTarget.Checked ? "Yes":"No" },
                        { "ADCPTransectColor", ColorTranslator.ToHtml(pnlADCPTransectColor.BackColor) },
                        { "SSCScale", comboSSCScale.SelectedItem.ToString() },
                        { "SSCLevels", txtSSCLevels.Text },
                        { "SSCvmin", txtSSCvmin.Text },
                        { "SSCvmax", txtSSCvmax.Text },
                        { "SSCCmapName", comboSSCcmap.SelectedItem.ToString() },
                        { "SSCBottomThreshold", txtSSCBottomThreshold.Text },
                        { "SSCPixelSizeM", txtSSCPixelSizeM.Text },
                        { "LayoutCbarTickDecimals", numLayoutCbarTickDecimals.Value.ToString() },
                        { "LayoutAxisTickDecimals", numLayoutAxisTickDecimals.Value.ToString() },
                        { "LayoutPadM", txtLayoutPadM.Text },
                        { "LayoutDistanceBinM", txtLayoutDistanceBinM.Text },
                        { "LayoutBarWidthScale", txtLayoutBarWidthScale.Text }
                    };
                }
                else
                {
                    MessageBox.Show("Worng Input! Please check the inputs and try again!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

            }
            else if (comboPlotType.SelectedItem.ToString() == "MT and HD Comparison")
            {
                if (ValidInputs(type: "HDMT"))
                {
                    var selectedMTModel = comboMTModel.SelectedItem as ComboBoxItem;
                    var selectedHDModel = comboHDModel.SelectedItem as ComboBoxItem;
                    var selectedADCP = comboADCP.SelectedItem as ComboBoxItem;
                    string adcpSeriesTarget;
                    if (comboADCPSeriesMode.SelectedItem.ToString().Equals("Bin", StringComparison.OrdinalIgnoreCase))
                        adcpSeriesTarget = numADCPSeriesTarget.Value.ToString();
                    else
                        adcpSeriesTarget = txtADCPSeriesTarget.Text;
                    inputs = new Dictionary<string, string>
                    {
                        { "Task", "HDMTComparison" },
                        { "Project", _Globals.Config.OuterXml.ToString() },
                        { "MTModelID", selectedMTModel.ID },
                        { "HDModelID", selectedHDModel.ID },
                        { "ADCPID", selectedADCP.ID },
                        { "ADCPTransectLineWidth", txtADCPTransectWidth.Text },
                        { "ADCPSeriesMode", comboADCPSeriesMode.SelectedItem.ToString() },
                        { "ADCPSeriesTarget", adcpSeriesTarget },
                        { "UseMean", checkADCPSeriesTarget.Checked ? "Yes":"No" },
                        { "ADCPQuiverEveryN", numADCPQuiverEveryN.Value.ToString() },
                        { "ADCPQuiverWidth", txtADCPQuiverWidth.Text },
                        { "ADCPQuiverHeadWidth", txtADCPQuiverHeadWidth.Text },
                        { "ADCPQuiverHeadLength", txtADCPQuiverHeadLength.Text },
                        { "ADCPQuiverScale", txtADCPQuiverScale.Text },
                        { "SSCScale", comboSSCScale.SelectedItem.ToString() },
                        { "SSCLevels", txtSSCLevels.Text },
                        { "SSCvmin", txtSSCvmin.Text },
                        { "SSCvmax", txtSSCvmax.Text },
                        { "SSCCmapName", comboSSCcmap.SelectedItem.ToString() },
                        { "SSCBottomThreshold", txtSSCBottomThreshold.Text },
                        { "SSCPixelSizeM", txtSSCPixelSizeM.Text },
                        { "ModelFieldPixelSizeM", txtModelFieldPixelSizeM.Text },
                        { "ModelFieldQuiverStrideN", numModelFieldQuiverStrideN.Value.ToString() },
                        { "ModelQuiverScale", txtModelQuiverScale.Text },
                        { "ModelQuiverWidth", txtModelQuiverWidth.Text },
                        { "ModelQuiverHeadWidth", txtModelQuiverHeadWidth.Text },
                        { "ModelQuiverHeadLength", txtModelQuiverHeadLength.Text },
                        { "ModelQuiverColor", ColorTranslator.ToHtml(pnlModelQuiverColor.BackColor) },
                        { "ModelQuiverMode", comboModelQuiverMode.SelectedItem.ToString() },
                        { "LayoutCbarTickDecimals", numLayoutCbarTickDecimals.Value.ToString() },
                        { "LayoutAxisTickDecimals", numLayoutAxisTickDecimals.Value.ToString() },
                        { "LayoutPadM", txtLayoutPadM.Text },
                    };
                }
                else
                {
                    MessageBox.Show("Worng Input! Please check the inputs and try again!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
            }
            else if (comboPlotType.SelectedItem.ToString() == "MT and HD Comparison Animation")
            {
                if (ValidInputs(type: "Animation"))
                {
                    var selectedMTModel = comboMTModel.SelectedItem as ComboBoxItem;
                    var selectedHDModel = comboHDModel.SelectedItem as ComboBoxItem;
                    string layoutBBox = txtAnimationBBox.Text;
                    if (!File.Exists(layoutBBox))
                    {
                        MessageBox.Show("Bounding Box Shapefile does not exist!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return;
                    }
                    inputs = new Dictionary<string, string>
                    {
                        { "Task", "HDMTAnimation" },
                        { "Project", _Globals.Config.OuterXml.ToString() },
                        { "MTModelID", selectedMTModel.ID },
                        { "HDModelID", selectedHDModel.ID },
                        { "SSCScale", comboSSCScale.SelectedItem.ToString() },
                        { "SSCLevels", txtSSCLevels.Text },
                        { "SSCvmin", txtSSCvmin.Text },
                        { "SSCvmax", txtSSCvmax.Text },
                        { "SSCCmapName", comboSSCcmap.SelectedItem.ToString() },
                        { "SSCBottomThreshold", txtSSCBottomThreshold.Text },
                        { "SSCPixelSizeM", txtSSCPixelSizeM.Text },
                        { "ModelFieldPixelSizeM", txtModelFieldPixelSizeM.Text },
                        { "ModelFieldQuiverStrideN", numModelFieldQuiverStrideN.Value.ToString() },
                        { "ModelQuiverScale", txtModelQuiverScale.Text },
                        { "ModelQuiverWidth", txtModelQuiverWidth.Text },
                        { "ModelQuiverHeadWidth", txtModelQuiverHeadWidth.Text },
                        { "ModelQuiverHeadLength", txtModelQuiverHeadLength.Text },
                        { "ModelQuiverColor", ColorTranslator.ToHtml(pnlModelQuiverColor.BackColor) },
                        { "AnimationStartIndex", checkAnimationUseStart.Checked ? "Start" : numAnimationStartIndex.Value.ToString() },
                        { "AnimationEndIndex", checkAnimationUseEnd.Checked ? "End" : numAnimationEndIndex.Value.ToString() },
                        { "AnimationTimeStep", numAnimationTimeStep.Value.ToString() },
                        { "AnimationInterval", numAnimationInterval.Value.ToString() },
                        { "AnimationOutputFile", txtAnimationOutputFile.Text },
                        { "LayoutCbarTickDecimals", numLayoutCbarTickDecimals.Value.ToString() },
                        { "LayoutAxisTickDecimals", numLayoutAxisTickDecimals.Value.ToString() },
                        { "LayoutBBox", layoutBBox}

                    };
                }

                else
                {
                    return;
                }
            }
                    
            string xmlInput = _Tools.GenerateInput(inputs);
            XmlDocument result = _Tools.CallPython(xmlInput);
            Dictionary<string, string> outputs = _Tools.ParseOutput(result);
            if (outputs.ContainsKey("Error"))
            {
                MessageBox.Show(outputs["Error"], "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
        }

        private void comboPlotType_SelectedIndexChanged(object sender, EventArgs e)
        {
            comboADCP.Items.Clear();
            comboHDModel.Items.Clear();
            comboMTModel.Items.Clear();
            if (comboPlotType.SelectedItem.ToString() == "HD Comparison")
            {
                PropHDModelComparison();
            }
            else if (comboPlotType.SelectedItem.ToString() == "MT Comparison")
            {
                PropMTModelComparison();
            }
            else if (comboPlotType.SelectedItem.ToString() == "MT and HD Comparison")
            {
                PropHDMTModelComparison();
            }
            else if (comboPlotType.SelectedItem.ToString() == "MT and HD Comparison Animation")
            {
                PropHDMTModelAnimation();
            }
        }

        private void checkADCPSeriesTarget_CheckedChanged(object? sender, EventArgs e)
        {
            if (checkADCPSeriesTarget.Checked)
            {
                numADCPSeriesTarget.Enabled = false;
                txtADCPSeriesTarget.Enabled = false;
            }
            else
            {
                numADCPSeriesTarget.Enabled = true;
                txtADCPSeriesTarget.Enabled = true;
            }
        }

        private void checkAnimationUseStart_CheckedChanged(object? sender, EventArgs e)
        {
            if (checkAnimationUseStart.Checked)
            {
                numAnimationStartIndex.Enabled = false;
            }
            else
            {
                numAnimationStartIndex.Enabled = true;
            }
        }

        private void checkAnimationUseEnd_CheckedChanged(object? sender, EventArgs e)
        {
            if (checkAnimationUseEnd.Checked)
            {
                numAnimationEndIndex.Enabled = false;
            }
            else
            {
                numAnimationEndIndex.Enabled = true;
            }
        }

        private void btnAnimationBBox_Click(object? sender, EventArgs e)
        {
            using (OpenFileDialog ofd = new OpenFileDialog())
            {
                ofd.Title = "Select Animation Bounding Box Shapefile";
                ofd.Filter = "Polygon Shapefile (*.shp)|*.shp";
                ofd.DefaultExt = "shp";
                if (ofd.ShowDialog() == DialogResult.OK)
                {
                    txtAnimationBBox.Text = ofd.FileName;
                }
            }
        }

        private void btnAnimationOutputFile_Click(object? sender, EventArgs e)
        {
            using (SaveFileDialog sfd = new SaveFileDialog())
            {
                sfd.Title = "Select Animation Output File";
                sfd.Filter = "MP4 files (*.mp4)|*.mp4|gif files (*.gif)|*.gif";
                sfd.DefaultExt = "gif";
                if (sfd.ShowDialog() == DialogResult.OK)
                {
                    txtAnimationOutputFile.Text = sfd.FileName;
                }
            }
        }

        private void btnAnimatiobBBox_Click(object? sender, EventArgs e)
        {
            using (OpenFileDialog ofd = new OpenFileDialog())
            {
                ofd.Title = "Select Animation Bounding Box Shapefile";
                ofd.Filter = "Polygon Shapefile (*.shp)|*.shp";
                ofd.DefaultExt = "shp";
                if (ofd.ShowDialog() == DialogResult.OK)
                {
                    txtAnimationBBox.Text = ofd.FileName;
                }
            }
        }

        private void btnChangeColor_Click(object? sender, EventArgs e)
        {
            Button btn = sender as Button;
            Panel pnl = null;
            if (btn.Name == "btnModelQuiverColor")
                pnl = pnlModelQuiverColor;
            else if (btn.Name == "btnADCPQuiverColor")
                pnl = pnlADCPQuiverColor;
            else if (btn.Name == "btnADCPTransectColor")
                pnl = pnlADCPTransectColor;
            if (pnl == null)
                return;
            using (ColorDialog cd = new ColorDialog())
            {
                cd.Color = pnl.BackColor;
                cd.FullOpen = true;
                if (cd.ShowDialog() == DialogResult.OK)
                {
                    pnl.BackColor = cd.Color;
                }
            }
        }
    }
}
