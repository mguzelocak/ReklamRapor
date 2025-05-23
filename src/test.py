# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import time

from facebook_business.adobjects.serverside.action_source import ActionSource
from facebook_business.adobjects.serverside.content import Content
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.adobjects.serverside.delivery_category import DeliveryCategory
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.api import FacebookAdsApi
import requests
import os

access_token = f'<{os.environ["ACCESS_TOKEN"]}>'
pixel_id = f'{os.environ["PIXEL_ID"]}>'

FacebookAdsApi.init(access_token=access_token)

user_data = UserData(
    emails=['joe@eg.com'],
    phones=['12345678901', '14251234567'],
    # It is recommended to send Client IP and User Agent for Conversions API Events.
    client_ip_address=request.META.get('REMOTE_ADDR'),
    client_user_agent=request.headers['User-Agent'],
    fbc='fb.1.1554763741205.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890',
    fbp='fb.1.1558571054389.1098115397',
)

content = Content(
    product_id='product123',
    quantity=1,
    delivery_category=DeliveryCategory.HOME_DELIVERY,
)

custom_data = CustomData(
    contents=[content],
    currency='usd',
    value=123.45,
)

event = Event(
    event_name='Purchase',
    event_time=int(time.time()),
    user_data=user_data,
    custom_data=custom_data,
    event_source_url='http://jaspers-market.com/product/123',
    action_source=ActionSource.WEBSITE,
)

events = [event]

event_request = EventRequest(
    events=events,
    pixel_id=pixel_id,
)

event_response = event_request.execute()
print(event_response)