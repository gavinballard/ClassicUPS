from binascii import a2b_base64

class Shipment(object):
    SHIPPING_SERVICES = {
        '1dayair': '01',  # Next Day Air
        '2dayair': '02',  # 2nd Day Air
        'ground': '03',  # Ground
        'express': '07',  # Express
        'worldwide_expedited': '08',  # Expedited
        'standard': '11',  # UPS Standard
        '3_day_select': '12',  # 3 Day Select
        'next_day_air_saver': '13',  # Next Day Air Saver
        'next_day_air_early_am': '14',  # Next Day Air Early AM
        'express_plus': '54',  # Express Plus
        '2nd_day_air_am': '59',  # 2nd Day Air A.M.
        'ups_saver': '65',  # UPS Saver.
        'ups_today_standard': '82',  # UPS Today Standard
        'ups_today_dedicated_courier': '83',  # UPS Today Dedicated Courier
        'ups_today_intercity': '84',  # UPS Today Intercity
        'ups_today_express': '85',  # UPS Today Express
        'ups_today_express_saver': '86',  # UPS Today Express Saver.
    }

    DCIS_TYPES = {
        'no_signature': 1,
        'signature_required': 2,
        'adult_signature_required': 3,
        'usps_delivery_confiratmion': 4,
    }

    def __init__(self, ups_conn, from_addr, to_addr, dimensions, weight,
                 file_format='EPL', reference_numbers=None, shipping_service='ground',
                 description='', dimensions_unit='IN', weight_unit='LBS',
                 delivery_confirmation=None):

        self.file_format = file_format
        shipping_request = {
            'ShipmentConfirmRequest': {
                'Request': {
                    'TransactionReference': {
                        'CustomerContext': 'get new shipment',
                        'XpciVersion': '1.0001',
                    },
                    'RequestAction': 'ShipConfirm',
                    'RequestOption': 'nonvalidate',  # TODO: what does this mean?
                },
                'Shipment': {
                    'Shipper': {
                        'Name': from_addr['name'],
                        'AttentionName': from_addr.get('attn') if from_addr.get('attn') else from_addr['name'],
                        'PhoneNumber': from_addr['phone'],
                        'ShipperNumber': ups_conn.shipper_number,
                        'Address': {
                            'AddressLine1': from_addr['address1'],
                            'City': from_addr['city'],
                            'StateProvinceCode': from_addr['state'],
                            'CountryCode': from_addr['country'],
                            'PostalCode': from_addr['postal_code'],
                        },
                    },
                    'ShipTo' : {
                        'CompanyName': to_addr['name'],
                        'AttentionName': to_addr.get('attn') if to_addr.get('attn') else to_addr['name'],
                        'PhoneNumber': to_addr['phone'],
                        'Address': {
                            'AddressLine1': to_addr['address1'],
                            'City': to_addr['city'],
                            'StateProvinceCode': to_addr['state'],
                            'CountryCode': to_addr['country'],
                            'PostalCode': to_addr['postal_code'],
                            # 'ResidentialAddress': '',  # TODO: omit this if not residential
                        },
                    },
                    'Service' : {  # TODO: add new service types
                        'Code': self.SHIPPING_SERVICES[shipping_service],
                        'Description': shipping_service,
                    },
                    'PaymentInformation': {  # TODO: Other payment information
                        'Prepaid': {
                            'BillShipper': {
                                'AccountNumber': ups_conn.shipper_number,
                            },
                        },
                    },
                    'Package': {
                        'PackagingType': {
                            'Code': '02',  # Box (see http://www.ups.com/worldshiphelp/WS11/ENU/AppHelp/Codes/Package_Type_Codes.htm)
                        },
                        'Dimensions': {
                            'UnitOfMeasurement': {
                                'Code': dimensions_unit,
                                # default unit: inches (IN)
                            },
                            'Length': dimensions['length'],
                            'Width': dimensions['width'],
                            'Height': dimensions['height'],
                        },
                        'PackageWeight': {
                            'UnitOfMeasurement': {
                                'Code': weight_unit,
                                # default unit: pounds (LBS)
                            },
                            'Weight': weight,
                        },
                        'PackageServiceOptions': {},
                    },
                },
                'LabelSpecification': {  # TODO: support GIF and EPL (and others)
                    'LabelPrintMethod': {
                        'Code': file_format,
                    },
                    'LabelStockSize': {
                        'Width': '6',
                        'Height': '4',
                    },
                    'HTTPUserAgent': 'Mozilla/4.5',
                    'LabelImageFormat': {
                        'Code': 'GIF',
                    },
                },
            },
        }

        if delivery_confirmation:
            shipping_request['ShipmentConfirmRequest']['Shipment']['Package']['PackageServiceOptions']['DeliveryConfirmation'] = {
                'DCISType': self.DCIS_TYPES[delivery_confirmation]
            }

        if reference_numbers:
            reference_dict = []
            for ref_code, ref_number in enumerate(reference_numbers):
                # allow custom reference codes to be set by passing tuples.
                # according to the docs ("Shipping Package -- WebServices
                # 8/24/2013") ReferenceNumber/Code should hint on the type of
                # the reference number. a list of codes can be found in
                # appendix I (page 503) in the same document.
                try:
                    ref_code, ref_number = ref_number
                except:
                    pass

                reference_dict.append({
                    'Code': ref_code,
                    'Value': ref_number
                })
            #reference_dict[0]['BarCodeIndicator'] = '1'

            if from_addr['country'] == 'US' and to_addr['country'] == 'US':
                shipping_request['ShipmentConfirmRequest']['Shipment']['Package']['ReferenceNumber'] = reference_dict
            else:
                shipping_request['ShipmentConfirmRequest']['Shipment']['Description'] = description
                shipping_request['ShipmentConfirmRequest']['Shipment']['ReferenceNumber'] = reference_dict

        if from_addr.get('address2'):
            shipping_request['ShipmentConfirmRequest']['Shipment']['Shipper']['Address']['AddressLine2'] = from_addr['address2']

        if to_addr.get('company'):
            shipping_request['ShipmentConfirmRequest']['Shipment']['ShipTo']['CompanyName'] = to_addr['company']

        if to_addr.get('address2'):
            shipping_request['ShipmentConfirmRequest']['Shipment']['ShipTo']['Address']['AddressLine2'] = to_addr['address2']

        self.confirm_result = ups_conn._transmit_request('ship_confirm', shipping_request)

        if 'ShipmentDigest' not in self.confirm_result.dict_response['ShipmentConfirmResponse']:
            error_string = self.confirm_result.dict_response['ShipmentConfirmResponse']['Response']['Error']['ErrorDescription']
            raise Exception(error_string)

        confirm_result_digest = self.confirm_result.dict_response['ShipmentConfirmResponse']['ShipmentDigest']
        ship_accept_request = {
            'ShipmentAcceptRequest': {
                'Request': {
                    'TransactionReference': {
                        'CustomerContext': 'shipment accept reference',
                        'XpciVersion': '1.0001',
                    },
                    'RequestAction': 'ShipAccept',
                },
                'ShipmentDigest': confirm_result_digest,
            }
        }

        self.accept_result = ups_conn._transmit_request('ship_accept', ship_accept_request)

    @property
    def cost(self):
        total_cost = self.confirm_result.dict_response['ShipmentConfirmResponse']['ShipmentCharges']['TotalCharges']['MonetaryValue']
        return float(total_cost)

    @property
    def tracking_number(self):
        tracking_number = self.confirm_result.dict_response['ShipmentConfirmResponse']['ShipmentIdentificationNumber']
        return tracking_number

    def get_label(self):
        raw_epl = self.accept_result.dict_response['ShipmentAcceptResponse']['ShipmentResults']['PackageResults']['LabelImage']['GraphicImage']
        return a2b_base64(raw_epl)

    def save_label(self, fd):
        fd.write(self.get_label())
