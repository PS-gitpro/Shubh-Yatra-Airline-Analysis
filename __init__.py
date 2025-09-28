"""
Shubh Yatra - Airline Risk Analysis Dashboard
Risk Factor Analysis for Indian Domestic Flights

Copyright (c) 2025 Prateek Singh. All Rights Reserved.
Licensed under the MIT License.
"""

__version__ = "1.0.0"
__author__ = "Prateek Singh"
__email__ = "contactprateeksingh01@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2025 Prateek Singh"

# Package imports
from .app import main

# Package metadata
__all__ = [
    "main",
    "__version__", 
    "__author__",
    "__email__",
    "__license__"
]

# Package description
__description__ = """
A comprehensive dashboard for analyzing risk factors and safety performance 
of Indian domestic airlines using Streamlit and machine learning.
"""

# Optional: Print package info when imported
print(f"Shubh Yatra {__version__} - Airline Risk Analysis Dashboard")
print(f"By {__author__} - {__email__}")
print(f"License: {__license__}")
print(f"{__copyright__}")
