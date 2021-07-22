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
            obj, created = models.Users.objects.update_or_create(**data)
            # print(created)
            # print(obj)
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
            obj, created = models.Users.objects.get_or_create(**data)
            # logger.info("Data created Successfully: ", created)
            return obj, created
        except Exception as e:
            logger.error("Data: ", data)
            logger.error('Failed to insert data user to database: ', e)
            return None, False

    @staticmethod
    def users_get(my_filter):
        # print(my_filter)

        users = models.Users.objects.filter(**my_filter).distinct()
        users_json = serializers.serialize('json', users)
        users_json = json.loads(users_json)
        if len(users_json) == 1:
            return users_json[0]
        return users_json


    @staticmethod
    def users_update(filter_data, updated_data):
        # print(my_filter)

        q = models.Users.objects.filter(**filter_data).update(**updated_data)
        # print(q)
        # print("output:", users_json[0])
        return q

