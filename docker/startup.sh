#!/bin/bash

cd /home/frappe/frappe-bench

# Set default site
bench use 192.168.20.118

# Enable static file serving for both sites
bench --site 192.168.20.118 set-config serve_static_assets 1
bench --site lms.localhost set-config serve_static_assets 1

# Clear cache
bench --site 192.168.20.118 clear-cache
bench --site lms.localhost clear-cache

# Start gunicorn
exec gunicorn -b 0.0.0.0:8000 --workers 2 --threads 4 --timeout 120 frappe.app:application --preload
