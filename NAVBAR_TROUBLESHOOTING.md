# 🔧 NAVBAR TROUBLESHOOTING GUIDE

## Masalah: Navbar masih menampilkan menu horizontal

### Solusi Quick Fix:

1. **Clear Browser Cache**
   - Tekan `Ctrl + Shift + Delete` (Chrome/Edge)
   - Atau `Ctrl + F5` untuk hard reload
   - Atau buka DevTools (F12) → Network tab → check "Disable cache"

2. **Verifikasi CSS Loading**
   Buka browser DevTools (F12) dan cek:
   ```
   Console → pastikan tidak ada error CSS
   Network → pastikan navbar.css?v=4.0 ter-load
   ```

3. **Test Navbar Secara Terpisah**
   Akses: `http://localhost:5000/templates/navbar_test.html`
   (atau sesuai port yang digunakan)

4. **Cek Console untuk Error**
   ```javascript
   // Buka Console (F12) dan ketik:
   console.log(window.navBar);
   // Harus menampilkan object NavigationBar
   ```

5. **Manual Toggle Test**
   Di Console, coba:
   ```javascript
   navBar.open()  // Harus buka dropdown
   navBar.close() // Harus tutup dropdown
   ```

### Verifikasi Visual:

✅ **Yang Benar:**
```
┌─────────────────────────────────────┐
│ Instagram Analysis ▼                │  ← Baris 1: Judul + chevron
│ Date Range: 1 Jan 2024 – 31 Jan... │  ← Baris 2: Date range
└─────────────────────────────────────┘

Saat diklik chevron ▼:
┌─────────────────────────────┐
│ 🎯 KPI Overview            │
│ 📊 Engagement              │
│ 📱 Content Types           │
│ ⭐ Top Performers          │
│ 🏆 Quality Score           │
│ 🏷️ Captions                │
│ ⏱️ Video Duration          │
└─────────────────────────────┘
```

❌ **Yang Salah:**
```
┌──────────────────────────────────────────────────────────────┐
│ 📊 🎯 KPI Overview 📊 Engagement 📱 Content Types ... (semua horizontal)
└──────────────────────────────────────────────────────────────┘
```

### Debug Checklist:

- [ ] Browser cache sudah di-clear
- [ ] navbar.css?v=4.0 ter-load (cek di Network tab)
- [ ] navbar.js?v=4.0 ter-load (cek di Network tab)
- [ ] Tidak ada error di Console
- [ ] Element `.navbar-dropdown` ada di DOM
- [ ] Element `.navbar-dropdown` memiliki `display: none !important` by default
- [ ] Saat klik chevron, class `show` ditambahkan ke `.navbar-dropdown`

### Inspect Element:

Klik kanan pada navbar → Inspect → pastikan structure-nya seperti ini:

```html
<nav class="analysis-navbar">
  <div class="navbar-content">
    <div class="navbar-header">
      <button class="navbar-trigger">
        <span class="navbar-title-text">Instagram Analysis</span>
        <svg class="chevron-icon">...</svg>
      </button>
      <div class="navbar-date-range">Date Range: ...</div>
    </div>
    
    <!-- INI HARUS HIDDEN BY DEFAULT -->
    <div class="navbar-dropdown" style="display: none;">
      <a class="dropdown-item">...</a>
      ...
    </div>
  </div>
</nav>
```

### Computed Styles:

Inspect `.navbar-dropdown` → Computed tab:
```
display: none           ← PENTING! Harus none by default
opacity: 0
visibility: hidden
```

Saat class `show` ditambahkan:
```
display: flex           ← Berubah jadi flex
opacity: 1
visibility: visible
```

### Force Reload Steps:

1. Stop server (Ctrl+C)
2. Clear browser cache completely
3. Restart server
4. Buka URL dengan `Ctrl + Shift + R` (hard reload)
5. Cek Network tab untuk memastikan v=4.0 ter-load

### Jika Masih Tidak Bekerja:

Tambahkan ini di `<head>` HTML:
```html
<style>
/* Force hide dropdown - ultimate fallback */
.navbar-dropdown {
    display: none !important;
}
.navbar-dropdown.show {
    display: flex !important;
}
</style>
```

### Kontak Jika Error Persists:

Kirim screenshot dari:
1. Browser DevTools → Console (F12)
2. Browser DevTools → Elements → .navbar-dropdown
3. Browser DevTools → Network → navbar.css?v=4.0

---

**Last Updated:** Version 4.0
**File:** NAVBAR_TROUBLESHOOTING.md
