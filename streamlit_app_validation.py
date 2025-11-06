#!/usr/bin/env python3
"""
Streamlit Cloud Entry Point for Validation-Enhanced Version

This file serves as the entry point for deploying the validation-enhanced version
of the SCS Mediator SDK to Streamlit Cloud as a separate app for A/B testing.

To deploy this version:
1. Go to https://share.streamlit.io/
2. Create a new app
3. Point to this repository
4. Set "Main file path" to: streamlit_app_validation.py
5. Deploy!

This will run the experimental version with model validation features.
"""

# Import and run the validation-enhanced multi-view app
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import and run the validation version
from scs_mediator_sdk.ui.validation_multi_view import main

if __name__ == "__main__":
    main()
