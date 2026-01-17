# 🔄 Migration Guide

## From Monolithic to Modular Structure

### ⚠️ Breaking Changes

File `app_flask.py` telah di-refactor menjadi struktur modular. File lama telah di-backup sebagai `app_flask.py.backup`.

### 📋 What Changed

#### Before (Monolithic):
```
app_flask.py (1000+ lines)
```

#### After (Modular):
```
app/
├── __init__.py           # App factory
├── config.py             # Configuration
├── routes/               # 4 route files
├── services/             # 4 service files
└── utils/                # 2 utility files

app.py                    # New entry point
```

### 🚀 How to Migrate

#### 1. Update Import Statements

**Old way:**
```bash
python app_flask.py
```

**New way:**
```bash
python app.py
```

#### 2. Environment Variables

Create `.env` file from template:
```bash
cp .env.example .env
```

Edit `.env` with your values:
```env
GROQ_API_KEY=your-actual-api-key
GROQ_MODEL=mixtral-8x7b-32768
```

#### 3. No Code Changes Required

Jika Anda hanya menggunakan aplikasi (tidak modify code), tidak ada perubahan yang diperlukan!

### 🔧 For Developers

#### Adding New Routes

**Old way** (dalam `app_flask.py`):
```python
@app.route('/new-endpoint')
def new_endpoint():
    # logic here
```

**New way** (dalam `app/routes/`):
```python
# app/routes/my_routes.py
from flask import Blueprint

my_bp = Blueprint('my_routes', __name__)

@my_bp.route('/new-endpoint')
def new_endpoint():
    # logic here
```

Register blueprint di `app/__init__.py`:
```python
from .routes.my_routes import my_bp
app.register_blueprint(my_bp)
```

#### Adding New Business Logic

**Old way**: All logic di `app_flask.py`

**New way**: Create service di `app/services/`:
```python
# app/services/my_service.py
class MyService:
    def do_something(self, data):
        # business logic here
        return result
```

Use in routes:
```python
from ..services.my_service import MyService

service = MyService()
result = service.do_something(data)
```

### 📊 Function Mapping

Berikut mapping dari old functions ke new locations:

| Old Location (app_flask.py) | New Location | Notes |
|------------------------------|--------------|-------|
| `serialize_data()` | `app/utils/serializer.py` | Utility function |
| `process_insight_data()` | `app/services/data_processor.py` | Main processing |
| `generate_advanced_insights()` | `app/services/insights_generator.py` | Insights generation |
| `calculate_content_quality_score()` | `app/services/quality_analyzer.py` | Quality analysis |
| `perform_quality_analysis()` | `app/services/quality_analyzer.py` | Quality analysis |
| `perform_outlier_analysis()` | `app/services/outlier_analyzer.py` | Outlier detection |
| `@app.route('/upload')` | `app/routes/upload.py` | Upload route |
| `@app.route('/data')` | `app/routes/data.py` | Data route |
| `@app.route('/quality-analysis')` | `app/routes/analysis.py` | Analysis routes |
| `@app.route('/outlier-analysis')` | `app/routes/analysis.py` | Analysis routes |
| `@app.route('/follower-trend')` | `app/routes/analysis.py` | Analysis routes |
| `@app.route('/content-type-analysis')` | `app/routes/analysis.py` | Analysis routes |
| `@app.route('/ai-chat')` | `app/routes/ai.py` | AI chat route |

### ✅ Testing Migration

1. **Backup your uploads** (if any):
```bash
cp -r uploads uploads_backup
```

2. **Test the new application**:
```bash
python app.py
```

3. **Verify all endpoints work**:
- Upload a CSV file
- Check data visualization
- Test quality analysis
- Test outlier analysis
- Test AI chat (if configured)

4. **If issues occur**:
```bash
# Rollback to old version
mv app_flask.py.backup app_flask.py
python app_flask.py
```

### 🐛 Common Issues

#### Issue: "Module not found"
**Solution**: Make sure you're running from project root:
```bash
cd /projects/workspace
python app.py
```

#### Issue: "GROQ_API_KEY not found"
**Solution**: Create `.env` file with your API key:
```bash
echo "GROQ_API_KEY=your-key-here" >> .env
```

#### Issue: "Template not found"
**Solution**: Templates are in `templates/` folder, ensure it exists.

### 📝 Benefits of New Structure

1. ✅ **Better Organization**: Easy to find specific functionality
2. ✅ **Easier Testing**: Each component can be tested independently
3. ✅ **Better Collaboration**: Multiple developers can work on different parts
4. ✅ **Scalability**: Easy to add new features without bloating files
5. ✅ **Maintainability**: Bug fixes are easier to locate and implement
6. ✅ **Reusability**: Services and utils can be reused across routes

### 🔄 Rollback Plan

If you need to rollback:

```bash
# Stop new app
# Ctrl+C

# Restore old file
mv app_flask.py.backup app_flask.py

# Run old app
python app_flask.py
```

### 📞 Support

Jika ada masalah saat migrasi, check:
1. `STRUCTURE.md` - Detailed documentation
2. `README.md` - Basic setup guide
3. Console logs - Error messages

### 🎯 Next Steps

1. ✅ Review new structure in `STRUCTURE.md`
2. ✅ Test all features
3. ✅ Update any custom code
4. ✅ Deploy with confidence!

---

**Note**: File `app_flask.py.backup` akan tetap ada sebagai reference. Anda bisa menghapusnya setelah yakin migrasi berhasil.
