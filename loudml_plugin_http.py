# This file is part of LoudML HTTP plug-in. LoudML HTTP plug-in is free software:
# you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Red Mint Network

import logging
import requests

from loudml.api import Hook

from voluptuous import (
    All,
    Any,
    Invalid,
    Optional,
    Required,
    Schema,
    Url,
)

class HTTPHook(Hook):
    CONFIG_SCHEMA = Schema({
        Required('url'): Url(),
        Optional('method', default='POST'): Any('POST', 'PUT', 'GET'),
    })

    def send_request(self, data):
        try:
            requests.request(self.config['method'], self.config['url'], timeout=1, json=data)
        except requests.exceptions.RequestException as exn:
            logging.error("cannot notify %s: %s", self.config['url'], exn)

    def on_anomaly_start(
        self,
        model,
        dt,
        score,
        predicted,
        observed,
        *args,
        **kwargs
    ):
        self.send_request({
            'type': 'anomaly_start',
            'model': model,
            'timestamp': dt.timestamp(),
            'score': score,
            'predicted': predicted,
            'observed': observed,
        })

    def on_anomaly_end(
        self,
        model,
        dt,
        score,
        *args,
        **kwargs
    ):
        self.send_request({
            'type': 'anomaly_end',
            'model': model,
            'timestamp': dt.timestamp(),
            'score': score,
        })
