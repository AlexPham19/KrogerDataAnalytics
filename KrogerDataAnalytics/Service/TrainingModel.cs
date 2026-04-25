using KrogerDataAnalytics.Components.Models;
using Microsoft.ML;
using Microsoft.ML.Data;
using System.Collections.Generic;
using System.Linq;

public class ProductTypeData
{
    public string Income_range { get; set; }
    public bool IsPrivate { get; set; } // true = private, false = public
}

public class ProductTypePrediction
{
    [ColumnName("PredictedLabel")]
    public bool IsPrivate { get; set; }
}

public class TrainingModel
{
    public TransformerChain<BinaryPredictionTransformer<Microsoft.ML.Trainers.FastTree.FastForestBinaryModelParameters>> TrainRandomForest(List<JoinedTransaction> data)
    {
        // Map your data to ProductTypeData
        var trainingData = data
            .Where(x => !string.IsNullOrEmpty(x.Income_range))
            .Select(x => new ProductTypeData
            {
                Income_range = x.Income_range,
                IsPrivate = x.Brand_type == "Private"
            }).ToList();

        var mlContext = new MLContext();
        var dataView = mlContext.Data.LoadFromEnumerable(trainingData);

        var pipeline = mlContext.Transforms.Categorical.OneHotEncoding("Income_range")
            .Append(mlContext.Transforms.Concatenate("Features", "Income_range"))
            .Append(mlContext.BinaryClassification.Trainers.FastForest(labelColumnName: "IsPrivate", featureColumnName: "Features"));

        return pipeline.Fit(dataView);

        // Save or use the model as needed
    }
}
