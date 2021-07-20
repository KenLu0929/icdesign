from . import models
import logging
from django.core import serializers
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


class QueryUsers:
    # insert users data
    @staticmethod
    def users_upsert(data):
        # user = models.User(**data)
        try:
            # user.save()
            obj, created = models.User.objects.update_or_create(**data)
            print(created)
            print(obj)
            # logger.info("Data created Successfully: ", created)
            return True
        except Exception as e:
            logger.error("Data: ", data)
            logger.error('Failed to insert data user to database: ', str(e))
            return False

    @staticmethod
    def users_getsert(data):
        # user = models.User(**data)
        try:
            # user.save()
            obj, created = models.User.objects.get_or_create(**data)
            # logger.info("Data created Successfully: ", created)
            return obj, created
        except Exception as e:
            logger.error("Data: ", data)
            logger.error('Failed to insert data user to database: ', str(e))
            return False

    @staticmethod
    def users_get(my_filter, amount=1):
        # print(my_filter)
        if amount == 1:
            users = models.User.objects.filter(**my_filter).distinct()
            users_json = serializers.serialize('json', users)
            users_json = json.loads(users_json)
            # print("output:", users_json[0])
            return users_json[0]
        else:
            users = models.User.objects.filter(**my_filter).distinct()
            users_json = serializers.serialize('json', users)
            users_json = json.loads(users_json)
            return users_json
