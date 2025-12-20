#!/usr/bin/env bash
# ============================================================================
# Render.com Build Script
# Portfolio Application - Django REST Framework + TypeScript Frontend
# ============================================================================
# This script handles the complete build process for deployment:
#   1. Backend: Python dependencies installation
#   2. Frontend: Node.js dependencies + TypeScript compilation
#   3. Django: Database migrations + Static file collection
# ============================================================================

set -o errexit  # Exit on error
set -o pipefail # Catch errors in pipelines

echo "============================================"
echo "🚀 Starting Portfolio Build Process"
echo "============================================"

# ----------------------------------------------------------------------------
# Step 1: Upgrade pip and install Python dependencies
# ----------------------------------------------------------------------------
echo ""
echo "📦 [1/5] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# ----------------------------------------------------------------------------
# Step 2: Build Frontend (TypeScript → JavaScript)
# ----------------------------------------------------------------------------
echo ""
echo "🎨 [2/5] Building Frontend..."

# Navigate to frontend directory
cd ../frontend

# Check if Node.js/npm is available
if command -v npm &> /dev/null; then
    echo "   → Installing Node.js dependencies..."
    npm install
    
    echo "   → Compiling TypeScript to JavaScript..."
    npm run build

    echo "   → Copying frontend assets into Django static directory..."
    mkdir -p ../portfolio_backend/static/frontend/dist
    cp -R dist/. ../portfolio_backend/static/frontend/dist/
    if [ -f style.css ]; then
        cp style.css ../portfolio_backend/static/frontend/style.css
    fi
    if [ -f favicon.ico ]; then
        cp favicon.ico ../portfolio_backend/static/frontend/favicon.ico
    fi
    
    echo "   ✅ Frontend build complete!"
else
    echo "   ⚠️  npm not found. Skipping frontend build."
    echo "   → Ensure frontend is pre-built or Node.js is installed."
fi

# Return to backend directory
cd ../portfolio_backend

# ----------------------------------------------------------------------------
# Step 3: Collect Static Files
# ----------------------------------------------------------------------------
echo ""
echo "📂 [3/5] Collecting static files..."
python manage.py collectstatic --noinput

# ----------------------------------------------------------------------------
# Step 4: Run Database Migrations
# ----------------------------------------------------------------------------
echo ""
echo "🗄️  [4/5] Running database migrations..."
python manage.py migrate --noinput

# ----------------------------------------------------------------------------
# Step 5: Create cache table (if using database cache)
# ----------------------------------------------------------------------------
echo ""
echo "💾 [5/5] Setting up cache tables..."
python manage.py createcachetable 2>/dev/null || echo "   → Cache table already exists or using different backend"

# ----------------------------------------------------------------------------
# Build Complete
# ----------------------------------------------------------------------------
echo ""
echo "============================================"
echo "✅ Build completed successfully!"
echo "============================================"
echo ""
echo "Ready to start with:"
echo "  gunicorn portfolio_backend.wsgi:application"
echo ""
