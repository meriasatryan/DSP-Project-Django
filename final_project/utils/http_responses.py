"""
This module contains various functions for generating HTTP responses in Django.

Functions:

    data_status: Returns a HttpResponse object with given data and HTTP status code 200.
    notify_status: Returns a HttpResponse object with empty content and HTTP status code 200.
    data_status_creative_campaign: Returns a HttpResponse object with given data and HTTP status code 201.
    data_status_post: Returns a HttpResponse object with given data and HTTP status code 201. The data is wrapped in a
    dictionary with a "data" key and a "status" key with value "ok".
    ok_status: Returns a HttpResponse object with HTTP status code 200.
    success_status_post: Returns a HttpResponse object with HTTP status code 201 and a dictionary with a "status" key
    and value "ok".
    success_status_delete: Returns a HttpResponse object with HTTP status code 204 and a dictionary with a "status" key
    and value "ok".
    failed_status: Returns a HttpResponse object with a dictionary with a "status" key and value equal to the given
    status parameter and HTTP status code 404.
    no_bid_status: Returns a HttpResponse object with content "No bid" and HTTP status code 204.
"""

import json
from django.http.response import HttpResponse


# used
def data_status(data):
    return HttpResponse(
        json.dumps(data),
        status=200,
        content_type="application/json"
    )


# used
def notify_status():
    response_text = ""
    response = HttpResponse(response_text, content_type="text/plain;charset=UTF-8", status=200)
    return response


# used
def data_status_creative_campaign(data):
    return HttpResponse(
        json.dumps(data),
        status=201,
        content_type="application/json"
    )


def data_status_post(data):
    return HttpResponse(
        json.dumps({"data": data, "status": "ok"}),
        status=201,
        content_type="application/json"
    )


def ok_status():
    return HttpResponse(
        status=200, content_type="application/json"
    )


def success_status_post():
    return HttpResponse(
        json.dumps({"status": "ok"}), status=201, content_type="application/json"
    )


def success_status_delete():
    return HttpResponse(
        json.dumps({"status": "ok"}), status=204, content_type="application/json"
    )


def failed_status(status):
    return HttpResponse(
        json.dumps({"status": status}), status=404, content_type="application/json"
    )


def no_bid_status():
    return HttpResponse(
        "No bid",
        status=204,
        content_type="text/plain;charset=UTF-8"
    )
