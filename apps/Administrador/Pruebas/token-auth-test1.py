import requests

def client():
    # credentials = {"username": "darwin", "password": "darwin"}

    # response = requests.post("http://127.0.0.1:8000/api/rest-auth/login/",
    #                           data=credentials)

    token_h = "Token e1dcd1e43f8a1998c8415582bfb4b1b7601ca5c0"
    headers = {"Authorization": token_h}

    response = requests.get("http://127.0.0.1:8000/administrador/personal",
                            headers=headers)

    print("Status Code: ", response.status_code)
    
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()