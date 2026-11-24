# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "ev_battery_swap"
app_title = "Frappe Ev Battery Swap Telematics Engine"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Ev Battery Swap Telematics Engine - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/ev_battery_swap/css/ev_battery_swap.bundle.css"
app_include_js = "/assets/ev_battery_swap/js/ev_battery_swap.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Ev Battery Swap Telematics Engine Entry": {
        "validate": "ev_battery_swap.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "ev_battery_swap.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "ev_battery_swap.tasks.hourly_sync"
    ],
    "daily": [
        "ev_battery_swap.tasks.daily_reconciliation"
    ],
    "weekly": [
        "ev_battery_swap.tasks.weekly_digest"
    ]
}
