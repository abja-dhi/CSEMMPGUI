using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using DHI.Generic.MikeZero;
using DHI.Generic.MikeZero.DFS;
using DHI.Generic.MikeZero.DFS.dfs123;
using DHI.Generic.MikeZero.DFS.dfsu;
using DHI.Generic.MikeZero.DFS.mesh;

namespace CSEMMPGUI_v1
{
    public partial class ModelMTPlot : Form
    {
        public XmlElement? model;
        public _ClassConfigurationManager _project = new();

        public static Label? lblTitle;
        public static TextBox? txtTitle;

        public static Label? lblFieldName;
        public static ComboBox? comboFieldName;

        public static Label? lblyAxisMode;
        public static ComboBox? comboyAxisMode;

        public static Label? lblcmap;
        public static ComboBox? combocmap;

        public static Label? lblvmin;
        public static TextBox? txtvmin;

        public static Label? lblvmax;
        public static TextBox? txtvmax;

        public static Label? lblMask;
        public static ComboBox? comboMask;

        public static Label? lblBinSelection;
        public static NumericUpDown? numericNBins;
        public static CheckBox? checkUseMean;

        public static Label? lblScale;
        public static TextBox? txtScale;

        public static Label? lblLineWidth;
        public static TextBox? txtLineWidth;

        public static Label? lblLineAlpha;
        public static TextBox? txtLineAlpha;

        public static Label? lblHistBins;
        public static NumericUpDown? numericHistBins;

        public static Label? lblBeamSelection;
        public static NumericUpDown? numericNBeams;

        private void PropMeshPlot()
        {
            tableProp.Controls.Clear();

            tableProp.RowStyles.Clear();
            tableProp.RowCount = 2;
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));

            tableProp.Controls.Add(lblTitle, 0, 0);
            tableProp.Controls.Add(txtTitle, 1, 0);
        }

        private void InitializeWidgets()
        {
            //
            // lblTitle
            //
            lblTitle = new Label();
            lblTitle.Dock = DockStyle.Fill;
            lblTitle.Name = "lblTitle";
            lblTitle.TabIndex = 0;
            lblTitle.Text = "Title";
            lblTitle.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtTitle
            // 
            txtTitle = new TextBox();
            txtTitle.Dock = DockStyle.Fill;
            txtTitle.Name = "txtTitle";
            txtTitle.TabIndex = 1;
            // 
            // lblFieldName
            // 
            lblFieldName = new Label();
            lblFieldName.Dock = DockStyle.Fill;
            lblFieldName.Name = "lblFieldName";
            lblFieldName.TabIndex = 0;
            lblFieldName.Text = "Field Name";
            lblFieldName.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboFieldName
            // 
            comboFieldName = new ComboBox();
            comboFieldName.Dock = DockStyle.Fill;
            comboFieldName.DropDownStyle = ComboBoxStyle.DropDownList;
            comboFieldName.FormattingEnabled = true;
            comboFieldName.Items.AddRange(new object[] { "Echo Intensity", "Correlation Magnitude", "Percent Good", "Absolute Backscatter", "Alpha s", "Alpha w", "Signal to Noise Ratio", "SSC" });
            comboFieldName.Name = "comboFieldName";
            comboFieldName.TabIndex = 14;
            comboFieldName.SelectedIndex = 0;
            // 
            // lblyAxisMode
            // 
            lblyAxisMode = new Label();
            lblyAxisMode.Dock = DockStyle.Fill;
            lblyAxisMode.Name = "lblyAxisMode";
            lblyAxisMode.TabIndex = 2;
            lblyAxisMode.Text = "y Axis Mode";
            lblyAxisMode.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboyAxisMode
            // 
            comboyAxisMode = new ComboBox();
            comboyAxisMode.Dock = DockStyle.Fill;
            comboyAxisMode.DropDownStyle = ComboBoxStyle.DropDownList;
            comboyAxisMode.FormattingEnabled = true;
            comboyAxisMode.Items.AddRange(new object[] { "Bin", "Depth" });
            comboyAxisMode.Name = "comboyAxisMode";
            comboyAxisMode.TabIndex = 8;
            comboyAxisMode.SelectedIndex = 0;
            // 
            // lblcmap
            // 
            lblcmap = new Label();
            lblcmap.Dock = DockStyle.Fill;
            lblcmap.Name = "lblcmap";
            lblcmap.TabIndex = 3;
            lblcmap.Text = "Colormap";
            lblcmap.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // combocmap
            // 
            combocmap = new ComboBox();
            combocmap.Dock = DockStyle.Fill;
            combocmap.DropDownStyle = ComboBoxStyle.DropDownList;
            combocmap.FormattingEnabled = true;
            combocmap.Name = "combocmap";
            combocmap.TabIndex = 9;
            combocmap.DrawMode = DrawMode.OwnerDrawFixed;
            combocmap.ItemHeight = 24; // more room for image
            combocmap.Items.Add(new ColormapItem("autumn", Image.FromFile(Path.Combine(_Globals.CMapsPath, "autumn.png"))));
            combocmap.Items.Add(new ColormapItem("cividis", Image.FromFile(Path.Combine(_Globals.CMapsPath, "cividis.png"))));
            combocmap.Items.Add(new ColormapItem("cool", Image.FromFile(Path.Combine(_Globals.CMapsPath, "cool.png"))));
            combocmap.Items.Add(new ColormapItem("hot", Image.FromFile(Path.Combine(_Globals.CMapsPath, "hot.png"))));
            combocmap.Items.Add(new ColormapItem("inferno", Image.FromFile(Path.Combine(_Globals.CMapsPath, "inferno.png"))));
            combocmap.Items.Add(new ColormapItem("jet", Image.FromFile(Path.Combine(_Globals.CMapsPath, "jet.png"))));
            combocmap.Items.Add(new ColormapItem("magma", Image.FromFile(Path.Combine(_Globals.CMapsPath, "magma.png"))));
            combocmap.Items.Add(new ColormapItem("plasma", Image.FromFile(Path.Combine(_Globals.CMapsPath, "plasma.png"))));
            combocmap.Items.Add(new ColormapItem("spring", Image.FromFile(Path.Combine(_Globals.CMapsPath, "spring.png"))));
            combocmap.Items.Add(new ColormapItem("summer", Image.FromFile(Path.Combine(_Globals.CMapsPath, "summer.png"))));
            combocmap.Items.Add(new ColormapItem("turbo", Image.FromFile(Path.Combine(_Globals.CMapsPath, "turbo.png"))));
            combocmap.Items.Add(new ColormapItem("viridis", Image.FromFile(Path.Combine(_Globals.CMapsPath, "viridis.png"))));
            combocmap.Items.Add(new ColormapItem("winter", Image.FromFile(Path.Combine(_Globals.CMapsPath, "winter.png"))));
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
            // 
            // lblvmin
            // 
            lblvmin = new Label();
            lblvmin.Dock = DockStyle.Fill;
            lblvmin.Name = "lblvmin";
            lblvmin.TabIndex = 4;
            lblvmin.Text = "Colomrap Minimum";
            lblvmin.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtvmin
            // 
            txtvmin = new TextBox();
            txtvmin.Dock = DockStyle.Fill;
            txtvmin.Name = "txtvmin";
            txtvmin.TabIndex = 11;

            // 
            // lblvmax
            // 
            lblvmax = new Label();
            lblvmax.Dock = DockStyle.Fill;
            lblvmax.Name = "lblvmax";
            lblvmax.TabIndex = 5;
            lblvmax.Text = "Colormap Maximum";
            lblvmax.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtvmax
            // 
            txtvmax = new TextBox();
            txtvmax.Dock = DockStyle.Fill;
            txtvmax.Name = "txtvmax";
            txtvmax.TabIndex = 12;
            // 
            // lblMask
            // 
            lblMask = new Label();
            lblMask.Dock = DockStyle.Fill;
            lblMask.Name = "lblMask";
            lblMask.TabIndex = 7;
            lblMask.Text = "Apply Masking?";
            lblMask.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboMask
            // 
            comboMask = new ComboBox();
            comboMask.Dock = DockStyle.Fill;
            comboMask.DropDownStyle = ComboBoxStyle.DropDownList;
            comboMask.FormattingEnabled = true;
            comboMask.Items.AddRange(new object[] { "Yes", "No" });
            comboMask.Name = "comboMask";
            comboMask.TabIndex = 10;
            comboMask.SelectedIndex = 0;
            //
            // lblBinSelection
            //
            lblBinSelection = new Label();
            lblBinSelection.Dock = DockStyle.Fill;
            lblBinSelection.Name = "lblBinSelection";
            lblBinSelection.TabIndex = 6;
            lblBinSelection.Text = "Bin Selection";
            lblBinSelection.TextAlign = ContentAlignment.MiddleLeft;
            //
            // numericNBins
            //
            numericNBins = new NumericUpDown();
            numericNBins.Dock = DockStyle.Fill;
            numericNBins.Minimum = 1;
            numericNBins.Maximum = 1000;
            numericNBins.Value = 1;
            numericNBins.Name = "numericNBins";
            numericNBins.TabIndex = 13;
            numericNBins.Enabled = false;
            //
            // checkUseMean
            //
            checkUseMean = new CheckBox();
            checkUseMean.Dock = DockStyle.Fill;
            checkUseMean.Name = "checkUseMean";
            checkUseMean.TabIndex = 15;
            checkUseMean.Text = "Use Mean";
            checkUseMean.TextAlign = ContentAlignment.MiddleLeft;
            checkUseMean.Checked = true;
            checkUseMean.CheckedChanged += CheckUseMean_CheckedChanged;
            //
            // lblScale
            //
            lblScale = new Label();
            lblScale.Dock = DockStyle.Fill;
            lblScale.Name = "lblScale";
            lblScale.TabIndex = 0;
            lblScale.Text = "Vector Scale";
            lblScale.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtScale
            // 
            txtScale = new TextBox();
            txtScale.Dock = DockStyle.Fill;
            txtScale.Name = "txtScale";
            txtScale.TabIndex = 16;
            txtScale.Text = "0.005";
            //
            // lblLineWidth
            //
            lblLineWidth = new Label();
            lblLineWidth.Dock = DockStyle.Fill;
            lblLineWidth.Name = "lblLineWidth";
            lblLineWidth.TabIndex = 0;
            lblLineWidth.Text = "Line Width";
            lblLineWidth.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtLineWidth
            //
            txtLineWidth = new TextBox();
            txtLineWidth.Dock = DockStyle.Fill;
            txtLineWidth.Name = "txtLineWidth";
            txtLineWidth.TabIndex = 17;
            txtLineWidth.Text = "2.5";
            //
            // lblLineAlpha
            //
            lblLineAlpha = new Label();
            lblLineAlpha.Dock = DockStyle.Fill;
            lblLineAlpha.Name = "lblLineAlpha";
            lblLineAlpha.TabIndex = 0;
            lblLineAlpha.Text = "Line Alpha";
            lblLineAlpha.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtLineAlpha
            //
            txtLineAlpha = new TextBox();
            txtLineAlpha.Dock = DockStyle.Fill;
            txtLineAlpha.Name = "txtLineAlpha";
            txtLineAlpha.TabIndex = 18;
            txtLineAlpha.Text = "0.9";
            //
            // lblHistBins
            lblHistBins = new Label();
            lblHistBins.Dock = DockStyle.Fill;
            lblHistBins.Name = "lblHistBins";
            lblHistBins.TabIndex = 0;
            lblHistBins.Text = "Number of Histogram Bins";
            lblHistBins.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtHistBins
            numericHistBins = new NumericUpDown();
            numericHistBins.Dock = DockStyle.Fill;
            numericHistBins.Name = "numericHistBins";
            numericHistBins.TabIndex = 19;
            numericHistBins.Minimum = 1;
            numericHistBins.Maximum = 50;
            numericHistBins.Value = 20;
            //
            // lblBeamSelection
            //
            lblBeamSelection = new Label();
            lblBeamSelection.Dock = DockStyle.Fill;
            lblBeamSelection.Name = "lblBeamSelection";
            lblBeamSelection.TabIndex = 6;
            lblBeamSelection.Text = "Beam Selection";
            lblBeamSelection.TextAlign = ContentAlignment.MiddleLeft;
            //
            // numericNBeams
            //
            numericNBeams = new NumericUpDown();
            numericNBeams.Dock = DockStyle.Fill;
            numericNBeams.Minimum = 1;
            numericNBeams.Maximum = 4;
            numericNBeams.Value = 1;
            numericNBeams.Name = "numericNBeams";
            numericNBeams.TabIndex = 13;
            numericNBeams.Enabled = false;
        }

        public ModelMTPlot(string? id)
        {
            InitializeComponent();
            InitializeWidgets();
            comboPlotType.SelectedIndex = 0;
            model = _project.GetObject(type: "MTModel", id: id);

            string path = model?.SelectSingleNode("Path")?.InnerText;
            if (!File.Exists(path))
            {
                MessageBox.Show(text: $"The specified model file does not exist: {path}", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                this.Close(); // Close the form if the file does not exist
            }
        }

        private void btnPlot_Click(object sender, EventArgs e)
        {
            string path = model?.SelectSingleNode("Path")?.InnerText;
            Dictionary<string, string> inputs = null;
            if (comboPlotType.SelectedItem.ToString() == "Mesh Plot")
            {
                inputs = new Dictionary<string, string>
                {
                    { "Task", "PlotModelMesh" },
                    { "Path", path },
                    { "Title", txtTitle.Text },

                };
            }
            //else if (comboPlotType.SelectedItem.ToString() == "Four Beam Flood Plot")
            //{
            //    inputs = new Dictionary<string, string>
            //    {
            //        { "Task", "PlotFourBeamFlood" },
            //        { "EPSG", _project.GetSetting("EPSG") },
            //        { "Water", waterProp.OuterXml.ToString() },
            //        { "Sediment", sedimentProp.OuterXml.ToString() },
            //        { "Instrument", adcp.OuterXml.ToString() },
            //        { "FieldName", comboFieldName.SelectedItem.ToString()},
            //        { "yAxisMode", comboyAxisMode.SelectedItem.ToString()},
            //        { "Colormap", combocmap.SelectedItem.ToString()},
            //        { "vmin", txtvmin.Text},
            //        { "vmax", txtvmax.Text},
            //        { "Title", txtTitle.Text},
            //        { "Mask", comboMask.SelectedItem.ToString()}
            //    };
            //}
            //else if (comboPlotType.SelectedItem.ToString() == "Single Beam Flood Plot")
            //{
            //    inputs = new Dictionary<string, string>
            //    {
            //        { "Task", "PlotSingleBeamFlood" },
            //        { "EPSG", _project.GetSetting("EPSG") },
            //        { "Water", waterProp.OuterXml.ToString() },
            //        { "Sediment", sedimentProp.OuterXml.ToString() },
            //        { "Instrument", adcp.OuterXml.ToString() },
            //        { "BeamSelection", numericNBeams.Value.ToString()},
            //        { "UseMean", checkUseMean.Checked ? "Yes" : "No"},
            //        { "FieldName", comboFieldName.SelectedItem.ToString()},
            //        { "yAxisMode", comboyAxisMode.SelectedItem.ToString()},
            //        { "Colormap", combocmap.SelectedItem.ToString()},
            //        { "vmin", txtvmin.Text},
            //        { "vmax", txtvmax.Text},
            //        { "Title", txtTitle.Text},
            //        { "Mask", comboMask.SelectedItem.ToString()}
            //    };
            //}
            //else if (comboPlotType.SelectedItem.ToString() == "Plot Transect Velocities")
            //{
            //    inputs = new Dictionary<string, string>
            //    {
            //        { "Task", "PlotTransectVelocities" },
            //        { "EPSG", _project.GetSetting("EPSG") },
            //        { "Water", waterProp.OuterXml.ToString() },
            //        { "Sediment", sedimentProp.OuterXml.ToString() },
            //        { "Instrument", adcp.OuterXml.ToString() },
            //        { "BinSelection", numericNBins.Value.ToString()},
            //        { "UseMean", checkUseMean.Checked ? "Yes" : "No"},
            //        { "VectorScale", txtScale.Text},
            //        { "Colormap", combocmap.SelectedItem.ToString()},
            //        { "vmin", txtvmin.Text},
            //        { "vmax", txtvmax.Text},
            //        { "Title", txtTitle.Text},
            //        { "LineWidth", txtLineWidth.Text},
            //        { "LineAlpha", txtLineAlpha.Text},
            //        { "HistBins", numericHistBins.Value.ToString()}
            //    };
            //}
            //else if (comboPlotType.SelectedItem.ToString() == "Beam Geometry Animation")
            //{
            //    inputs = new Dictionary<string, string>
            //    {
            //        { "Task", "PlotBeamGeometryAnimation" },
            //        { "EPSG", _project.GetSetting("EPSG") },
            //        { "Water", waterProp.OuterXml.ToString() },
            //        { "Sediment", sedimentProp.OuterXml.ToString() },
            //        { "Instrument", adcp.OuterXml.ToString() }
            //    };
            //}
            //else if (comboPlotType.SelectedItem.ToString() == "Transect Animation")
            //{
            //    inputs = new Dictionary<string, string>
            //    {
            //        { "Task", "PlotTransectAnimation" },
            //        { "EPSG", _project.GetSetting("EPSG") },
            //        { "Water", waterProp.OuterXml.ToString() },
            //        { "Sediment", sedimentProp.OuterXml.ToString() },
            //        { "Instrument", adcp.OuterXml.ToString() },
            //        { "Colormap", combocmap.SelectedItem.ToString()},
            //        { "vmin", txtvmin.Text},
            //        { "vmax", txtvmax.Text}
            //    };
            //}
            //else
            //{
            //    return;
            //}

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
            if (comboPlotType.SelectedItem.ToString() == "Mesh Plot")
            {
                PropMeshPlot();
            }
            //else if (comboPlotType.SelectedItem.ToString() == "Four Beam Flood Plot")
            //{
            //    PropFourBeamFloodPlot();
            //}
            //else if (comboPlotType.SelectedItem.ToString() == "Single Beam Flood Plot")
            //{
            //    PropSingleBeamFloodPlot();
            //}
            //else if (comboPlotType.SelectedItem.ToString() == "Plot Transect Velocities")
            //{
            //    PlotTransectVelocities();
            //}
            //else if (comboPlotType.SelectedItem.ToString() == "Beam Geometry Animation")
            //{
            //    tableProp.Controls.Clear();
            //}
            //else if (comboPlotType.SelectedItem.ToString() == "Transect Animation")
            //{
            //    PlotTransectAnimation();
            //}
        }

        private void CheckUseMean_CheckedChanged(object? sender, EventArgs e)
        {
            if (checkUseMean.Checked)
            {
                numericNBins.Enabled = false;
                numericNBeams.Enabled = false;
            }
            else
            {
                numericNBins.Enabled = true;
                numericNBeams.Enabled = true;
            }
        }
    }
}
