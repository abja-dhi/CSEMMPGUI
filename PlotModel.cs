using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.Windows.Forms;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public partial class PlotModel : Form
    {
        public PlotModel(XmlNode model)
        {
            InitializeComponent();
            comboColormaps.DrawMode = DrawMode.OwnerDrawFixed;
            string current = Directory.GetParent(AppContext.BaseDirectory)?.Parent?.Parent?.Parent?.FullName;
            string colormapsPath = Path.Combine(current, _Globals._ColorMapsPath);
            foreach (var file in Directory.GetFiles(colormapsPath, "*.png"))
            {
                string name = Path.GetFileNameWithoutExtension(file);
                Image img = Image.FromFile(file);
                comboColormaps.Items.Add(new ColormapItem(name, img));
            }
            comboColormaps.DrawItem += comboColormaps_DrawItem;
        }

        private void comboColormaps_DrawItem(object sender, DrawItemEventArgs e)
        {
            if (e.Index < 0) return; // No item to draw
            var item = (ColormapItem)comboColormaps.Items[e.Index];
            e.DrawBackground();
            e.Graphics.DrawImage(item.Preview, e.Bounds.Left + 2, e.Bounds.Top + 2, 100, 30);
            using var brush = new SolidBrush(e.ForeColor);
            e.Graphics.DrawString(item.Name, e.Font, brush, e.Bounds.Left + 110, e.Bounds.Top + 6);
            e.DrawFocusRectangle();
        }
    }
}
