
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace KrogerDataAnalytics.Components.Models
{
    [Table("400_transactions")]
    public class Transaction
    {
        [Key]
        public int TransactionId { get; set; } // Add this field manually

        [Column("BASKET_NUM")]
        public int Basket_num { get; internal set; }
        [Column("HSHD_NUM")]
        public short Hshd_num { get; internal set; }
        [Column("PURCHASE")]
        public DateTime? Date { get; internal set; }
        [Column("PRODUCT_NUM")]
        public int Product_num { get; internal set; }
        [Column("SPEND")]
        public double? Spend { get; internal set; }
        [Column("UNITS")]
        public byte? Units { get; internal set; }
        [Column("STORE_R")]
        public string? Store_region { get; internal set; }
        [Column("WEEK_NUM")]
        public byte? Week_num { get; internal set; }
        [Column("YEAR")]
        public short? Year { get; internal set; }
    }
}