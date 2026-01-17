# 🚀 Quick Reference Card

## 📝 File Quick Access

### 📚 Documentation Files
| File | What's Inside | When to Read |
|------|---------------|--------------|
| `README.md` | Project overview, quick start | ⭐ Start here! |
| `STRUCTURE.md` | Architecture details | When developing |
| `MIGRATION.md` | Old → New guide | When migrating |
| `DIAGRAMS.md` | Visual architecture | Understanding flow |
| `REFACTORING_SUMMARY.md` | What changed | Overview of refactor |
| `.env.example` | Environment template | Setup project |

### 🏗️ Application Files
| Location | Purpose | Main Responsibility |
|----------|---------|---------------------|
| `app.py` | Entry point | Start application |
| `app/__init__.py` | App factory | Create Flask app |
| `app/config.py` | Configuration | Settings management |
| `app/routes/` | Endpoints | Handle HTTP requests |
| `app/services/` | Business logic | Data processing |
| `app/utils/` | Helpers | Utility functions |

---

## 🎯 Common Tasks

### 🚀 Start the Application
```bash
python app.py
```

### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### ⚙️ Configure Environment
```bash
cp .env.example .env
nano .env  # Edit your settings
```

### 🔍 Check Structure
```bash
tree app/  # Or: ls -R app/
```

---

## 📁 Directory Cheat Sheet

```
app/
├── routes/              # "What endpoint?"
│   ├── upload.py       # POST /upload
│   ├── data.py         # GET /data
│   ├── analysis.py     # GET /quality-analysis, /outlier-analysis, etc
│   └── ai.py           # POST /ai-chat
│
├── services/            # "What logic?"
│   ├── data_processor.py      # Main processing
│   ├── quality_analyzer.py    # Quality analysis
│   ├── outlier_analyzer.py    # Top/Bottom analysis
│   └── insights_generator.py  # Generate insights
│
└── utils/               # "What helper?"
    ├── serializer.py   # JSON conversion
    └── validators.py   # Input validation
```

---

## 🔗 API Endpoints Quick Reference

| Endpoint | Method | Purpose | Returns |
|----------|--------|---------|---------|
| `/` | GET | Homepage | HTML |
| `/upload` | POST | Upload CSV | Processed data |
| `/data` | GET | Get data | JSON data |
| `/quality-analysis` | GET | Quality metrics | Quality data |
| `/outlier-analysis` | GET | Top/Bottom 5 | Outlier data |
| `/follower-trend` | GET | Follower growth | Trend data |
| `/content-type-analysis` | GET | Content types | Type analysis |
| `/ai-chat` | POST | AI assistant | AI response |

---

## 🎨 Code Patterns

### Adding New Route
```python
# 1. Create file: app/routes/my_feature.py
from flask import Blueprint, jsonify

my_bp = Blueprint('my_feature', __name__)

@my_bp.route('/my-endpoint')
def my_endpoint():
    return jsonify({'status': 'ok'})

# 2. Register in app/__init__.py
from .routes.my_feature import my_bp
app.register_blueprint(my_bp)
```

### Adding New Service
```python
# 1. Create file: app/services/my_service.py
class MyService:
    def analyze(self, data):
        # Your logic here
        return result

# 2. Use in route:
from ..services.my_service import MyService

service = MyService()
result = service.analyze(data)
```

### Adding New Utility
```python
# 1. Create file: app/utils/my_util.py
def my_helper(data):
    # Helper logic
    return processed_data

# 2. Use anywhere:
from app.utils.my_util import my_helper

result = my_helper(input_data)
```

---

## 🔧 Environment Variables

```env
# Flask
FLASK_ENV=development        # or 'production'
DEBUG=True                   # False in production
SECRET_KEY=your-secret-key
HOST=0.0.0.0
PORT=5000

# Groq AI
GROQ_API_KEY=your-api-key
GROQ_MODEL=mixtral-8x7b-32768
```

---

## 📊 Data Flow Cheat Sheet

```
User → Route → Service → Utils → Response
 │      │        │         │        │
 │      │        │         │        └─ JSON data
 │      │        │         └─────────── Helpers
 │      │        └───────────────────── Processing
 │      └────────────────────────────── HTTP handler
 └───────────────────────────────────── Request
```

---

## 🐛 Debugging Tips

### Check if app is running
```bash
curl http://localhost:5000/
```

### Test specific endpoint
```bash
curl http://localhost:5000/data
```

### View logs
```bash
# Run app with
python app.py
# Watch terminal output
```

### Check imports
```python
# In Python shell:
from app import create_app
app = create_app()
print(app.url_map)  # Shows all routes
```

---

## 📦 Import Patterns

### In Routes (from `app/routes/`)
```python
from flask import Blueprint, jsonify, request
from ..services import DataProcessor, QualityAnalyzer
from ..utils import serialize_data, validate_csv_columns
from ..config import Config
```

### In Services (from `app/services/`)
```python
import pandas as pd
from ..utils import serialize_data
```

### In Main App (from `app.py`)
```python
from app import create_app
from app.config import Config
```

---

## 🎯 Module Responsibilities

| Module | Input | Output | Side Effects |
|--------|-------|--------|--------------|
| **Routes** | HTTP Request | HTTP Response | None |
| **Services** | Data/DataFrame | Processed data | May store in memory |
| **Utils** | Any data | Transformed data | None |
| **Config** | Environment vars | Config object | None |

---

## 🔑 Key Files Content

### `app.py` (Entry Point)
```python
from app import create_app
app = create_app()
if __name__ == '__main__':
    app.run()
```

### `app/__init__.py` (Factory)
```python
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Register blueprints
    return app
```

### `app/config.py` (Settings)
```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    # ... other settings
```

---

## 💡 Best Practices

### DO ✅
- Keep routes thin (only HTTP)
- Put logic in services
- Use utils for reusable code
- Follow existing patterns
- Document new features

### DON'T ❌
- Mix HTTP and business logic
- Duplicate code
- Hardcode values
- Skip validation
- Ignore errors

---

## 🚨 Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Wrong directory | Run from project root |
| `Template not found` | Missing folder | Check `templates/` exists |
| `GROQ_API_KEY not set` | Missing env var | Create `.env` file |
| `Port already in use` | App running | Stop old process or change port |
| `Import error` | Circular import | Check import order |

---

## 📞 Getting Help

1. Check error message in terminal
2. Review relevant documentation:
   - Routes issue → See `app/routes/`
   - Logic issue → See `app/services/`
   - Config issue → Check `app/config.py`
3. Check documentation files
4. Review similar working code

---

## 🎓 Learning Path

### Beginner
1. Read `README.md`
2. Run the app
3. Explore routes
4. Check one service

### Intermediate
1. Read `STRUCTURE.md`
2. Understand data flow
3. Modify existing feature
4. Add simple endpoint

### Advanced
1. Read `DIAGRAMS.md`
2. Create new service
3. Implement complex feature
4. Refactor existing code

---

## ⚡ Performance Tips

```python
# Cache results
@lru_cache(maxsize=128)
def expensive_function(data):
    pass

# Use generators for large data
def process_data():
    for item in large_dataset:
        yield transform(item)

# Batch operations
df.apply(lambda x: process(x))  # Vectorized
```

---

## 🔒 Security Checklist

- ✅ Use environment variables for secrets
- ✅ Validate all inputs
- ✅ Sanitize file uploads
- ✅ Set SECRET_KEY in production
- ✅ Turn off DEBUG in production
- ✅ Use HTTPS in production

---

## 📝 Git Commands

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Add new feature"

# Push
git push origin main
```

---

**Quick Reference**: ✅ Ready to use!

Keep this card handy for daily development 🚀
