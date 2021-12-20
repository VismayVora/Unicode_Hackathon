import requests
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


def send_message(request, user):
    
    url = "https://api.wassenger.com/v1/messages"

    # current_site = get_current_site(request).domain
    # relative_link = f"/req-doc/{pk}/items/"
    # link = 'http://'+current_site+relative_link
    link = request.build_absolute_uri()

    payload = {
        "phone": str(user.phone_no),
        "message": f"Hello {user.name}, There is a new requirement posted on BEST DEAL which might interest you. Copy this link and paste on a browser: {link}"
    }
    headers = {
        "Content-Type": "application/json",
        "Token": "c0e1717b3de1545647d396ea3d59000aa65429387b643e0a7d979729370f47b4936b795410d6fd73"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)