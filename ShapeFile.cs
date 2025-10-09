using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSEMMPGUI_v1
{
    public class ShapeFile
    {
        public string Name { get; set; }
        public string Path { get; set; }
        public string Kind { get; set; }
        // Polygon specific properties
        public string PolyEdgeColor { get; set; }
        public string PolyLineWidth { get; set; }
        public string PolyFaceColor { get; set; }
        public string PolyAlpha { get; set; }
        // Line specific properties
        public string LineColor { get; set; }
        public string LineLineWidth { get; set; }
        public string LineAlpha { get; set; }
        // Point specific properties 
        public string PointColor { get; set; }
        public string PointMarker { get; set; }
        public string PointMarkerSize { get; set; }
        public string PointAlpha { get; set; }
        // Lable related properties
        public string LabelText { get; set; }
        public string LabelFontSize { get; set; }
        public string LabelColor { get; set; }
        public string LabelHA { get; set; }
        public string LabelVA { get; set; }
        public string LabelOffsetPointsX { get; set; }
        public string LabelOffsetPointsY { get; set; }
        public string LabelOffsetDataX { get; set; }
        public string LabelOffsetDataY { get; set; }
        public ShapeFile(string name, string path, string kind)
        {
            Name = name;
            Path = path;
            Kind = kind;
            
            PointColor = "#000000"; // default point color
            PointMarker = "o"; // default point marker
            PointMarkerSize = "12"; // default point marker size
            PointAlpha = "1.0"; // default point transparency
            
            LineColor = "#000000"; // default line color
            LineLineWidth = "1.0"; // default line width
            LineAlpha = "1.0"; // default line transparency
            
            PolyEdgeColor = "#000000"; // default polygon edge color
            PolyLineWidth = "0.8"; // default polygon line width
            PolyFaceColor = "#000000"; // default polygon face color
            PolyAlpha = "1.0"; // default polygon transparency
            
            LabelText = ""; // default label text
            LabelFontSize = "8"; // default label font size
            LabelColor = "#000000"; // default label color
            LabelHA = "Left"; // default label horizontal alignment
            LabelVA = "Center"; // default label vertical alignment
            LabelOffsetPointsX = "0"; // default label offset in points (X)
            LabelOffsetPointsY = "0"; // default label offset in points (Y)
            LabelOffsetDataX = "0"; // default label offset in data units (X)
            LabelOffsetDataY = "0"; // default label offset in data units (Y)
        }
        public override string ToString()
        {
            return Name; // fallback
        }
    }
}
