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
        public double WaterDensity { get; set; } = 1023.0;
        public double WaterSalinity { get; set; } = 32.0;
        public double WaterTemperature { get; set; } = 10.0;
        public double WaterpH { get; set; } = 8.1;
        public double SedimentDiameter { get; set; } = 2.5e-4;
        public double SedimentDensity { get; set; } = 2650.0;
        public XmlElement? survey; // Make 'survey' nullable to fix CS8618
        public _ClassConfigurationManager _project = new();

        public void Initialize()
        {
            survey = _Globals.Config.CreateElement("Survey");
            survey.SetAttribute("type", "Survey");
            survey.SetAttribute("name", "New Survey");
            survey.SetAttribute("id", _project.GetNextId().ToString());
            _project.SaveConfig(saveMode: 2);
        }

        public string GetAttribute(string attribute)
        {
            if (survey == null)
            {
                throw new InvalidOperationException("Survey is not initialized.");
            }
            return survey.GetAttribute(attribute);
        }

        public void SaveSurvey(string? name = null,
            double? waterDensity = 1023.0,
            double? waterSalinity = 32.0,
            double? waterTemperature = null,
            double? waterPH = 8.1,
            double? sedimentDiameter = 2.5e-4,
            double? sedimentDensity = 2650)
        {
            if (survey == null)
            {
                throw new InvalidOperationException("Survey is not initialized.");
            }

            if (!string.IsNullOrWhiteSpace(name))
            {
                survey.SetAttribute("name", name);
            }
            XmlElement? water = _Globals.Config.CreateElement("Water");
            water.SetAttribute("Density", waterDensity.ToString());
            water.SetAttribute("Salinity", waterSalinity.ToString());
            water.SetAttribute("Temperature", waterTemperature.ToString());
            water.SetAttribute("pH", waterPH.ToString());
            survey.AppendChild(water);
            XmlElement? sediment = _Globals.Config.CreateElement("Sediment");
            sediment.SetAttribute("Diameter", sedimentDiameter.ToString());
            sediment.SetAttribute("Density", sedimentDensity.ToString());
            WaterDensity = waterDensity ?? WaterDensity;
            WaterSalinity = waterSalinity ?? WaterSalinity;
            WaterTemperature = waterTemperature ?? WaterTemperature;
            WaterpH = waterPH ?? WaterpH;
            SedimentDiameter = sedimentDiameter ?? SedimentDiameter;
            SedimentDensity = sedimentDensity ?? SedimentDensity;
            survey.AppendChild(sediment);
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
            _project.SaveConfig(saveMode: 2);
            
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
