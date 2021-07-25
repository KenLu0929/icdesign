from . import models
import logging
from django.core import serializers
import json
from icdesign.utils import get_fields_only

# Get an instance of a logger
logger = logging.getLogger(__name__)

'''
Query for table Users
'''


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
    def users_get(my_filter, select_all=False):
        # print(my_filter)

        users = models.Users.objects.filter(**my_filter).distinct()
        users_json = serializers.serialize('json', users)
        users_json = json.loads(users_json)
        users_json = get_fields_only(users_json)
        if select_all:
            return users_json
        if len(users_json) == 1:
            users_json = users_json[0]
            return users_json
        elif len(users_json) == 0:
            return {}
        return users_json

    @staticmethod
    def users_update(filter_data, updated_data):
        # print(my_filter)

        q = models.Users.objects.filter(**filter_data).update(**updated_data)
        # print(q)
        # print("output:", users_json[0])
        return q


'''
Query for table exams
'''


class QueryExams:
    # insert users data
    @staticmethod
    def exams_upsert(data):
        # user = models.User(**data)
        try:
            # user.save()
            models.Exams.objects.update_or_create(**data)
            # print(created)
            # print(obj)
            # logger.info("Data created Successfully: ", created)
            return True
        except Exception as e:
            logger.error("Data: ", data)
            logger.error('Failed to insert data user to database: ', str(e))
            return False

    @staticmethod
    def exams_getsert(data):
        # user = models.User(**data)
        try:
            # user.save()
            obj, created = models.Exams.objects.get_or_create(**data)
            # logger.info("Data created Successfully: ", created)
            return obj, created
        except Exception as e:
            logger.error("Data: ", data)
            logger.error('Failed to insert data user to database: ', e)
            return None, False

    @staticmethod
    def exams_get(my_filter, select_all=False):
        # print(my_filter)

        exams = models.Exams.objects.filter(**my_filter).distinct()
        exams_json = serializers.serialize('json', exams)
        exams_json = json.loads(exams_json)

        exams_json = get_fields_only(exams_json)
        if select_all:
            return exams_json
        if len(exams_json) == 1:
            exams_json = exams_json[0]
            return exams_json
        elif len(exams_json) == 0:
            return {}
        return exams_json

    @staticmethod
    def exams_update(filter_data, updated_data):
        # print(my_filter)

        q = models.Exams.objects.filter(**filter_data).update(**updated_data)
        # print(q)
        # print("output:", users_json[0])
        return q


'''
Query for table exams_logs
'''


class QueryExamsLogs:
    # insert users data
    @staticmethod
    def exams_upsert(data):
        # user = models.User(**data)
        try:
            # user.save()
            obj, created = models.ExamLogs.objects.update_or_create(**data)
            # users_get
            # logger.info("Data created Successfully: ", created)
            return True
        except Exception as e:
            logger.error("Data: ", data)
            logger.error('Failed to insert data user to database: ', str(e))
            return False

    @staticmethod
    def exams_getsert(data):
        # user = models.User(**data)
        try:
            # user.save()
            obj, created = models.ExamLogs.objects.get_or_create(**data)
            # logger.info("Data created Successfully: ", created)
            return obj, created
        except Exception as e:
            logger.error("Data: ", data)
            logger.error('Failed to insert data user to database: ', e)
            return None, False

    @staticmethod
    def exams_get(my_filter, select_all=False):
        # print(my_filter)

        exams = models.ExamLogs.objects.filter(**my_filter).distinct()
        exams_json = serializers.serialize('json', exams)
        exams_json = json.loads(exams_json)

        exams_json = get_fields_only(exams_json)
        if select_all:
            return exams_json
        if len(exams_json) == 1:
            exams_json = exams_json[0]
            return exams_json
        elif len(exams_json) == 0:
            return {}
        return exams_json

    @staticmethod
    def exams_update(filter_data, updated_data):
        # print(my_filter)

        q = models.ExamLogs.objects.filter(**filter_data).update(**updated_data)
        # print(q)
        # print("output:", users_json[0])
        return q


class QueryNews:

    @staticmethod
    def news_get():
        # print(my_filter)

        news = models.News.objects.all().distinct()
        news_json = serializers.serialize('json', news)
        news_json = json.loads(news_json)
        news_json = get_fields_only(news_json)

        return news_json
