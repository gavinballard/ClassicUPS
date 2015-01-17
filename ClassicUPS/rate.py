from datetime import datetime

class Rate(object):

    def __init__(self, ups_conn, shipper = None, ship_to = None, packages = None):
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
                    # 'Service': { # Optional
                    #     'Code': '',
                    # },
                    # 'NumOfPieces': '', # Optional, total # of pieces in all pallets.

                    # Add packages.
                    'Package': packages,

                    # 'ShipmentServiceOptions': {
                    #     'SaturdayPickup': '', # True if exists
                    #     'SaturdayDelivery': '', # True if exists
                    #     'OnCallAir': {
                    #         'Schedule': {
                    #             'PickupDay': '', # 01 - same day, 02 - future day
                    #             'Method': '', # 01 - internet, 02 - phone
                    #         }
                    #     },
                    #     'DeliveryConfirmation': {
                    #         'DCISType': '', # 1 - signature, 2 - adult
                    #     },
                    #
                    #     # Delivery options.
                    #     # Special content indicators
                    # },
                    #
                    # 'RateInformation': {
                    #     'NegotiatedRatesIndicator': '', # presence, adds rates n stuff?
                    #     'RateChartIndicator': '', # presences, does something
                    #     'RatingMethodRequestedIndicator': '', # presence, return more information on calc. methods
                    # },
                },
            }
        }

        # Perform the request.
        self.result = ups_conn._transmit_request('rate', rate_request)
