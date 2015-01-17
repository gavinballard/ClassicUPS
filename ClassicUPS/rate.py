# Currently, these are just for shipments originating in the US.
SHIPPING_SERVICES = {
    '01': 'Next Day Air',
    '02': 'Second Day Air',
    '03': 'Ground',
    '07': 'Worldwide Express',
    '08': 'Worldwide Expedited',
    '11': 'Standard',
    '12': 'Three-Day Select',
    '13': 'Next Day Air Saver',
    '14': 'Next Day Air Early A.M.',
    '54': 'Worldwide Express Plus',
    '59': 'Second Day Air A.M.',
    '65': 'Saver',
    '82': 'Today Standard',
    '83': 'Today Dedicated Courier',
    '84': 'Today Intercity',
    '85': 'Today Express',
    '86': 'Today Express Saver',
}

class Rate(object):

    def __init__(self, ups_conn, shipper = None, ship_to = None, packages = None, service_options = None):
        rate_request = {
            'RatingServiceSelectionRequest': {
                'Request': {
                    'TransactionReference': {
                        'CustomerContext': 'Rating and Service',
                        'XpciVersion': '1.0',
                    },
                    'RequestAction': 'Rate',
                    'RequestOption': 'Shop',
                },
                'PickupType': {
                    'Code': '01',
                    'Description': 'Daily Pickup',
                },
                'Shipment': {
                    'Description': 'Rate',
                    'Shipper': shipper or {},
                    'ShipTo': ship_to or {},
                    #'ShipFrom': {
                    #    'CompanyName': '',
                    #    'PhoneNumber': '',
                    #    'Address': {
                    #        'AddressLine1': '',
                    #        'AddressLine2': '',
                    #         'AddressLine3': '',
                    #         'City': '',
                    #         'StateProvinceCode': '', # Need for negotiated rates.
                    #         'PostalCode': '',
                    #         'CountryCode': '',
                    #     }
                    # },

                    # Add packages.
                    'Package': packages,

                    # Set service options.
                    'ShipmentServiceOptions': service_options,

                    # 'RateInformation': {
                    #     'NegotiatedRatesIndicator': '', # presence, adds rates n stuff?
                    #     'RateChartIndicator': '', # presences, does something
                    #     'RatingMethodRequestedIndicator': '', # presence, return more information on calc. methods
                    # }
                },
            }
        }

        # Perform the request.
        self.result = ups_conn._transmit_request('rate', rate_request)

    @property
    def rates(self):
        """
        Extract the returned rates from the result.
        """
        rates = []
        try:
            for rated_shipment in self.result.dict_response['RatingServiceSelectionResponse']['RatedShipment']:
                service_code = rated_shipment['Service']['Code']
                rates.append({
                    'service_code': service_code,
                    'service_name': SHIPPING_SERVICES.get(service_code, service_code),
                    'cost_transportation': rated_shipment['TransportationCharges']['MonetaryValue'],
                    'cost_other': rated_shipment['ServiceOptionsCharges']['MonetaryValue'],
                    'cost_total': rated_shipment['TotalCharges']['MonetaryValue'],
                    'currency': rated_shipment['TotalCharges']['CurrencyCode'],
                })
        except KeyError:
            return []
        return rates
