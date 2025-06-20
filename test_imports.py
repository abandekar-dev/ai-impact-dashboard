#!/usr/bin/env python3

# Test basic imports
try:
    import sys
    print(f"Python version: {sys.version}")
    print("Basic imports working")
except Exception as e:
    print(f"Basic import error: {e}")

try:
    import numpy as np
    print(f"NumPy version: {np.__version__}")
    print("NumPy imported successfully")
except Exception as e:
    print(f"NumPy import error: {e}")

try:
    import pandas as pd
    print(f"Pandas version: {pd.__version__}")
    print("Pandas imported successfully")
except Exception as e:
    print(f"Pandas import error: {e}")

try:
    import streamlit as st
    print("Streamlit imported successfully")
except Exception as e:
    print(f"Streamlit import error: {e}")