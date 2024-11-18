# Application Revenue Projection Tool

## Project Overview
Create an enterprise-grade Streamlit application for fashion tech startups to model and visualize revenue projections, user growth, and marketing campaign impacts. The tool should serve as a comprehensive financial modeling tool suitable for investor presentations and strategic planning.

## Core Technical Requirements

### Architecture
-All calculations should be done in a single script. Then, the calculated data in other scripts should be used directly. In this way, there should be no errors in the calculations.
- All parameters can be changed from the sidebar
- All default constant parameters should be in the constant.py script. Other scripts should import from there
- Implement a clean, modular architecture following SOLID principles
- Centralize all calculations in a dedicated ProjectionService.
- Use dataclasses for data models with proper validation
- Implement comprehensive error handling and input validation
- Follow type hints throughout the codebase
- Maintain separation of concerns between UI, business logic, and data

### Data Models
1. Subscription Tier Model (all users are subscibe):
   - Tier name (Basic/Standard/Premium)
   - Monthly price
   - Features list
   - User distribution percentage
   - Revenue calculation methods

2. Marketing Campaign Model:
   - Campaign name and ID
   - Reach and cost metrics
   - Duration and timing
   - Conversion funnel rates
   - ROI calculation methods

3. Growth Scenario Model:
   - Scenario name and parameters
   - Growth rate calculations
   - Retention metrics
   - Organic acquisition rates

4. Projection Results Model:
   - Monthly projection data
   - Aggregated metrics
   - Campaign impacts
   - Revenue distribution

## Feature Specifications

### 1. Subscription Management
- Configure three tiers (Basic/Standard/Premium)
- Dynamic pricing controls ($0-100/month)
- Feature set management per tier
- User distribution modeling (must total 100%)
- Tier-specific retention rates

### 2. Marketing Campaign System
- Multi-campaign support
- Campaign timing and duration
- Reach and cost modeling
- Conversion funnel:
  * Reach → Downloads (0.1-10%)
  * Downloads → Active Users (1-50%)
  * Active → Subscribers (1-100%)
- Campaign ROI calculations
- Campaign comparison tools

### 3. Growth Modeling
- Three base scenarios:
  * Conservative (3% monthly)
  * Moderate (8% monthly)
  * Aggressive (12% monthly)
  * Custom (1-200%)
- Customizable parameters:
  * Organic growth rate
  * User retention rate
  * Initial user base
  * Market saturation limits

### 4. Financial Metrics
- Revenue Metrics:
  * Monthly Recurring Revenue (MRR)
  * Annual Recurring Revenue (ARR)
  * Revenue by tier
  * Revenue growth rate

- User Metrics:
  * Total Active Users
  * Users by tier
  * Growth rate
  * Churn rate

- Business Metrics:
  * Customer Acquisition Cost (CAC)
  * Lifetime Value (LTV)
  * LTV/CAC ratio
  * Payback period
  * Burn rate

### 5. Visualizations

#### Charts
1. Revenue Charts:
   - Monthly revenue by tier (stacked area)
   - Cumulative revenue growth
   - Revenue distribution pie chart

2. User Growth Charts:
   - Monthly active users (line)
   - User acquisition by source
   - Retention curves
   - Churn visualization

3. Campaign Performance:
   - Campaign ROI comparison
   - Conversion funnel visualization
   - Campaign timing impact chart

#### Tables
1. Monthly Projection Table:
   - User metrics by month
   - Revenue metrics by month
   - Growth rates
   - Campaign impacts

2. Financial Summary Table:
   - Key metrics summary
   - Year-end projections
   - Scenario comparisons

### 6. Export/Import Functionality
- Export to Excel/CSV
- JSON data export
- Scenario saving/loading
- Chart image export
- PDF report generation

### 7. UI/UX Requirements
- Professional, minimal design
- Responsive layout
- Interactive tooltips
- Error messaging
- Loading states
- Input validation
- Mobile optimization

### 8. Campaign Timeline Management
- Allow users to set campaign start month (1-12)
- Configure campaign duration (1-12 months)
- Automatically calculate and validate end dates
- Prevent invalid date combinations
- Show warnings for overlapping campaigns
- Support multiple concurrent campaigns

### 9. Visual Components
#### A. Campaign Timeline Chart (Gantt Style)
- Horizontal bars showing campaign durations
- Color-coded campaign blocks
- Interactive tooltips showing:
  * Campaign name
  * Start month
  * Duration
  * Budget
  * Expected reach
  * Current status
- Month-by-month grid overlay
- Campaign overlap indicators

## Technical Stack
- Frontend: Streamlit
- Data Processing: Pandas
- Visualization: Plotly
- Export: XlsxWriter
- Validation: Pydantic
- Testing: Pytest

## Code Organization
src/
├── services/
│ ├── projection_service.py
│ └── export_service.py
├── models/
│ ├── subscription.py
│ ├── campaign.py
│ ├── growth_scenario.py
│ └── projection_results.py
├── components/
│ ├── metrics_display.py
│ ├── chart_display.py
│ ├── data_table.py
│ └── campaign_manager.py
├── config/
│ ├── constants.py
│ └── validation.py
└── utils/
├── calculations.py
└── formatters.py
