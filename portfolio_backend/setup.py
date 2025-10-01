#!/usr/bin/env python
"""
Setup script for Portfolio Backend
Automates the initial setup process
"""

import os
import sys
import subprocess
import secrets


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed")
        print(f"   {e.stderr}")
        return False


def generate_secret_key():
    """Generate a Django secret key"""
    return secrets.token_urlsafe(50)


def create_env_file():
    """Create .env file from .env.example"""
    if os.path.exists('.env'):
        overwrite = input(".env file already exists. Overwrite? (y/N): ")
        if overwrite.lower() != 'y':
            print("Skipping .env creation")
            return
    
    if not os.path.exists('.env.example'):
        print("❌ .env.example not found!")
        return
    
    # Read example file
    with open('.env.example', 'r') as f:
        content = f.read()
    
    # Generate secret key
    secret_key = generate_secret_key()
    content = content.replace('your-secret-key-here-generate-a-strong-one', secret_key)
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(content)
    
    print("✅ .env file created with generated SECRET_KEY")


def main():
    """Main setup process"""
    print_header("Portfolio Backend Setup")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Step 1: Create virtual environment
    print_header("Step 1: Virtual Environment")
    if not os.path.exists('venv'):
        if run_command(f"{sys.executable} -m venv venv", "Creating virtual environment"):
            print("Virtual environment created at ./venv")
            print("\nTo activate it:")
            if os.name == 'nt':  # Windows
                print("  venv\\Scripts\\activate")
            else:  # Unix
                print("  source venv/bin/activate")
        else:
            print("Please install virtualenv and try again")
    else:
        print("Virtual environment already exists")
    
    # Determine pip command
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Step 2: Install dependencies
    print_header("Step 2: Installing Dependencies")
    run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
    run_command(f"{pip_cmd} install -r requirements.txt", "Installing requirements")
    
    # Step 3: Environment configuration
    print_header("Step 3: Environment Configuration")
    create_env_file()
    
    # Step 4: Database setup
    print_header("Step 4: Database Setup")
    run_command(f"{python_cmd} manage.py makemigrations", "Creating migrations")
    run_command(f"{python_cmd} manage.py migrate", "Running migrations")
    
    # Step 5: Create directories
    print_header("Step 5: Creating Directories")
    os.makedirs('media/projects', exist_ok=True)
    os.makedirs('media/projects/thumbnails', exist_ok=True)
    os.makedirs('media/blog', exist_ok=True)
    os.makedirs('staticfiles', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    print("✅ Required directories created")
    
    # Step 6: Collect static files
    print_header("Step 6: Collecting Static Files")
    run_command(f"{python_cmd} manage.py collectstatic --noinput", "Collecting static files")
    
    # Step 7: Create superuser
    print_header("Step 7: Create Superuser")
    print("You can create a superuser now or skip and do it later.")
    create_superuser = input("Create superuser now? (Y/n): ")
    
    if create_superuser.lower() != 'n':
        subprocess.run(f"{python_cmd} manage.py createsuperuser", shell=True)
    
    # Final message
    print_header("Setup Complete! 🎉")
    print("Next steps:")
    print("\n1. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Review .env file and update configuration")
    print("   - Set your email credentials")
    print("   - Configure allowed hosts")
    print("   - Set CORS origins")
    
    print("\n3. Start development server:")
    print("   python manage.py runserver")
    
    print("\n4. Access the application:")
    print("   API: http://localhost:8000/api/")
    print("   Admin: http://localhost:8000/admin/")
    
    print("\n5. For production deployment, see DEPLOYMENT.md")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed: {e}")
        sys.exit(1)
