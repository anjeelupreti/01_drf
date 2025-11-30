import requests
import json

BASE_URL = "http://127.0.0.1:8000/user/api/auth"

def test_all_endpoints():
    # 1. Login
    print("=== 1. Testing Login ===")
    login_data = {"email": "admin@gmail.com", "password": "Admin123!"}
    login_response = requests.post(f"{BASE_URL}/login/", json=login_data)
    print(f"Status: {login_response.status_code}")
    print(json.dumps(login_response.json(), indent=2))
    
    if login_response.status_code != 200:
        print("Login failed! Exiting.")
        return
    
    tokens = login_response.json()
    access_token = tokens['access']
    refresh_token = tokens['refresh']
    
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    
    # 2. List Users
    print("\n=== 2. Testing List Users ===")
    users_response = requests.get(f"{BASE_URL}/users/", headers=headers)
    print(f"Status: {users_response.status_code}")
    print(json.dumps(users_response.json(), indent=2))
    
    # 3. List Countries
    print("\n=== 3. Testing List Countries ===")
    countries_response = requests.get(f"{BASE_URL}/countries/", headers=headers)
    print(f"Status: {countries_response.status_code}")
    print(json.dumps(countries_response.json(), indent=2))
    
    # 4. Create User
    print("\n=== 4. Testing Create User ===")
    user_data = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "role": "member",
        "country": 1
    }
    create_response = requests.post(f"{BASE_URL}/users/create/", headers=headers, json=user_data)
    print(f"Status: {create_response.status_code}")
    print(json.dumps(create_response.json(), indent=2))
    
    # 5. Get User Details
    print("\n=== 5. Testing Get User Details ===")
    user_detail_response = requests.get(f"{BASE_URL}/users/1/", headers=headers)
    print(f"Status: {user_detail_response.status_code}")
    print(json.dumps(user_detail_response.json(), indent=2))
    
    # 6. Refresh Token
    print("\n=== 6. Testing Token Refresh ===")
    refresh_data = {"refresh": refresh_token}
    refresh_response = requests.post(f"{BASE_URL}/token/refresh/", json=refresh_data)
    print(f"Status: {refresh_response.status_code}")
    print(json.dumps(refresh_response.json(), indent=2))

if __name__ == "__main__":
    test_all_endpoints()