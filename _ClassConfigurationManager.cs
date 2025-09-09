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
            _Globals.Config.AppendChild(root);

            XmlElement settings = _Globals.Config.CreateElement("Settings");
            settings.SetAttribute("type", "Settings");
            settings.SetAttribute("id", "1");
            XmlNode? nodeName = _Globals.Config.CreateElement("Name");
            nodeName.InnerText = "Untitiled-Project";
            settings.AppendChild(nodeName);
            XmlNode? nodeDirectory = _Globals.Config.CreateElement("Directory");
            string appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            string projectDir = System.IO.Path.Combine(appData, "PlumeTrack");
            nodeDirectory.InnerText = projectDir;
            settings.AppendChild(nodeDirectory);
            XmlNode? nodeEPSG = _Globals.Config.CreateElement("EPSG");
            nodeEPSG.InnerText = "4326"; // Default EPSG code
            settings.AppendChild(nodeEPSG);
            XmlNode? nodeDescription = _Globals.Config.CreateElement("Description");
            nodeDescription.InnerText = "";
            settings.AppendChild(nodeDescription);
            root.AppendChild(settings);

            XmlElement mapSettings = _Globals.Config.CreateElement("MapSettings");
            mapSettings.SetAttribute("type", "MapSettings");
            mapSettings.SetAttribute("id", "2");
            XmlElement mapSetting2D = _Globals.Config.CreateElement("Map2D");
            XmlNode bgcolor2D = _Globals.Config.CreateElement("BackgroundColor");
            bgcolor2D.InnerText = "#000000";
            mapSetting2D.AppendChild(bgcolor2D);
            XmlNode fieldName2D = _Globals.Config.CreateElement("FieldName");
            fieldName2D.InnerText = "Echo Intensity";
            mapSetting2D.AppendChild(fieldName2D);
            XmlNode cmap2D = _Globals.Config.CreateElement("ColorMap");
            cmap2D.InnerText = "jet";
            mapSetting2D.AppendChild(cmap2D);
            XmlNode minValue2D = _Globals.Config.CreateElement("vmin");
            minValue2D.InnerText = string.Empty;
            mapSetting2D.AppendChild(minValue2D);
            XmlNode maxValue2D = _Globals.Config.CreateElement("vmax");
            maxValue2D.InnerText = string.Empty;
            mapSetting2D.AppendChild(maxValue2D);
            XmlNode padDeg2D = _Globals.Config.CreateElement("Padding");
            padDeg2D.InnerText = "0.03";
            mapSetting2D.AppendChild(padDeg2D);
            XmlNode nGridLines2D = _Globals.Config.CreateElement("NGridLines");
            nGridLines2D.InnerText = "10";
            mapSetting2D.AppendChild(nGridLines2D);
            XmlNode gridOpacity2D = _Globals.Config.CreateElement("GridOpacity");
            gridOpacity2D.InnerText = "0.35";
            mapSetting2D.AppendChild(gridOpacity2D);
            XmlNode gridColor2D = _Globals.Config.CreateElement("GridColor");
            gridColor2D.InnerText = "#333333";
            mapSetting2D.AppendChild(gridColor2D);
            XmlNode gridWidth2D = _Globals.Config.CreateElement("GridWidth");
            gridWidth2D.InnerText = "1";
            mapSetting2D.AppendChild(gridWidth2D);
            XmlNode nAxisTicks2D = _Globals.Config.CreateElement("NAxisTicks");
            nAxisTicks2D.InnerText = "7";
            mapSetting2D.AppendChild(nAxisTicks2D);
            XmlNode tickFontSize2D = _Globals.Config.CreateElement("TickFontSize");
            tickFontSize2D.InnerText = "10";
            mapSetting2D.AppendChild(tickFontSize2D);
            XmlNode tickNDecimals2D = _Globals.Config.CreateElement("TickNDecimals");
            tickNDecimals2D.InnerText = "4";
            mapSetting2D.AppendChild(tickNDecimals2D);
            XmlNode axisLabelFontSize2D = _Globals.Config.CreateElement("AxisLabelFontSize");
            axisLabelFontSize2D.InnerText = "12";
            mapSetting2D.AppendChild(axisLabelFontSize2D);
            XmlNode axisLabelColor2D = _Globals.Config.CreateElement("AxisLabelColor");
            axisLabelColor2D.InnerText = "#cccccc";
            mapSetting2D.AppendChild(axisLabelColor2D);
            XmlNode hoverFontSize2D = _Globals.Config.CreateElement("HoverFontSize");
            hoverFontSize2D.InnerText = "9";
            mapSetting2D.AppendChild(hoverFontSize2D);
            XmlNode transectLineWidth2D = _Globals.Config.CreateElement("TransectLineWidth");
            transectLineWidth2D.InnerText = "3";
            mapSetting2D.AppendChild(transectLineWidth2D);
            XmlNode verticalAggBinItem2D = _Globals.Config.CreateElement("VerticalAggBinItem");
            verticalAggBinItem2D.InnerText = "Bin";
            mapSetting2D.AppendChild(verticalAggBinItem2D);
            XmlNode verticalAggBinTarget2D = _Globals.Config.CreateElement("VerticalAggBinTarget");
            verticalAggBinTarget2D.InnerText = "Mean";
            mapSetting2D.AppendChild(verticalAggBinTarget2D);
            XmlNode verticalAggBeam2D = _Globals.Config.CreateElement("VerticalAggBeam");
            verticalAggBeam2D.InnerText = "Mean";
            mapSetting2D.AppendChild(verticalAggBeam2D);
            XmlNode surveys2D = _Globals.Config.CreateElement("Surveys");
            mapSetting2D.AppendChild(surveys2D);

            XmlElement mapSetting3D = _Globals.Config.CreateElement("Map3D");
            XmlNode bgcolor3D = _Globals.Config.CreateElement("BackgroundColor");
            bgcolor3D.InnerText = "#000000";
            mapSetting3D.AppendChild(bgcolor3D);
            XmlNode fieldName3D = _Globals.Config.CreateElement("FieldName");
            fieldName3D.InnerText = "Echo Intensity";
            mapSetting3D.AppendChild(fieldName3D);
            XmlNode cmap3D = _Globals.Config.CreateElement("ColorMap");
            cmap3D.InnerText = "jet";
            mapSetting3D.AppendChild(cmap3D);
            XmlNode minValue3D = _Globals.Config.CreateElement("vmin");
            minValue3D.InnerText = string.Empty;
            mapSetting3D.AppendChild(minValue3D);
            XmlNode maxValue3D = _Globals.Config.CreateElement("vmax");
            maxValue3D.InnerText = string.Empty;
            mapSetting3D.AppendChild(maxValue3D);
            XmlNode padDeg3D = _Globals.Config.CreateElement("Padding");
            padDeg3D.InnerText = "0.03";
            mapSetting3D.AppendChild(padDeg3D);
            XmlNode nGridLines3D = _Globals.Config.CreateElement("NGridLines");
            nGridLines3D.InnerText = "10";
            mapSetting3D.AppendChild(nGridLines3D);
            XmlNode gridOpacity3D = _Globals.Config.CreateElement("GridOpacity");
            gridOpacity3D.InnerText = "0.35";
            mapSetting3D.AppendChild(gridOpacity3D);
            XmlNode gridColor3D = _Globals.Config.CreateElement("GridColor");
            gridColor3D.InnerText = "#333333";
            mapSetting3D.AppendChild(gridColor3D);
            XmlNode gridWidth3D = _Globals.Config.CreateElement("GridWidth");
            gridWidth3D.InnerText = "1";
            mapSetting3D.AppendChild(gridWidth3D);
            XmlNode nAxisTicks3D = _Globals.Config.CreateElement("NAxisTicks");
            nAxisTicks3D.InnerText = "7";
            mapSetting3D.AppendChild(nAxisTicks3D);
            XmlNode tickFontSize3D = _Globals.Config.CreateElement("TickFontSize");
            tickFontSize3D.InnerText = "10";
            mapSetting3D.AppendChild(tickFontSize3D);
            XmlNode tickNDecimals3D = _Globals.Config.CreateElement("TickNDecimals");
            tickNDecimals3D.InnerText = "4";
            mapSetting3D.AppendChild(tickNDecimals3D);
            XmlNode axisLabelFontSize3D = _Globals.Config.CreateElement("AxisLabelFontSize");
            axisLabelFontSize3D.InnerText = "12";
            mapSetting3D.AppendChild(axisLabelFontSize3D);
            XmlNode axisLabelColor3D = _Globals.Config.CreateElement("AxisLabelColor");
            axisLabelColor3D.InnerText = "#cccccc";
            mapSetting3D.AppendChild(axisLabelColor3D);
            XmlNode hoverFontSize3D = _Globals.Config.CreateElement("HoverFontSize");
            hoverFontSize3D.InnerText = "9";
            mapSetting3D.AppendChild(hoverFontSize3D);
            XmlNode zScale3D = _Globals.Config.CreateElement("ZScale");
            zScale3D.InnerText = "3.0";
            mapSetting3D.AppendChild(zScale3D);
            XmlNode surveys3D = _Globals.Config.CreateElement("Surveys");
            mapSetting3D.AppendChild(surveys3D);

            XmlElement mapSettingShp = _Globals.Config.CreateElement("MapShapefiles");
            
            mapSettings.AppendChild(mapSetting2D);
            mapSettings.AppendChild(mapSetting3D);
            mapSettings.AppendChild(mapSettingShp);
            root.AppendChild(mapSettings);

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
            string projectName = GetSetting(settingName: "Name");
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
            var nodes = _Globals.Config.SelectNodes("//*[@id]");
            int maxId = -1;

            foreach (XmlNode node in nodes)
            {
                if (int.TryParse(node.Attributes["id"].Value, out int val))
                {
                    if (val > maxId)
                        maxId = val;
                }
            }

            return maxId + 1;

        }

        public XmlNodeList GetObjects(string type)
        {
            if (_Globals.Config.DocumentElement == null)
            {
                throw new InvalidOperationException("Configuration is not initialized.");
            }

            // XPath selects elements with the given "type" attribute
            string xpath = $"//*[@type='{type}']";
            var objectNodes = _Globals.Config.DocumentElement.SelectNodes(xpath);

            return objectNodes ?? new XmlNodeListAdapter(); // return empty if null
        }

        // Helper class to return an empty XmlNodeList when needed
        private class XmlNodeListAdapter : XmlNodeList
        {
            public override XmlNode Item(int index) => null;
            public override System.Collections.IEnumerator GetEnumerator() { yield break; }
            public override int Count => 0;
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
