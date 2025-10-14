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


    public partial class ProjectPlot : Form
    {
        public XmlNodeList? hdModels;
        public XmlElement? hdModel;
        public XmlNodeList? mtModels;
        public XmlElement? mtModel;
        public XmlNodeList? adcps;
        public XmlElement? adcp;
        public _ClassConfigurationManager _project = new();

        public static Label? lblHDModel;
        public static ComboBox? comboHDModel;

        public static Label? lblMTModel;
        public static ComboBox? comboMTModel;

        public static Label? lblADCP;
        public static ComboBox? comboADCP;

        public static Label? lblModelQuiverMode;
        public static ComboBox? comboModelQuiverMode;

        public static Label? lblFieldPixelSize;
        public static TextBox? txtFieldPixelSize;

        public static Label? lblFieldQuiverStrideN;
        public static NumericUpDown? numFieldQuiverStrideN;

        public static Label? lblcmap;
        public static ComboBox? combocmap;

        public static Label? lblScale;
        public static ComboBox? comboScale;

        public static Label? lblvmin;
        public static TextBox? txtvmin;

        public static Label? lblvmax;
        public static TextBox? txtvmax;

        public static Label? lblColorBarTickDecimals;
        public static NumericUpDown? numColorBarTickDecimals;

        public static Label? lblAxisTickDecimals;
        public static NumericUpDown? numAxisTickDecimals;

        public static Label? lblPadM;
        public static TextBox? txtPadM;

        public static Label? lblPixelSizeM;
        public static TextBox? txtPixelSizeM;

        public static Label? lblCMapBottomThreshold;
        public static TextBox? txtCMapBottomThreshold;

        public static Label? lblTransectColor;
        public static Panel? pnlTransectCOlor;
        public static Button? btnTransectColor;

        public static Label? lblBinConfiguration;
        public static ComboBox? comboBinConfiguration;

        public static Label? lblBinTarget;
        public static TextBox? txtBinTarget;
        public static NumericUpDown? numBinTarget;
        public static CheckBox checkBinTarget;

        public static Label? lblBeamSelection;
        public static NumericUpDown? numericNBeams;

        public static Label? lblQuiverEveryN;
        public static NumericUpDown? numericQuiverEveryN;

        public static Label? lblQuiverScale;
        public static TextBox? txtQuiverScale;

        public static Label? lblQuiverColor;
        public static Panel? pnlQuiverColor;
        public static Button? btnQuiverColor;

        public static Label? lblTransectLineWidth;
        public static TextBox? txtTransectLineWidth;

        public static Label? lblAnimationStartIndex;
        public static NumericUpDown? numericAnimationStartIndex;
        public static CheckBox? checkAnimationStartIndex;

        public static Label? lblAnimationEndIndex;
        public static NumericUpDown? numericAnimationEndIndex;
        public static CheckBox? checkAnimationEndIndex;

        public static Label? lblAnimationTimeStep;
        public static NumericUpDown? numericAnimationTimeStep;

        public static Label? lblAnimationInterval;
        public static NumericUpDown? numericAnimationInterval;

        public static Label? lblAnimationOutputFile;
        public static TextBox? txtAnimationOutputFile;
        public static Button? btnAnimationOutputFile;

        public static Label? lblQuiverWidth;
        public static TextBox? txtQuiverWidth;

        public static Label? lblQuiverHeadWidth;
        public static TextBox? txtQuiverHeadWidth;

        public static Label? lblQuiverHeadLength;
        public static TextBox? txtQuiverHeadLength;

        public static Label? lblsscLevels;
        public static TextBox? txtsscLevels;

        private void PropHDModelComparison()
        {
            XmlNodeList? hdModels = _project.GetObjects("HDModel");
            foreach (XmlNode node in hdModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboHDModel.Items.Add(item);
            }
            XmlNodeList adcps = _project.GetObjects("VesselMountedADCP");
            foreach (XmlNode node in adcps)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboADCP.Items.Add(item);
            }
            tableProp.Controls.Clear();

            tableProp.RowStyles.Clear();
            tableProp.RowCount = 10;
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));

            tableProp.Controls.Add(lblHDModel, 0, 0);
            tableProp.Controls.Add(comboHDModel, 1, 0);
            tableProp.Controls.Add(lblADCP, 0, 1);
            tableProp.Controls.Add(comboADCP, 1, 1);
            tableProp.Controls.Add(lblcmap, 0, 5);
            tableProp.Controls.Add(combocmap, 1, 5);
            tableProp
            tableProp.Controls.Add(lblModelQuiverMode, 0, 2);
            tableProp.Controls.Add(comboModelQuiverMode, 1, 2);
            tableProp.Controls.Add(lblFieldPixelSize, 0, 3);
            tableProp.Controls.Add(txtFieldPixelSize, 1, 3);
            tableProp.Controls.Add(lblFieldQuiverStrideN, 0, 4);
            tableProp.Controls.Add(numFieldQuiverStrideN, 1, 4);
            
        }

        private void PropMTModelComparison()
        {
            XmlNodeList? mtModels = _project.GetObjects("MTModel");
            foreach (XmlNode node in mtModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboMTModel.Items.Add(item);
            }
            XmlNodeList? adcps = _project.GetObjects("VesselMountedADCP");
            foreach (XmlNode node in adcps)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboADCP.Items.Add(item);
            }
            tableProp.Controls.Clear();

            tableProp.RowStyles.Clear();
            tableProp.RowCount = 19;
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));

            tableProp.Controls.Add(lblMTModel, 0, 0);
            tableProp.Controls.Add(comboMTModel, 1, 0);
            tableProp.Controls.Add(lblADCP, 0, 1);
            tableProp.Controls.Add(comboADCP, 1, 1);
            tableProp.Controls.Add(lblScale, 0, 2);
            tableProp.Controls.Add(comboScale, 1, 2);
            tableProp.Controls.Add(lblvmin, 0, 3);
            tableProp.Controls.Add(txtvmin, 1, 3);
            tableProp.Controls.Add(lblvmax, 0, 4);
            tableProp.Controls.Add(txtvmax, 1, 4);
            tableProp.Controls.Add(lblcmap, 0, 5);
            tableProp.Controls.Add(combocmap, 1, 5);
            tableProp.Controls.Add(lblColorBarTickDecimals, 0, 6);
            tableProp.Controls.Add(numColorBarTickDecimals, 1, 6);
            tableProp.Controls.Add(lblAxisTickDecimals, 0, 7);
            tableProp.Controls.Add(numAxisTickDecimals, 1, 7);
            tableProp.Controls.Add(lblPadM, 0, 8);
            tableProp.Controls.Add(txtPadM, 1, 8);
            tableProp.Controls.Add(lblPixelSizeM, 0, 9);
            tableProp.Controls.Add(txtPixelSizeM, 1, 9);
            tableProp.Controls.Add(lblCMapBottomThreshold, 0, 10);
            tableProp.Controls.Add(txtCMapBottomThreshold, 1, 10);
            tableProp.Controls.Add(lblTransectColor, 0, 11);
            tableProp.Controls.Add(pnlTransectCOlor, 1, 11);
            tableProp.Controls.Add(btnTransectColor, 2, 11);
            tableProp.Controls.Add(lblBinConfiguration, 0, 12);
            tableProp.Controls.Add(comboBinConfiguration, 1, 12);
            tableProp.Controls.Add(lblBinTarget, 0, 13);
            tableProp.Controls.Add(numBinTarget, 1, 13);
            tableProp.Controls.Add(txtBinTarget, 1, 13);
            tableProp.Controls.Add(checkBinTarget, 2, 13);

        }

        private void PropHDMTModelComparison()
        {
            XmlNodeList? hdModels = _project.GetObjects("HDModel");
            foreach (XmlNode node in hdModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboHDModel.Items.Add(item);
            }
            XmlNodeList? mtModels = _project.GetObjects("MTModel");
            foreach (XmlNode node in mtModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboMTModel.Items.Add(item);
            }
            XmlNodeList? adcps = _project.GetObjects("VesselMountedADCP");
            foreach (XmlNode node in adcps)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboADCP.Items.Add(item);
            }
            tableProp.Controls.Clear();

            tableProp.RowStyles.Clear();
            tableProp.RowCount = 22;
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));

            tableProp.Controls.Add(lblHDModel, 0, 0);
            tableProp.Controls.Add(comboHDModel, 1, 0);
            tableProp.Controls.Add(lblMTModel, 0, 1);
            tableProp.Controls.Add(comboMTModel, 1, 1);
            tableProp.Controls.Add(lblADCP, 0, 2);
            tableProp.Controls.Add(comboADCP, 1, 2);
            tableProp.Controls.Add(lblScale, 0, 3);
            tableProp.Controls.Add(comboScale, 1, 3);
            tableProp.Controls.Add(lblcmap, 0, 4);
            tableProp.Controls.Add(combocmap, 1, 4);
            tableProp.Controls.Add(lblvmin, 0, 5);
            tableProp.Controls.Add(txtvmin, 1, 5);
            tableProp.Controls.Add(lblvmax, 0, 6);
            tableProp.Controls.Add(txtvmax, 1, 6);
            tableProp.Controls.Add(lblCMapBottomThreshold, 0, 7);
            tableProp.Controls.Add(txtCMapBottomThreshold, 1, 7);
            tableProp.Controls.Add(lblPixelSizeM, 0, 8);
            tableProp.Controls.Add(txtPixelSizeM, 1, 8);
            tableProp.Controls.Add(lblPadM, 0, 9);
            tableProp.Controls.Add(txtPadM, 1, 9);
            tableProp.Controls.Add(lblColorBarTickDecimals, 0, 10);
            tableProp.Controls.Add(numColorBarTickDecimals, 1, 10);
            tableProp.Controls.Add(lblAxisTickDecimals, 0, 11);
            tableProp.Controls.Add(numAxisTickDecimals, 1, 11);
            tableProp.Controls.Add(lblModelQuiverMode, 0, 12);
            tableProp.Controls.Add(comboModelQuiverMode, 1, 12);
            tableProp.Controls.Add(lblFieldPixelSize, 0, 13);
            tableProp.Controls.Add(txtFieldPixelSize, 1, 13);
            tableProp.Controls.Add(lblFieldQuiverStrideN, 0, 14);
            tableProp.Controls.Add(numFieldQuiverStrideN, 1, 14);
            tableProp.Controls.Add(lblQuiverScale, 0, 15);
            tableProp.Controls.Add(txtQuiverScale, 1, 15);
            tableProp.Controls.Add(lblQuiverColor, 0, 16);
            tableProp.Controls.Add(pnlQuiverColor, 1, 16);
            tableProp.Controls.Add(btnQuiverColor, 2, 16);
            tableProp.Controls.Add(lblQuiverEveryN, 0, 17);
            tableProp.Controls.Add(numericQuiverEveryN, 1, 17);
            tableProp.Controls.Add(lblTransectLineWidth, 0, 18);
            tableProp.Controls.Add(txtTransectLineWidth, 1, 18);
            tableProp.Controls.Add(lblBinConfiguration, 0, 19);
            tableProp.Controls.Add(comboBinConfiguration, 1, 19);
            tableProp.Controls.Add(lblBinTarget, 0, 20);
            tableProp.Controls.Add(numBinTarget, 1, 20);
            tableProp.Controls.Add(txtBinTarget, 1, 20);
            tableProp.Controls.Add(checkBinTarget, 2, 20);

        }

        private void PropHDMTModelAnimation()
        {
            XmlNodeList? hdModels = _project.GetObjects("HDModel");
            foreach (XmlNode node in hdModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboHDModel.Items.Add(item);
            }
            XmlNodeList? mtModels = _project.GetObjects("MTModel");
            foreach (XmlNode node in mtModels)
            {
                XmlElement element = (XmlElement)node;
                string name = element.GetAttribute("name");
                string id = element.GetAttribute("id");
                ComboBoxItem? item = new ComboBoxItem(name, id);
                comboMTModel.Items.Add(item);
            }
            tableProp.Controls.Clear();

            tableProp.RowStyles.Clear();
            tableProp.RowCount = 19;
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableProp.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));

            tableProp.Controls.Add(lblHDModel, 0, 0);
            tableProp.Controls.Add(comboHDModel, 1, 0);
            tableProp.Controls.Add(lblMTModel, 0, 1);
            tableProp.Controls.Add(comboMTModel, 1, 1);
            tableProp.Controls.Add(lblScale, 0, 2);
            tableProp.Controls.Add(comboScale, 1, 2);
            tableProp.Controls.Add(lblcmap, 0, 3);
            tableProp.Controls.Add(combocmap, 1, 3);
            tableProp.Controls.Add(lblvmin, 0, 4);
            tableProp.Controls.Add(txtvmin, 1, 4);
            tableProp.Controls.Add(lblvmax, 0, 5);
            tableProp.Controls.Add(txtvmax, 1, 5);
            tableProp.Controls.Add(lblCMapBottomThreshold, 0, 6);
            tableProp.Controls.Add(txtCMapBottomThreshold, 1, 6);
            tableProp.Controls.Add(lblPixelSizeM, 0, 7);
            tableProp.Controls.Add(txtPixelSizeM, 1, 7);
            tableProp.Controls.Add(lblAxisTickDecimals, 0, 8);
            tableProp.Controls.Add(numAxisTickDecimals, 1, 8);
            tableProp.Controls.Add(lblFieldPixelSize, 0, 9);
            tableProp.Controls.Add(txtFieldPixelSize, 1, 9);
            tableProp.Controls.Add(lblFieldQuiverStrideN, 0, 10);
            tableProp.Controls.Add(numFieldQuiverStrideN, 1, 10);
            tableProp.Controls.Add(lblQuiverScale, 0, 11);
            tableProp.Controls.Add(txtQuiverScale, 1, 11);
            tableProp.Controls.Add(lblQuiverColor, 0, 12);
            tableProp.Controls.Add(pnlQuiverColor, 1, 12);
            tableProp.Controls.Add(btnQuiverColor, 2, 12);
            tableProp.Controls.Add(lblAnimationStartIndex, 0, 13);
            tableProp.Controls.Add(numericAnimationStartIndex, 1, 13);
            tableProp.Controls.Add(checkAnimationStartIndex, 2, 13);
            tableProp.Controls.Add(lblAnimationEndIndex, 0, 14);
            tableProp.Controls.Add(numericAnimationEndIndex, 1, 14);
            tableProp.Controls.Add(checkAnimationEndIndex, 2, 14);
            tableProp.Controls.Add(lblAnimationTimeStep, 0, 15);
            tableProp.Controls.Add(numericAnimationTimeStep, 1, 15);
            tableProp.Controls.Add(lblAnimationInterval, 0, 16);
            tableProp.Controls.Add(numericAnimationInterval, 1, 16);
            tableProp.Controls.Add(lblAnimationOutputFile, 0, 17);
            tableProp.Controls.Add(txtAnimationOutputFile, 1, 17);
            tableProp.Controls.Add(btnAnimationOutputFile, 2, 17);

        }


        private void InitializeWidgets()
        {
            //
            // lblHDModel
            //
            lblHDModel = new Label();
            lblHDModel.Dock = DockStyle.Fill;
            lblHDModel.Name = "lblHDModel";
            lblHDModel.TabIndex = 0;
            lblHDModel.Text = "HD Model";
            lblHDModel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboHDModel
            // 
            comboHDModel = new ComboBox();
            comboHDModel.Dock = DockStyle.Fill;
            comboHDModel.DropDownStyle = ComboBoxStyle.DropDownList;
            comboHDModel.FormattingEnabled = true;
            comboHDModel.Name = "comboHDModel";
            comboHDModel.TabIndex = 14;
            comboHDModel.DisplayMember = "name";
            comboHDModel.ValueMember = "id";
            //
            // lblMTModel
            //
            lblMTModel = new Label();
            lblMTModel.Dock = DockStyle.Fill;
            lblMTModel.Name = "lblMTModel";
            lblMTModel.TabIndex = 0;
            lblMTModel.Text = "MT Model";
            lblMTModel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboMTModel
            // 
            comboMTModel = new ComboBox();
            comboMTModel.Dock = DockStyle.Fill;
            comboMTModel.DropDownStyle = ComboBoxStyle.DropDownList;
            comboMTModel.FormattingEnabled = true;
            comboMTModel.Name = "comboMTModel";
            comboMTModel.TabIndex = 14;
            comboMTModel.DisplayMember = "name";
            comboMTModel.ValueMember = "id";
            //
            // lblADCP
            //
            lblADCP = new Label();
            lblADCP.Dock = DockStyle.Fill;
            lblADCP.Name = "lblADCP";
            lblADCP.TabIndex = 0;
            lblADCP.Text = "ADCP";
            lblADCP.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboADCP
            // 
            comboADCP = new ComboBox();
            comboADCP.Dock = DockStyle.Fill;
            comboADCP.DropDownStyle = ComboBoxStyle.DropDownList;
            comboADCP.FormattingEnabled = true;
            comboADCP.Name = "comboADCP";
            comboADCP.TabIndex = 14;
            comboADCP.DisplayMember = "name";
            comboADCP.ValueMember = "id";
            //   
            // lblModelQuiverMode
            //
            lblModelQuiverMode = new Label();
            lblModelQuiverMode.Dock = DockStyle.Fill;
            lblModelQuiverMode.Name = "lblModelQuiverMode ";
            lblModelQuiverMode.TabIndex = 0;
            lblModelQuiverMode.Text = "Model Quiver Mode";
            lblModelQuiverMode.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboFieldName
            // 
            comboModelQuiverMode = new ComboBox();
            comboModelQuiverMode.Dock = DockStyle.Fill;
            comboModelQuiverMode.DropDownStyle = ComboBoxStyle.DropDownList;
            comboModelQuiverMode.FormattingEnabled = true;
            comboModelQuiverMode.Items.AddRange(new object[] { "Field", "Transect" });
            comboModelQuiverMode.Name = "comboModelQuiverMode";
            comboModelQuiverMode.TabIndex = 14;
            comboModelQuiverMode.SelectedIndex = 0;
            // 
            // lblFieldPixelSize
            // 
            lblFieldPixelSize = new Label();
            lblFieldPixelSize.Dock = DockStyle.Fill;
            lblFieldPixelSize.Name = "lblFieldPixelSize";
            lblFieldPixelSize.TabIndex = 0;
            lblFieldPixelSize.Text = "Field Pixel Size";
            lblFieldPixelSize.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtFieldPixelSize
            // 
            txtFieldPixelSize = new TextBox();
            txtFieldPixelSize.Dock = DockStyle.Fill;
            txtFieldPixelSize.Name = "txtFieldPixelSize";
            txtFieldPixelSize.TabIndex = 1;
            txtFieldPixelSize.Text = "100";
            //
            // lblFieldQuiverStrideN
            //
            lblFieldQuiverStrideN = new Label();
            lblFieldQuiverStrideN.Dock = DockStyle.Fill;
            lblFieldQuiverStrideN.Name = "lblFieldQuiverStrideN";
            lblFieldQuiverStrideN.TabIndex = 6;
            lblFieldQuiverStrideN.Text = "Number of Field Quiver Stride";
            lblFieldQuiverStrideN.TextAlign = ContentAlignment.MiddleLeft;
            //
            // numFieldQuiverStrideN
            //
            numFieldQuiverStrideN = new NumericUpDown();
            numFieldQuiverStrideN.Dock = DockStyle.Fill;
            numFieldQuiverStrideN.Minimum = 1;
            numFieldQuiverStrideN.Maximum = 10;
            numFieldQuiverStrideN.Value = 3;
            numFieldQuiverStrideN.Name = "numFieldQuiverStrideN";
            numFieldQuiverStrideN.TabIndex = 13;
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
            // lblScale
            //
            lblScale = new Label();
            lblScale.Dock = DockStyle.Fill;
            lblScale.Name = "lblScale ";
            lblScale.TabIndex = 0;
            lblScale.Text = "Scale";
            lblScale.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboScale
            // 
            comboScale = new ComboBox();
            comboScale.Dock = DockStyle.Fill;
            comboScale.DropDownStyle = ComboBoxStyle.DropDownList;
            comboScale.FormattingEnabled = true;
            comboScale.Items.AddRange(new object[] { "Log", "Normal" });
            comboScale.Name = "comboScale";
            comboScale.TabIndex = 14;
            comboScale.SelectedIndex = 0;
            // 
            // lblvmin
            // 
            lblvmin = new Label();
            lblvmin.Dock = DockStyle.Fill;
            lblvmin.Name = "lblvmin";
            lblvmin.TabIndex = 0;
            lblvmin.Text = "Minimum Value";
            lblvmin.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtvmin
            // 
            txtvmin = new TextBox();
            txtvmin.Dock = DockStyle.Fill;
            txtvmin.Name = "txtvmin";
            txtvmin.TabIndex = 1;
            // 
            // lblvmax
            // 
            lblvmax = new Label();
            lblvmax.Dock = DockStyle.Fill;
            lblvmax.Name = "lblvmax";
            lblvmax.TabIndex = 0;
            lblvmax.Text = "Maximum Value";
            lblvmax.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtvmax
            // 
            txtvmax = new TextBox();
            txtvmax.Dock = DockStyle.Fill;
            txtvmax.Name = "txtvmax";
            txtvmax.TabIndex = 1;
            //
            // lblColorBarTickDecimals
            //
            lblColorBarTickDecimals = new Label();
            lblColorBarTickDecimals.Dock = DockStyle.Fill;
            lblColorBarTickDecimals.Name = "lblColorBarTickDecimals";
            lblColorBarTickDecimals.TabIndex = 6;
            lblColorBarTickDecimals.Text = "Colorbar Ticks Decimal";
            lblColorBarTickDecimals.TextAlign = ContentAlignment.MiddleLeft;
            //
            // numColorBarTickDecimals
            //
            numColorBarTickDecimals = new NumericUpDown();
            numColorBarTickDecimals.Dock = DockStyle.Fill;
            numColorBarTickDecimals.Minimum = 1;
            numColorBarTickDecimals.Maximum = 5;
            numColorBarTickDecimals.Value = 2;
            numColorBarTickDecimals.Name = "numColorBarTickDecimals";
            numColorBarTickDecimals.TabIndex = 13;

            //
            // lblAxisTickDecimals
            //
            lblAxisTickDecimals = new Label();
            lblAxisTickDecimals.Dock = DockStyle.Fill;
            lblAxisTickDecimals.Name = "lblAxisTickDecimals";
            lblAxisTickDecimals.TabIndex = 6;
            lblAxisTickDecimals.Text = "Axis Ticks Decimal";
            lblAxisTickDecimals.TextAlign = ContentAlignment.MiddleLeft;
            //
            // numAxisTickDecimals
            //
            numAxisTickDecimals = new NumericUpDown();
            numAxisTickDecimals.Dock = DockStyle.Fill;
            numAxisTickDecimals.Minimum = 1;
            numAxisTickDecimals.Maximum = 5;
            numAxisTickDecimals.Value = 3;
            numAxisTickDecimals.Name = "numAxisTickDecimals";
            numAxisTickDecimals.TabIndex = 13;
            // 
            // lblPadM
            // 
            lblPadM = new Label();
            lblPadM.Dock = DockStyle.Fill;
            lblPadM.Name = "lblPadM";
            lblPadM.TabIndex = 0;
            lblPadM.Text = "Pad";
            lblPadM.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtPadM
            // 
            txtPadM = new TextBox();
            txtPadM.Dock = DockStyle.Fill;
            txtPadM.Name = "txtPadM";
            txtPadM.TabIndex = 1;
            txtPadM.Text = "2000";
            // 
            // lblPixelSizeM
            // 
            lblPixelSizeM = new Label();
            lblPixelSizeM.Dock = DockStyle.Fill;
            lblPixelSizeM.Name = "lblPixelSizeM";
            lblPixelSizeM.TabIndex = 0;
            lblPixelSizeM.Text = "Pixels Size";
            lblPixelSizeM.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtPixelSizeM
            // 
            txtPixelSizeM = new TextBox();
            txtPixelSizeM.Dock = DockStyle.Fill;
            txtPixelSizeM.Name = "txtPixelSizeM";
            txtPixelSizeM.TabIndex = 1;
            txtPixelSizeM.Text = "10";
            // 
            // lblCMapBottomThreshold
            // 
            lblCMapBottomThreshold = new Label();
            lblCMapBottomThreshold.Dock = DockStyle.Fill;
            lblCMapBottomThreshold.Name = "lblCMapBottomThreshold";
            lblCMapBottomThreshold.TabIndex = 0;
            lblCMapBottomThreshold.Text = "Colormap Bottom Threshold";
            lblCMapBottomThreshold.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtCMapBottomThreshold
            // 
            txtCMapBottomThreshold = new TextBox();
            txtCMapBottomThreshold.Dock = DockStyle.Fill;
            txtCMapBottomThreshold.Name = "txtCMapBottomThreshold";
            txtCMapBottomThreshold.TabIndex = 1;
            txtCMapBottomThreshold.Text = "0.01";
            // 
            // lblTransectColor
            // 
            lblTransectColor = new Label();
            lblTransectColor.Dock = DockStyle.Fill;
            lblTransectColor.Name = "lblTransectColor";
            lblTransectColor.TabIndex = 0;
            lblTransectColor.Text = "Transect Color";
            lblTransectColor.TextAlign = ContentAlignment.MiddleLeft;
            //
            // pnlTransectCOlor
            //
            pnlTransectCOlor = new Panel();
            pnlTransectCOlor.Dock = DockStyle.Fill;
            pnlTransectCOlor.Name = "pnlTransectCOlor";
            pnlTransectCOlor.BackColor = Color.Red;
            pnlTransectCOlor.TabIndex = 0;
            //
            // btnTransectColor
            //
            btnTransectColor = new Button();
            btnTransectColor.Dock = DockStyle.Left;
            btnTransectColor.Name = "btnTransectColor";
            btnTransectColor.TabIndex = 1;
            btnTransectColor.Text = "...";
            btnTransectColor.UseVisualStyleBackColor = true;
            btnTransectColor.Click += btnChangeColor_Click;
            //   
            // lblBinConfiguration
            //
            lblBinConfiguration = new Label();
            lblBinConfiguration.Dock = DockStyle.Fill;
            lblBinConfiguration.Name = "lblBinConfiguration";
            lblBinConfiguration.TabIndex = 0;
            lblBinConfiguration.Text = "Bin Configuration";
            lblBinConfiguration.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // comboBinConfiguration
            // 
            comboBinConfiguration = new ComboBox();
            comboBinConfiguration.Dock = DockStyle.Fill;
            comboBinConfiguration.DropDownStyle = ComboBoxStyle.DropDownList;
            comboBinConfiguration.FormattingEnabled = true;
            comboBinConfiguration.Items.AddRange(new object[] { "Bin", "Depth", "HAB" });
            comboBinConfiguration.Name = "comboBinConfiguration";
            comboBinConfiguration.TabIndex = 14;
            comboBinConfiguration.SelectedIndex = 0;
            comboBinConfiguration.SelectedIndexChanged += comboBinConfiguration_SelectedIndexChanged;
            //   
            // lblBinTarget
            //
            lblBinTarget = new Label();
            lblBinTarget.Dock = DockStyle.Fill;
            lblBinTarget.Name = "lblBinTarget";
            lblBinTarget.TabIndex = 0;
            lblBinTarget.Text = "Bin Target";
            lblBinTarget.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtBinTarget
            // 
            txtBinTarget = new TextBox();
            txtBinTarget.Dock = DockStyle.Fill;
            txtBinTarget.Name = "txtBinTarget";
            txtBinTarget.TabIndex = 1;
            txtBinTarget.Visible = false;
            //
            // numBinTarget
            //
            numBinTarget = new NumericUpDown();
            numBinTarget.Dock = DockStyle.Fill;
            numBinTarget.Minimum = 1;
            numBinTarget.Maximum = 100;
            numBinTarget.Value = 1;
            numBinTarget.Name = "numBinTarget";
            numBinTarget.TabIndex = 13;
            numBinTarget.Visible = true;
            //
            // checkBinTarget
            //
            checkBinTarget = new CheckBox();
            checkBinTarget.Dock = DockStyle.Fill;
            checkBinTarget.Name = "checkBinTarget";
            checkBinTarget.TabIndex = 15;
            checkBinTarget.Text = "Use Mean";
            checkBinTarget.TextAlign = ContentAlignment.MiddleLeft;
            checkBinTarget.Checked = false;
            checkBinTarget.CheckedChanged += checkBinTarget_CheckedChanged;
            //
            // lblQuiverEveryN
            //
            lblQuiverEveryN = new Label();
            lblQuiverEveryN.Dock = DockStyle.Fill;
            lblQuiverEveryN.Name = "lblQuiverEveryN";
            lblQuiverEveryN.TabIndex = 0;
            lblQuiverEveryN.Text = "Quiver Every N";
            lblQuiverEveryN.TextAlign = ContentAlignment.MiddleLeft;
            //
            // numericQuiverEveryN
            //
            numericQuiverEveryN = new NumericUpDown();
            numericQuiverEveryN.Dock = DockStyle.Fill;
            numericQuiverEveryN.Minimum = 1;
            numericQuiverEveryN.Maximum = 30;
            numericQuiverEveryN.Value = 20;
            numericQuiverEveryN.Name = "numericQuiverEveryN";
            numericQuiverEveryN.TabIndex = 13;
            //
            // lblQuiverScale
            //
            lblQuiverScale = new Label();
            lblQuiverScale.Dock = DockStyle.Fill;
            lblQuiverScale.Name = "lblQuiverScale";
            lblQuiverScale.TabIndex = 0;
            lblQuiverScale.Text = "Quiver Scale";
            lblQuiverScale.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtQuiverScale
            //
            txtQuiverScale = new TextBox();
            txtQuiverScale.Dock = DockStyle.Fill;
            txtQuiverScale.Name = "txtQuiverScale";
            txtQuiverScale.TabIndex = 1;
            txtQuiverScale.Text = "3";
            //
            // lblQuiverColor
            //
            lblQuiverColor = new Label();
            lblQuiverColor.Dock = DockStyle.Fill;
            lblQuiverColor.Name = "lblQuiverColor";
            lblQuiverColor.TabIndex = 0;
            lblQuiverColor.Text = "Model Quiver Color";
            lblQuiverColor.TextAlign = ContentAlignment.MiddleLeft;
            //
            // pnlQuiverColor
            //
            pnlQuiverColor = new Panel();
            pnlQuiverColor.Dock = DockStyle.Fill;
            pnlQuiverColor.Name = "pnlQuiverColor";
            pnlQuiverColor.BackColor = Color.Black;
            pnlQuiverColor.TabIndex = 0;
            //
            // btnQuiverColor
            //
            btnQuiverColor = new Button();
            btnQuiverColor.Dock = DockStyle.Left;
            btnQuiverColor.Name = "btnQuiverColor";
            btnQuiverColor.TabIndex = 1;
            btnQuiverColor.Text = "...";
            btnQuiverColor.UseVisualStyleBackColor = true;
            btnQuiverColor.Click += btnChangeColor_Click;
            //
            // lblTransectLineWidth
            //
            lblTransectLineWidth = new Label();
            lblTransectLineWidth.Dock = DockStyle.Fill;
            lblTransectLineWidth.Name = "lblTransectLineWidth";
            lblTransectLineWidth.TabIndex = 0;
            lblTransectLineWidth.Text = "ADCP Transect Line Width";
            lblTransectLineWidth.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtTransectLineWidth
            //
            txtTransectLineWidth = new TextBox();
            txtTransectLineWidth.Dock = DockStyle.Fill;
            txtTransectLineWidth.Name = "txtTransectLineWidth";
            txtTransectLineWidth.TabIndex = 1;
            txtTransectLineWidth.Text = "1.8";
            //
            // lblAnimationStartIndex
            //
            lblAnimationStartIndex = new Label();
            lblAnimationStartIndex.Dock = DockStyle.Fill;
            lblAnimationStartIndex.Name = "lblAnimationStartIndex";
            lblAnimationStartIndex.TabIndex = 0;
            lblAnimationStartIndex.Text = "Animation Start Time Index";
            lblAnimationStartIndex.TextAlign = ContentAlignment.MiddleLeft;
            //
            // numAnimationStartIndex
            //
            numericAnimationStartIndex = new NumericUpDown();
            numericAnimationStartIndex.Dock = DockStyle.Fill;
            numericAnimationStartIndex.Minimum = 0;
            numericAnimationStartIndex.Maximum = 9999;
            numericAnimationStartIndex.Value = 0;
            numericAnimationStartIndex.Name = "numericAnimationStartIndex";
            numericAnimationStartIndex.TabIndex = 13;
            numericAnimationStartIndex.Enabled = false;
            //
            // checkAnimationStartIndex
            //
            checkAnimationStartIndex = new CheckBox();
            checkAnimationStartIndex.Dock = DockStyle.Fill;
            checkAnimationStartIndex.Name = "checkAnimationStartIndex";
            checkAnimationStartIndex.TabIndex = 15;
            checkAnimationStartIndex.Text = "Use Model Start Time";
            checkAnimationStartIndex.TextAlign = ContentAlignment.MiddleLeft;
            checkAnimationStartIndex.Checked = true;
            checkAnimationStartIndex.CheckedChanged += checkAnimationStartIndex_CheckedChanged;
            //
            // lblAnimationEndIndex
            //
            lblAnimationEndIndex = new Label();
            lblAnimationEndIndex.Dock = DockStyle.Fill;
            lblAnimationEndIndex.Name = "lblAnimationEndIndex";
            lblAnimationEndIndex.TabIndex = 0;
            lblAnimationEndIndex.Text = "Animation End Time Index";
            lblAnimationEndIndex.TextAlign = ContentAlignment.MiddleLeft;
            //
            // numAnimationEndIndex
            //
            numericAnimationEndIndex = new NumericUpDown();
            numericAnimationEndIndex.Dock = DockStyle.Fill;
            numericAnimationEndIndex.Minimum = 1;
            numericAnimationEndIndex.Maximum = 9999;
            numericAnimationEndIndex.Value = 1;
            numericAnimationEndIndex.Name = "numericAnimationEndIndex";
            numericAnimationEndIndex.TabIndex = 13;
            numericAnimationEndIndex.Enabled = false;
            //
            // checkAnimationEndIndex
            //
            checkAnimationEndIndex = new CheckBox();
            checkAnimationEndIndex.Dock = DockStyle.Fill;
            checkAnimationEndIndex.Name = "checkAnimationEndIndex";
            checkAnimationEndIndex.TabIndex = 15;
            checkAnimationEndIndex.Text = "Use Model End Time";
            checkAnimationEndIndex.TextAlign = ContentAlignment.MiddleLeft;
            checkAnimationEndIndex.Checked = true;
            checkAnimationEndIndex.CheckedChanged += checkAnimationEndIndex_CheckedChanged;
            //
            // lblAnimationTimeStep
            //
            lblAnimationTimeStep = new Label();
            lblAnimationTimeStep.Dock = DockStyle.Fill;
            lblAnimationTimeStep.Name = "lblAnimationTimeStep";
            lblAnimationTimeStep.TabIndex = 0;
            lblAnimationTimeStep.Text = "Animation Time Step (in model time steps)";
            lblAnimationTimeStep.TextAlign = ContentAlignment.MiddleLeft;
            //
            // numAnimationTimeStep
            //
            numericAnimationTimeStep = new NumericUpDown();
            numericAnimationTimeStep.Dock = DockStyle.Fill;
            numericAnimationTimeStep.Minimum = 1;
            numericAnimationTimeStep.Maximum = 100;
            numericAnimationTimeStep.Value = 1;
            numericAnimationTimeStep.Name = "numericAnimationTimeStep";
            numericAnimationTimeStep.TabIndex = 13;
            //
            // lblAnimationInterval
            //
            lblAnimationInterval = new Label();
            lblAnimationInterval.Dock = DockStyle.Fill;
            lblAnimationInterval.Name = "lblAnimationInterval";
            lblAnimationInterval.TabIndex = 0;
            lblAnimationInterval.Text = "Animation Interval (ms)";
            lblAnimationInterval.TextAlign = ContentAlignment.MiddleLeft;
            //
            // numAnimationInterval
            //
            numericAnimationInterval = new NumericUpDown();
            numericAnimationInterval.Dock = DockStyle.Fill;
            numericAnimationInterval.Minimum = 0.1M;
            numericAnimationInterval.Maximum = 10000;
            numericAnimationInterval.Value = 0.1M;
            numericAnimationInterval.Increment = 0.1M;
            numericAnimationInterval.DecimalPlaces = 1;
            numericAnimationInterval.Name = "numericAnimationInterval";
            numericAnimationInterval.TabIndex = 13;
            //
            // lblAnimationOutputFile
            //
            lblAnimationOutputFile = new Label();
            lblAnimationOutputFile.Dock = DockStyle.Fill;
            lblAnimationOutputFile.Name = "lblAnimationOutputFile";
            lblAnimationOutputFile.TabIndex = 0;
            lblAnimationOutputFile.Text = "Animation Output File";
            lblAnimationOutputFile.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtAnimationOutputFile
            //
            txtAnimationOutputFile = new TextBox();
            txtAnimationOutputFile.Dock = DockStyle.Fill;
            txtAnimationOutputFile.Name = "txtAnimationOutputFile";
            txtAnimationOutputFile.TabIndex = 1;
            txtAnimationOutputFile.Text = "";
            //
            // btnAnimationOutputFile
            //
            btnAnimationOutputFile = new Button();
            btnAnimationOutputFile.Dock = DockStyle.Left;
            btnAnimationOutputFile.Name = "btnAnimationOutputFile";
            btnAnimationOutputFile.TabIndex = 1;
            btnAnimationOutputFile.Text = "...";
            btnAnimationOutputFile.UseVisualStyleBackColor = true;
            btnAnimationOutputFile.Click += btnAnimationOutputFile_Click;
            // 
            // lblQuiverWidth
            // 
            lblQuiverWidth = new Label();
            lblQuiverWidth.Dock = DockStyle.Fill;
            lblQuiverWidth.Name = "lblQuiverWidth";
            lblQuiverWidth.TabIndex = 0;
            lblQuiverWidth.Text = "Quiver Width";
            lblQuiverWidth.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtQuiverWidth
            // 
            txtQuiverWidth = new TextBox();
            txtQuiverWidth.Dock = DockStyle.Fill;
            txtQuiverWidth.Name = "txtQuiverWidth";
            txtQuiverWidth.TabIndex = 1;
            txtQuiverWidth.Text = "0.001";
            //
            // lblQuiverHeadWidth
            //
            lblQuiverHeadWidth = new Label();
            lblQuiverHeadWidth.Dock = DockStyle.Fill;
            lblQuiverHeadWidth.Name = "lblQuiverHeadWidth";
            lblQuiverHeadWidth.TabIndex = 0;
            lblQuiverHeadWidth.Text = "Quiver Head Width";
            lblQuiverHeadWidth.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtQuiverHeadWidth
            //
            txtQuiverHeadWidth = new TextBox();
            txtQuiverHeadWidth.Dock = DockStyle.Fill;
            txtQuiverHeadWidth.Name = "txtQuiverHeadWidth";
            txtQuiverHeadWidth.TabIndex = 1;
            txtQuiverHeadWidth.Text = "2.0";
            //
            // lblQuiverHeadLength
            //
            lblQuiverHeadLength = new Label();
            lblQuiverHeadLength.Dock = DockStyle.Fill;
            lblQuiverHeadLength.Name = "lblQuiverHeadLength";
            lblQuiverHeadLength.TabIndex = 0;
            lblQuiverHeadLength.Text = "Quiver Head Length";
            lblQuiverHeadLength.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtQuiverHeadLength
            //
            txtQuiverHeadLength = new TextBox();
            txtQuiverHeadLength.Dock = DockStyle.Fill;
            txtQuiverHeadLength.Name = "txtQuiverHeadLength";
            txtQuiverHeadLength.TabIndex = 1;
            txtQuiverHeadLength.Text = "2.5";
            //
            // lblsscLevels
            //
            lblsscLevels = new Label();
            lblsscLevels.Dock = DockStyle.Fill;
            lblsscLevels.Name = "lblsscLevels";
            lblsscLevels.TabIndex = 0;
            lblsscLevels.Text = "SSC Levels (comma separated)";
            lblsscLevels.TextAlign = ContentAlignment.MiddleLeft;
            //
            // txtsscLevels
            //
            txtsscLevels = new TextBox();
            txtsscLevels.Dock = DockStyle.Fill;
            txtsscLevels.Name = "txtsscLevels";
            txtsscLevels.TabIndex = 1;
            txtsscLevels.Text = "0.001,0.01,0.1,1,10";

        }

        public ProjectPlot()
        {
            InitializeComponent();
            InitializeWidgets();
        }

        private void btnPlot_Click(object sender, EventArgs e)
        {
            Dictionary<string, string> inputs = null;
            if (comboPlotType.SelectedItem.ToString() == "HD Comparison")
            {
                var selectedHDModel = comboHDModel.SelectedItem as ComboBoxItem;
                var selectedADCP = comboADCP.SelectedItem as ComboBoxItem;
                inputs = new Dictionary<string, string>
                {
                    { "Task", "HDComparison" },
                    { "Project", _Globals.Config.OuterXml.ToString() },
                    { "ModelID", selectedHDModel.ID},
                    { "ADCPID", selectedADCP.ID},
                    { "ModelQuiverMode", comboModelQuiverMode.SelectedItem.ToString()},
                    { "FieldPixelSize", txtFieldPixelSize.Text},
                    { "FieldQuiverStrideN", numFieldQuiverStrideN.Value.ToString()},
                    { "Colormap", combocmap.SelectedItem.ToString()},

                };
            }
            else if (comboPlotType.SelectedItem.ToString() == "MT Comparison")
            {
                var selectedMTModel = comboMTModel.SelectedItem as ComboBoxItem;
                var selectedADCP = comboADCP.SelectedItem as ComboBoxItem;
                string binTarget;
                if (comboBinConfiguration.SelectedIndex == 0)
                    binTarget = numBinTarget.Value.ToString();
                else
                    binTarget = txtBinTarget.Text;
                inputs = new Dictionary<string, string>
                {
                    { "Task", "MTComparison" },
                    { "Project", _Globals.Config.OuterXml.ToString() },
                    { "ModelID", selectedMTModel.ID },
                    { "ADCPID", selectedADCP.ID },
                    { "Scale", comboScale.SelectedItem.ToString() },
                    { "vmin", txtvmin.Text },
                    { "vmax", txtvmax.Text },
                    { "Colormap", combocmap.SelectedItem.ToString() },
                    { "ColorBarTickDecimals", numColorBarTickDecimals.Value.ToString() },
                    { "AxisTickDecimals", numAxisTickDecimals.Value.ToString() },
                    { "PadM", txtPadM.Text },
                    { "PixelSizeM", txtPixelSizeM.Text },
                    { "CMapBottomThreshold", txtCMapBottomThreshold.Text },
                    { "TransectColor", ColorTranslator.ToHtml(pnlTransectCOlor.BackColor) },
                    { "BinConfiguration", comboBinConfiguration.SelectedItem.ToString() },
                    { "BinTarget", binTarget },
                    { "UseMean", checkBinTarget.Checked ? "Yes" : "No" }
                };
            }
            else if (comboPlotType.SelectedItem.ToString() == "MT and HD Comparison")
            {
                var selectedMTModel = comboMTModel.SelectedItem as ComboBoxItem;
                var selectedHDModel = comboHDModel.SelectedItem as ComboBoxItem;
                var selectedADCP = comboADCP.SelectedItem as ComboBoxItem;
                string binTarget;
                if (comboBinConfiguration.SelectedIndex == 0)
                    binTarget = numBinTarget.Value.ToString();
                else
                    binTarget = txtBinTarget.Text;
                inputs = new Dictionary<string, string>
                {
                    { "Task", "HDMTComparison" },
                    { "Project", _Globals.Config.OuterXml.ToString() },
                    { "MTModelID", selectedMTModel.ID },
                    { "HDModelID", selectedHDModel.ID },
                    { "ADCPID", selectedADCP.ID },
                    { "Scale", comboScale.SelectedItem.ToString() },
                    { "vmin", txtvmin.Text },
                    { "vmax", txtvmax.Text },
                    { "Colormap", combocmap.SelectedItem.ToString() },
                    { "CMapBottomThreshold", txtCMapBottomThreshold.Text },
                    { "PixelSizeM", txtPixelSizeM.Text },
                    { "PadM", txtPadM.Text },
                    { "ColorBarTickDecimals", numColorBarTickDecimals.Value.ToString() },
                    { "AxisTickDecimals", numAxisTickDecimals.Value.ToString() },
                    { "ModelQuiverMode", comboModelQuiverMode.SelectedItem.ToString()},
                    { "QuiverEveryN", numericQuiverEveryN.Value.ToString() },
                    { "QuiverScale", txtQuiverScale.Text},
                    { "QuiverColorModel", ColorTranslator.ToHtml(pnlQuiverColor.BackColor) },
                    { "TransectLineWidth", txtTransectLineWidth.Text },
                    { "FieldPixelSize", txtFieldPixelSize.Text},
                    { "FieldQuiverStrideN", numFieldQuiverStrideN.Value.ToString()},
                    { "BinConfiguration", comboBinConfiguration.SelectedItem.ToString() },
                    { "BinTarget", binTarget },
                    { "UseMean", checkBinTarget.Checked ? "Yes" : "No" },

                };
            }
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
            else
            {
                return;
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

        private void checkBinTarget_CheckedChanged(object? sender, EventArgs e)
        {
            if (checkBinTarget.Checked)
            {
                numBinTarget.Enabled = false;
                txtBinTarget.Enabled = false;
            }
            else
            {
                numBinTarget.Enabled = true;
                txtBinTarget.Enabled = true;
            }
        }

        private void comboBinConfiguration_SelectedIndexChanged(object? sender, EventArgs e)
        {
            if (comboBinConfiguration.SelectedItem.ToString() == "Bin")
            {
                numBinTarget.Visible = true;
                txtBinTarget.Visible = false;
            }
            else
            {
                numBinTarget.Visible = false;
                txtBinTarget.Visible = true;
            }
        }

        private void checkAnimationStartIndex_CheckedChanged(object? sender, EventArgs e)
        {
            if (checkAnimationStartIndex.Checked)
            {
                numericAnimationStartIndex.Enabled = false;
            }
            else
            {
                numericAnimationStartIndex.Enabled = true;
            }
        }

        private void checkAnimationEndIndex_CheckedChanged(object? sender, EventArgs e)
        {
            if (checkAnimationEndIndex.Checked)
            {
                numericAnimationEndIndex.Enabled = false;
            }
            else
            {
                numericAnimationEndIndex.Enabled = true;
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

        private void btnChangeColor_Click(object? sender, EventArgs e)
        {
            Button btn = sender as Button;
            Panel pnl = null;
            if (btn.Name == "btnTransectColor")
                pnl = pnlTransectCOlor;
            else if (btn.Name == "btnQuiverColor")
                pnl = pnlQuiverColor;
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
