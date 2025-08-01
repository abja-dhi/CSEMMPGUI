using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace CSEMMPGUI_v1
{
    public class SurveyManager
    {
        public string Name { get; set; } = string.Empty; // Initialize to avoid CS8618
        public XmlElement? survey; // Make 'survey' nullable to fix CS8618

        public string GetDefaultName()
        {
            int nSurveys = ConfigurationManager.NSurveys();
            return $"Survey {nSurveys + 1}";
        }
        
        public void Initialize()
        {
            survey = Globals.Config.CreateElement("Survey");
            survey.SetAttribute("type", "Survey");
            survey.SetAttribute("name", GetDefaultName());
            survey.SetAttribute("id", (ConfigurationManager.NSurveys()+1).ToString());
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
            XmlNode? existingSurvey = Globals.Config.DocumentElement?.SelectSingleNode(xpath);
            if (existingSurvey != null)
            {
                // Update existing survey
                XmlNode imported = Globals.Config.ImportNode(survey, true);
                Globals.Config.DocumentElement?.ReplaceChild(imported, existingSurvey);
            }
            else
            {
                // Add new survey
                Globals.Config.DocumentElement?.AppendChild(survey);
            }
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
