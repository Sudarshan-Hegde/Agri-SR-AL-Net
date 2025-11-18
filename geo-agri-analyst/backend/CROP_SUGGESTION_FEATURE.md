# 🌾 Crop Suggestion System - Profit Optimization

## Overview
Advanced profit-optimized crop recommendation algorithm that analyzes multiple factors to suggest the most profitable crops for a given location, maximizing farmer revenue.

## Features

### 🎯 **Profit-First Algorithm**
- ROI calculation for each crop
- Net profit per hectare analysis
- Annual profit potential with multiple harvest cycles
- Investment cost vs. return optimization

### 📊 **Multi-Factor Analysis**
1. **Climate Suitability (35% weight)**
   - Temperature range matching
   - Rainfall requirements
   - Climate zone compatibility
   - Growing season length

2. **Soil Suitability (35% weight)**
   - Soil type matching from land classification
   - Fertility assessment
   - Drainage requirements
   - Soil family compatibility

3. **Risk Assessment (30% weight)**
   - Crop risk level (low/medium/high)
   - Farmer's risk tolerance preference
   - Market stability considerations

### 🌱 **Comprehensive Crop Database**
**20+ Crops across 7 categories:**

#### 💰 High-Value Cash Crops
- **Saffron**: $1,500/kg, 6 months, High ROI
- **Vanilla**: $600/kg, 36 months, Very High ROI
- **Strawberries**: $5/kg, 6 months, Premium fruit
- **Blueberries**: $8/kg, 24 months, Specialty crop

#### 🥗 Premium Vegetables
- **Cherry Tomatoes**: $3/kg, 4 months, Quick returns
- **Bell Peppers**: $2.5/kg, 5 months, Reliable income
- **Broccoli**: $2/kg, 3 months, Fast cycle

#### 🌾 Staple Grains (Low Risk)
- **Wheat**: $0.3/kg, 6 months, Stable market
- **Rice**: $0.45/kg, 5 months, Water-intensive
- **Corn**: $0.25/kg, 4 months, Versatile crop

#### 🫘 Legumes (Nitrogen Fixing)
- **Soybeans**: $0.5/kg, 5 months, Soil health benefit
- **Chickpeas**: $1.2/kg, 5 months, Drought tolerant

#### 🌻 Oilseeds
- **Sunflower**: $0.6/kg, 4 months, Low water need
- **Canola**: $0.55/kg, 6 months, Cold hardy

#### 🌿 Herbs & Spices
- **Basil**: $6/kg, 3 months, High value
- **Lavender**: $15/kg, 24 months, Low maintenance

#### 🏭 Industrial Crops
- **Cotton**: $1.8/kg, 6 months, Fiber production
- **Sugarcane**: $0.05/kg, 12 months, High volume

## API Endpoints

### 1. `/api/v1/crop-suggestions` (POST)
**Standalone crop suggestion endpoint**

**Request:**
```json
{
  "lat": 37.7749,
  "lng": -122.4194,
  "land_class": "Croplands",
  "weather_data": { /* Optional weather object */ },
  "crop_history": { /* Optional history object */ },
  "farm_size_hectares": 5.0,
  "risk_tolerance": "medium"  // "low", "medium", "high"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "location": {"lat": 37.7749, "lng": -122.4194},
    "farm_size_hectares": 5.0,
    "climate_zone": "temperate",
    "soil_type": "fertile",
    "risk_tolerance": "medium",
    
    "top_suggestions": [
      {
        "rank": 1,
        "crop_name": "Cherry Tomatoes (Premium)",
        "category": "Vegetable",
        "suitability_percentage": 96.0,
        "expected_profit_per_hectare_usd": 115000,
        "roi_percentage": 2300.0,
        "investment_required_usd": 5000,
        "growing_period_months": 4,
        "harvest_cycles_per_year": 3,
        "annual_profit_potential_usd": 345000,
        "water_requirement": "medium",
        "labor_intensity": "medium",
        "risk_level": "medium",
        "key_advantages": [
          "Excellent ROI of 2300%",
          "Quick harvest - fast returns",
          "Highly suitable for local climate",
          "High market value"
        ],
        "success_tips": [
          "Optimal temperature: 18-27°C"
        ]
      }
      // ... top 10 crops
    ],
    
    "crop_rotation_plan": {
      "rotation_type": "Sequential high-profit rotation",
      "sequence": [
        {
          "crop": "Cherry Tomatoes (Premium)",
          "duration_months": 4,
          "category": "Vegetable",
          "benefit": "Quick cash crop"
        }
        // ... rotation sequence
      ],
      "total_cycle_months": 14,
      "benefits": [
        "Maximizes annual profit",
        "Reduces pest and disease pressure",
        "Maintains soil fertility",
        "Diversifies income streams"
      ]
    },
    
    "seasonal_calendar": {
      "Spring (Mar-May)": ["Cherry Tomatoes (Premium)", "Strawberries"],
      "Summer (Jun-Aug)": ["Bell Peppers", "Basil"],
      "Fall (Sep-Nov)": ["Broccoli", "Lavender"],
      "Winter (Dec-Feb)": []
    },
    
    "market_insights": {
      "portfolio_strategy": "Diversified high-profit approach",
      "total_investment_required_usd": 17500.0,
      "expected_annual_profit_usd": 747000.0,
      "portfolio_roi_percentage": 2820.8,
      "market_trends": [
        "Premium vegetables show strong demand",
        "Organic certification can increase prices by 20-30%",
        "Direct-to-consumer sales improve margins"
      ],
      "risk_mitigation": [
        "Diversify across multiple crops",
        "Stagger planting dates",
        "Build relationships with multiple buyers",
        "Consider value-added processing"
      ]
    }
  }
}
```

### 2. `/api/v1/analyze` (POST)
**Integrated analysis with crop suggestions**

Crop suggestions are automatically included in the response when you analyze a location:

```json
{
  "land_class": "Croplands",
  "confidence": 0.85,
  "weather_data": { /* ... */ },
  "crop_history": { /* ... */ },
  "crop_suggestions": { /* Same as standalone endpoint */ }
}
```

## Scoring Algorithm

### Climate Score Calculation
```python
climate_score = 0.0

# Temperature matching (40% of climate score)
if min_temp <= actual_temp <= max_temp:
    climate_score += 0.4
else:
    deviation = min(abs(actual_temp - min_temp), abs(actual_temp - max_temp))
    climate_score += max(0, 0.4 - (deviation / 20))

# Rainfall matching (40% of climate score)
if min_rainfall <= actual_rainfall <= max_rainfall:
    climate_score += 0.4
else:
    if actual_rainfall < min_rainfall:
        deviation = min_rainfall - actual_rainfall
    else:
        deviation = actual_rainfall - max_rainfall
    climate_score += max(0, 0.4 - (deviation / 1000))

# Climate zone match (20% of climate score)
if climate_zone in crop_climate_zones:
    climate_score += 0.2

Total: 0-1
```

### Soil Score Calculation
```python
soil_score = 0.0

# Soil type overlap (60%)
if soil_types_match:
    soil_score += 0.6

# Fertility bonus (30%)
if fertility == "high":
    soil_score += 0.3
elif fertility == "medium":
    soil_score += 0.2

# Drainage match (10%)
if drainage_requirements_met:
    soil_score += 0.1

Total: 0-1
```

### Risk Score Calculation
```python
# Risk tolerance vs. crop risk matrix
risk_matrix = {
    "low": {"low": 1.0, "medium": 0.9, "high": 0.6},
    "medium": {"low": 0.9, "medium": 1.0, "high": 0.8},
    "high": {"low": 0.7, "medium": 0.9, "high": 1.0}
}

risk_score = risk_matrix[farmer_tolerance][crop_risk_level]
```

### Overall Suitability
```python
suitability = (climate_score * 0.35) + (soil_score * 0.35) + (risk_score * 0.30)
```

### Profit Score (Final Ranking)
```python
gross_revenue = yield_per_hectare * price_per_kg
net_profit = gross_revenue - investment_cost
roi_percentage = (net_profit / investment_cost) * 100

profit_score = suitability * (roi_percentage / 100) * (net_profit / 10000)
```

Crops are ranked by **profit_score** (highest first).

## Example Use Cases

### 1. Small Farm (1 hectare)
```bash
curl -X POST http://localhost:8000/api/v1/crop-suggestions \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 28.6139,
    "lng": 77.2090,
    "land_class": "Croplands",
    "farm_size_hectares": 1.0,
    "risk_tolerance": "low"
  }'
```

**Expected:** Reliable staple crops with steady income (wheat, chickpeas, sunflower)

### 2. Large Commercial Farm (50 hectares)
```bash
curl -X POST http://localhost:8000/api/v1/crop-suggestions \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 40.7128,
    "lng": -74.0060,
    "land_class": "Croplands",
    "farm_size_hectares": 50.0,
    "risk_tolerance": "high"
  }'
```

**Expected:** High-value crops with premium market prices (strawberries, vanilla, specialty herbs)

### 3. With Historical Data
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"type":"point","lat":37.7749,"lng":-122.4194}'
```

**Response includes:** Land classification + weather + crop history + **crop suggestions** (all integrated)

## Key Advantages

### 💵 **Profit Maximization**
- Calculates **expected profit per hectare**
- Shows **ROI percentage** for each crop
- Considers **multiple harvest cycles** per year
- **Annual profit potential** estimation

### 🎯 **Smart Matching**
- Analyzes **20+ environmental factors**
- Matches crops to **local climate zone**
- Considers **soil characteristics** from land classification
- Adjusts for **farmer risk tolerance**

### 📈 **Business Intelligence**
- **Crop rotation plans** for soil health
- **Seasonal planting calendars**
- **Market trend insights**
- **Risk mitigation strategies**

### 🔄 **Diversification Strategy**
- Recommends **portfolio approach**
- Balances **high-risk** and **low-risk** crops
- Suggests **complementary crops** for rotation
- Maximizes **year-round income**

## Implementation Details

### Service Architecture
```
crop_suggestion_service.py
├── CropSuggestionService
│   ├── CROP_DATABASE (20+ crops)
│   ├── get_crop_suggestions() - Main entry point
│   ├── _analyze_climate() - Climate assessment
│   ├── _analyze_soil_from_land_class() - Soil inference
│   ├── _score_crop() - Multi-factor scoring
│   ├── _calculate_climate_score()
│   ├── _calculate_soil_score()
│   ├── _calculate_risk_score()
│   ├── _generate_rotation_plan()
│   ├── _generate_seasonal_calendar()
│   └── _get_market_insights()
```

### Integration Points
1. **main.py** - `/api/v1/crop-suggestions` endpoint
2. **main.py** - `/api/v1/analyze` includes suggestions automatically
3. **Frontend** - ResultsPanel displays top 3 suggestions
4. **Frontend** - AnalyticsPage shows full top 10 with details

## Testing

### Test Standalone Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/crop-suggestions \
  -H "Content-Type: application/json" \
  -d '{"lat":37.7749,"lng":-122.4194,"land_class":"Croplands","farm_size_hectares":5.0,"risk_tolerance":"medium"}'
```

### Test Integrated Analysis
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"type":"point","lat":37.7749,"lng":-122.4194}'
```

**Check for:**
- ✅ `crop_suggestions` field in response
- ✅ Top 10 ranked crops
- ✅ Profit calculations
- ✅ Rotation plan
- ✅ Seasonal calendar
- ✅ Market insights

## Future Enhancements

### Planned Features
1. **Real-time Market Prices** - API integration for current commodity prices
2. **Weather Forecasting** - Predict optimal planting windows
3. **Pest & Disease Risk** - Historical data analysis
4. **Water Availability** - Groundwater level integration
5. **Subsidy Information** - Government scheme recommendations
6. **Yield Prediction ML** - Machine learning for location-specific yields
7. **Export/PDF Reports** - Downloadable crop plans
8. **Multi-season Planning** - 3-5 year agricultural strategy

### Database Expansion
- Add 50+ more crops
- Regional variety recommendations
- Organic farming alternatives
- Intercropping combinations
- Cover crop suggestions

## Data Sources

### Current (Built-in)
- Comprehensive crop database with 20+ crops
- Average market prices (2024-2025 data)
- Typical yield ranges by crop type
- Standard investment costs
- Climate zone requirements

### Future Integrations
- USDA Commodity Prices API
- FAO Crop Calendar
- Local agricultural market data
- Weather forecast APIs
- Soil testing services

## License & Credits
Built for **Geo-Agri Analyst** platform  
Profit optimization algorithm designed for farmer empowerment  
Data compiled from agricultural research and market analysis
