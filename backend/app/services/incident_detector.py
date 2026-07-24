def detect_incident(rca):

    incidents = []

    for item in rca:

        # CSV Analyzer
        if "type" in item:
            incident_name = item["type"]

        # LOG Analyzer
        else:
            incident_name = item["error"]

        severity = item["severity"]

        if severity == "CRITICAL":
            priority = "P1"

        elif severity == "HIGH":
            priority = "P1"
        elif severity == "MEDIUM":
            priority = "P2"
        else:
            priority = "P3"

        incidents.append({
            "incident": incident_name,
            "priority": priority,
            "severity": severity
        })

    return incidents