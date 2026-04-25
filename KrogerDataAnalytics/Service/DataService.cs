using KrogerDataAnalytics.Components.Models;
using Microsoft.EntityFrameworkCore;

namespace KrogerDataAnalytics.Service
{
    public class DataService
    {
        private readonly IDbContextFactory<AppDbContext> _dbFactory;

        public DataService(IDbContextFactory<AppDbContext> dbFactory)
        {
            _dbFactory = dbFactory;
        }
        
        public async Task<List<JoinedTransaction>> GetDataPullAsync()
        {
            using var context = _dbFactory.CreateDbContext();

            return await (from t in context.Transactions
                          join h in context.Households on t.Hshd_num equals h.Hshd_num
                          join p in context.Products on t.Product_num equals p.Product_num
                          orderby t.Hshd_num, t.Basket_num, t.Date, t.Product_num, p.Department, p.Commodity
                          select new JoinedTransaction
                          {
                              Hshd_num = t.Hshd_num,
                              Basket_num = t.Basket_num,
                              Date = t.Date ?? DateTime.MinValue,
                              Product_num = t.Product_num,
                              Spend = t.Spend ?? 0,
                              Units = t.Units ?? 0,
                              Store_region = t.Store_region,
                              Week_num = t.Week_num ?? 0,
                              Year = t.Year ?? 0,
                              Department = p.Department,
                              Commodity = p.Commodity,
                              Brand_type = p.Brand_type,
                              Natural_organic_flag = p.Natural_organic_flag,
                              Loyalty_flag = h.Loyalty_flag,
                              Age_range = h.Age_range,
                              Marital_status = h.Marital_status,
                              Income_range = h.Income_range,
                              Homeowner_desc = h.Homeowner_desc,
                              Hshd_composition = h.Hshd_composition,
                              Hshd_size = h.Hshd_size ?? 0,
                              Children = h.Children
                          }).ToListAsync();
        }

        public async Task<List<JoinedTransaction>> GetDataPullAsync(int hshdNum)
        {
            using var context = _dbFactory.CreateDbContext();

            return await (from t in context.Transactions
                          join h in context.Households on t.Hshd_num equals h.Hshd_num
                          join p in context.Products on t.Product_num equals p.Product_num
                          where t.Hshd_num == hshdNum
                          orderby t.Hshd_num, t.Basket_num, t.Date, t.Product_num, p.Department, p.Commodity
                          select new JoinedTransaction
                          {
                              Hshd_num = t.Hshd_num,
                              Basket_num = t.Basket_num,
                              Date = t.Date ?? DateTime.MinValue,
                              Product_num = t.Product_num,
                              Spend = t.Spend ?? 0,
                              Units = t.Units ?? 0,
                              Store_region = t.Store_region,
                              Week_num = t.Week_num ?? 0,
                              Year = t.Year ?? 0,
                              Department = p.Department,
                              Commodity = p.Commodity,
                              Brand_type = p.Brand_type,
                              Natural_organic_flag = p.Natural_organic_flag,
                              Loyalty_flag = h.Loyalty_flag,
                              Age_range = h.Age_range,
                              Marital_status = h.Marital_status,
                              Income_range = h.Income_range,
                              Homeowner_desc = h.Homeowner_desc,
                              Hshd_composition = h.Hshd_composition,
                              Hshd_size = h.Hshd_size ?? 0,
                              Children = h.Children
                          }).ToListAsync();
        }
    }
}
