using System.Web;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public static class ConfigData
    {
        

        

        public static string GetProjectPath()
        {
            XmlNode pathNode = Config.DocumentElement?.SelectSingleNode("Settings/Path");
            return pathNode != null ? pathNode.InnerText : null;
        }

        public static void SetProjectPath(string path)
        {
            XmlNode settingsNode = Config.DocumentElement?.SelectSingleNode("Settings");
            if (settingsNode == null)
            {
                settingsNode = Config.CreateElement("Settings");
                Config.DocumentElement.AppendChild(settingsNode);
            }

            XmlNode pathNode = settingsNode.SelectSingleNode("Path");
            if (pathNode == null)
            {
                pathNode = Config.CreateElement("Path");
                settingsNode.AppendChild(pathNode);
            }
            pathNode.InnerText = path;
        }

        public static void SetProjectDir(string path)
        {
            XmlNode settingsNode = Config.DocumentElement?.SelectSingleNode("Settings");
            if (settingsNode == null)
            {
                settingsNode = Config.CreateElement("Settings");
                Config.DocumentElement.AppendChild(settingsNode);
            }

            XmlNode pathNode = settingsNode.SelectSingleNode("Directory");
            if (pathNode == null)
            {
                pathNode = Config.CreateElement("Directory");
                settingsNode.AppendChild(pathNode);
            }
            pathNode.InnerText = path;
        }

        public static string GetProjectDir()
        {
            XmlNode dirNode = Config.DocumentElement?.SelectSingleNode("Settings/Directory");
            if (dirNode.InnerText != null && dirNode.InnerText.Trim().Length > 0)
            {
                return dirNode.InnerText;
            }
            else
            {
                return Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            }
        }

        public static void SetProjectName(string name)
        {
            XmlNode projectName = Config.DocumentElement.SelectSingleNode("Settings/Name");
            if (projectName != null)
            {
                return;
            }
            XmlNode settingsNode = Config.DocumentElement?.SelectSingleNode("Settings");
            if (settingsNode == null)
            {
                settingsNode = Config.CreateElement("Settings");
                Config.DocumentElement.AppendChild(settingsNode);
            }

            XmlNode nameNode = settingsNode.SelectSingleNode("Name");
            if (nameNode == null)
            {
                nameNode = Config.CreateElement("Name");
                settingsNode.AppendChild(nameNode);
            }
            nameNode.InnerText = name;
        }

        public static XmlNode GetSettings()
        {
            XmlNode settings = Config.DocumentElement?.SelectSingleNode("Settings");
            if (settings == null)
            {
                settings = Config.CreateElement("Settings");
                Config.DocumentElement?.AppendChild(settings);
            }
            return settings;
        }

        public static void updateNode(XmlNode root, string field, string value)
        {
            XmlNode node = root.SelectSingleNode(field);
            if (node == null)
            {
                node = Config.CreateElement(field);
                root.AppendChild(node);
            }
            node.InnerText = value;
        }

        public static void SetSettings(string directory, string name, string epsg, string description)
        {
            XmlNode settings = Config.DocumentElement.SelectSingleNode("Settings");
            if (settings == null)
            {
                settings = Config.CreateElement("Settings");
                Config.DocumentElement.AppendChild(settings);
            }
            updateNode(settings, "Directory", directory);
            updateNode(settings, "Name", name);
            updateNode(settings, "EPSG", epsg);
            updateNode(settings, "Description", description);

        }

        public static bool IsModified
        {
            get
            {
                XmlNode root = Config.DocumentElement;
                if (root == null) return false;

                // Check for elements other than Settings
                bool hasContentNodes = root.ChildNodes
                    .Cast<XmlNode>()
                    .Any(node => node.Name != "Settings");

                // Check if any setting value is not empty
                XmlNode settings = root.SelectSingleNode("Settings");
                bool hasFilledSettings = settings?.ChildNodes
                    .Cast<XmlNode>()
                    .Any(n => !string.IsNullOrWhiteSpace(n.InnerText)) == true;

                return hasContentNodes || hasFilledSettings;
            }
        }

        public static List<XmlNode> GetModels()
        {
            XmlNode root = Config.DocumentElement;
            if (root == null) return new List<XmlNode>();
            return root.SelectNodes("Model").Cast<XmlNode>().Where(n => n.Attributes?["type"]?.Value == "Model").ToList();
        }

        public static void SaveConfig()
        {
            if (Config.DocumentElement == null)
            {
                InitializeProject();
            }
            string path = GetProjectPath();
            if (string.IsNullOrEmpty(path) || !File.Exists(path))
            {
                using SaveFileDialog sfd = new SaveFileDialog
                {
                    Filter = "MT Project Files (*.mtproj)|*.mtproj",
                    Title = "Save Project",
                    InitialDirectory = GetProjectDir()
                };
                if (sfd.ShowDialog() == DialogResult.OK)
                {
                    path = sfd.FileName;
                    if (!Path.GetExtension(path).Equals(".mtproj", StringComparison.OrdinalIgnoreCase))
                    {
                        path += ".mtproj";
                    }
                    SetProjectPath(path);
                    SetProjectDir(Path.GetDirectoryName(path));
                    SetProjectName(Path.GetFileNameWithoutExtension(path));
                }
                else
                {
                    return; // User cancelled, do not proceed
                }
            }
            Config.Save(path);
        }

        public static XmlNode GetModelByName(string modelName)
        {
            XmlNode root = Config.DocumentElement;
            if (root == null) return null;

            return root.SelectNodes("Model")
                .Cast<XmlNode>()
                .FirstOrDefault(m =>
                    string.Equals(m.Attributes?["name"]?.Value?.Trim(), modelName, StringComparison.OrdinalIgnoreCase));
        }

        public static void AddModelByName(string modelName, string path)
        {
            XmlElement modelNode = Config.CreateElement("Model");
            modelNode.SetAttribute("type", "Model");
            modelNode.SetAttribute("name", modelName);
            XmlElement pathNode = Config.CreateElement("Path");
            pathNode.InnerText = path;
            modelNode.AppendChild(pathNode);
            Config.DocumentElement?.AppendChild(modelNode);
        }

        public static int GetModelCount()
        {
            XmlNode root = Config.DocumentElement;
            if (root == null) return 0;

            return root.SelectNodes("Model")
                .Cast<XmlNode>()
                .Count(m => m.Attributes?["type"]?.Value == "Model");
        }

        public static int GetSurveyCount()
        {
            XmlNode root = Config.DocumentElement;
            if (root == null) return 0;

            return root.SelectNodes("Survey")
                .Cast<XmlNode>()
                .Count(s => s.Attributes?["type"]?.Value == "Survey");
        }

        public static string GetDefaultModelName()
        {
            int modelCount = GetModelCount();
            return $"Model {modelCount + 1}";
        }

        public static string GetDefaultSurveyName()
        {
            int surveyCount = GetSurveyCount();
            return $"Survey {surveyCount + 1}";
        }
    }
}
