from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData
from os import environ as env

from logging import getLogger
logger = getLogger(__name__)

class CachetAlertPlugin(AlertPlugin):
    name = "Cachetq Alert"
    slug = "cabot_alert_cachetq"
    author = "Jonathan R Martinelli"
    version = "0.0.1"
    font_icon = "fa fa-code"

    user_config_form = CachetAlertUserSettingsForm

    def send_alert(self, service, users, duty_officers):
        message = service.get_status_message()
        for u in users:
            logger.info('{} - This is bad for your {}.'.format(
                message,
                u.cabot_alert_skeleton_settings.favorite_bone))

        return True

class CachetAlertUserData(AlertPluginUserData):
    name = "Cachetq Plugin"
    cachetq_alias = models.CharField(max_length=50, blank=True)

    def serialize(self):
        return {
            "cachetq_alias": self.cachetq_alias
        }
