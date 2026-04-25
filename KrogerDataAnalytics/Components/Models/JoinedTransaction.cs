namespace KrogerDataAnalytics.Components.Models
{
    public class JoinedTransaction
    {
        // Transaction Data
        public int Hshd_num { get; set; }
        public int Basket_num { get; set; }
        public DateTime Date { get; set; }
        public int Product_num { get; set; }
        public double Spend { get; set; }
        public int Units { get; set; }
        public string? Store_region { get; set; }
        public int Week_num { get; set; }
        public int Year { get; set; }

        // Product Data
        public string? Department { get; set; }
        public string? Commodity { get; set; }
        public string? Brand_type { get; set; }
        public string? Natural_organic_flag { get; set; }

        // Household Data
        public bool? Loyalty_flag { get; set; } 
        public string? Age_range { get; set; } 
        public string? Marital_status { get; set; }
        public string? Income_range { get; set; } 
        public string? Homeowner_desc { get; set; }
        public string? Hshd_composition { get; set; }
        public int Hshd_size { get; set; }
        public string? Children { get; set; }
    }
}
