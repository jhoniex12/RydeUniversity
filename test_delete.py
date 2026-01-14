"""
Quick test script to verify DELETE endpoint works
"""
import requests
import time

# Wait a moment for server to be ready
time.sleep(2)

try:
    # Test DELETE endpoint
    response = requests.delete('http://localhost:5000/api/students/1')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')
    
    if response.status_code == 200:
        print('\n✅ DELETE endpoint works correctly!')
    else:
        print('\n❌ DELETE endpoint returned an error')
        
except Exception as e:
    print(f'Error: {e}')
