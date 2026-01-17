# 📁 Project Structure Documentation

## 📂 Struktur Direktori

```
/projects/workspace/
├── 📁 app/                          # Main application package
│   ├── 📄 __init__.py              # Flask app factory
│   ├── 📄 config.py                # Application configuration
│   │
│   ├── 📁 routes/                  # Route handlers (Blueprints)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 upload.py           # File upload & processing routes
│   │   ├── 📄 data.py             # Data retrieval routes
│   │   ├── 📄 analysis.py         # Analysis endpoints
│   │   └── 📄 ai.py               # AI chat routes
│   │
│   ├── 📁 services/                # Business logic layer
│   │   ├── 📄 __init__.py
│   │   ├── 📄 data_processor.py   # Main data processing
│   │   ├── 📄 quality_analyzer.py # Content quality analysis
│   │   ├── 📄 outlier_analyzer.py # Outlier detection
│   │   └── 📄 insights_generator.py # Insight generation
│   │
│   └── 📁 utils/                   # Utility functions
│       ├── 📄 __init__.py
│       ├── 📄 serializer.py       # Data serialization
│       └── 📄 validators.py       # Input validation
│
├── 📁 templates/                    # HTML templates
│   └── 📄 index_dynamic.html
│
├── 📁 uploads/                      # Upload directory
│
├── 📄 app.py                        # Main entry point
├── 📄 app_flask.py                  # Legacy file (deprecated)
├── 📄 .env                          # Environment variables
├── 📄 requirements.txt              # Python dependencies
└── 📄 README.md                     # Project documentation
```

## 🏗️ Architecture Overview

### 1. **Application Factory Pattern** (`app/__init__.py`)
- Menggunakan Flask Application Factory untuk modularitas
- Memudahkan testing dan konfigurasi berbeda (dev/prod)
- Mendaftarkan semua blueprints secara terorganisir

### 2. **Blueprints (Routes)**
Routes dipisah berdasarkan fungsionalitas:

#### `routes/upload.py` 📤
- Upload file CSV
- Validasi file
- Trigger data processing
- Menyimpan processed data dalam memori

#### `routes/data.py` 📊
- Endpoint untuk mengambil data yang sudah diproses
- Simple data retrieval

#### `routes/analysis.py` 🔍
- Quality analysis endpoint
- Outlier analysis endpoint
- Follower trend analysis
- Content type analysis

#### `routes/ai.py` 🤖
- AI chat integration
- Groq API communication
- Context building untuk AI

### 3. **Services (Business Logic)**

#### `services/data_processor.py` ⚙️
**Tanggung Jawab:**
- Data cleaning & preprocessing
- Feature engineering (time features, engagement metrics)
- Statistical calculations
- Aggregations dan grouping
- Koordinasi dengan insights generator

**Methods:**
- `process_insight_data()` - Main processing pipeline
- `_clean_data()` - Data cleaning
- `_add_time_features()` - Add time-based columns
- `_calculate_engagement_metrics()` - Calculate ER, virality, etc
- `_analyze_post_type_performance()` - Group by post type
- `_analyze_time_performance()` - Weekly performance
- Dan methods lainnya...

#### `services/quality_analyzer.py` 📈
**Tanggung Jawab:**
- Content quality scoring
- Percentile-based categorization
- Quality tier distribution
- Deep engagement metrics

**Methods:**
- `calculate_content_quality_score()` - Score calculation
- `perform_quality_analysis()` - Full analysis pipeline

#### `services/outlier_analyzer.py` 🎯
**Tanggung Jawab:**
- Top 5 vs Bottom 5 analysis
- Duration analysis
- Outlier detection

**Methods:**
- `perform_outlier_analysis()` - Main analysis
- `_analyze_duration()` - Video duration analysis
- `_prepare_posts_data()` - Post data preparation

#### `services/insights_generator.py` 💡
**Tanggung Jawab:**
- Generate actionable insights
- Pattern recognition
- Recommendations generation

**Methods:**
- `generate_advanced_insights()` - Main insights generation
- `_generate_content_format_insights()` - Format optimization
- `_generate_timing_insight()` - Best posting times
- `_generate_virality_insight()` - Viral content analysis

### 4. **Utils (Helper Functions)**

#### `utils/serializer.py` 🔄
- Serialize pandas/numpy objects ke JSON
- Handle NaN, inf values
- Type conversion

#### `utils/validators.py` ✅
- Validate CSV columns
- Validate file extensions
- Input validation

### 5. **Configuration** (`app/config.py`)
**Environment-based configuration:**
- `Config` - Base configuration
- `DevelopmentConfig` - Development settings
- `ProductionConfig` - Production settings

**Settings:**
- Flask settings (SECRET_KEY, DEBUG)
- Upload settings (folder, max size)
- Groq AI configuration
- Application settings

## 🔄 Data Flow

```
1. User uploads CSV → routes/upload.py
                    ↓
2. Validation → utils/validators.py
                    ↓
3. Processing → services/data_processor.py
                    ↓
4. Store in memory (global variable)
                    ↓
5. User requests analysis → routes/analysis.py
                    ↓
6. Get stored data → routes/upload.py (get_processed_data)
                    ↓
7. Analyze → services/quality_analyzer.py
         → services/outlier_analyzer.py
                    ↓
8. Return results → JSON response
```

## 🎯 Design Principles

### 1. **Separation of Concerns**
- Routes hanya handle HTTP request/response
- Services contain business logic
- Utils untuk helper functions

### 2. **Single Responsibility**
- Setiap class/function punya 1 tanggung jawab
- Easy to test dan maintain

### 3. **DRY (Don't Repeat Yourself)**
- Reusable components di utils
- Shared logic di base classes

### 4. **Modularity**
- Easy to add new features
- Easy to replace components
- Independent testing

## 🚀 Cara Menjalankan

### Development Mode:
```bash
python app.py
```

### Production Mode:
```bash
export FLASK_ENV=production
python app.py
```

## 📝 Environment Variables

Create `.env` file:
```env
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=mixtral-8x7b-32768
HOST=0.0.0.0
PORT=5000
```

## 🔧 Adding New Features

### Menambah Endpoint Baru:

1. **Create route** di `app/routes/`:
```python
from flask import Blueprint

new_feature_bp = Blueprint('new_feature', __name__)

@new_feature_bp.route('/new-endpoint')
def new_endpoint():
    return jsonify({'message': 'Hello!'})
```

2. **Register blueprint** di `app/__init__.py`:
```python
from .routes import new_feature_bp
app.register_blueprint(new_feature_bp)
```

### Menambah Service Baru:

1. **Create service** di `app/services/`:
```python
class NewAnalyzer:
    def analyze(self, df):
        # Your logic here
        pass
```

2. **Import di `__init__.py`**:
```python
from .new_analyzer import NewAnalyzer
```

3. **Use in routes**:
```python
from ..services import NewAnalyzer

analyzer = NewAnalyzer()
result = analyzer.analyze(df)
```

## 🧪 Testing

Struktur ini memudahkan testing:

```python
# Test services independently
from app.services import DataProcessor

def test_data_processor():
    processor = DataProcessor()
    result = processor.process_insight_data(sample_df)
    assert result is not None
```

## 📊 Benefits of This Structure

✅ **Maintainability**: Easy to find and fix bugs
✅ **Scalability**: Easy to add new features
✅ **Testability**: Each component can be tested independently
✅ **Readability**: Clear organization and naming
✅ **Reusability**: Shared components in utils
✅ **Separation of Concerns**: Clean architecture
✅ **Flexibility**: Easy to swap implementations

## 🔄 Migration dari Old Structure

Old file `app_flask.py` (1000+ lines) sekarang dipecah menjadi:
- Routes: 4 files (~50-150 lines each)
- Services: 4 files (~100-200 lines each)
- Utils: 2 files (~20-50 lines each)
- Config: 1 file (~50 lines)
- Main: 1 file (~20 lines)

**Total: 12 files yang lebih terorganisir vs 1 monolithic file**
