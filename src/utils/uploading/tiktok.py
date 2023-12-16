import requests
import json

def send_post_request():

    url = "https://open.tiktokapis.com/v2/post/publish/content/init/"
    header = {
        'Authorization': 'Bearer act.example12345Example12345Example', #TODO
        'Content-Type': 'application/json'
    }
    data = {
        "post_info": {
            "title": "funny cat",
            "description": "this will be a #funny photo on your @tiktok #fyp",
            "disable_comment": "true",
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "auto_add_music": "true"
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "photo_cover_index": 1,
            "photo_images": [
                "http://yourserver.com/obj/example-image-01.webp",
                "http://yourserver.com/obj/example-image-02.webp"
            ]
        },
        "post_mode": "DIRECT_POST",
        "media_type": "PHOTO"
    }

    response = requests.post(url, headers=header, data=json.dumps(data))
    print(response.text)