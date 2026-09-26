# -*- coding: utf-8 -*-
"""
API Client Module.

This module provides HTTP client functionality for interacting with
external services.

Copyright (c) 2026 Example Corp.
Author: Dev Team <dev@example.com>
License: MIT
"""

import requests
import json


API_BASE_URL = "https://api.example.com/v1"
AUTH_ENDPOINT = "/auth/token"

# 参考文档：https://docs.example.com/api-reference
# 项目主页：https://github.com/example/project


def fetch_user_data(user_id):
    """Fetch user data from the remote API."""
    headers = {"Authorization": "Bearer dummy-token"}
    url = f"{API_BASE_URL}/users/{user_id}"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def upload_report(report_data):
    """Upload a report to the server."""
    url = f"{API_BASE_URL}/reports"
    response = requests.post(url, json=report_data, timeout=60)
    return response.status_code == 200
