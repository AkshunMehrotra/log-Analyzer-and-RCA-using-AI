RCA_RULES = {
    "DATABASE": {
        "root_cause": "Database connectivity issue.",
        "possible_reasons": [
            "Database server unavailable",
            "Connection timeout",
            "Deadlock",
            "Connection pool exhausted"
        ],
        "recommendations": [
            "Check database server health",
            "Review slow queries",
            "Increase connection pool",
            "Check DB logs"
        ],
        "severity": "HIGH"
    },

    "API": {
        "root_cause": "External API failure.",
        "possible_reasons": [
            "Service unavailable (503)",
            "API timeout",
            "Network issue"
        ],
        "recommendations": [
            "Retry API request",
            "Check API health",
            "Verify API gateway"
        ],
        "severity": "HIGH"
    },

    "AUTH": {
        "root_cause": "Authentication failure.",
        "possible_reasons": [
            "Invalid credentials",
            "Expired password",
            "Account locked"
        ],
        "recommendations": [
            "Verify credentials",
            "Reset password",
            "Unlock account"
        ],
        "severity": "MEDIUM"
    },

    "SECURITY": {
        "root_cause": "Security policy violation.",
        "possible_reasons": [
            "Multiple failed logins",
            "Possible brute-force attack"
        ],
        "recommendations": [
            "Review security logs",
            "Enable MFA",
            "Block suspicious IPs"
        ],
        "severity": "HIGH"
    },

    "SPEECHENGINE": {
        "root_cause": "Speech service timeout.",
        "possible_reasons": [
            "Speech engine unavailable",
            "Network latency"
        ],
        "recommendations": [
            "Restart speech service",
            "Use backup speech engine"
        ],
        "severity": "MEDIUM"
    },

    "SYSTEM": {
        "root_cause": "Application process crashed.",
        "possible_reasons": [
            "Unhandled exception",
            "Memory leak",
            "CPU overload"
        ],
        "recommendations": [
            "Restart service",
            "Check crash logs",
            "Monitor memory usage"
        ],
        "severity": "CRITICAL"
    },

    "NETWORK": {
        "root_cause": "Network connectivity issue.",
        "possible_reasons": [
            "CRM server unreachable",
            "Packet loss",
            "DNS failure"
        ],
        "recommendations": [
            "Check network connectivity",
            "Restart network service",
            "Verify firewall"
        ],
        "severity": "HIGH"
    }
}


def analyze_errors(errors):

    results = []

    for error in errors:

        message = error["message"].upper()

        matched = False

        for keyword, details in RCA_RULES.items():

            if keyword in message:

                results.append({
                    "timestamp": error["timestamp"],
                    "error": error["message"],
                    "root_cause": details["root_cause"],
                    "possible_reasons": details["possible_reasons"],
                    "recommendations": details["recommendations"],
                    "severity": details["severity"]
                })

                matched = True
                break

        if not matched:

            results.append({
                "timestamp": error["timestamp"],
                "error": error["message"],
                "root_cause": "Unknown error.",
                "possible_reasons": [
                    "Manual investigation required."
                ],
                "recommendations": [
                    "Check application logs.",
                    "Contact support team."
                ],
                "severity": "LOW"
            })

    return results