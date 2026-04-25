using CsvHelper.Configuration;
using KrogerDataAnalytics.Components.Models;

namespace KrogerDataAnalytics.Service;

public sealed class BasketRuleMap : ClassMap<BasketRule>
{
    public BasketRuleMap()
    {
        Map(m => m.Antecedents).Name("antecedents");
        Map(m => m.Consequents).Name("consequents");

        Map(m => m.AntecedentSupport).Name("antecedent support");
        Map(m => m.ConsequentSupport).Name("consequent support");
        Map(m => m.Support).Name("support");
        Map(m => m.Confidence).Name("confidence");
        Map(m => m.Lift).Name("lift");

        Map(m => m.Leverage).Name("leverage");
        Map(m => m.Conviction).Name("conviction");
        Map(m => m.ZhangsMetric).Name("zhangs_metric");
        Map(m => m.Jaccard).Name("jaccard");
        Map(m => m.Certainty).Name("certainty");
        Map(m => m.Kulczynski).Name("kulczynski");
    }
}