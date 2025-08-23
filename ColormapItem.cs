using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSEMMPGUI_v1
{
    public class ColormapItem
    {
        public string Name { get; set; }
        public Image Preview { get; set; }

        public ColormapItem(string name, Image preview)
        {
            Name = name;
            Preview = preview;
        }

        public override string ToString()
        {
            return Name; // fallback
        }
    }

}
