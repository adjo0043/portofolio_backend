#!/usr/bin/env python
"""
Utility script to generate a new Django secret key.
Run this script to generate a secure secret key for your Django project.
"""

from django.core.management.utils import get_random_secret_key

def generate_secret_key():
    """Generate a new Django secret key"""
    return get_random_secret_key()

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Your new Django secret key:")
    print(secret_key)
    print("\nAdd this to your environment variables or .env file:")
    print(f"SECRET_KEY={secret_key}")