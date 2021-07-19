from . import models
import logging

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
            logger.info("Data created Successfully: ", created)
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


            return created
        except Exception as e:
            logger.error("Data: ", data)
            logger.error('Failed to insert data user to database: ', str(e))
            return False

    @staticmethod
    def users_get(my_filter, column_name):

        users = models.User.objects.filter(**my_filter).values(column_name).distinct()

        return users
