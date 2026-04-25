using CsvHelper;
using CsvHelper.Configuration;
using KrogerDataAnalytics.Components.Models;
using System.Globalization;

namespace KrogerDataAnalytics.Service;

public class BasketRuleService
{
    private readonly IWebHostEnvironment _env;

    public BasketRuleService(IWebHostEnvironment env)
    {
        _env = env;
    }

    public List<BasketRule> LoadRules()
    {
        var filePath = Path.Combine(
            _env.WebRootPath,
            "charts",
            "basket_association_rules.csv"
        );

        if (!File.Exists(filePath))
            return new List<BasketRule>();

        var config = new CsvConfiguration(CultureInfo.InvariantCulture)
        {
            HeaderValidated = null,
            MissingFieldFound = null
        };

        using var reader = new StreamReader(filePath);
        using var csv = new CsvReader(reader, config);

        csv.Context.RegisterClassMap<BasketRuleMap>();

        return csv.GetRecords<BasketRule>()
                  .OrderByDescending(r => r.Lift)
                  .ToList();
    }
}