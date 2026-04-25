namespace KrogerDataAnalytics.Components.Models;

public class BasketRule
{
    public string Antecedents { get; set; } = "";
    public string Consequents { get; set; } = "";

    public double AntecedentSupport { get; set; }
    public double ConsequentSupport { get; set; }
    public double Support { get; set; }
    public double Confidence { get; set; }
    public double Lift { get; set; }

    public double Leverage { get; set; }
    public double Conviction { get; set; }
    public double ZhangsMetric { get; set; }
    public double Jaccard { get; set; }
    public double Certainty { get; set; }
    public double Kulczynski { get; set; }
}