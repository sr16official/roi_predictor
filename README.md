# Rental ROI Calculator 🏠

A comprehensive web application for calculating Return on Investment (ROI) for rental properties. This tool helps investors make informed decisions by predicting rental income, property values, and calculating investment returns.

## 🚀 Features

- **Property Analysis**: Calculate ROI based on property details like size, location, and amenities
- **Rent Prediction**: AI-powered rental income estimation
- **Price Prediction**: Property value prediction using machine learning models
- **Interactive Dashboard**: Visual charts and comprehensive metrics
- **Location-Based**: Consider proximity to key facilities (metro stations, hospitals, etc.)
- **Indian Market Focus**: Optimized for Indian real estate market with proper number formatting

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python
- **ML Models**: Custom prediction models for rent and price
- **API Endpoints**:
  - `/calculate_roi` - Main ROI calculation endpoint
  - Health checks and static file serving
- **Security**: Optional API key authentication
- **CORS**: Configured for frontend integration

### Frontend (Vanilla JavaScript)
- **Framework**: Pure HTML, CSS, JavaScript
- **Charts**: Interactive visualizations using Chart.js
- **UI**: Responsive design with modern styling
- **Number Formatting**: Indian number format support (lakhs, crores)

## 📁 Project Structure

```
roi/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── roi_service.py       # ML prediction services
│   └── models/              # ML model files
├── frontend/
│   ├── index.html           # Main HTML page
│   ├── app.js              # Frontend JavaScript logic
│   └── style.css           # Styling
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js (optional, for development)
- Docker (recommended for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd roi
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the backend**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Open frontend**
   Open `frontend/index.html` in your browser or serve it with a web server.

### Docker Deployment

1. **Build and run with Docker**
   ```bash
   docker build -t rental-roi .
   docker run -p 8000:8000 rental-roi
   ```

## 📊 API Usage

### Calculate ROI Endpoint

**POST** `/calculate_roi`

**Request Body:**
```json
{
  "size_sq_ft": 1200,
  "propertyType": "2BHK",
  "bedrooms": 2,
  "latitude": 28.6139,
  "longitude": 77.2090,
  "localityName": "Connaught Place",
  "suburbName": "New Delhi",
  "cityName": "Delhi",
  "closest_metro_station_km": 0.5,
  "Aiims_dist_km": 5.2,
  "NDRLW_dist_km": 3.8
}
```

**Response:**
```json
{
  "predicted_rent": 25000,
  "predicted_price": 12000000,
  "annual_rent": 300000,
  "gross_yield_percent": 2.5
}
```

## 🎯 Key Features Explained

### Property Metrics
- **Predicted Rent**: Monthly rental income estimation
- **Predicted Price**: Property valuation prediction
- **Annual Rent**: Yearly rental income
- **Gross Yield**: ROI percentage calculation

### Location Factors
- Distance to metro stations
- Proximity to healthcare facilities (AIIMS)
- Distance to railway stations (NDRLW)
- Locality and suburb analysis

### Visualizations
- **Bar Charts**: Rent vs Price comparisons
- **Pie Charts**: Yield breakdown
- **Responsive Design**: Works on all devices

## 🔧 Configuration

### Environment Variables
- `API_KEY`: Optional API key for authentication
- `PORT`: Server port (default: 8000)

### Model Files
Place your trained ML models in the `backend/models/` directory:
- `rent_model.pkl` - Rental prediction model
- `price_model.pkl` - Price prediction model

## 🚀 Deployment

### Hugging Face Spaces
This project is configured for easy deployment on Hugging Face Spaces:

1. Connect your repository
2. Select Docker SDK
3. Deploy automatically

### Other Platforms
- **Heroku**: Use Docker deployment
- **AWS**: Deploy on ECS or EC2
- **Google Cloud**: Use Cloud Run
- **Azure**: Container Instances

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with FastAPI for robust backend API
- Chart.js for beautiful visualizations
- Optimized for Indian real estate market
- Machine learning models for accurate predictions

## 📞 Support

For support and queries:
- Create an issue in the repository
- Check the documentation
- Review the API endpoints section

---

**Made with ❤️ for real estate investors**
