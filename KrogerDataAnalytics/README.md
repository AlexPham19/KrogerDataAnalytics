# RetailIQ — Blazor WebAssembly App

A multi-page Blazor WASM retail analytics application covering all four requirements.

## Project Structure

```
BlazorRetailApp/
├── App.razor                        # Root router
├── _Imports.razor                   # Global using statements
├── Program.cs                       # DI & app entry point
├── BlazorRetailApp.csproj
│
├── Pages/
│   ├── Login.razor                  # Req 1 — Username, Email, Password form
│   ├── SearchPulls.razor            # Req 2 — Search by Hshd_num, sortable table
│   ├── DataLoad.razor               # Req 3 — Upload Transactions/Households/Products CSVs
│   └── Dashboard.razor              # Req 4 — Retail analytics dashboard with charts
│
├── Shared/
│   └── MainLayout.razor             # Sidebar nav, topbar, auth state
│
├── Models/
│   └── DataModels.cs                # Transaction, Household, Product records
│
├── Services/
│   └── AppServices.cs               # TransactionService + AuthService (singleton)
│
└── wwwroot/
    ├── index.html                   # Host page, Chart.js CDN, JS interop
    └── css/
        └── app.css                  # Full global stylesheet
```

## Getting Started

### Prerequisites
- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)

### Run locally
```bash
cd BlazorRetailApp
dotnet run
# Open https://localhost:5001
```

### Publish
```bash
dotnet publish -c Release -o publish/
# Deploy publish/wwwroot to any static host (Azure Static Web Apps, GitHub Pages, Netlify, etc.)
```

## Pages

| Route        | File                  | Requirement |
|--------------|-----------------------|-------------|
| `/`          | `Login.razor`         | #1 — Registration form with validation |
| `/search`    | `SearchPulls.razor`   | #2 — Search by Hshd_num, multi-column sort |
| `/load`      | `DataLoad.razor`      | #3 — CSV upload for all three datasets |
| `/dashboard` | `Dashboard.razor`     | #4 — KPI cards + 5 interactive charts |

## CSV Format

### Transactions.csv
```
Hshd_num,Basket_num,Date,Product_num,Spend,Units,Store_r,Department,Commodity
10,1234,2023-01-15,5678,3.99,2,5,Grocery,Milk
```

### 400_households.csv
```
Hshd_num,L,Age_range,Marital,Income_range,Homeowner,Hshd_composition,Hshd_size,Children
10,Y,35-44,Married,50-74K,Homeowner,2 Adults,2,0
```

### 400_products.csv
```
Product_num,Department,Commodity,Brand_ty,Natural_organic_flag
5678,Grocery,Milk,Private,N
```

## Architecture Notes

- **TransactionService** is a singleton that seeds 600+ synthetic records on startup, so all pages work immediately without uploading CSVs.
- **AuthService** is a simple in-memory state holder. Replace with `AuthenticationStateProvider` + ASP.NET Identity for production.
- **Chart.js** is loaded via CDN in `index.html`. The `renderDashboard` JS function is called from `Dashboard.razor` via `IJSRuntime`.
- All sort logic in `SearchPulls.razor` runs in C# — no JS required.
