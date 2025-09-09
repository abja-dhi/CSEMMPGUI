using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Xml;

namespace CSEMMPGUI_v1
{
    internal static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main(string[] args)
        {
            
            // To customize application configuration such as set high DPI settings or default font,
            // see https://aka.ms/applicationconfiguration.
            ApplicationConfiguration.Initialize();
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            using (var splash = new __SplashPage())
            {
                splash.Show();
                splash.Refresh();
                Dictionary<string, string> inputs = null;
                inputs = new Dictionary<string, string>
                    {
                        { "Task", "HelloBackend" },
                    };
                string xmlInput = _Tools.GenerateInput(inputs);
                XmlDocument result = _Tools.CallPython(xmlInput);
                Dictionary<string, string> outputs = _Tools.ParseOutput(result);
                splash.Close();
            }
            Application.Run(new __PlumeTrack(args));
        }
    }
}