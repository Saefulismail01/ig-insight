# 🎨 Architecture Diagrams

## 📊 Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Instagram Dashboard                      │
│                       (Flask App)                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      app/__init__.py                        │
│                   (Application Factory)                     │
│  • Creates Flask app                                        │
│  • Registers blueprints                                     │
│  • Configures settings                                      │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Routes     │      │   Services   │      │    Utils     │
│ (Blueprints) │◄────►│ (Business    │◄────►│  (Helpers)   │
│              │      │   Logic)     │      │              │
└──────────────┘      └──────────────┘      └──────────────┘
```

## 🔄 Request Flow

```
User Request
     │
     ▼
┌─────────────┐
│  Browser    │
└─────────────┘
     │
     │ HTTP Request
     ▼
┌─────────────────────────────────────┐
│         Flask Application           │
│         (app/__init__.py)          │
└─────────────────────────────────────┘
     │
     │ Route to Blueprint
     ▼
┌─────────────────────────────────────┐
│        Routes (Blueprints)          │
│  • upload_bp   • data_bp           │
│  • analysis_bp • ai_bp             │
└─────────────────────────────────────┘
     │
     │ Call Service
     ▼
┌─────────────────────────────────────┐
│           Services                  │
│  • DataProcessor                   │
│  • QualityAnalyzer                 │
│  • OutlierAnalyzer                 │
│  • InsightsGenerator               │
└─────────────────────────────────────┘
     │
     │ Use Utils
     ▼
┌─────────────────────────────────────┐
│            Utils                    │
│  • Serializer                      │
│  • Validators                      │
└─────────────────────────────────────┘
     │
     │ Return Data
     ▼
┌─────────────────────────────────────┐
│         JSON Response               │
└─────────────────────────────────────┘
     │
     │ HTTP Response
     ▼
┌─────────────┐
│  Browser    │
└─────────────┘
```

## 📁 Directory Structure (Visual)

```
workspace/
│
├── 📱 app/                          Main Application Package
│   │
│   ├── 🏗️ __init__.py              App Factory (creates Flask app)
│   ├── ⚙️ config.py                Configuration (Dev/Prod settings)
│   │
│   ├── 🛣️ routes/                  HTTP Request Handlers
│   │   ├── __init__.py
│   │   ├── 📤 upload.py           Upload & process CSV
│   │   ├── 📊 data.py             Get processed data
│   │   ├── 🔍 analysis.py         Analysis endpoints
│   │   └── 🤖 ai.py               AI chat integration
│   │
│   ├── 🧠 services/                Business Logic Layer
│   │   ├── __init__.py
│   │   ├── ⚙️ data_processor.py   Core data processing
│   │   ├── 📈 quality_analyzer.py Quality analysis
│   │   ├── 🎯 outlier_analyzer.py Outlier detection
│   │   └── 💡 insights_generator.py Generate insights
│   │
│   └── 🔧 utils/                   Helper Functions
│       ├── __init__.py
│       ├── 🔄 serializer.py       Data serialization
│       └── ✅ validators.py       Input validation
│
├── 🎨 templates/                    HTML Templates
│   └── index_dynamic.html
│
├── 📁 uploads/                      File Upload Directory
│   └── .gitkeep
│
├── 🚀 app.py                        Entry Point
├── 📋 requirements.txt              Dependencies
├── 🔐 .env                          Environment Variables
├── 📝 .env.example                  Env Template
├── 🚫 .gitignore                    Git Ignore Rules
│
└── 📚 Documentation/
    ├── README.md                    Quick Start
    ├── STRUCTURE.md                 Architecture Guide
    ├── MIGRATION.md                 Migration Help
    └── REFACTORING_SUMMARY.md       Summary
```

## 🔗 Component Relationships

```
┌───────────────────────────────────────────────────────────┐
│                        Routes                             │
│  ┌─────────┐  ┌──────┐  ┌──────────┐  ┌──────────┐    │
│  │ Upload  │  │ Data │  │ Analysis │  │   AI     │    │
│  └────┬────┘  └───┬──┘  └────┬─────┘  └────┬─────┘    │
└───────┼───────────┼──────────┼─────────────┼───────────┘
        │           │          │             │
        │           │          │             │
┌───────┼───────────┼──────────┼─────────────┼───────────┐
│       │           │          │             │           │
│       ▼           │          ▼             │           │
│  ┌──────────┐    │   ┌──────────────┐    │           │
│  │   Data   │◄───┼───│   Quality    │    │           │
│  │ Processor│    │   │   Analyzer   │    │           │
│  └─────┬────┘    │   └──────────────┘    │           │
│        │         │          ▲             │           │
│        │         │          │             │           │
│        │         │   ┌──────────────┐    │           │
│        │         └───│   Outlier    │    │           │
│        │             │   Analyzer   │    │           │
│        │             └──────────────┘    │           │
│        │                                 │           │
│        │    ┌──────────────┐            │           │
│        └───►│   Insights   │◄───────────┘           │
│             │  Generator   │                        │
│             └──────────────┘                        │
│                                                     │
│                    Services Layer                  │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                     Utils                           │
│  ┌──────────────┐        ┌──────────────┐         │
│  │  Serializer  │        │  Validators  │         │
│  └──────────────┘        └──────────────┘         │
└─────────────────────────────────────────────────────┘
```

## 🔄 Data Processing Flow

```
CSV File Upload
      │
      ▼
┌─────────────┐
│  Validator  │ (validates file type & structure)
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Data Processor  │
│                 │
│ Steps:          │
│ 1. Clean data   │───┐
│ 2. Add features │   │
│ 3. Calculate    │   │
│    metrics      │   │
│ 4. Analyze      │   │
└────────┬────────┘   │
         │            │
         │            │ Uses Utils
         │            │
         ▼            ▼
┌──────────────────────────┐
│  Insights Generator      │
│  • Content strategy      │
│  • Timing optimization   │
│  • Virality analysis     │
│  • Engagement insights   │
└──────────┬───────────────┘
           │
           ▼
    ┌─────────────┐
    │ Serializer  │ (convert to JSON)
    └──────┬──────┘
           │
           ▼
    ┌──────────────┐
    │ JSON Response│
    └──────────────┘
```

## 🎯 Service Dependencies

```
┌────────────────────────────────────────┐
│         DataProcessor                  │
│  • Main processing pipeline            │
│  • Coordinates other services          │
└───────────────┬────────────────────────┘
                │
        ┌───────┴───────┐
        ▼               ▼
┌──────────────┐  ┌──────────────┐
│  Insights    │  │ Serializer   │
│  Generator   │  │   (Utils)    │
└──────────────┘  └──────────────┘

┌────────────────────────────────────────┐
│      QualityAnalyzer                   │
│  • Independent service                 │
│  • Uses DataFrame directly             │
└───────────────┬────────────────────────┘
                │
                ▼
         ┌──────────────┐
         │ Serializer   │
         │   (Utils)    │
         └──────────────┘

┌────────────────────────────────────────┐
│      OutlierAnalyzer                   │
│  • Independent service                 │
│  • Specialized analysis                │
└───────────────┬────────────────────────┘
                │
                ▼
         ┌──────────────┐
         │ Serializer   │
         │   (Utils)    │
         └──────────────┘
```

## 📊 Blueprint Registration Flow

```
app.py (Entry Point)
      │
      │ imports
      ▼
┌─────────────────┐
│ create_app()    │
│ (app/__init__) │
└────────┬────────┘
         │
         │ Registers Blueprints:
         │
         ├──► upload_bp     (app/routes/upload.py)
         ├──► data_bp       (app/routes/data.py)
         ├──► analysis_bp   (app/routes/analysis.py)
         └──► ai_bp         (app/routes/ai.py)
         │
         ▼
┌─────────────────┐
│  Flask App      │
│  (with all      │
│   endpoints)    │
└─────────────────┘
```

## 🔐 Configuration Flow

```
.env file
    │
    │ loaded by
    ▼
┌──────────────┐
│ load_dotenv()│
└──────┬───────┘
       │
       ▼
┌──────────────────────────┐
│   app/config.py          │
│                          │
│   Config (Base)          │
│   ├─ DevelopmentConfig   │
│   └─ ProductionConfig    │
└──────────┬───────────────┘
           │
           │ used by
           ▼
    ┌─────────────┐
    │ create_app()│
    └─────────────┘
```

## 📱 User Interaction Flow

```
User Action: Upload CSV
         │
         ▼
┌─────────────────┐
│  Frontend JS    │
└────────┬────────┘
         │
         │ POST /upload
         ▼
┌─────────────────┐
│  upload_bp      │ (routes/upload.py)
└────────┬────────┘
         │
         │ validate & process
         ▼
┌─────────────────┐
│ DataProcessor   │ (services/data_processor.py)
└────────┬────────┘
         │
         │ store in memory
         ▼
┌─────────────────┐
│ processed_data  │ (global variable)
└────────┬────────┘
         │
         │ return JSON
         ▼
┌─────────────────┐
│  Frontend JS    │
└────────┬────────┘
         │
         │ display dashboard
         ▼
┌─────────────────┐
│  User sees      │
│  visualizations │
└─────────────────┘
```

## 🎓 Design Pattern: Factory Pattern

```
┌─────────────────────────────────────┐
│     Application Factory Pattern     │
└─────────────────────────────────────┘

Instead of:
───────────
app = Flask(__name__)
app.config['DEBUG'] = True
# ... direct configuration


Using Factory:
──────────────
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # ... setup
    return app

Benefits:
✅ Multiple instances
✅ Easy testing
✅ Flexible configuration
✅ Clean separation
```

## 📦 Module Import Flow

```
app.py
  │
  └─► from app import create_app
         │
         └─► app/__init__.py
                │
                ├─► from .config import config
                │     │
                │     └─► app/config.py
                │
                ├─► from .routes import (all blueprints)
                │     │
                │     └─► app/routes/__init__.py
                │            │
                │            ├─► upload_bp
                │            ├─► data_bp
                │            ├─► analysis_bp
                │            └─► ai_bp
                │
                └─► registers all blueprints
```

---

**Visual Guides Status**: ✅ Complete

These diagrams help understand:
- 🏗️ Overall architecture
- 🔄 Data flow
- 📁 File organization
- 🔗 Component relationships
- 🎯 Design patterns used
