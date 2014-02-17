from datetime import datetime

class TimeInTransit(object):

    def __init__(self, ups_conn, from_addr, to_addr, pickup_date, weight = None, value = None, weight_unit = 'LBS', value_unit = 'USD'):
        time_in_transit_request = {
            'TimeInTransitRequest': {
                'Request': {
                    'TransactionReference': {
                        'CustomerContext': 'Get time in transit',
                        'XpciVersion': '1.0',
                    },
                    'RequestAction': 'TimeInTransit',
                },
                'TransitFrom': {
                  'AddressArtifactFormat': {
                      'PostcodePrimaryLow': from_addr['postal_code'],
                      'CountryCode': from_addr['country']
                  }
                },
                'TransitTo': {
                  'AddressArtifactFormat': {
                      'PostcodePrimaryLow': to_addr['postal_code'],
                      'CountryCode': to_addr['country']
                  }
                },
                'PickupDate': pickup_date.strftime('%Y%m%d'),
                'InvoiceLineTotal': {
                    'CurrencyCode': value_unit,
                    'MonetaryValue': value
                },
                'ShipmentWeight': {
                    'UnitOfMeasurement': {
                        'Code': weight_unit,
                    },
                    'Weight': weight
                },
            }
        }

        self.result = ups_conn._transmit_request('timeintransit', time_in_transit_request)

        self.services = {}
        for service_summary in self.result.dict_response['TimeInTransitResponse']['TransitResponse']['ServiceSummary']:
          service_code = service_summary['Service']['Code']
          self.services[service_code] = service_summary

    def get_service(self, service_code):
      return self.services[service_code]

    def get_service_delivery_date(self, service_code):
      return datetime.strptime(self.get_service(service_code)['EstimatedArrival']['Date'], '%Y-%m-%d')