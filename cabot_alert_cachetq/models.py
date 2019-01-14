from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData
from os import environ as env
from pprint import pprint
from logging import getLogger
logger = getLogger(__name__)

class CachetqAlertPlugin(AlertPlugin):
    name = "Cachetq Alert"
    slug = "cabot_alert_cachetq"
    author = "Jonathan R Martinelli"
    version = "0.0.1"
    font_icon = "fa fa-code"

#    cachetq_aliases = [u.cachetq_alias for u in CachetqAlertUserData.objects.filter(user__user__in=users)]

    def send_alert(self, service, users, duty_officers):
	logger.info('Beginning Test, self: ')
        pprint(dir(self))
        logger.info('Service: ')
        pprint(dir(service))
        logger.info('Users: ')
        pprint(dir(users))
        logger.info('Duty Officers: ')
        pprint(dir(duty_officers))
        for u in users:
            logger.info('This is bad for your {}.'.format(
                u.cabot_alert_cachetq_settings.favorite_bone))

        return True

class CachetqAlertUserData(AlertPluginUserData):
    name = "Cachetq Plugin"
    cachetq_alias = "test" #models.CharField(max_length=50, blank=True)

    def serialize(self):
        return {
            "cachetq_alias": self.cachetq_alias
        }
