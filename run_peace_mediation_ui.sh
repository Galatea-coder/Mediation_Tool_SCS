#!/bin/bash
# Launch script for Peace Mediation UI

echo "================================================"
echo "  SCS Mediator SDK v2 - Peace Mediation Tools  "
echo "================================================"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to project directory
cd "$SCRIPT_DIR"

echo "Project directory: $SCRIPT_DIR"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Error: Streamlit is not installed"
    echo ""
    echo "Please install it with:"
    echo "  pip install streamlit"
    echo ""
    exit 1
fi

echo "✅ Streamlit found"
echo ""

# Set Python path to include the source directory
export PYTHONPATH="${SCRIPT_DIR}/src:${PYTHONPATH}"

echo "🚀 Launching Peace Mediation UI..."
echo ""
echo "The UI will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "================================================"
echo ""

# Launch the UI
streamlit run src/scs_mediator_sdk/ui/peace_mediation_ui.py
