import requests
import os

# Test the API endpoint
url = "http://127.0.0.1:8000/api/summarize/"

# Find an existing PDF file to test with
pdf_path = r"C:\Users\admin\Desktop\DOCSUM\media\documents\atention.pdf"

if os.path.exists(pdf_path):
    print(f"Testing with file: {pdf_path}")
    
    with open(pdf_path, 'rb') as f:
        files = {'file': ('atention.pdf', f, 'application/pdf')}
        
        try:
            response = requests.post(url, files=files, timeout=180)
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
else:
    print(f"File not found: {pdf_path}")