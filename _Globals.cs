using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public static class _Globals
    {
        // Basic configuration settings
        public static string PythonDllPath = @"C:\Program Files\Python311\python311.dll";
        public static string PythonModulePath = @"C:\Users\abja\OneDrive - DHI\61803553-05 EMMP Support Group\github\CSEMMPGUI";
        public static string BackendModuleName = "backend.backend";

        // XML document for project configuration
        public static XmlDocument Config { get; private set; } = new XmlDocument();
    }
}
