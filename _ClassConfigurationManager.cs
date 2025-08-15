using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.NetworkInformation;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using Microsoft.WindowsAPICodePack.Dialogs;

namespace CSEMMPGUI_v1
{
    public static class _ClassConfigurationManager
    {
        public static bool hasChanged = false;
        public static bool isSaved = false;
        public static int saveCount;

        public static void InitializeProject(string name)
        {
            _Globals.Config.RemoveAll();
            XmlDeclaration xmlDeclaration = _Globals.Config.CreateXmlDeclaration("1.0", "UTF-8", null);
            _Globals.Config.AppendChild(xmlDeclaration);
            XmlElement root = _Globals.Config.CreateElement("Project");
            root.SetAttribute("type", "Project");
            root.SetAttribute("nextid", "1");
            _Globals.Config.AppendChild(root);

            XmlElement settings = _Globals.Config.CreateElement("Settings");
            XmlNode? nodeName = _Globals.Config.CreateElement("Name");
            nodeName.InnerText = name;
            settings.AppendChild(nodeName);
            XmlNode? nodeDirectory = _Globals.Config.CreateElement("Directory");
            nodeDirectory.InnerText = string.Empty;
            settings.AppendChild(nodeDirectory);
            XmlNode? nodeEPSG = _Globals.Config.CreateElement("EPSG");
            nodeEPSG.InnerText = "4326"; // Default EPSG code
            settings.AppendChild(nodeEPSG);
            XmlNode? nodeDescription = _Globals.Config.CreateElement("Description");
            nodeDescription.InnerText = "";
            settings.AppendChild(nodeDescription);

            root.AppendChild(settings);
        }

        public static string GetSetting(string settingName)
        {
            XmlNode? settingNode = _Globals.Config.DocumentElement?.SelectSingleNode($"Settings/{settingName}");
            return settingNode?.InnerText ?? string.Empty;
        }

        public static void SetSetting(string settingName, string value)
        {
            XmlNode? settingNode = _Globals.Config.DocumentElement?.SelectSingleNode($"Settings/{settingName}");
            if (settingNode == null)
            {
                settingNode = _Globals.Config.CreateElement(settingName);
                _Globals.Config.DocumentElement?.SelectSingleNode("Settings")?.AppendChild(settingNode);
            }
            settingNode.InnerText = value;
        }

        public static string? GetProjectPath()
        {
            string projectDir = GetSetting(settingName: "Directory");
            if (String.IsNullOrEmpty(projectDir))
            {
                var fbd = new CommonOpenFileDialog
                {
                    IsFolderPicker = true,
                    Title = "Select Project Directory",
                    NavigateToShortcut = true,
                    InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
                    EnsurePathExists = true,
                };
                
                if (fbd.ShowDialog() == CommonFileDialogResult.Ok)
                {
                    SetSetting(settingName: "Directory", value: fbd.FileName);
                    projectDir = fbd.FileName;
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

        public static void SaveConfig(int saveMode)
        {
            if (_Globals.Config.DocumentElement == null)
            {
                InitializeProject(name: "Project");
            }
            string? path = GetProjectPath();
            if (String.IsNullOrEmpty(path))
            {
                MessageBox.Show(text: "Project path is not set. Please set the project directory first.", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
                return;
            }
            if (File.Exists(path) && saveMode == 0)
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
                    _Globals.Config.Save(path);
                    isSaved = true;
                    hasChanged = false;
                }
            }
            else
            {
                _Globals.Config.Save(path);
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
                _Globals.Config.Load(filePath);
                isSaved = true;
                hasChanged = false;
                saveCount = 0;
            }
            catch (Exception ex)
            {
                MessageBox.Show(text: $"Failed to load project file: {ex.Message}", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
            }
        }

        public static int NObjects(string type)
        {
            XmlNodeList? objectNodes = _Globals.Config.DocumentElement?.SelectNodes(type);
            if (objectNodes == null)
            {
                return 0; // No objects found
            }
            return objectNodes.Count;
        }

        public static void DeleteNode(string type, string id)
        {
            if (_Globals.Config.DocumentElement == null)
            {
                throw new InvalidOperationException("Configuration is not initialized.");
            }
            string xpath = $"//{type}[@id='{id}' and @type='{type}']";
            XmlNode? nodeToDelete = _Globals.Config.DocumentElement.SelectSingleNode(xpath);
            if (nodeToDelete != null && nodeToDelete.ParentNode != null)
            {
                nodeToDelete.ParentNode.RemoveChild(nodeToDelete);
                hasChanged = true;
            }
            else
            {
                throw new InvalidOperationException($"Node of type '{type}' with id '{id}' not found.");
            }
        }

        public static int GetNextId()
        {
            return int.Parse(_Globals.Config.DocumentElement?.GetAttribute("nextid") ?? "1");
        }

        public static List<XmlElement> GetObjects(string type)
        {
            var result = new List<XmlElement>();
            if (_Globals.Config.DocumentElement == null)
            {
                throw new InvalidOperationException("Configuration is not initialized.");
            }
            var objectNodes = _Globals.Config.DocumentElement.SelectNodes(type);
            if (objectNodes == null)
            {
                return result; // No objects found
            }
            foreach (XmlNode node in objectNodes)
            {
                if (node is XmlElement element && element.GetAttribute("type") == type)
                {
                    result.Add(element);
                }
            }
            return result;
        }
    }
}
