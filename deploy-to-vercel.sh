#!/bin/bash

# Zero Entropy ChatGPT Clone - Vercel Deployment Script
# Elon Musk's first-principles approach to deployment automation

set -e  # Exit on any error

echo "🚀 Zero Entropy ChatGPT Clone - Vercel Deployment"
echo "=================================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with your credentials:"
    echo "  cp .env.example .env"
    echo "  # Edit .env with your actual API keys"
    exit 1
fi

# Verify database connection
echo "🗄️ Testing NEON database connection..."
if psql "$DATABASE_URL" -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Database connection successful"
else
    echo "❌ Database connection failed. Please check DATABASE_URL in .env"
    exit 1
fi

# Build frontend
echo "🎨 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo ""
echo "🎉 Deployment Complete!"
echo "=================================================="
echo "Your Zero Entropy ChatGPT Clone is now live!"
echo ""
echo "Next steps:"
echo "1. Set environment variables in Vercel dashboard"
echo "2. Test the deployed application"
echo "3. Add knowledge documents via API"
echo ""
echo "Environment variables to set in Vercel:"
echo "- OPENAI_API_KEY"
echo "- DATABASE_URL" 
echo "- NEXTAUTH_SECRET"
echo "- NODE_ENV=production"
echo ""
echo "🔗 Access your app at the Vercel URL provided above"
