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
        public List<string> surveyIDs = new List<string>();
        public List<string> shapefileIDs = new List<string>();
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

        int GetIndex(List<string> list, string value)
        {
            int index = list.IndexOf(value);
            return index >= 0 ? index : -1;
        }

        private void PopulateFields()
        {
            XmlNode bgcolor2D = mapSettings2D.SelectSingleNode("BackgroundColor");
            pnl2DBackColor.BackColor = ColorTranslator.FromHtml(bgcolor2D.InnerText ?? "#000000");
            XmlNode fieldName2D = mapSettings2D.SelectSingleNode("FieldName");
            selectComboByValue(combo2DFieldName, fieldName2D.InnerText ?? "Echo Intensity");
            XmlNode cmap2D = mapSettings2D.SelectSingleNode("ColorMap");
            combo2Dcmap.SelectedItem = combo2Dcmap.Items
                .Cast<ColormapItem>()
                .FirstOrDefault(i => i.Name.Equals(cmap2D.InnerText ?? "jet", StringComparison.OrdinalIgnoreCase));
            XmlNode minValue2D = mapSettings2D.SelectSingleNode("vmin");
            txt2Dvmin.Text = minValue2D.InnerText ?? string.Empty;
            XmlNode maxValue2D = mapSettings2D.SelectSingleNode("vmax");
            txt2Dvmax.Text = maxValue2D.InnerText ?? string.Empty;
            XmlNode padDeg2D = mapSettings2D.SelectSingleNode("Padding");
            txt2DPagDeg.Text = padDeg2D.InnerText ?? "0.03";
            XmlNode nGridLines2D = mapSettings2D.SelectSingleNode("NGridLines");
            num2DNGridLines.Value = int.Parse(nGridLines2D.InnerText ?? "10");
            XmlNode gridOpacity2D = mapSettings2D.SelectSingleNode("GridOpacity");
            txt2DGridOpacity.Text = gridOpacity2D.InnerText ?? "0.35";
            XmlNode gridColor2D = mapSettings2D.SelectSingleNode("GridColor");
            pnl2DGridColor.BackColor = ColorTranslator.FromHtml(gridColor2D.InnerText ?? "#333333");
            XmlNode gridWidth2D = mapSettings2D.SelectSingleNode("GridWidth");
            txt2DGridWidth.Text = gridWidth2D.InnerText ?? "1";
            XmlNode nAxisTicks2D = mapSettings2D.SelectSingleNode("NAxisTicks");
            num2DNAxisTicks.Value = int.Parse(nAxisTicks2D.InnerText ?? "7");
            XmlNode tickFontSize2D = mapSettings2D.SelectSingleNode("TickFontSize");
            num2DTickFontSize.Value = int.Parse(tickFontSize2D.InnerText ?? "10");
            XmlNode tickNDecimals2D = mapSettings2D.SelectSingleNode("TickNDecimals");
            num2DNTicksDecimals.Value = int.Parse(tickNDecimals2D.InnerText ?? "4");
            XmlNode axisLabelFontSize2D = mapSettings2D.SelectSingleNode("AxisLabelFontSize");
            num2DAxisLabelFontSize.Value = int.Parse(axisLabelFontSize2D.InnerText ?? "12");
            XmlNode axisLabelColor2D = mapSettings2D.SelectSingleNode("AxisLabelColor");
            pnl2DAxisLabelColor.BackColor = ColorTranslator.FromHtml(axisLabelColor2D.InnerText ?? "#cccccc");
            XmlNode hoverFontSize2D = mapSettings2D.SelectSingleNode("HoverFontSize");
            num2DHoverFontSize.Value = int.Parse(hoverFontSize2D.InnerText ?? "9");
            XmlNode transectLineWidth2D = mapSettings2D.SelectSingleNode("TransectLineWidth");
            txt2DTransectLineWidth.Text = transectLineWidth2D.InnerText ?? "3";
            XmlNode verticalAggBinItem2D = mapSettings2D.SelectSingleNode("VerticalAggBinItem");
            selectComboByValue(combo2DBins, verticalAggBinItem2D.InnerText ?? "Bin");
            if (combo2DBins.SelectedItem.ToString() == "Bin")
            {
                num2DBins.Enabled = true;
                num2DBins.Visible = true;
                txt2DDepth.Enabled = false;
                txt2DDepth.Visible = false;
            }
            else
            {
                num2DBins.Enabled = false;
                num2DBins.Visible = false;
                txt2DDepth.Enabled = true;
                txt2DDepth.Visible = true;
            }
            XmlNode verticalAggBinTarget2D = mapSettings2D.SelectSingleNode("VerticalAggBinTarget");

            if (verticalAggBinTarget2D.InnerText == "Mean")
            {
                num2DBins.Enabled = false;
                txt2DDepth.Enabled = false;
                check2DBins.Checked = true;
            }
            else
            {
                check2DBins.Checked = false;
                if (combo2DBins.SelectedItem.ToString() == "Bin")
                {
                    num2DBins.Enabled = true;
                    num2DBins.Value = int.Parse(verticalAggBinTarget2D.InnerText ?? "1");
                }
                else
                {
                    txt2DDepth.Enabled = true;
                    txt2DDepth.Text = verticalAggBinTarget2D.InnerText ?? "0";
                }
            }
            XmlNode verticalAggBeam2D = mapSettings2D.SelectSingleNode("VerticalAggBeam");
            if (verticalAggBeam2D.InnerText == "Mean")
            {
                check2DBeams.Checked = true;
                num2DBeams.Enabled = false;
            }
            else
            {
                num2DBeams.Value = int.Parse(verticalAggBeam2D.InnerText ?? "1");
                check2DBeams.Checked = false;
            }

            XmlElement survey2Ds = mapSettings2D.SelectSingleNode("Surveys") as XmlElement;
            List<XmlNode> surveys2D = survey2Ds.SelectNodes("Survey")?.Cast<XmlNode>().ToList() ?? new List<XmlNode>();
            for (int i = 0; i < surveys2D.Count; i++)
            {
                int index = GetIndex(surveyIDs, surveys2D[i].InnerText);
                if (index > 0)
                {
                    list2DSurveys.SetItemChecked(index, true);
                }
            }

            XmlNode bgcolor3D = mapSettings3D.SelectSingleNode("BackgroundColor");
            pnl3DBackColor.BackColor = ColorTranslator.FromHtml(bgcolor3D.InnerText ?? "#000000");
            XmlNode fieldName3D = mapSettings3D.SelectSingleNode("FieldName");
            selectComboByValue(combo3DFieldName, fieldName3D.InnerText ?? "Echo Intensity");
            XmlNode cmap3D = mapSettings3D.SelectSingleNode("ColorMap");
            combo3Dcmap.SelectedItem = combo3Dcmap.Items
                .Cast<ColormapItem>()
                .FirstOrDefault(i => i.Name.Equals(cmap3D.InnerText ?? "jet", StringComparison.OrdinalIgnoreCase));
            XmlNode minValue3D = mapSettings3D.SelectSingleNode("vmin");
            txt3Dvmin.Text = minValue3D.InnerText ?? string.Empty;
            XmlNode maxValue3D = mapSettings3D.SelectSingleNode("vmax");
            txt3Dvmax.Text = maxValue3D.InnerText ?? string.Empty;
            XmlNode padDeg3D = mapSettings3D.SelectSingleNode("Padding");
            txt3DPagDeg.Text = padDeg3D.InnerText ?? "0.03";
            XmlNode nGridLines3D = mapSettings3D.SelectSingleNode("NGridLines");
            num3DNGridLines.Value = int.Parse(nGridLines3D.InnerText ?? "10");
            XmlNode gridOpacity3D = mapSettings3D.SelectSingleNode("GridOpacity");
            txt3DGridOpacity.Text = gridOpacity3D.InnerText ?? "0.35";
            XmlNode gridColor3D = mapSettings3D.SelectSingleNode("GridColor");
            pnl3DGridColor.BackColor = ColorTranslator.FromHtml(gridColor3D.InnerText ?? "#333333");
            XmlNode gridWidth3D = mapSettings3D.SelectSingleNode("GridWidth");
            txt3DGridWidth.Text = gridWidth3D.InnerText ?? "1";
            XmlNode nAxisTicks3D = mapSettings3D.SelectSingleNode("NAxisTicks");
            num3DNAxisTicks.Value = int.Parse(nAxisTicks3D.InnerText ?? "7");
            XmlNode tickFontSize3D = mapSettings3D.SelectSingleNode("TickFontSize");
            num3DTickFontSize.Value = int.Parse(tickFontSize3D.InnerText ?? "10");
            XmlNode tickNDecimals3D = mapSettings3D.SelectSingleNode("TickNDecimals");
            num3DNTicksDecimals.Value = int.Parse(tickNDecimals3D.InnerText ?? "4");
            XmlNode axisLabelFontSize3D = mapSettings3D.SelectSingleNode("AxisLabelFontSize");
            num3DAxisLabelFontSize.Value = int.Parse(axisLabelFontSize3D.InnerText ?? "12");
            XmlNode axisLabelColor3D = mapSettings3D.SelectSingleNode("AxisLabelColor");
            pnl3DAxisLabelColor.BackColor = ColorTranslator.FromHtml(axisLabelColor3D.InnerText ?? "#cccccc");
            XmlNode hoverFontSize3D = mapSettings3D.SelectSingleNode("HoverFontSize");
            num3DHoverFontSize.Value = int.Parse(hoverFontSize3D.InnerText ?? "9");
            XmlNode zScale3D = mapSettings3D.SelectSingleNode("ZScale");
            txt3DZScale.Text = zScale3D.InnerText ?? "3.0";

            XmlElement survey3Ds = mapSettings3D.SelectSingleNode("Surveys") as XmlElement;
            List<XmlNode> surveys3D = survey3Ds.SelectNodes("Survey")?.Cast<XmlNode>().ToList() ?? new List<XmlNode>();
            for (int i = 0; i < surveys3D.Count; i++)
            {
                int index = GetIndex(surveyIDs, surveys3D[i].InnerText);
                if (index > 0)
                {
                    list3DSurveys.SetItemChecked(index, true);
                }
            }


            XmlNodeList shapefiles = mapShapefiles.SelectNodes("Shapefile");
            if (shapefiles != null)
            {
                foreach (XmlElement shapefile in shapefiles)
                {
                    string id = shapefile.GetAttribute("id");
                    int index = GetIndex(shapefileIDs, id);
                    string checkStatus = shapefile.SelectSingleNode("Checked")?.InnerText ?? "false";
                    if (index > 0 && checkStatus.ToLower() == "true")
                    {
                        listShapefiles.SetItemChecked(index, true);
                    }
                }
            }

            isSaved = true; // Initially, fields are populated and considered saved
        }

        public MapOptions()
        {
            InitializeComponent();
            InitializeWidgets();
            mapSettings = _project.GetObject("MapSettings", "2");
            mapSettings2D = mapSettings.SelectSingleNode("Map2D") as XmlElement;
            mapSettings3D = mapSettings.SelectSingleNode("Map3D") as XmlElement;
            mapShapefiles = mapSettings.SelectSingleNode("MapShapefiles") as XmlElement;
            XmlNodeList surveys = _project.GetObjects(type: "Survey");
            foreach (XmlNode surveyNode in surveys)
            {
                XmlElement survey = (XmlElement)surveyNode;
                string surveyName = survey.GetAttribute("name");
                list2DSurveys.Items.Add(surveyName);
                list3DSurveys.Items.Add(surveyName);
                surveyIDs.Add(survey.GetAttribute("id"));
            }
            XmlNodeList shapefiles = _project.GetObjects(type: "Shapefile");
            foreach (XmlNode shapefileNode in shapefiles)
            {
                XmlElement shapefile = (XmlElement)shapefileNode;
                string shapefileName = shapefile.GetAttribute("name");
                listShapefiles.Items.Add(shapefileName);
                shapefileIDs.Add(shapefile.GetAttribute("id"));

                // Store each shapefile's XmlElement in the new dictionary
                XmlElement existingShpSettings = mapShapefiles.SelectSingleNode($"Shapefile[@id='{shapefile.GetAttribute("id")}']") as XmlElement;
                if (existingShpSettings != null)
                {
                    shapefileSettings[shapefile.GetAttribute("id")] = existingShpSettings;
                }
                else
                {
                    // If settings don't exist, create a new XmlElement for it
                    XmlElement newShpSettings = _Globals.Config.CreateElement("Shapefile");
                    newShpSettings.SetAttribute("id", shapefile.GetAttribute("id"));
                    mapShapefiles.AppendChild(newShpSettings);
                    shapefileSettings[shapefile.GetAttribute("id")] = newShpSettings;
                }
            }
            PopulateFields();

            if (shapefiles.Count > 0)
            {
                currentShapefileIndex = 0;
                XmlElement shapefile = (XmlElement)shapefiles[0];
                bool checkStatus = shapefile.SelectSingleNode("Checked")?.InnerText.ToLower() == "true";
                PopulateProperties(shapefile);
                listShapefiles.SetSelected(0, checkStatus);
            }
            else
                currentShapefileIndex = -1;

            MessageBox.Show(currentShapefileIndex.ToString());
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
                    int status = SaveSettings();
                    if (status == 1)
                    {
                        this.Close();
                        return;
                    }
                    else
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

        private void btn2DBackColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog
            {
                AllowFullOpen = true,
                AnyColor = true,
                FullOpen = true,
                Color = pnl2DBackColor.BackColor,
            };
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                pnl2DBackColor.BackColor = colorDialog.Color;
            }
        }

        private void btn2DGridColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog
            {
                AllowFullOpen = true,
                AnyColor = true,
                FullOpen = true,
                Color = pnl2DGridColor.BackColor,
            };
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                pnl2DGridColor.BackColor = colorDialog.Color;
            }
        }

        private void btn2DAxisLabelColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog
            {
                AllowFullOpen = true,
                AnyColor = true,
                FullOpen = true,
                Color = pnl2DAxisLabelColor.BackColor,
            };
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                pnl2DAxisLabelColor.BackColor = colorDialog.Color;
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
        }

        private void btn3DBackColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog
            {
                AllowFullOpen = true,
                AnyColor = true,
                FullOpen = true,
                Color = pnl3DBackColor.BackColor,
            };
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                pnl3DBackColor.BackColor = colorDialog.Color;
            }
        }

        private void btn3DGridColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog
            {
                AllowFullOpen = true,
                AnyColor = true,
                FullOpen = true,
                Color = pnl3DGridColor.BackColor,
            };
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                pnl3DGridColor.BackColor = colorDialog.Color;
            }
        }

        private void btn3DAxisLabelColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog
            {
                AllowFullOpen = true,
                AnyColor = true,
                FullOpen = true,
                Color = pnl3DAxisLabelColor.BackColor,
            };
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                pnl3DAxisLabelColor.BackColor = colorDialog.Color;
            }
        }

        private int SaveSettings()
        {
            try
            {
                //XmlElement? mapSettings = _project.GetObject("MapSettings", "2") as XmlElement;
                //XmlElement? mapSettings2D = mapSettings?.SelectSingleNode("Map2D") as XmlElement;
                if (mapSettings2D != null)
                {
                    var bgColorNode = mapSettings2D.SelectSingleNode("BackgroundColor");
                    if (bgColorNode != null)
                        bgColorNode.InnerText = ColorTranslator.ToHtml(pnl2DBackColor.BackColor);

                    var fieldNameNode = mapSettings2D.SelectSingleNode("FieldName");
                    if (fieldNameNode != null)
                        fieldNameNode.InnerText = getValueByIndex(combo2DFieldName, combo2DFieldName.SelectedIndex);

                    var colorMapNode = mapSettings2D.SelectSingleNode("ColorMap");
                    if (colorMapNode != null)
                        colorMapNode.InnerText = ((ColormapItem)combo2Dcmap.SelectedItem).Name;

                    var vminNode = mapSettings2D.SelectSingleNode("vmin");
                    if (vminNode != null)
                        vminNode.InnerText = txt2Dvmin.Text;

                    var vmaxNode = mapSettings2D.SelectSingleNode("vmax");
                    if (vmaxNode != null)
                        vmaxNode.InnerText = txt2Dvmax.Text;

                    var paddingNode = mapSettings2D.SelectSingleNode("Padding");
                    if (paddingNode != null)
                        paddingNode.InnerText = txt2DPagDeg.Text;

                    var nGridLinesNode = mapSettings2D.SelectSingleNode("NGridLines");
                    if (nGridLinesNode != null)
                        nGridLinesNode.InnerText = num2DNGridLines.Value.ToString();

                    var gridOpacityNode = mapSettings2D.SelectSingleNode("GridOpacity");
                    if (gridOpacityNode != null)
                        gridOpacityNode.InnerText = txt2DGridOpacity.Text;

                    var gridColorNode = mapSettings2D.SelectSingleNode("GridColor");
                    if (gridColorNode != null)
                        gridColorNode.InnerText = ColorTranslator.ToHtml(pnl2DGridColor.BackColor);

                    var gridWidthNode = mapSettings2D.SelectSingleNode("GridWidth");
                    if (gridWidthNode != null)
                        gridWidthNode.InnerText = txt2DGridWidth.Text;

                    var nAxisTicksNode = mapSettings2D.SelectSingleNode("NAxisTicks");
                    if (nAxisTicksNode != null)
                        nAxisTicksNode.InnerText = num2DNAxisTicks.Value.ToString();

                    var tickFontSizeNode = mapSettings2D.SelectSingleNode("TickFontSize");
                    if (tickFontSizeNode != null)
                        tickFontSizeNode.InnerText = num2DTickFontSize.Value.ToString();

                    var tickNDecimalsNode = mapSettings2D.SelectSingleNode("TickNDecimals");
                    if (tickNDecimalsNode != null)
                        tickNDecimalsNode.InnerText = num2DNTicksDecimals.Value.ToString();

                    var axisLabelFontSizeNode = mapSettings2D.SelectSingleNode("AxisLabelFontSize");
                    if (axisLabelFontSizeNode != null)
                        axisLabelFontSizeNode.InnerText = num2DAxisLabelFontSize.Value.ToString();

                    var axisLabelColorNode = mapSettings2D.SelectSingleNode("AxisLabelColor");
                    if (axisLabelColorNode != null)
                        axisLabelColorNode.InnerText = ColorTranslator.ToHtml(pnl2DAxisLabelColor.BackColor);

                    var hoverFontSizeNode = mapSettings2D.SelectSingleNode("HoverFontSize");
                    if (hoverFontSizeNode != null)
                        hoverFontSizeNode.InnerText = num2DHoverFontSize.Value.ToString();

                    var transectLineWidthNode = mapSettings2D.SelectSingleNode("TransectLineWidth");
                    if (transectLineWidthNode != null)
                        transectLineWidthNode.InnerText = txt2DTransectLineWidth.Text;

                    var verticalAggBinItemNode = mapSettings2D.SelectSingleNode("VerticalAggBinItem");
                    if (verticalAggBinItemNode != null)
                        verticalAggBinItemNode.InnerText = getValueByIndex(combo2DBins, combo2DBins.SelectedIndex);

                    var verticalAggBinTargetNode = mapSettings2D.SelectSingleNode("VerticalAggBinTarget");
                    if (verticalAggBinTargetNode != null)
                    {
                        if (check2DBins.Checked)
                            verticalAggBinTargetNode.InnerText = "Mean";
                        else
                        {
                            if (combo2DBins.SelectedItem.ToString() == "Bin")
                                verticalAggBinTargetNode.InnerText = num2DBins.Value.ToString();
                            else
                                verticalAggBinTargetNode.InnerText = txt2DDepth.Text;
                        }
                    }

                    var verticalAggBeamNode = mapSettings2D.SelectSingleNode("VerticalAggBeam");
                    if (verticalAggBeamNode != null)
                    {
                        if (check2DBeams.Checked)
                            verticalAggBeamNode.InnerText = "Mean";
                        else
                            verticalAggBeamNode.InnerText = num2DBeams.Value.ToString();
                    }

                    XmlElement surveys2D = mapSettings2D.SelectSingleNode("Surveys") as XmlElement;
                    surveys2D.RemoveAll();
                    for (int i = 0; i < list2DSurveys.Items.Count; i++)
                    {
                        if (list2DSurveys.GetItemChecked(i))
                        {
                            XmlElement surveyElement = _Globals.Config.CreateElement("Survey");
                            surveyElement.InnerText = surveyIDs[i];
                            surveys2D.AppendChild(surveyElement);
                        }
                    }
                }

                //XmlElement? mapSettings3D = mapSettings?.SelectSingleNode("Map3D") as XmlElement;
                if (mapSettings3D != null)
                {
                    var bgColorNode = mapSettings3D.SelectSingleNode("BackgroundColor");
                    if (bgColorNode != null)
                        bgColorNode.InnerText = ColorTranslator.ToHtml(pnl3DBackColor.BackColor);

                    var fieldNameNode = mapSettings3D.SelectSingleNode("FieldName");
                    if (fieldNameNode != null)
                        fieldNameNode.InnerText = getValueByIndex(combo3DFieldName, combo3DFieldName.SelectedIndex);

                    var colorMapNode = mapSettings3D.SelectSingleNode("ColorMap");
                    if (colorMapNode != null)
                        colorMapNode.InnerText = ((ColormapItem)combo3Dcmap.SelectedItem).Name;

                    var vminNode = mapSettings3D.SelectSingleNode("vmin");
                    if (vminNode != null)
                        vminNode.InnerText = txt3Dvmin.Text;

                    var vmaxNode = mapSettings3D.SelectSingleNode("vmax");
                    if (vmaxNode != null)
                        vmaxNode.InnerText = txt3Dvmax.Text;

                    var paddingNode = mapSettings3D.SelectSingleNode("Padding");
                    if (paddingNode != null)
                        paddingNode.InnerText = txt3DPagDeg.Text;

                    var nGridLinesNode = mapSettings3D.SelectSingleNode("NGridLines");
                    if (nGridLinesNode != null)
                        nGridLinesNode.InnerText = num3DNGridLines.Value.ToString();

                    var gridOpacityNode = mapSettings3D.SelectSingleNode("GridOpacity");
                    if (gridOpacityNode != null)
                        gridOpacityNode.InnerText = txt3DGridOpacity.Text;

                    var gridColorNode = mapSettings3D.SelectSingleNode("GridColor");
                    if (gridColorNode != null)
                        gridColorNode.InnerText = ColorTranslator.ToHtml(pnl3DGridColor.BackColor);

                    var gridWidthNode = mapSettings3D.SelectSingleNode("GridWidth");
                    if (gridWidthNode != null)
                        gridWidthNode.InnerText = txt3DGridWidth.Text;

                    var nAxisTicksNode = mapSettings3D.SelectSingleNode("NAxisTicks");
                    if (nAxisTicksNode != null)
                        nAxisTicksNode.InnerText = num3DNAxisTicks.Value.ToString();

                    var tickFontSizeNode = mapSettings3D.SelectSingleNode("TickFontSize");
                    if (tickFontSizeNode != null)
                        tickFontSizeNode.InnerText = num3DTickFontSize.Value.ToString();

                    var tickNDecimalsNode = mapSettings3D.SelectSingleNode("TickNDecimals");
                    if (tickNDecimalsNode != null)
                        tickNDecimalsNode.InnerText = num3DNTicksDecimals.Value.ToString();

                    var axisLabelFontSizeNode = mapSettings3D.SelectSingleNode("AxisLabelFontSize");
                    if (axisLabelFontSizeNode != null)
                        axisLabelFontSizeNode.InnerText = num3DAxisLabelFontSize.Value.ToString();

                    var axisLabelColorNode = mapSettings3D.SelectSingleNode("AxisLabelColor");
                    if (axisLabelColorNode != null)
                        axisLabelColorNode.InnerText = ColorTranslator.ToHtml(pnl3DAxisLabelColor.BackColor);

                    var hoverFontSizeNode = mapSettings3D.SelectSingleNode("HoverFontSize");
                    if (hoverFontSizeNode != null)
                        hoverFontSizeNode.InnerText = num3DHoverFontSize.Value.ToString();

                    var zScaleNode = mapSettings3D.SelectSingleNode("ZScale");
                    if (zScaleNode != null)
                        zScaleNode.InnerText = txt3DZScale.Text;

                    XmlElement surveys3D = mapSettings3D.SelectSingleNode("Surveys") as XmlElement;
                    surveys3D.RemoveAll();
                    for (int i = 0; i < list3DSurveys.Items.Count; i++)
                    {
                        if (list3DSurveys.GetItemChecked(i))
                        {
                            XmlElement surveyElement = _Globals.Config.CreateElement("Survey");
                            surveyElement.InnerText = surveyIDs[i];
                            surveys3D.AppendChild(surveyElement);
                        }
                    }
                }

                //XmlElement? mapShapefiles = mapSettings?.SelectSingleNode("MapShapefiles") as XmlElement;
                foreach (var shpElement in shapefileSettings.Values)
                {
                    // The updates are already in the XmlElements in the dictionary.
                    // You just need to ensure the parent node in the main XML document is correct.
                    // This is handled by how you populated the dictionary in the constructor.
                }

                _project.SaveConfig(saveMode: 3);
                return 1;
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    text: $"An error occurred while saving settings: {ex.Message}",
                    caption: "Save Error",
                    buttons: MessageBoxButtons.OK,
                    icon: MessageBoxIcon.Error);
                return 0;
            }
            finally
            {
                isSaved = true;
            }
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
                XmlElement newShapefile = _Globals.Config.CreateElement("Shapefile");
                newShapefile.SetAttribute("name", selectedName);
                newShapefile.SetAttribute("type", "Shapefile");
                string id = _project.GetNextId().ToString();
                newShapefile.SetAttribute("id", id);
                XmlElement pathElement = _Globals.Config.CreateElement("Path");
                pathElement.InnerText = selectedPath;
                newShapefile.AppendChild(pathElement);
                XmlElement typeElement = _Globals.Config.CreateElement("Type");
                typeElement.InnerText = selectedType;
                newShapefile.AppendChild(typeElement);
                XmlElement checkedElement = _Globals.Config.CreateElement("Checked");
                checkedElement.InnerText = "true"; // Default to checked when added
                newShapefile.AppendChild(checkedElement);
                XmlElement colorElement = _Globals.Config.CreateElement("Color");
                colorElement.InnerText = "#FF0000"; // Default color red, can be modified later
                newShapefile.AppendChild(colorElement);
                XmlElement sizeElement = _Globals.Config.CreateElement("Size");
                sizeElement.InnerText = "6"; // Default marker size
                newShapefile.AppendChild(sizeElement);


                if (selectedType.Contains("Point"))
                {
                    XmlElement labelElement = _Globals.Config.CreateElement("Label");
                    labelElement.InnerText = ""; // Default no label
                    newShapefile.AppendChild(labelElement);
                    XmlElement labelFontSizeElement = _Globals.Config.CreateElement("LabelFontSize");
                    labelFontSizeElement.InnerText = "11"; // Default font size
                    newShapefile.AppendChild(labelFontSizeElement);
                    XmlElement labelColorElement = _Globals.Config.CreateElement("LabelColor");
                    labelColorElement.InnerText = "#FFC0CB"; // Default label color pink
                    newShapefile.AppendChild(labelColorElement);
                }
                
                else
                {
                    MessageBox.Show(
                        text: "Unsupported shapefile type.",
                        caption: "Error",
                        buttons: MessageBoxButtons.OK,
                        icon: MessageBoxIcon.Error
                        );
                }
                shapefileIDs.Add(id);
                mapShapefiles.AppendChild(newShapefile);
                PopulateProperties(newShapefile);
                listShapefiles.Items.Add(selectedName, true); // Add and check the new shapefile
                isSaved = false;
            }
        }

        private void PopulateProperties(XmlElement shapefile)
        {
            string type = shapefile.SelectSingleNode("Type")?.InnerText ?? "";
            txtShpFilename.Text = shapefile.SelectSingleNode("Path")?.InnerText ?? "";
            txtShpType.Text = type;
            pnlShpColor.BackColor = ColorTranslator.FromHtml(shapefile.SelectSingleNode("Color")?.InnerText ?? "#FF0000");
            txtShpSize.Text = shapefile.SelectSingleNode("Size")?.InnerText ?? "6";

            if (type.Contains("Point"))
            {
                lblShpSize.Text = "Marker Size";
                lblShpLabel.Visible = true;
                txtShpLabel.Visible = true;
                txtShpLabel.Text = shapefile.SelectSingleNode("Label")?.InnerText ?? "";
                lblShpLabelFontSize.Visible = true;
                numShpLabelFontSize.Visible = true;
                numShpLabelFontSize.Value = int.Parse(shapefile.SelectSingleNode("LabelFontSize")?.InnerText ?? "11");
                lblShpLabelColor.Visible = true;
                pnlShpLabelColor.Visible = true;
                btnShpLabelColor.Visible = true;
                pnlShpLabelColor.BackColor = ColorTranslator.FromHtml(shapefile.SelectSingleNode("LabelColor")?.InnerText ?? "#FFC0CB");
            }
            else if (type.Contains("Line"))
            {
                lblShpSize.Text = "Line Width";
                lblShpLabel.Visible = false;
                txtShpLabel.Visible = false;
                lblShpLabelFontSize.Visible = false;
                numShpLabelFontSize.Visible = false;
                lblShpLabelColor.Visible = false;
                pnlShpLabelColor.Visible = false;
                btnShpLabelColor.Visible = false;
            }
            else if (type.Contains("Polygon"))
            {
                lblShpSize.Text = "Width";
                lblShpLabel.Visible = false;
                txtShpLabel.Visible = false;
                lblShpLabelFontSize.Visible = false;
                numShpLabelFontSize.Visible = false;
                lblShpLabelColor.Visible = false;
                pnlShpLabelColor.Visible = false;
                btnShpLabelColor.Visible = false;
            }
        }

        private void UpdateShapefile()
        {
            string id = shapefileIDs[currentShapefileIndex];
            XmlElement shapefile = _project.GetObject(type: "Shapefile", id: id) as XmlElement;
            shapefile.SelectSingleNode("Color")!.InnerText = ColorTranslator.ToHtml(pnlShpColor.BackColor);
            shapefile.SelectSingleNode("Size")!.InnerText = txtShpSize.Text;

            string type = shapefile.SelectSingleNode("Type")?.InnerText ?? "";
            if (type.Contains("Point"))
            {
                shapefile.SelectSingleNode("Label")!.InnerText = txtShpLabel.Text;
                shapefile.SelectSingleNode("LabelFontSize")!.InnerText = numShpLabelFontSize.Value.ToString();
                shapefile.SelectSingleNode("LabelColor")!.InnerText = ColorTranslator.ToHtml(pnlShpLabelColor.BackColor);
            }
        }

        private void listShapefiles_MouseClick(object sender, MouseEventArgs e)
        {
            UpdateShapefile();
            _project.SaveConfig(saveMode: 3);
            int index = listShapefiles.IndexFromPoint(e.Location);
            if (index != ListBox.NoMatches)
            {
                Rectangle itemRect = listShapefiles.GetItemRectangle(index);
                Rectangle checkBoxRect = new Rectangle(itemRect.Location, new Size(16, itemRect.Height));
                if (checkBoxRect.Contains(e.Location))
                {
                    listShapefiles.SetItemChecked(index, !listShapefiles.GetItemChecked(index));
                    isSaved = false;
                }
                else
                {
                    
                    string id = shapefileIDs[index];
                    string xpath = $"Shapefile[@id='{id}']";
                    XmlNode shapefileNode = mapShapefiles.SelectSingleNode(xpath);
                    XmlElement shapefileElement = shapefileNode as XmlElement;
                    if (shapefileElement != null)
                    {
                        PopulateProperties(shapefileElement);
                    }
                    currentShapefileIndex = index;
                }
            }
        }

        private void listShapefiles_SelectedIndexChanged(object sender, EventArgs e)
        {
            UpdateShapefile();
            _project.SaveConfig(saveMode: 3);
            if (listShapefiles.SelectedIndex >= 0)
            {
                currentShapefileIndex = listShapefiles.SelectedIndex;
                string selectedShpID = shapefileIDs[currentShapefileIndex];

                if (shapefileSettings.TryGetValue(selectedShpID, out XmlElement shapefile))
                {
                    PopulateProperties(shapefile);
                }
            }
        }

        private void btnShpColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog
            {
                AllowFullOpen = true,
                AnyColor = true,
                FullOpen = true,
                Color = pnlShpColor.BackColor,
            };
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                pnlShpColor.BackColor = colorDialog.Color;
            }

            if (currentShapefileIndex >= 0)
            {
                string currentShpID = shapefileIDs[currentShapefileIndex];
                if (shapefileSettings.TryGetValue(currentShpID, out XmlElement shapefile))
                {
                    var node = shapefile.SelectSingleNode("Color");
                    if (node != null)
                    {
                        node.InnerText = ColorTranslator.ToHtml(pnlShpColor.BackColor);
                        isSaved = false;
                    }
                }
            }
        }

        private void btnShpLabelColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog
            {
                AllowFullOpen = true,
                AnyColor = true,
                FullOpen = true,
                Color = pnlShpLabelColor.BackColor,
            };
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                pnlShpLabelColor.BackColor = colorDialog.Color;
            }
            if (currentShapefileIndex >= 0)
            {
                string currentShpID = shapefileIDs[currentShapefileIndex];
                if (shapefileSettings.TryGetValue(currentShpID, out XmlElement shapefile))
                {
                    var node = shapefile.SelectSingleNode("LabelColor");
                    if (node != null)
                    {
                        node.InnerText = ColorTranslator.ToHtml(pnlShpLabelColor.BackColor);
                        isSaved = false;
                    }
                }
            }
        }

        private void txtShpSize_TextChanged(object sender, EventArgs e)
        {
            if (currentShapefileIndex >= 0)
            {
                string currentShpID = shapefileIDs[currentShapefileIndex];
                if (shapefileSettings.TryGetValue(currentShpID, out XmlElement shapefile))
                {
                    var node = shapefile.SelectSingleNode("Size");
                    if (node != null)
                    {
                        node.InnerText = txtShpSize.Text;
                        isSaved = false;
                    }
                }
            }
        }

        private void txtShpLabel_TextChanged(object sender, EventArgs e)
        {
            if (currentShapefileIndex >= 0)
            {
                string currentShpID = shapefileIDs[currentShapefileIndex];
                if (shapefileSettings.TryGetValue(currentShpID, out XmlElement shapefile))
                {
                    var node = shapefile.SelectSingleNode("Label");
                    if (node != null)
                    {
                        node.InnerText = txtShpLabel.Text;
                        isSaved = false;
                    }
                }
            }
        }

        private void numShpLabelFontSize_ValueChanged(object sender, EventArgs e)
        {
            if (currentShapefileIndex >= 0)
            {
                string currentShpID = shapefileIDs[currentShapefileIndex];
                if (shapefileSettings.TryGetValue(currentShpID, out XmlElement shapefile))
                {
                    var node = shapefile.SelectSingleNode("LabelFontSize");
                    if (node != null)
                    {
                        node.InnerText = numShpLabelFontSize.Value.ToString();
                        isSaved = false;
                    }
                }
            }
        }
    }
}
