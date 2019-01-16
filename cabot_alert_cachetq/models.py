from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData
from os import environ as env
from pprint import pprint
from logging import getLogger
from django.template import Context, Template

import requests
import json

logger = getLogger(__name__)

cachetq_template="""
Service {{ service.name }}{% if service.overall_status == service.PASSING_STATUS %} is back to normal {% else %}\ 
reporting *{{ service.overall_status }}* status{% endif %}:\
{% if service.overall_status != service.PASSING_STATUS %}Checks failing:\
{% for check in service.all_failing_checks %}\
    - {{ check.name }}
{% endfor %}\
{% endif %}
"""    

class CachetqAlertPlugin(AlertPlugin):
    name = "Cachetq Alert"
    slug = "cabot_alert_cachetq"
    author = "Jonathan R Martinelli"
    version = "0.0.1"

    def send_alert(self, service, users, duty_officers):
        logger.info('Sending Cachetq Alert')

        component_id = json.loads(env.get('CACHETQ_COMPONENT_ID'))
        component_status = json.loads(env.get('CACHETQ_COMPONENT_STATUS'))

        if service.name in component_id:
            incidents = self._get_cachetq_incidents(service, component_id)

            c = Context({ 'service': service })
            message = Template(cachetq_template).render(c)

            if incidents:
                incident_id = incidents[0]['id']
                if incidents[0]['status'] != 4:
                    self._update_cachetq_incident(message, service, component_status, component_id, incident_id)
                elif service.overall_status != service.PASSING_STATUS:
                    self._create_cachetq_incident(message, service, component_status, component_id)   
            elif service.overall_status != service.PASSING_STATUS:
                self._create_cachetq_incident(message, service, component_status, component_id)
        else:
            logger.warning('Service not found in config: %s', service.name)

    def _create_cachetq_incident(self, message, service, component_status, component_id):      
        logger.info('Creating Cachetq Alert to: %s', service.overall_status)
        
        url = env.get('CACHETQ_URL') + "/incidents"
        headers = {'Content-Type':'application/json', 'X-Cachet-Token': env.get('CACHETQ_TOKEN')}
        requests.post(url, 
            headers=headers,
            data=json.dumps({
                'name': service.name,
                'message': message,
                'status': 1, #Investigating
                'visible': 1,
                'component_id': component_id[service.name],
                'component_status': component_status[service.overall_status],
                'notify': True
            })
        )
       
    def _update_cachetq_incident(self, message, service, component_status, component_id, incident_id):
    	logger.info('Updating Cachetq Alert to: %s', service.overall_status)
                
        url = env.get('CACHETQ_URL') + "/incidents/{id}".format( id=incident_id )
        headers = {'Content-Type':'application/json', 'X-Cachet-Token': env.get('CACHETQ_TOKEN')}
        requests.put(url, 
            headers=headers,
            data=json.dumps({
                'name': service.name,
                'message': message,
                'status': 4, #Fixed
                'visible': 1,
                'component_id': component_id[service.name],
                'component_status': component_status[service.overall_status],
                'notify': True
            })
        )
    
    def _get_cachetq_incidents(self, service, component_id):
    	logger.info('Find existent incident: %s', service.name)

        name = service.name
        component = component_id[name]

        url = env.get('CACHETQ_URL') + "/incidents"
        response = requests.get(url, params={
            'name':name,
            'component_id': component
            }
        )
        return json.loads(response.text)['data']

class CachetqAlertUserData(AlertPluginUserData):
    name = "Cachetq Plugin"