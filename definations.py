
LOCATION = { SGW, HALL, LB, JMSB, FB, LOYOLA, EV, ER, ALL}

ALERT_TITLE = { FIRE_ALARM, SECURITY_ALARM, WEATHER_ALARM, POWER_ALARM, BUILDING_EVAQ, EARTHQUAKE_ALARM, 
               FIRE_CONTROLLED, SECURITY_CONTROLLED, WEATHER_CONTROLLED, POWER_CONTROLLED, 
               BUILDING_CONTROLLED, EARTHQUAKE_CONTROLLED }

ALERT_DESCRIPTION = { EVACUATE_BUILDING, STAY_AT_HOME, LOCKDOWN, SHELTER_IN_PLACE, SEEK_SHELTER, 
                     REMAIN_OUTSIDE_BUILDING, REMAIN_INSIDE_BUILDING, FOLLOW_INSTRUCTIONS, 
                     MONITOR_UPDATES, REPORT_SUSPICIOUS_ACTIVITY, REPORT_EMERGENCY} 

ALERT_CATEGORY = { FIRE, SECURITY, WEATHER, POWER, BUILDING, EARTHQUAKE, GENERAL} 
                # power outages, building closures,
                #and other urgent campus situations.

ALERT_SEVERITY = { ALERT, WARNING, ADVISORY, CRITICAL }

UDP_MESSAGES = {"REGISTRED", "REGISTER", "REGISTRATION_DENIED", "DE-REGISTER", # 2.1. Registration and De-registration (Communications through UDP):
                  
                "ALERT_RECEIVED",  "ALERT_EXPIRED", "ALERT_RESOLVED", "ALERT_DRILL", "INFO", "WARNING" 
                # INFO and WARNING alerts do not require acknowledgements in the basic implementation.
                 
                  "SUBSCRIBER", "PUBLISHER", "BOTH_S&P",

                  "SUBSCRIBE", "UNSUBSCRIBE", "UNSUBSCRIBED", "SUBSCRIPTION_DENIED", "SUBSCRIPTION_CONFIRMED",# 2.2. Alert Subscription (UDP)

                  "PUBLISH_ALERT ", "ALERT_ACCEPTED", "ALERT_DENIED"  # 2.3. Publishing an Emergency Incident (UDP)

                  "ALERT", # 2.4. Emergency Alert Distribution (UDP) 

                  "ALERT_ACK" # 2.5. Reliable Delivery of Critical Alerts (UDP)

                  "UPDATE_ALERT", "ALERT_UPDATED", "ALERT_UPDATE",  # 2.6 Updating an Existing Incident (UDP)
                  
                  "CLOSE_ALERT", "ALERT_CLOSED", "ALL_CLEAR" # 2.7 CLOSING NA INCIDENT

                  "STATUS_REPORT", "STATUS_RECORDED", "STATUS_REJECTED",  # 2.8 User Safety/Response Status (UDP)

                  "ATTACH_REQ", "ATTACH_INFO" , "ATTACH_DENIED", # 2.9 A Peer-to-Peer Incident Attachments (UDP Coordination + TCP Data Transfer)

                 "GET_ATTACHMENT", "ATTACH_DATA", "ATTACH_OK", "ATTACH_ERROR", # 2.9 B Direct Publisher-to-Subscriber Transfer (TCP) 
                 # After receiving ATTACH_INFO, the subscriber opens a TCP connection directly to the event
                 # publisher at the returned IP address and TCP port. The subscriber then requests the file directly
                 # from that peer:

                 " GET_ACTIVE_ALERTS", "ACTIVE_ALERTS" # 2.10 Recovering Current Emergency Information (TCP)
                  } 

MESSAGE_STATUS = { "ACK", "UNCONFRIMED"} # MORE TO COME PROBABLY     , "ALERT_ACK" - in 2.5
#  UDP is used for short control and real-time notification messages, including registration,
# subscriptions, emergency alerts, alert acknowledgments, incident updates, and user statuS reports.

#For simplicity, the basic project assumes that a client-provided role is valid. 
# Authentication and authorization mechanisms are not required, but may be 
# implemented as bonus features.


str : Incident_ID, Name, Location, Title, Description, Category, Severity, Timestamp, Status

def create_incident(incident_id, name, location, title, description, category, severity, timestamp, status):
    incident = {
        "Incident_ID": incident_id,
        "Name": name,
        "Location": location,
        "Title": title,
        "Description": description,
        "Category": category,
        "Severity": severity,
        "Timestamp": timestamp,
        "Status": status
    }
    return incident

def update_incident(incident, **kwargs):    
    for key, value in kwargs.items():
        if key in incident:
            incident[key] = value
    return incident

def get_incident_info(incident):
    return incident

def delete_incident(incident):
    incident.clear()
    return incident

def list_incidents(incidents):
    return incidents

def filter_incidents_by_location(incidents, location):
    return [incident for incident in incidents if incident["Location"] == location]

def filter_incidents_by_category(incidents, category):
    return [incident for incident in incidents if incident["Category"] == category]

def filter_incidents_by_severity(incidents, severity):
    return [incident for incident in incidents if incident["Severity"] == severity]

def filter_incidents_by_status(incidents, status):
    return [incident for incident in incidents if incident["Status"] == status]

def filter_incidents_by_time_range(incidents, start_time, end_time):
    return [incident for incident in incidents if start_time <= incident["Timestamp"] <= end_time]

def sort_incidents_by_time(incidents, ascending=True):
    return sorted(incidents, key=lambda x: x["Timestamp"], reverse=not ascending)

def sort_incidents_by_severity(incidents, ascending=True):
    severity_order = { "PUBLISH_ALERT": 1, "ALERT": 2, "WARNING": 3, "ADVISORY": 4, "CRITICAL": 5 }
    return sorted(incidents, key=lambda x: severity_order.get(x["Severity"], float('inf')), reverse=not ascending)  









