using KrogerDataAnalytics.Components.Models;
using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Household> Households { get; set; }
    public DbSet<Transaction> Transactions { get; set; }
    public DbSet<Product> Products { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Define relationship: Transaction links to Household and Product
        modelBuilder.Entity<Transaction>()
            .HasOne<Household>()
            .WithMany()
            .HasForeignKey(t => t.Hshd_num);

        modelBuilder.Entity<Transaction>()
            .HasOne<Product>()
            .WithMany()
            .HasForeignKey(t => t.Product_num);
    }
}