from . import models
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# insert users data
def users_insert(data):
    # user = models.User(**data)
    try:
        # user.save()
        obj, created = models.User.update_or_create(**data)
        logger.info("Data created Successfully: ", created)
        return True
    except Exception as e:
        logger.error("Data: ", data)
        logger.error('Failed to insert data user to database: ', str(e))
        return False


def users_get(my_filter, column_name):

    users = models.User.objects.filter(my_filter).values(column_name).distinct()

    return users
