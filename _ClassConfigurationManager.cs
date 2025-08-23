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
    public class _ClassConfigurationManager
    {
        public bool isSaved;

        public void InitializeProject()
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
            nodeName.InnerText = string.Empty;
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
            isSaved = false;
        }

        public string GetSetting(string settingName)
        {
            XmlNode? settingNode = _Globals.Config.DocumentElement?.SelectSingleNode($"Settings/{settingName}");
            return settingNode?.InnerText ?? string.Empty;
        }

        public void SetSetting(string settingName, string value)
        {
            XmlNode? settingNode = _Globals.Config.DocumentElement?.SelectSingleNode($"Settings/{settingName}");
            if (settingNode == null)
            {
                settingNode = _Globals.Config.CreateElement(settingName);
                _Globals.Config.DocumentElement?.SelectSingleNode("Settings")?.AppendChild(settingNode);
            }
            settingNode.InnerText = value;
        }

        public string? GetProjectPath()
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
                    return "0"; // User cancelled the dialog
                }
            }
            string projectName = GetSetting(settingName: "Name");
            if (String.IsNullOrEmpty(projectName))
            {
                return null; // Project name is not set
            }
            return System.IO.Path.Combine(projectDir, $"{projectName}.mtproj");
        }

        public void SaveConfig(int saveMode)
        {
            string? path = GetProjectPath();
            if (String.IsNullOrEmpty(path) || path == "0")
            {
                return;
            }
            _Globals.Config.Save(path);
            isSaved = true;
        }

        public void LoadConfig(string filePath)
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
            }
            catch (Exception ex)
            {
                MessageBox.Show(text: $"Failed to load project file: {ex.Message}", caption: "Error", buttons: MessageBoxButtons.OK, icon: MessageBoxIcon.Error);
            }
        }

        public int NObjects(string type)
        {
            XmlNodeList? objectNodes = _Globals.Config.DocumentElement?.SelectNodes(type);
            if (objectNodes == null)
            {
                return 0; // No objects found
            }
            return objectNodes.Count;
        }

        public void DeleteNode(string type, string id)
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
                
            }
            else
            {
                throw new InvalidOperationException($"Node of type '{type}' with id '{id}' not found.");
            }
        }

        public int GetNextId()
        {
            return int.Parse(_Globals.Config.DocumentElement?.GetAttribute("nextid") ?? "1");
        }

        public List<XmlElement> GetObjects(string type)
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

        public XmlElement? GetObject(string type, string id)
        {
            XmlDocument doc = _Globals.Config;
            XmlElement? element = doc.SelectSingleNode($"//{type}[@id='{id}' and @type='{type}']") as XmlElement;
            return element;
        }

        public XmlElement? GetParent(string type, string id)
        {
            XmlDocument doc = _Globals.Config;
            XmlElement? element = doc.SelectSingleNode($"//{type}[@id='{id}' and @type='{type}']/..") as XmlElement;
            return element?.ParentNode as XmlElement;
        }
    }
}
