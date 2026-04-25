using KrogerDataAnalytics.Service;
using Microsoft.AspNetCore.Mvc;

[Route("api/[controller]")]
[ApiController]
public class DashboardController : Controller
{
    private readonly IDataService _dataService;

    public DashboardController(IDataService dataService)
    {
        _dataService = dataService;
    }

    public async Task<ActionResult> IndexAsync()
    {
        var _allResults = await _dataService.GetDataPullAsync();
        TrainingModel trainingModel = new TrainingModel();
        trainingModel.TrainRandomForest((List<KrogerDataAnalytics.Components.Models.JoinedTransaction>)_allResults);
        return View();
    }
}

public interface IDataService
{
    Task<IEnumerable<object>> GetDataPullAsync();
}
