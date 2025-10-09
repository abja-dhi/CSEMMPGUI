using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSEMMPGUI_v1
{
    public class ComboBoxItem
    {
        public string Text { get; set; }
        public string ID { get; set; }

        public ComboBoxItem(string text, string id)
        {
            Text = text;
            ID = id;
        }

        public override string ToString()
        {
            return Text; // what shows in the dropdown
        }
    }
}
