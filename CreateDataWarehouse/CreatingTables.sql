-- Clients Table
CREATE TABLE [wealth-data].[dbo].[Clients] (
    ClientID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(255) NOT NULL
);

-- Assets Table
CREATE TABLE [wealth-data].[dbo].[Assets] (
    AssetID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(255) NOT NULL,
    AssetType NVARCHAR(50) NOT NULL,
    CurrentValue DECIMAL(18,2) NOT NULL
);

-- Portfolios Table
CREATE TABLE [wealth-data].[dbo].[Portfolios] (
    PortfolioID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(255) NOT NULL,
    ClientID INT NOT NULL FOREIGN KEY REFERENCES [wealth-data].[dbo].[Clients](ClientID),
    RiskLevel NVARCHAR(50) NOT NULL
);

-- PortfolioAssets Table
CREATE TABLE [wealth-data].[dbo].[PortfolioAssets] (
    PortfolioAssetID INT IDENTITY(1,1) PRIMARY KEY,
    PortfolioID INT NOT NULL FOREIGN KEY REFERENCES [wealth-data].[dbo].[Portfolios](PortfolioID),
    AssetID INT NOT NULL FOREIGN KEY REFERENCES [wealth-data].[dbo].[Assets](AssetID),
    Allocation DECIMAL(5,2) NOT NULL CHECK (Allocation >= 0 AND Allocation <= 100)
);

-- FinancialGoals Table
CREATE TABLE [wealth-data].[dbo].[FinancialGoals] (
    GoalID INT IDENTITY(1,1) PRIMARY KEY,
    ClientID INT NOT NULL FOREIGN KEY REFERENCES [wealth-data].[dbo].[Clients](ClientID),
    GoalDescription NVARCHAR(255) NOT NULL,
    TargetAmount DECIMAL(18,2) NOT NULL,
    TargetDate DATE NOT NULL
);

-- RiskAssessmentMetrics Table
CREATE TABLE [wealth-data].[dbo].[RiskAssessmentMetrics] (
    MetricID INT IDENTITY(1,1) PRIMARY KEY,
    AssetID INT NOT NULL FOREIGN KEY REFERENCES [wealth-data].[dbo].[Assets](AssetID),
    MetricName NVARCHAR(50) NOT NULL,
    Value DECIMAL(10,4) NOT NULL,
    Timestamp DATETIME NOT NULL
);

-- RiskProfileMapping Table
CREATE TABLE [wealth-data].[dbo].[RiskProfileMapping] (
    MappingID INT IDENTITY(1,1) PRIMARY KEY,
    RiskLevel NVARCHAR(50) NOT NULL,
    AssetType NVARCHAR(50) NOT NULL,
    RecommendedAllocation DECIMAL(5,2) NOT NULL CHECK (RecommendedAllocation >= 0 AND RecommendedAllocation <= 100)
);

-- HistoricalProjections Table
CREATE TABLE [wealth-data].[dbo].[HistoricalProjections] (
    ProjectionID INT IDENTITY(1,1) PRIMARY KEY,
    PortfolioID INT NOT NULL FOREIGN KEY REFERENCES [wealth-data].[dbo].[Portfolios](PortfolioID),
    Date DATE NOT NULL,
    PredictedValue DECIMAL(18,2) NOT NULL,
    ActualValue DECIMAL(18,2) NOT NULL
);
