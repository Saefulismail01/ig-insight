#!/usr/bin/env python3
"""
Script untuk generate SECRET_KEY untuk Flask
"""

import secrets

def generate_secret_key():
    """Generate a secure random secret key"""
    return secrets.token_hex(32)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("=" * 60)
    print("🔑 SECRET KEY GENERATED")
    print("=" * 60)
    print(f"\n{secret_key}\n")
    print("=" * 60)
    print("📝 Copy secret key di atas dan paste ke file .env")
    print("   Ganti value SECRET_KEY dengan key yang baru generated")
    print("=" * 60)
