#!/usr/bin/env python
import os
import sys

# Add the Django project to the path
sys.path.append(r'C:\Users\admin\Desktop\DOCSUM')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

# Now import and test our service
from summarizer.service import generate_summary_from_file

# Test with an existing PDF
pdf_path = r"C:\Users\admin\Desktop\DOCSUM\media\documents\atention.pdf"

if os.path.exists(pdf_path):
    print(f"Testing summarization with: {pdf_path}")
    try:
        summary = generate_summary_from_file(pdf_path)
        print("\n--- SUMMARY ---")
        print(summary)
        print("--- END SUMMARY ---")
    except Exception as e:
        print(f"Error during summarization: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"File not found: {pdf_path}")