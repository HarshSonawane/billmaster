import requests
import json
from django.conf import settings

headers = {
    'Content-Type': 'application/json'
}


def verify_token(id, token):
    url = "https://graph.facebook.com/me?fields=name,email&access_token=" + token
    response = requests.request("GET", url, headers=headers)
    json_response = response.json()

    if json_response["id"] == id:
        return { "status": True, "data": json_response } 
    else:
        return { "status": False, "data": json_response }


def manual_login(user):
    print(user.username)
    response = requests.request(
        "POST",
        settings.HOSTNAME + "rest/auth/login/",
        data = { "username": user.username, "password": user.username }
    )

    return response.json()
