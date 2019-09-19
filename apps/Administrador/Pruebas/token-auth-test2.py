import requests

def client():

    # data = {
    #     "username": "darwin1", 
    #     "email": "test@gmail.com",
    #     "password1": "darwin12345",
    #     "password2": "darwin12345"
    #     }

    # response = requests.post("http://127.0.0.1:8000/api/rest-auth/registration/",
    #                          data=data)

    token_h = "Token 8f901d8666059a0c196f8239ab4efc4a57a93377"
    headers = {"Authorization": token_h}

    response = requests.get("http://127.0.0.1:8000/administrador/personal/",
                            headers=headers)

    print("Status Code: ", response.status_code)
    
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()