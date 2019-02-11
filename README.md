Cabot Cachet Alert Plugin
=====

This is a Cachet alert plugin for Cabot. It integrates with Cachet API: 
* Creates incidents with _Investigating_ status when a Cabot check goes to a Fail status;
* Updates incidents with _Fixed_ status, when a Cabot check comes back to normal. 

## Usage:

Add the following properties to Cabot config file (development.env\production.env):

* **CACHETQ_URL:** Cachet URL
* **CACHETQ_TOKEN:** Cachet token for API Authentication
* **CACHETQ_COMPONENT_STATUS:** Needed to map cabot statuses to Cachetq Component Statuses:
    * Example: 
        ```
        {
            "PASSING":1,
            "WARNING":2,
            "ERROR":3,
            "CRITICAL":4
         }
        ```
* **CACHETQ_COMPONENT_ID:** Needed to map Cabot services to Cachet Components:
    * Example: 
        ```
        {
            "Service1": CACHET_COMPONENT_ID_FOR_SERVICE1, 
            "Service2": CACHET_COMPONENT_ID_FOR_SERVICE2
        }
        ```
Concat _cabot_alert_cachetq_ to **CABOT_PLUGINS_ENABLED** property in default.env Cabot file. Example below:
```
CABOT_PLUGINS_ENABLED=cabot_alert_hipchat,cabot_alert_twilio,cabot_alert_email,cabot_alert_slack,cabot_alert_cachetq
```

**Next:** Follow Writing Alert Plugins section in Cabot documentation: https://cabotapp.com/dev/writing-alert-plugins.html. If you are using https://github.com/cabotapp/docker-cabot, a great guideline to install this plugin to docker-cabot is https://github.com/cabotapp/docker-cabot/issues/26.

