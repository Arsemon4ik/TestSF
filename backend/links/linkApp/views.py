import json
import re
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

# для тестов
from django.test import Client



# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)


@api_view(['GET','POST'])
def manage_items(request, *args, **kwargs):
    items = {}
    urls = []
    for key in redis_instance.keys("*"):
        items[key.decode('utf-8')] = redis_instance.get(key)
    if request.method == 'GET':
        response = {
            'domains': items,
            "status": "ok"
        }
        return Response(response, status=200)

    elif request.method == 'POST':
        body = json.loads(request.body)
        body_key = list(body.keys())[0]
        value = body[body_key]
        urlsFromDB = [url.decode('utf-8') for url in items.values()]

        for item in value:
            full_url = re.search('https?://([A-Za-z_0-9.-]+).*|([a-z_0-9.-]+)', item)
            tmpLst = []
            now = datetime.now()
            key = now.strftime("%H%M%S%f")[:-3]
            print(full_url.group(1), full_url.group(2))

            if full_url.group(2) and full_url.group(2) not in urlsFromDB and full_url.group(2) not in tmpLst:
                redis_instance.set(key, full_url.group(2))
                tmpLst.append(full_url.group(2))

            elif full_url.group(1) and full_url.group(1) not in urlsFromDB and full_url.group(1) not in tmpLst:
                redis_instance.set(key, full_url.group(1))
                tmpLst.append(full_url.group(1))

        response = {
            'status': "ok"
        }
        return Response(response, 201)


# тесты главного метода manage_items() (запускать нужно с консоли manage shell)

# c = Client()

# get_request = c.get('visited_links/', {})
# post_request = c.post('visited_links/', {'https://hello'})
# print(get_request.status_code == 200, post_request.status_code == 201)



