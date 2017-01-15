from __future__ import absolute_import
from django.utils.translation import ugettext as _
from zerver.lib.actions import check_send_message
from zerver.lib.response import json_success, json_error
from zerver.decorator import REQ, has_request_variables, api_key_only_webhook_view
from zerver.lib.validator import check_dict, check_string

from zerver.models import Client, UserProfile

from django.http import HttpRequest, HttpResponse
from typing import Dict, Any, Iterable, Optional, Text

@api_key_only_webhook_view('HomeAssistant')
@has_request_variables
def api_homeassistant_webhook(request, user_profile, client,
                           payload=REQ(argument_type='body'),
                           stream=REQ(default='test'),
                           topic=REQ(default='Home Assistant')):
    # type: (HttpRequest, UserProfile, Client, Dict[str, Iterable[Dict[str, Any]]], Text, Optional[Text]) -> HttpResponse

    try:
        body = payload.message
    except KeyError as e:
        return json_error(_("Missing key {} in JSON").format(str(e)))

    check_send_message(user_profile, client, 'stream', [stream], topic, body)

    return json_success()