#!/usr/bin/env python
import os
import sys

# Add the Django project to the path
sys.path.append(r'C:\Users\admin\Desktop\DOCSUM')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

# Now import and check the database
from summarizer.models import Document

def check_database():
    print("=== DATABASE CHECK ===")
    
    # Count total documents
    total_docs = Document.objects.count()
    print(f"Total documents in database: {total_docs}")
    
    if total_docs > 0:
        print("\n=== RECENT DOCUMENTS ===")
        # Get the 5 most recent documents
        recent_docs = Document.objects.order_by('-uploaded_at')[:5]
        
        for i, doc in enumerate(recent_docs, 1):
            print(f"\n{i}. File: {doc.file.name}")
            print(f"   Uploaded: {doc.uploaded_at}")
            print(f"   Has Summary: {'Yes' if doc.summary else 'No'}")
            if doc.summary:
                # Show first 100 characters of summary
                summary_preview = doc.summary[:100] + "..." if len(doc.summary) > 100 else doc.summary
                print(f"   Summary Preview: {summary_preview}")
    
    # Check files with summaries (simple check)
    docs_with_summaries = Document.objects.filter(summary__isnull=False)
    print(f"\nDocuments with summaries: {docs_with_summaries.count()}")
    
    # Manual check for error vs successful summaries
    successful_count = 0
    error_count = 0
    for doc in docs_with_summaries:
        if doc.summary and "error" in doc.summary.lower():
            error_count += 1
        elif doc.summary and doc.summary.strip():
            successful_count += 1
    
    print(f"Documents with successful summaries: {successful_count}")
    print(f"Documents with error summaries: {error_count}")

if __name__ == "__main__":
    check_database()