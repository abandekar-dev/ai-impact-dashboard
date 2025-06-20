#!/usr/bin/env python3
import sys
import os

# Test numpy import
try:
    import numpy as np
    print(f"✓ NumPy {np.__version__} imported successfully")
except ImportError as e:
    print(f"✗ NumPy import failed: {e}")
    sys.exit(1)

# Test pandas import
try:
    import pandas as pd
    print(f"✓ Pandas {pd.__version__} imported successfully")
except ImportError as e:
    print(f"✗ Pandas import failed: {e}")
    sys.exit(1)

# Test plotly import
try:
    import plotly
    print(f"✓ Plotly {plotly.__version__} imported successfully")
except ImportError as e:
    print(f"✗ Plotly import failed: {e}")

# Test streamlit import
try:
    import streamlit as st
    print(f"✓ Streamlit imported successfully")
except ImportError as e:
    print(f"✗ Streamlit import failed: {e}")

print("All core dependencies are working correctly!")