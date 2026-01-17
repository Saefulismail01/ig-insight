# 📊 Instagram Meta Insight Dashboard 🚀

Dashboard web interaktif untuk menganalisis data Instagram Meta Insight dari file CSV. ✨

## ✨ Fitur

- 📊 **Visualisasi Data Interaktif**: Grafik batang, garis, dan heatmap untuk analisis performa 📈
- 📁 **Upload CSV**: Mudah upload file CSV Instagram Insight 💾
- 📱 **Responsive Design**: Tampilan optimal di desktop dan mobile 💻📲
- 📈 **Analisis Real-time**: Statistik deskriptif dan korelasi metrik 🔍
- 🎨 **Modern UI**: Desain bersih dengan Tailwind CSS ✨

## 🏗️ Struktur Proyek

Proyek ini menggunakan **modular architecture** dengan separation of concerns:

```
app/
├── routes/          # API endpoints (Blueprints)
├── services/        # Business logic
├── utils/           # Helper functions
└── config.py        # Configuration
```

📖 **Lihat [STRUCTURE.md](STRUCTURE.md) untuk dokumentasi lengkap!**

## 🛠️ Instalasi

1. Install dependencies: 📦
```bash
pip install -r requirements.txt
```

2. Setup environment variables: 🔐
```bash
cp .env.example .env
# Edit .env file dengan API keys Anda
```

3. Jalankan aplikasi: ▶️
```bash
python app.py
```

4. Buka browser dan akses: 🌐
```
http://localhost:5000
```

## 📖 Cara Penggunaan

1. 🌐 Buka dashboard di browser
2. 📤 Upload file CSV Instagram Insight
3. 👀 Lihat analisis dan visualisasi data secara otomatis

## 📋 Struktur CSV yang Didukung

Dashboard mendukung file CSV Instagram Insight dengan kolom:
- 🆔 Post ID
- 👤 Account ID
- 📛 Account username
- ✍️ Account name
- 📝 Description
- ⏱️ Duration (sec)
- 📅 Publish time
- 🔗 Permalink
- 📷 Post type
- 👁️ Views
- 📡 Reach
- ❤️ Likes
- 🔄 Shares
- ➕ Follows
- 💬 Comments
- 🔖 Saves

## 🚀 Teknologi

- **Backend**: Flask (Python) 🐍
- **Frontend**: HTML5, Tailwind CSS, Chart.js 🎨
- **Data Processing**: Pandas 🐼
- **Icons**: Lucide Icons 🎯
