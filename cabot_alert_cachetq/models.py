from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData
from os import environ as env
from pprint import pprint
from logging import getLogger
from django.template import Context, Template

import requests
import json

logger = getLogger(__name__)

component_status = json.loads(env.get('CACHETQ_COMPONENT_STATUS'))
component_id = json.loads(env.get('CACHETQ_COMPONENT_ID'))
cachetq_url = env.get('CACHETQ_URL')
cachetq_template="""Service {{ service.name }}\
{% if service.overall_status == service.PASSING_STATUS %}*is back to normal*{% else %}\ 
reporting *{{ service.overall_status }}* status{% endif %}:\
{% if service.overall_status != service.PASSING_STATUS %}Checks failing:\
{% for check in service.all_failing_checks %}\
    - {{ check.name }} {% if check.last_result.error %} ({{ check.last_result.error|safe }}){% endif %}
{% endfor %}\
{% endif %}"""    

class CachetqAlertPlugin(AlertPlugin):
    name = "Cachetq Alert"
    slug = "cabot_alert_cachetq"
    author = "Jonathan R Martinelli"
    version = "0.0.1"

    def send_alert(self, service, users, duty_officers):
    	logger.info('Sending Cachetq Alert')

        incidents = self._get_cachetq_incidents(service)

        c = Context({ 'service': service })
        message = Template(cachetq_template).render(c)

        if incidents:
            incident_id = incidents[0]['id']
            if incidents[0]['status'] != 4:
                self._update_cachetq_incident(self, message, service)
        else:
            self._create_cachetq_incident(self, message, service)

    def _create_cachetq_incident(self, message, service):
    	logger.info('Creating Cachetq Alert to: %s', service.overall_status)

        resp = requests.post(cachetq_url, data=json.dumps({
            'name': service.name,
            'message': message,
            'status': 1, #Investigating
            'visible': 1,
            'component_id': component_id[service.name],
            'component_status': component_status[service.overall_status],
            'notify': true
        }))

    def _update_cachetq_incident(self, message, service):
    	logger.info('Updating Cachetq Alert to: %s', service.overall_status)
        
        resp = requests.put(cachetq_url, data=json.dumps({
            'name': service.name,
            'message': message,
            'status': 4, #Fixed
            'visible': 1,
            'component_id': component_id[service.name],
            'component_status': component_status[service.overall_status],
            'notify': true
        }))
    
    def _get_cachetq_incidents(service):
    	logger.info('Find existente incident: %s', service.name)

        name = service.name
        component = component_id[name]

        url = cachetq_url + "/incidents"
        resp = requests.get(url, params={
            'name':name,
            'component_id': component
            }
        )
        
        return json.loads(resp.text)['data']   

class CachetqAlertUserData(AlertPluginUserData):
    name = "Cachetq Plugin"