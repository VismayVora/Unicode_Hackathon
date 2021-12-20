import requests
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


def send_message(request, user):
    
    url = "https://api.wassenger.com/v1/messages"

    current_site = get_current_site(request).domain
    relative_link = reverse('items-api')
    link = 'http://'+current_site+relative_link

    payload = {
        "phone": str(user.number),
        "message": "Hello {user.name}, There is a new requirement posted on BEST DEAL which might interest you. Click on this link: {link}"
    }
    headers = {
        "Content-Type": "application/json",
        "Token": "c0e1717b3de1545647d396ea3d59000aa65429387b643e0a7d979729370f47b4936b795410d6fd73"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)