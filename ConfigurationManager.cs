using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.NetworkInformation;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public static class ConfigurationManager
    {
        public static bool hasChanged = false;
        public static bool isSaved = false;
        public static int saveCount = 0;

        public static void InitializeProject(string name)
        {
            Globals.Config.RemoveAll();
            XmlDeclaration xmlDeclaration = Globals.Config.CreateXmlDeclaration("1.0", "UTF-8", null);
            Globals.Config.AppendChild(xmlDeclaration);
            XmlElement root = Globals.Config.CreateElement("Project");
            root.SetAttribute("type", "Project");
            Globals.Config.AppendChild(root);

            XmlElement settings = Globals.Config.CreateElement("Settings");
            XmlNode? nodeName = Globals.Config.CreateElement("Name");
            nodeName.InnerText = name;
            settings.AppendChild(nodeName);
            XmlNode? nodeDirectory = Globals.Config.CreateElement("Directory");
            nodeDirectory.InnerText = string.Empty;
            settings.AppendChild(nodeDirectory);
            XmlNode? nodeEPSG = Globals.Config.CreateElement("EPSG");
            nodeEPSG.InnerText = "4326"; // Default EPSG code
            settings.AppendChild(nodeEPSG);
            XmlNode? nodeDescription = Globals.Config.CreateElement("Description");
            nodeDescription.InnerText = "";
            settings.AppendChild(nodeDescription);

            root.AppendChild(settings);
        }

        public static string GetSetting(string settingName)
        {
            XmlNode? settingNode = Globals.Config.DocumentElement?.SelectSingleNode($"Settings/{settingName}");
            return settingNode?.InnerText ?? string.Empty;
        }

        public static void SetSetting(string settingName, string value)
        {
            XmlNode? settingNode = Globals.Config.DocumentElement?.SelectSingleNode($"Settings/{settingName}");
            if (settingNode == null)
            {
                settingNode = Globals.Config.CreateElement(settingName);
                Globals.Config.DocumentElement?.SelectSingleNode("Settings")?.AppendChild(settingNode);
            }
            settingNode.InnerText = value;
        }

        public static string? GetProjectPath()
        {
            string projectDir = GetSetting(settingName: "Directory");
            if (String.IsNullOrEmpty(projectDir))
            {
                FolderBrowserDialog fbd = new FolderBrowserDialog
                {
                    Description = "Select the project directory",
                    ShowNewFolderButton = true,
                    InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
                };
                if (fbd.ShowDialog() == DialogResult.OK)
                {
                    SetSetting(settingName: "Directory", value: fbd.SelectedPath);
                    return fbd.SelectedPath;
                }
                else
                {
                    MessageBox.Show(text: "Project directory is not set. Please set the project directory first.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                    return null; // User cancelled the dialog
                }
            }
            string projectName = GetSetting(settingName: "Name");
            if (String.IsNullOrEmpty(projectName))
            {
                MessageBox.Show(text: "Project name is not set. Please set the project name first.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return null; // Project name is not set
            }
            return System.IO.Path.Combine(projectDir, $"{projectName}.mtproj");
        }

        public static void SaveConfig()
        {
            if (Globals.Config.DocumentElement == null)
            {
                InitializeProject(name: "Project");
            }
            string? path = GetProjectPath();
            if (String.IsNullOrEmpty(path))
            {
                MessageBox.Show(text: "Project path is not set. Please set the project directory first.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return;
            }
            if (File.Exists(path) && saveCount == 0)
            {
                DialogResult result = MessageBox.Show(
                    text: "The project file already exists. Do you want to overwrite it?",
                    caption: "Confirm Overwrite",
                    buttons: MessageBoxButtons.YesNo,
                    icon: MessageBoxIcon.Warning
                );
                if (result == DialogResult.No)
                {
                    return; // User chose not to overwrite
                }
                else
                {
                    Globals.Config.Save(path);
                    isSaved = true;
                    hasChanged = false;
                    saveCount++;
                }
            }
            else
            {
                Globals.Config.Save(path);
            }
        }

        public static void LoadConfig(string filePath)
        {
            if (string.IsNullOrEmpty(filePath) || !System.IO.File.Exists(filePath))
            {
                MessageBox.Show(text: "The specified project file does not exist.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return;
            }
            try
            {
                Globals.Config.Load(filePath);
                isSaved = true;
                hasChanged = false;
                saveCount = 0;
            }
            catch (Exception ex)
            {
                MessageBox.Show(text: $"Failed to load project file: {ex.Message}", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
            }
        }

        public static int NSurveys()
        {
            XmlNodeList? surveyNodes = Globals.Config.DocumentElement?.SelectNodes("Survey");
            if (surveyNodes == null)
            {
                return 0; // No surveys found
            }
            return surveyNodes.Count;
        }

        public static int NModels()
        {
            XmlNodeList? modelNodes = Globals.Config.DocumentElement?.SelectNodes("Model");
            if (modelNodes == null)
            {
                return 0; // No models found
            }
            return modelNodes.Count;
        }
    }
}
