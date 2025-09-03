using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public static class _Globals
    {
        public static string basePath = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        // Basic configuration settings
        public static string PythonDllPath = @"C:\Program Files\Python311\python311.dll";
        public static string PythonModulePath = basePath;
        public static string BackendModuleName = "backend.backend";
        public static string CMapsPath = Path.Combine(basePath, "colormaps");

        // XML document for project configuration
        public static XmlDocument Config { get; private set; } = new XmlDocument();
        public static bool isSaved;
        // Global pathes
        public static string _ColorMapsPath = "colormaps";
    }
}
