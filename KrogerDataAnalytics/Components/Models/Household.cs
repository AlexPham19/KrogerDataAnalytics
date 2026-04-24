using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace KrogerDataAnalytics.Components.Models
{
    [Table("400_households")]
    public class Household
    {
        [Key]
        [Column("HSHD_NUM")]
        public short Hshd_num { get; internal set; }
        [Column("L")]
        public bool? Loyalty_flag { get; internal set; }
        [Column("AGE_RANGE")]
        public string? Age_range { get; internal set; }
        [Column("MARITAL")]
        public string? Marital_status { get; internal set; }
        [Column("INCOME_RANGE")]
        public string? Income_range { get; internal set; }
        [Column("HOMEOWNER")]
        public string? Homeowner_desc { get; internal set; }
        [Column("HSHD_COMPOSITION")]
        public string? Hshd_composition { get; internal set; }
        [Column("HH_SIZE")]
        public byte? Hshd_size { get; internal set; }
        [Column("CHILDREN")]
        public string? Children { get; internal set; }
    }
}