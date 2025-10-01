# API Testing Guide

## Table of Contents
1. [Quick Test](#quick-test)
2. [Using cURL](#using-curl)
3. [Using Postman](#using-postman)
4. [Using Python Requests](#using-python-requests)
5. [Common Test Scenarios](#common-test-scenarios)

---

## Quick Test

After starting the server:
```bash
python manage.py runserver
```

Visit these URLs in your browser:
- API Root: http://localhost:8000/api/
- Projects: http://localhost:8000/api/projects/
- Blog: http://localhost:8000/api/blog/
- Health Check: http://localhost:8000/api/health/
- Admin: http://localhost:8000/admin/

---

## Using cURL

### Get Projects List
```bash
curl http://localhost:8000/api/projects/
```

### Get Single Project
```bash
curl http://localhost:8000/api/projects/my-project-slug/
```

### Search Projects
```bash
curl "http://localhost:8000/api/projects/?search=django"
```

### Filter Projects
```bash
curl "http://localhost:8000/api/projects/?is_featured=true&page_size=5"
```

### Get Blog Posts
```bash
curl http://localhost:8000/api/blog/
```

### Search Blog Posts
```bash
curl "http://localhost:8000/api/blog/search/?q=python"
```

### Submit Contact Form
```bash
curl -X POST http://localhost:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Test Message",
    "message": "This is a test message from cURL"
  }'
```

### Subscribe to Newsletter
```bash
curl -X POST http://localhost:8000/api/subscribe/ \
  -H "Content-Type: application/json" \
  -d '{"email": "subscriber@example.com"}'
```

### Health Check
```bash
curl http://localhost:8000/api/health/
```

---

## Using Postman

### 1. Import Collection
Create a new collection with these requests:

### GET Projects
```
Method: GET
URL: {{base_url}}/api/projects/
```

### POST Contact Form
```
Method: POST
URL: {{base_url}}/api/contact/
Headers:
  Content-Type: application/json
Body (raw JSON):
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "subject": "Business Inquiry",
  "message": "I would like to discuss a project opportunity.",
  "phone": "+1234567890"
}
```

### Environment Variables
```
base_url: http://localhost:8000
```

---

## Using Python Requests

### Install Requests
```bash
pip install requests
```

### Test Script
```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_projects_list():
    """Test getting projects list"""
    response = requests.get(f"{BASE_URL}/projects/")
    print(f"Status: {response.status_code}")
    print(f"Projects: {len(response.json()['results'])}")
    return response.json()

def test_project_detail(slug):
    """Test getting single project"""
    response = requests.get(f"{BASE_URL}/projects/{slug}/")
    print(f"Status: {response.status_code}")
    print(f"Project: {response.json()['title']}")
    return response.json()

def test_blog_search(query):
    """Test blog search"""
    response = requests.get(f"{BASE_URL}/blog/search/", params={"q": query})
    print(f"Status: {response.status_code}")
    print(f"Results: {response.json()['count']}")
    return response.json()

def test_contact_form():
    """Test contact form submission"""
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message with more than 10 characters."
    }
    response = requests.post(f"{BASE_URL}/contact/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()['message']}")
    return response.json()

def test_subscribe():
    """Test newsletter subscription"""
    data = {"email": "newsubscriber@example.com"}
    response = requests.post(f"{BASE_URL}/subscribe/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()['message']}")
    return response.json()

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health/")
    print(f"Status: {response.status_code}")
    print(f"Health: {response.json()['status']}")
    return response.json()

if __name__ == "__main__":
    print("Testing API Endpoints...\n")
    
    print("1. Testing Projects List")
    test_projects_list()
    print("\n" + "="*50 + "\n")
    
    print("2. Testing Blog Search")
    test_blog_search("django")
    print("\n" + "="*50 + "\n")
    
    print("3. Testing Contact Form")
    test_contact_form()
    print("\n" + "="*50 + "\n")
    
    print("4. Testing Newsletter Subscription")
    test_subscribe()
    print("\n" + "="*50 + "\n")
    
    print("5. Testing Health Check")
    test_health_check()
    print("\n" + "="*50 + "\n")
```

---

## Common Test Scenarios

### 1. Pagination Test
```python
import requests

# Get first page
response = requests.get("http://localhost:8000/api/projects/", params={"page": 1, "page_size": 5})
data = response.json()
print(f"Total items: {data['count']}")
print(f"Total pages: {data['total_pages']}")
print(f"Current page: {data['current_page']}")

# Get next page
if data['next']:
    next_response = requests.get(data['next'])
    print(f"Next page items: {len(next_response.json()['results'])}")
```

### 2. Filtering Test
```python
# Filter featured projects
response = requests.get("http://localhost:8000/api/projects/", params={
    "is_featured": "true",
    "status": "published"
})
print(f"Featured projects: {response.json()['count']}")

# Filter by technology
response = requests.get("http://localhost:8000/api/projects/", params={
    "technologies": "django"
})
print(f"Django projects: {response.json()['count']}")
```

### 3. Search Test
```python
# Search in multiple fields
response = requests.get("http://localhost:8000/api/projects/", params={
    "search": "e-commerce"
})
print(f"Search results: {response.json()['count']}")
```

### 4. Rate Limiting Test
```python
import requests
import time

# Test contact form rate limiting (10 per hour)
for i in range(15):
    data = {
        "name": f"Test User {i}",
        "email": f"test{i}@example.com",
        "subject": "Test",
        "message": "This is a test message."
    }
    response = requests.post("http://localhost:8000/api/contact/", json=data)
    print(f"Attempt {i+1}: Status {response.status_code}")
    
    if response.status_code == 429:
        print("Rate limit exceeded!")
        break
    
    time.sleep(1)
```

### 5. Validation Test
```python
# Test invalid email
response = requests.post("http://localhost:8000/api/contact/", json={
    "name": "Test",
    "email": "invalid-email",
    "subject": "Test",
    "message": "Test message"
})
print(f"Status: {response.status_code}")
print(f"Errors: {response.json()}")

# Test short message
response = requests.post("http://localhost:8000/api/contact/", json={
    "name": "Test",
    "email": "test@example.com",
    "subject": "Test",
    "message": "Short"
})
print(f"Status: {response.status_code}")
print(f"Errors: {response.json()}")
```

### 6. Performance Test
```python
import requests
import time

def measure_response_time(url, iterations=10):
    times = []
    for _ in range(iterations):
        start = time.time()
        response = requests.get(url)
        end = time.time()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    print(f"Average response time: {avg_time:.3f}s")
    print(f"Min: {min(times):.3f}s, Max: {max(times):.3f}s")

# Test project list endpoint
print("Testing /api/projects/ performance:")
measure_response_time("http://localhost:8000/api/projects/")

# Test blog list endpoint
print("\nTesting /api/blog/ performance:")
measure_response_time("http://localhost:8000/api/blog/")
```

### 7. Cache Test
```python
import requests
import time

# First request (not cached)
start = time.time()
response1 = requests.get("http://localhost:8000/api/projects/")
time1 = time.time() - start
print(f"First request (no cache): {time1:.3f}s")

# Second request (should be cached)
start = time.time()
response2 = requests.get("http://localhost:8000/api/projects/")
time2 = time.time() - start
print(f"Second request (cached): {time2:.3f}s")

print(f"Speed improvement: {((time1 - time2) / time1) * 100:.1f}%")
```

---

## Expected Response Formats

### Success Response (200 OK)
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/projects/?page=2",
  "previous": null,
  "total_pages": 2,
  "current_page": 1,
  "results": [...]
}
```

### Created Response (201 Created)
```json
{
  "message": "Thank you for your message! We will get back to you soon.",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "submitted_at": "2024-01-20T15:30:00Z"
  }
}
```

### Validation Error (400 Bad Request)
```json
{
  "email": ["Invalid email format"],
  "message": ["Message must be at least 10 characters"]
}
```

### Rate Limit Error (429 Too Many Requests)
```json
{
  "error": "Too many requests. Please try again later."
}
```

### Server Error (500 Internal Server Error)
```json
{
  "detail": "Internal server error"
}
```

---

## Automated Testing

### Run Django Tests
```bash
python manage.py test

# With coverage
pytest --cov=api --cov-report=html
```

### Load Testing with Locust
```bash
pip install locust

# Create locustfile.py
# Run: locust -f locustfile.py --host=http://localhost:8000
```

---

## Monitoring Endpoints

### Health Check
```bash
# Should return 200 OK
curl http://localhost:8000/api/health/

# Response:
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected"
}
```

---

**Happy Testing! 🧪**
