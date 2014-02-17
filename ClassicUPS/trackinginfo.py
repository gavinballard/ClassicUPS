from datetime import datetime

class TrackingInfo(object):

    def __init__(self, ups_conn, tracking_number):
        self.tracking_number = tracking_number

        tracking_request = {
            'TrackRequest': {
                'Request': {
                    'TransactionReference': {
                        'CustomerContext': 'Get tracking status',
                        'XpciVersion': '1.0',
                    },
                    'RequestAction': 'Track',
                    'RequestOption': 'activity',
                },
                'TrackingNumber': tracking_number,
            },
        }

        self.result = ups_conn._transmit_request('track', tracking_request)

    @property
    def shipment_activities(self):
        # Possible Status.StatusType.Code values:
        #   I: In Transit
        #   D: Delivered
        #   X: Exception
        #   P: Pickup
        #   M: Manifest

        shipment_activities = (self.result.dict_response['TrackResponse']
                                      ['Shipment']['Package']['Activity'])
        if type(shipment_activities) != list:
            shipment_activities = [shipment_activities]

        return shipment_activities

    @property
    def delivered(self):
        delivered = [x for x in self.shipment_activities
                     if x['Status']['StatusType']['Code'] == 'D']
        if delivered:
            return datetime.strptime(delivered[0]['Date'], '%Y%m%d')

    @property
    def in_transit(self):
        in_transit = [x for x in self.shipment_activities
                     if x['Status']['StatusType']['Code'] == 'I']

        return len(in_transit) > 0