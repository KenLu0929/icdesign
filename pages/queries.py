from . import models
import logging
from django.core import serializers
import json
from icdesign import utils
from django.db import IntegrityError
from icdesign import error_messages

# Get an instance of a logger
logger = logging.getLogger(__name__)

'''
Query for table Users
'''

class QueryUsers:
    
    @staticmethod
    def users_upsert(data):
        """update users data or create data

        Args:
            data (dict): user data

        Returns:
            bool: successful
        """        

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
        """get users data or create data
        (If not existing ,create new user
        If it is existing ,get user data
        If something is wrong, record in log)

        Args:
            data (dict): user data

        Returns:
            any, bool: model.users or none, created or not
        """

        try:
            obj, created = models.Users.objects.get_or_create(**data)
            # logger.info("Data created Successfully: ", created)
            return obj, created
        except Exception as e:
            logger.error("Data: ", data)
            logger.error('Failed to insert data user to database: ', e)
            return None, False

    @staticmethod
    def users_get(my_filter, select_all=False):
        """ Get users data if it meet conditions

        Args:
            my_filter (dict): filter condition
            select_all (bool): get all user data or not. Defaults to False.

        Returns:
            list or dict : users data
        """        

        # print(my_filter)
        users = models.Users.objects.filter(**my_filter).distinct()
        users_json = serializers.serialize('json', users)
        users_json = json.loads(users_json)
        users_json = utils.get_fields_only(users_json)

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
        """update the user's data

        Args:
            filter_data (dict): filter condition
            updated_data (dict): update data

        Returns:
            int,error_messages: result,error message
        """        

        try:
            q = models.Users.objects.filter(**filter_data).update(**updated_data)
            return q, None
        except IntegrityError:
            return None, error_messages.EMAIL_TAKEN

    @staticmethod
    def users_checking_fields_exists(filter_data):
        """Check user is existing or not

        Args:
            filter_data (dict): filter condition

        Returns:
            bool: result of checking
        """

        q = models.Users.objects.filter(**filter_data).exists()
        return q


'''
Query for table exams
'''


class QueryExams:
    # insert users data
    @staticmethod
    def exams_upsert(data):
        """update exams data or create (if not existing )

        Args:
            data (dict): exams data

        Returns:
            bool : successful
        """        

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
        """get exams data or create (if not existing)

        Args:
            data (dict): exams data

        Returns:
            any, bool : data object or none, successful
        """        

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
        """Get exams data if meet condition and
        order by the "exam start time" and return

        Args:
            my_filter (dict): condition (ex: exam_is_active)
            select_all (bool): get all data or not. Defaults to False.

        Returns:
            list or dict : exams data(Exams model)
        """

        # print(my_filter)
        exams = models.Exams.objects.filter(**my_filter).order_by("exam_name").distinct()
        exams_json = serializers.serialize('json', exams)
        exams_json = json.loads(exams_json)
        exams_json = utils.get_fields_only(exams_json)
        
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
        """update exams data

        Args:
            filter_data (dict): filter data
            updated_data (dict): update data

        Returns:
            int : successful
        """        

        # print(my_filter)

        q = models.Exams.objects.filter(**filter_data).update(**updated_data)
        # print(q)
        # print("output:", users_json[0])
        return q


'''
Query for table exams_logs
'''


class QueryExamsLogs:
    @staticmethod
    def exams_upsert(data):
        """update examslogs date or create (if not existing)

        Args:
            data (dict): examslogs data

        Returns:
            bool: successful
        """        

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
        """get examslogs data or create ( if not existing )

        Args:
            data (dict): examslogs data

        Returns:
            any or none, bool: data object, successful
        """        

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
        """Get examslog data if meet condition and return

        Args:
            my_filter (dict): conditions (ex : user's ID)
            select_all (bool): get all data or not. Defaults to False.

        Returns:
            list or dict: exam logs data (ExamLogs model)
        """        

        # print(my_filter)

        exams = models.ExamLogs.objects.filter(**my_filter).distinct()
        exams_json = serializers.serialize('json', exams)
        exams_json = json.loads(exams_json)
        exams_json = utils.get_fields_only(exams_json)
        
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
        """update examslogs data

        Args:
            filter_data (dict): filter data
            updated_data (dict or list): update data

        Returns:
            int: successful
        """

        # print(my_filter)

        q = models.ExamLogs.objects.filter(**filter_data).update(**updated_data)
        # print(q)
        # print("output:", users_json[0])
        return q

    @staticmethod
    def exams_delete(my_filter):
        try:
            q = models.ExamLogs.objects.filter(**my_filter).delete()
            return True
        except Exception as e:
            logger.error("Data: ", my_filter)
            logger.error('Failed to delete data user to database: ', str(e))
            return False

    @staticmethod
    def exams_ins(data):
        q = models.ExamLogs.objects.filter(**data)
        return q

'''
Query for table news
'''

class QueryNews:

    @staticmethod
    def news_get():
        """ Get news data(only active=1)

        Returns:
            list or dict : value of fields( news model )
        """        

        news = models.News.objects.filter(news_is_active=1).distinct()
        news_json = serializers.serialize('json', news)
        news_json = json.loads(news_json)
        news_json = utils.get_fields_only(news_json)

        return news_json


"""
Query for table counterexamslogs
"""

class QueryCounterExamsLogs:

    @staticmethod
    def users_upsert():
        """create a blank data in counterexamslogs table

        Returns:
            bool: successful
        """        

        # user = models.User(**data)
        try:
            cel = models.CounterExamsLogs()
            cel.content = ""
            cel.save()
            return True
        except Exception as e:
            logger.error('Failed to insert data user to database: ', str(e))
            return False


"""
Query for table settingapp
"""

class QuerySettingApp:

    @staticmethod
    def setting_get(select_all=False):
        """get setting data

        Args:
            select_all (bool): get all data or not. Defaults to False.

        Returns:
            dict or list: setting data(SettingApp model)
        """

        # print(my_filter)

        setting = models.SettingApp.objects.all()
        setting_json = serializers.serialize('json', setting)
        setting_json = json.loads(setting_json)

        setting_json = utils.get_fields_only(setting_json)
        if select_all:
            return setting_json
        if len(setting_json) == 1:
            exams_json = setting_json[0]
            return exams_json
        elif len(setting_json) == 0:
            return {}
        return setting_json
