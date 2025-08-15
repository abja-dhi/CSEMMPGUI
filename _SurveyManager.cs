using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public class _SurveyManager
    {
        public string Name { get; set; } = string.Empty; // Initialize to avoid CS8618
        public XmlElement? survey; // Make 'survey' nullable to fix CS8618

        public void Initialize()
        {
            survey = _Globals.Config.CreateElement("Survey");
            survey.SetAttribute("type", "Survey");
            survey.SetAttribute("name", "New Survey");
            survey.SetAttribute("id", _ClassConfigurationManager.GetNextId().ToString());
            int nextId = _ClassConfigurationManager.GetNextId();
            _Globals.Config.DocumentElement?.SetAttribute("nextid", (nextId + 1).ToString());
            _ClassConfigurationManager.SaveConfig(saveMode: 2);
        }

        public string GetAttribute(string attribute)
        {
            if (survey == null)
            {
                throw new InvalidOperationException("Survey is not initialized.");
            }
            return survey.GetAttribute(attribute);
        }

        public void SaveSurvey(string? name = null)
        {
            if (survey == null)
            {
                throw new InvalidOperationException("Survey is not initialized.");
            }

            if (!string.IsNullOrWhiteSpace(name))
            {
                survey.SetAttribute("name", name);
            }

            string id = GetAttribute(attribute: "id");
            string xpath = $"//Project/Survey[@id='{id}' and @type='Survey']";
            XmlNode? existingSurvey = _Globals.Config.DocumentElement?.SelectSingleNode(xpath);
            if (existingSurvey != null)
            {
                // Update existing survey
                if (existingSurvey is XmlElement existingElement)
                {
                    existingElement.SetAttribute("name", survey.GetAttribute("name"));
                }
                else
                {
                    throw new InvalidOperationException("Existing survey node is not an XmlElement.");
                }
                XmlNode imported = _Globals.Config.ImportNode(survey, true);
                _Globals.Config.DocumentElement?.ReplaceChild(imported, existingSurvey);
            }
            else
            {
                // Add new survey
                _Globals.Config.DocumentElement?.AppendChild(survey);
            }
            _ClassConfigurationManager.SaveConfig(saveMode: 2);
            int nextId = _ClassConfigurationManager.GetNextId();
            _Globals.Config.DocumentElement?.SetAttribute("nextid", (nextId+1).ToString());
        }

        public int NInstrument(string type)
        {
            if (survey == null)
            {
                throw new InvalidOperationException("Survey is not initialized.");
            }
            string xpath = $"./{type}[@type='{type}']";
            XmlNodeList? instruments = survey.SelectNodes(xpath);
            return instruments?.Count ?? 0;
        }
    }
}
