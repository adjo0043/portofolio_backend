import os
import django
import sys

print("Starting admin creation script...")

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
    django.setup()
    print("Django setup complete.")

    from django.contrib.auth import get_user_model
    User = get_user_model()
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin'

    if not User.objects.filter(username=username).exists():
        print(f"Creating user {username}...")
        User.objects.create_superuser(username, email, password)
        print("Superuser created successfully.")
    else:
        print(f"User {username} already exists. Updating password...")
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        print("Superuser password updated.")

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
