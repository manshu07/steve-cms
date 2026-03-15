#!/bin/bash
# Setup script for pre-commit hooks

set -e  # Exit on error

echo "🔧 Setting up pre-commit hooks..."
echo ""

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo "📦 Installing pre-commit..."
    pip install pre-commit
else
    echo "✅ pre-commit already installed"
fi

echo ""
echo "🔗 Installing git hooks..."
pre-commit install

echo ""
echo "🧪 Running pre-commit on all files (first time setup)..."
pre-commit run --all-files || {
    echo ""
    echo "⚠️  Some hooks failed. You can:"
    echo "   1. Fix the issues manually"
    echo "   2. Run: pre-commit run --all-files"
    echo "   3. Commit with --no-verify to skip (not recommended)"
    exit 1
}

echo ""
echo "✅ Pre-commit hooks installed successfully!"
echo ""
echo "📝 What this does:"
echo "  • Runs smoke tests before every commit"
echo "  • Runs integration tests before every commit"
echo "  • Checks for unapplied migrations"
echo "  • Verifies model field integrity"
echo "  • Formats code with black"
echo "  • Lints code with flake8"
echo ""
echo "🚀 Now every commit will automatically run tests!"
echo ""
echo "To skip hooks (not recommended): git commit --no-verify"
