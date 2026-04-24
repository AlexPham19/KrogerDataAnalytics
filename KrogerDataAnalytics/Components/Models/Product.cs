using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace KrogerDataAnalytics.Components.Models
{
    [Table("400_products")]
    public class Product
    {
        [Key]
        [Column("PRODUCT_NUM")]
        public int Product_num { get; internal set; }
        [Column("DEPARTMENT")]
        public string? Department { get; internal set; }
        [Column("COMMODITY")]
        public string? Commodity { get; internal set; }
        [Column("BRAND_TY")]
        public string? Brand_type { get; internal set; }
        [Column("NATURAL_ORGANIC_FLAG")]
        public string? Natural_organic_flag { get; internal set; }
    }
}