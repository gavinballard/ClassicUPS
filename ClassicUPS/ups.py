import json
import urllib

import xmltodict
from dict2xml import dict2xml

from shipment import Shipment
from trackinginfo import TrackingInfo
from timeintransit import TimeInTransit
from rate import Rate


class UPSConnection(object):

    test_urls = {
        'track': 'https://wwwcie.ups.com/ups.app/xml/Track',
        'ship_confirm': 'https://wwwcie.ups.com/ups.app/xml/ShipConfirm',
        'ship_accept': 'https://wwwcie.ups.com/ups.app/xml/ShipAccept',
        'timeintransit': 'https://wwwcie.ups.com/ups.app/xml/TimeInTransit',
        'rate': 'https://wwwcie.ups.com/ups.app/xml/Rate',
    }

    production_urls = {
        'track': 'https://onlinetools.ups.com/ups.app/xml/Track',
        'ship_confirm': 'https://onlinetools.ups.com/ups.app/xml/ShipConfirm',
        'ship_accept': 'https://onlinetools.ups.com/ups.app/xml/ShipAccept',
        'timeintransit': 'https://onlinetools.ups.com/ups.app/xml/TimeInTransit',
        'rate': 'https://onlinetools.ups.com/ups.app/xml/Rate',
    }

    def __init__(self, license_number, user_id, password, shipper_number=None,
                 debug=False):

        self.license_number = license_number
        self.user_id = user_id
        self.password = password
        self.shipper_number = shipper_number
        self.debug = debug

    def _generate_xml(self, url_action, ups_request):
        access_request = {
            'AccessRequest': {
                'AccessLicenseNumber': self.license_number,
                'UserId': self.user_id,
                'Password': self.password,
            }
        }

        xml = u'''
        <?xml version="1.0"?>
        {access_request_xml}

        <?xml version="1.0"?>
        {api_xml}
        '''.format(
            request_type=url_action,
            access_request_xml=dict2xml(access_request),
            api_xml=dict2xml(ups_request),
        )

        return xml

    def _transmit_request(self, url_action, ups_request):
        url = self.production_urls[url_action]
        if self.debug:
            url = self.test_urls[url_action]

        xml = self._generate_xml(url_action, ups_request)
        resp = urllib.urlopen(url, xml.encode('ascii', 'xmlcharrefreplace'))\
                .read()

        return UPSResult(resp)

    def tracking_info(self, *args, **kwargs):
        return TrackingInfo(self, *args, **kwargs)

    def create_shipment(self, *args, **kwargs):
        return Shipment(self, *args, **kwargs)

    def time_in_transit(self, *args, **kwargs):
        return TimeInTransit(self, *args, **kwargs)

    def rate(self, *args, **kwargs):
        return Rate(self, *args, **kwargs)


class UPSResult(object):

    def __init__(self, response):
        self.response = response

    @property
    def xml_response(self):
        return self.response

    @property
    def dict_response(self):
        return json.loads(json.dumps(xmltodict.parse(self.xml_response)))
