#!/usr/bin/env python3
"""
Streamlit Cloud Entry Point for Multiplayer Version

This file serves as the entry point for deploying the multiplayer version
of the SCS Mediator SDK to Streamlit Cloud.

Multiplayer Features:
- Facilitator creates session and gets session code
- Players join with session code
- Turn-based negotiation with accept/reject votes
- Simulation tests the final agreed-upon terms

To deploy:
1. Go to https://share.streamlit.io/
2. Create a new app
3. Point to this repository
4. Set "Main file path" to: streamlit_app_multiplayer.py
5. Deploy!
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import and run the multiplayer app
from scs_mediator_sdk.ui.multiplayer_app import main

if __name__ == "__main__":
    main()
