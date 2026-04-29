# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0,
    "Orlando": 0.85,
    "Miami": 1.2,
    "Jacksonville": 0.75,
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9

    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday

    for store in stores:
        store_factor = store_performance[store]

        for dept in departments:
            dept_factor = dept_performance[dept]

            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)

                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise

                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range

                # Calculate profit
                profit = sales_amount * profit_margin

                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range

    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])

    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income

    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)

    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))

    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)

    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)

    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"

    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]

    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()

    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(
        5,
        np.random.normal(loc=4.0, scale=0.3) * (store_performance[store] ** 0.5)
    )

    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----


# TODO 1: Descriptive Analytics - Overview of Current Performance
def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics
    REQUIRED: Create and return dictionary with keys:
    - 'total_sales': float
    - 'total_profit': float
    - 'avg_profit_margin': float
    - 'sales_by_store': pandas Series
    - 'sales_by_dept': pandas Series
    """
    total_sales = float(sales_df["Sales"].sum())
    total_profit = float(sales_df["Profit"].sum())
    avg_profit_margin = float(sales_df["ProfitMargin"].mean())

    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)

    print(f"\nTotal Sales: ${total_sales:,.2f}")
    print(f"Total Profit: ${total_profit:,.2f}")
    print(f"Average Profit Margin: {avg_profit_margin:.2%}")

    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'avg_profit_margin': avg_profit_margin,
        'sales_by_store': sales_by_store,
        'sales_by_dept': sales_by_dept
    }


def visualize_sales_distribution():
    """
    Create visualizations showing how sales are distributed
    REQUIRED: Return tuple of three figures (store_fig, dept_fig, time_fig)
    """
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.month)["Sales"].sum()

    # Store figure
    store_fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(sales_by_store.index, sales_by_store.values)
    ax1.set_title("Annual Sales by Store")
    ax1.set_xlabel("Store")
    ax1.set_ylabel("Sales ($)")
    ax1.tick_params(axis='x', rotation=45)
    store_fig.tight_layout()

    # Department figure
    dept_fig, ax2 = plt.subplots(figsize=(8, 5))
    ax2.bar(sales_by_dept.index, sales_by_dept.values)
    ax2.set_title("Annual Sales by Department")
    ax2.set_xlabel("Department")
    ax2.set_ylabel("Sales ($)")
    ax2.tick_params(axis='x', rotation=45)
    dept_fig.tight_layout()

    # Time figure
    time_fig, ax3 = plt.subplots(figsize=(8, 5))
    ax3.plot(monthly_sales.index, monthly_sales.values, marker='o')
    ax3.set_title("Monthly Sales Trend")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Sales ($)")
    ax3.set_xticks(monthly_sales.index)
    time_fig.tight_layout()

    return store_fig, dept_fig, time_fig


def analyze_customer_segments():
    """
    Analyze customer segments and their relationship to spending
    REQUIRED: Return dictionary with keys:
    - 'segment_counts': pandas Series
    - 'segment_avg_spend': pandas Series
    - 'segment_loyalty': pandas DataFrame
    """
    segment_counts = customer_df["Segment"].value_counts()
    segment_avg_spend = customer_df.groupby("Segment")["MonthlySpend"].mean().sort_values(ascending=False)
    segment_loyalty = pd.crosstab(customer_df["Segment"], customer_df["LoyaltyTier"])

    return {
        'segment_counts': segment_counts,
        'segment_avg_spend': segment_avg_spend,
        'segment_loyalty': segment_loyalty
    }


# TODO 2: Diagnostic Analytics - Understanding Relationships
def analyze_sales_correlations():
    """
    Analyze correlations between various factors and sales performance
    REQUIRED: Return dictionary with keys:
    - 'store_correlations': pandas DataFrame
    - 'top_correlations': list of tuples (factor, correlation)
    - 'correlation_fig': matplotlib figure
    """
    merged_df = operational_df.merge(store_df, on="Store")

    numeric_cols = [
        "AnnualSales", "AnnualProfit", "SalesPerSqFt", "ProfitPerSqFt",
        "SalesPerStaff", "InventoryTurnover", "CustomerSatisfaction",
        "SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"
    ]
    store_correlations = merged_df[numeric_cols].corr()

    sales_corr = store_correlations["AnnualSales"].drop("AnnualSales")
    sales_corr = sales_corr.sort_values(key=lambda x: x.abs(), ascending=False)
    top_correlations = list(sales_corr.head(5).items())

    correlation_fig, ax = plt.subplots(figsize=(9, 7))
    cax = ax.imshow(store_correlations, cmap="coolwarm", aspect="auto", vmin=-1, vmax=1)
    ax.set_xticks(range(len(store_correlations.columns)))
    ax.set_xticklabels(store_correlations.columns, rotation=90)
    ax.set_yticks(range(len(store_correlations.index)))
    ax.set_yticklabels(store_correlations.index)
    ax.set_title("Correlation Matrix of Store Performance Factors")
    correlation_fig.colorbar(cax, ax=ax)
    correlation_fig.tight_layout()

    return {
        'store_correlations': store_correlations,
        'top_correlations': top_correlations,
        'correlation_fig': correlation_fig
    }


def compare_store_performance():
    """
    Compare stores across different operational metrics
    REQUIRED: Return dictionary with keys:
    - 'efficiency_metrics': pandas DataFrame (with SalesPerSqFt, SalesPerStaff)
    - 'performance_ranking': pandas Series (ranked by profit)
    - 'comparison_fig': matplotlib figure
    """
    efficiency_metrics = operational_df.set_index("Store")[["SalesPerSqFt", "SalesPerStaff"]]
    performance_ranking = operational_df.set_index("Store")["AnnualProfit"].sort_values(ascending=False)

    comparison_fig, ax = plt.subplots(figsize=(8, 5))
    performance_ranking.plot(kind="bar", ax=ax)
    ax.set_title("Store Ranking by Annual Profit")
    ax.set_xlabel("Store")
    ax.set_ylabel("Annual Profit ($)")
    ax.tick_params(axis='x', rotation=45)
    comparison_fig.tight_layout()

    return {
        'efficiency_metrics': efficiency_metrics,
        'performance_ranking': performance_ranking,
        'comparison_fig': comparison_fig
    }


def analyze_seasonal_patterns():
    """
    Identify and visualize seasonal patterns in sales data
    REQUIRED: Return dictionary with keys:
    - 'monthly_sales': pandas Series
    - 'dow_sales': pandas Series (day of week)
    - 'seasonal_fig': matplotlib figure
    """
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.month)["Sales"].sum()
    dow_sales = sales_df.groupby(sales_df["Date"].dt.day_name())["Sales"].sum()
    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow_sales = dow_sales.reindex(dow_order)

    seasonal_fig, axes = plt.subplots(2, 1, figsize=(9, 8))

    axes[0].plot(monthly_sales.index, monthly_sales.values, marker='o')
    axes[0].set_title("Monthly Sales Pattern")
    axes[0].set_xlabel("Month")
    axes[0].set_ylabel("Sales ($)")
    axes[0].set_xticks(monthly_sales.index)

    axes[1].bar(dow_sales.index, dow_sales.values)
    axes[1].set_title("Sales by Day of Week")
    axes[1].set_xlabel("Day of Week")
    axes[1].set_ylabel("Sales ($)")
    axes[1].tick_params(axis='x', rotation=45)

    seasonal_fig.tight_layout()

    return {
        'monthly_sales': monthly_sales,
        'dow_sales': dow_sales,
        'seasonal_fig': seasonal_fig
    }


# TODO 3: Predictive Analytics - Basic Forecasting
def predict_store_sales():
    """
    Use linear regression to predict store sales based on store characteristics
    REQUIRED: Return dictionary with keys:
    - 'coefficients': dict (feature: coefficient)
    - 'r_squared': float
    - 'predictions': pandas Series
    - 'model_fig': matplotlib figure
    """
    model_df = operational_df.merge(store_df, on="Store").set_index("Store")

    feature_cols = ["SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"]
    X = model_df[feature_cols].to_numpy(dtype=float)
    y = model_df["AnnualSales"].to_numpy(dtype=float)

    # Linear regression using least squares
    X_design = np.column_stack([np.ones(len(X)), X])
    beta = np.linalg.lstsq(X_design, y, rcond=None)[0]
    y_pred = X_design @ beta

    ss_res = ((y - y_pred) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    r_squared = float(1 - ss_res / ss_tot)

    coefficients = {feature: float(coef) for feature, coef in zip(feature_cols, beta[1:])}
    predictions = pd.Series(y_pred, index=model_df.index)

    model_fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(y, y_pred)
    line_min = min(y.min(), y_pred.min())
    line_max = max(y.max(), y_pred.max())
    ax.plot([line_min, line_max], [line_min, line_max], linestyle="--")
    ax.set_title("Actual vs Predicted Store Sales")
    ax.set_xlabel("Actual Annual Sales")
    ax.set_ylabel("Predicted Annual Sales")
    model_fig.tight_layout()

    return {
        'coefficients': coefficients,
        'r_squared': r_squared,
        'predictions': predictions,
        'model_fig': model_fig
    }


def forecast_department_sales():
    """
    Analyze and forecast departmental sales trends
    REQUIRED: Return dictionary with keys:
    - 'dept_trends': pandas DataFrame
    - 'growth_rates': pandas Series
    - 'forecast_fig': matplotlib figure
    """
    monthly_dept_sales = sales_df.groupby([sales_df["Date"].dt.month, "Department"])["Sales"].sum().unstack()

    dept_trends = monthly_dept_sales.rolling(window=3, min_periods=1).mean()
    growth_rates = monthly_dept_sales.pct_change().mean().fillna(0)

    forecast_fig, ax = plt.subplots(figsize=(9, 6))
    for dept in monthly_dept_sales.columns:
        ax.plot(monthly_dept_sales.index, monthly_dept_sales[dept], marker='o', label=dept)
    ax.set_title("Department Monthly Sales Trends")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales ($)")
    ax.legend()
    forecast_fig.tight_layout()

    return {
        'dept_trends': dept_trends,
        'growth_rates': growth_rates,
        'forecast_fig': forecast_fig
    }


# TODO 4: Integrated Analysis - Business Insights and Recommendations
def identify_profit_opportunities():
    """
    Identify the most profitable combinations and potential opportunities
    REQUIRED: Return dictionary with keys:
    - 'top_combinations': pandas DataFrame (top 10 store-dept combinations)
    - 'underperforming': pandas DataFrame (bottom 10)
    - 'opportunity_score': pandas Series (by store)
    """
    combo_profit = sales_df.groupby(["Store", "Department"]).agg(
        TotalSales=("Sales", "sum"),
        TotalProfit=("Profit", "sum"),
        AvgProfitMargin=("ProfitMargin", "mean")
    ).reset_index()

    top_combinations = combo_profit.sort_values("TotalProfit", ascending=False).head(10)
    underperforming = combo_profit.sort_values("TotalProfit", ascending=True).head(10)

    annual_profit = operational_df.set_index("Store")["AnnualProfit"]
    weekly_marketing = store_df.set_index("Store")["WeeklyMarketingSpend"]
    opportunity_score = (annual_profit / weekly_marketing).sort_values(ascending=False)

    print("\nTop 10 Profitable Store-Department Combinations:")
    print(top_combinations)
    print("\nBottom 10 Underperforming Store-Department Combinations:")
    print(underperforming)
    print("\nOpportunity Score by Store:")
    print(opportunity_score)

    return {
        'top_combinations': top_combinations,
        'underperforming': underperforming,
        'opportunity_score': opportunity_score
    }


def develop_recommendations():
    """
    Develop actionable recommendations based on the analysis
    REQUIRED: Return list of at least 5 recommendation strings
    """
    sales_metrics = analyze_sales_performance()
    customer_analysis = analyze_customer_segments()

    top_store = sales_metrics["sales_by_store"].idxmax()
    low_store = sales_metrics["sales_by_store"].idxmin()
    top_dept = sales_metrics["sales_by_dept"].idxmax()
    low_dept = sales_metrics["sales_by_dept"].idxmin()
    top_segment = customer_analysis["segment_avg_spend"].idxmax()

    recommendations = [
        f"Increase inventory and staffing support in {top_store}, since it generates the highest annual sales and is best positioned to capture additional demand.",
        f"Develop a performance improvement plan for {low_store}, including local promotions, cost control, and merchandising changes to improve traffic and profitability.",
        f"Expand or more aggressively promote the {top_dept} department, because it is the strongest revenue driver and offers the fastest path to additional sales growth.",
        f"Review pricing, assortment, and in-store placement for the {low_dept} department, which is underperforming relative to the other departments.",
        f"Target {top_segment} customers with tailored loyalty rewards and personalized offers, since this segment delivers the highest average monthly spending.",
        "Align staffing and stock levels with weekend demand, especially Saturday and Sunday, to reduce missed sales caused by higher customer traffic.",
        "Use square footage, staffing, and marketing spend together when making future expansion decisions, because they show a strong relationship with store sales performance."
    ]

    return recommendations


# TODO 5: Summary Report
def generate_executive_summary():
    """
    Generate an executive summary of key findings and recommendations
    REQUIRED: Print executive summary with sections:
    - Overview (1 paragraph)
    - Key Findings (3-5 bullet points)
    - Recommendations (3-5 bullet points)
    - Expected Impact (1 paragraph)
    """
    sales_metrics = analyze_sales_performance()
    customer_analysis = analyze_customer_segments()
    seasonality = analyze_seasonal_patterns()
    recommendations = develop_recommendations()

    top_store = sales_metrics["sales_by_store"].idxmax()
    top_dept = sales_metrics["sales_by_dept"].idxmax()
    top_segment = customer_analysis["segment_avg_spend"].idxmax()
    strongest_month = int(seasonality["monthly_sales"].idxmax())
    strongest_day = seasonality["dow_sales"].idxmax()

    print("Overview")
    print(
        f"GreenGrocer generated ${sales_metrics['total_sales']:,.2f} in annual sales and "
        f"${sales_metrics['total_profit']:,.2f} in annual profit, with an average profit margin of "
        f"{sales_metrics['avg_profit_margin']:.2%}. The business is performing well overall, but results vary "
        f"meaningfully by store, department, and time period, which creates clear opportunities for better "
        f"resource allocation and more focused growth strategies."
    )

    print("\nKey Findings")
    print(f"- {top_store} is the strongest-performing store by annual sales.")
    print(f"- {top_dept} is the top revenue-generating department across the business.")
    print(f"- {top_segment} is the highest-spending customer segment on average.")
    print(f"- Month {strongest_month} delivered the highest total sales, confirming clear seasonal demand patterns.")
    print(f"- {strongest_day} is the strongest sales day of the week, showing the importance of weekend readiness.")

    print("\nRecommendations")
    for rec in recommendations[:5]:
        print(f"- {rec}")

    print("\nExpected Impact")
    print(
        "If GreenGrocer reallocates labor, marketing, and inventory toward its best-performing stores, departments, "
        "and customer segments while also improving weaker locations, the company should be able to increase both "
        "revenue and profitability. Better alignment with seasonal and day-of-week demand patterns should also improve "
        "operational efficiency, reduce missed sales opportunities, and support more sustainable long-term growth."
    )


# Main function to execute all analyses
def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)

    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()

    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()

    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()

    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()

    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()

    plt.show()

    return {
        'sales_metrics': sales_metrics,
        'customer_analysis': customer_analysis,
        'correlations': correlations,
        'store_comparison': store_comparison,
        'seasonality': seasonality,
        'sales_model': sales_model,
        'dept_forecast': dept_forecast,
        'opportunities': opportunities,
        'recommendations': recommendations
    }


# Run the main function
if __name__ == "__main__":
    results = main()