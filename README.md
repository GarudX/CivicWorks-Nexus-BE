# Map Rendering API

FastAPI service for extracting location information from PDF maps using OpenAI Vision API.

## Features

- 🗺️ **PDF Map Processing**: Extract location names and linear feet measurements from map PDFs
- 📍 **Address Matching**: Match locations with addresses from routing PDFs using fuzzy matching
- 🔗 **Google Maps Integration**: Generate Google Maps links for each location
- 🔒 **API Key Authentication**: Secure endpoints with X-API-Key header authentication
- 📝 **Comprehensive Logging**: Request/response logging with file and console output
- 🏗️ **Clean Architecture**: Route-Controller-Service-Repository pattern
- 💰 **Development Mode**: Use hardcoded data to save API costs during development

## Architecture

```
map-rendering-api/
├── config/              # Configuration and settings
│   ├── settings.py      # Pydantic settings with .env support
│   └── __init__.py
├── middleware/          # Custom middleware
│   ├── auth.py          # API key authentication
│   ├── logging.py       # Request/response logging
│   └── __init__.py
├── models/              # Pydantic models and schemas
│   ├── schemas.py       # Request/response models
│   └── __init__.py
├── repositories/        # Data access layer
│   ├── location_repository.py  # Hardcoded dev data
│   └── __init__.py
├── services/            # Business logic layer
│   ├── pdf_service.py          # PDF to image conversion
│   ├── openai_service.py       # OpenAI API integration
│   ├── location_service.py     # Location processing logic
│   └── __init__.py
├── controllers/         # Request handling layer
│   ├── location_controller.py  # Location endpoint controller
│   └── __init__.py
├── routes/              # API routes
│   ├── location_routes.py      # Location endpoints
│   ├── health_routes.py        # Health check endpoint
│   └── __init__.py
├── utils/               # Utility functions
│   ├── logger.py        # Logging configuration
│   └── __init__.py
├── logs/                # Log files (auto-created)
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .env.example         # Example environment variables
└── README.md            # This file
```

## Installation

1. **Clone the repository** (if not already done)

2. **Navigate to the project directory**
   ```bash
   cd map-rendering-api
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set your values:
   - `OPENAI_API_KEY`: Your OpenAI API key (required for production mode)
   - `ENVIRONMENT`: `development` or `production`
   - `API_KEY`: Your custom API key for authentication
   - `MODEL`: OpenAI model to use (default: `gpt-4o-mini`)

## Usage

### Start the server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 1. Health Check
```bash
GET /health
```

No authentication required. Returns API status and environment info.

**Response:**
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0"
}
```

#### 2. Extract Locations from PDFs
```bash
POST /api/v1/locations/extract
```

**Headers:**
```
X-API-Key: your-secret-api-key-here
Content-Type: multipart/form-data
```

**Form Data:**
- `map_pdf` (required): PDF file with map and location markers
- `routing_pdf` (optional): PDF file with routing information and addresses
- `zoom` (optional): Render zoom level (2.0-6.0, default: 4.0)
- `max_pages` (optional): Maximum pages to process (1-200, default: 30)

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/locations/extract" \
  -H "X-API-Key: your-secret-api-key-here" \
  -F "map_pdf=@path/to/map.pdf" \
  -F "routing_pdf=@path/to/routing.pdf" \
  -F "zoom=4.0" \
  -F "max_pages=30"
```

**Example using Python requests:**
```python
import requests

url = "http://localhost:8000/api/v1/locations/extract"
headers = {"X-API-Key": "your-secret-api-key-here"}

files = {
    "map_pdf": open("map.pdf", "rb"),
    "routing_pdf": open("routing.pdf", "rb")
}

data = {
    "zoom": 4.0,
    "max_pages": 30
}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.json())
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully extracted 10 locations",
  "locations": [
    {
      "page": 1,
      "location_name": "Bay Village Garden",
      "full_address": "32 Melrose St, Boston, MA 02116, USA",
      "linear_feet": 84.8,
      "maps_url": "https://www.google.com/maps/dir/?api=1&destination=..."
    }
  ],
  "total_locations": 10
}
```

## Environment Modes

### Development Mode
Set `ENVIRONMENT=development` in `.env`

- Uses hardcoded location and address data
- No OpenAI API calls (saves costs)
- Instant responses
- Perfect for testing and development

### Production Mode
Set `ENVIRONMENT=production` in `.env`

- Processes actual PDF files
- Uses OpenAI Vision API to extract data
- Requires valid `OPENAI_API_KEY`
- Real-time extraction from uploaded PDFs

## Authentication

All endpoints except `/health`, `/docs`, and `/redoc` require authentication using the `X-API-Key` header.

Set your API key in `.env`:
```
API_KEY=your-secret-api-key-here
```

Include it in requests:
```
X-API-Key: your-secret-api-key-here
```

## Logging

Logs are written to both console and file:
- **Console**: All log levels (DEBUG and above)
- **File**: `logs/app.log` (INFO and above)
- **Rotation**: 10MB max file size, 5 backup files

Configure logging in `.env`:
```
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid file type, missing parameters)
- `401`: Unauthorized (missing API key)
- `403`: Forbidden (invalid API key)
- `500`: Internal server error

Error response format:
```json
{
  "detail": "Error message here",
  "error_type": "ErrorType"
}
```

## Development

### Project Structure Pattern

This project follows the **Route-Controller-Service-Repository** pattern:

1. **Routes** (`routes/`): Define API endpoints and request/response handling
2. **Controllers** (`controllers/`): Handle HTTP requests, validate input, call services
3. **Services** (`services/`): Contain business logic and orchestrate operations
4. **Repositories** (`repositories/`): Handle data access (currently hardcoded data)

### Adding New Endpoints

1. Create a new route in `routes/`
2. Create a controller in `controllers/`
3. Add business logic in `services/`
4. Define models in `models/schemas.py`

## Dependencies

- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **PyMuPDF**: PDF processing
- **Pillow**: Image processing
- **OpenAI**: OpenAI API client
- **python-dotenv**: Environment variable management

## License

MIT License

## Support

For issues or questions, please contact the development team.
