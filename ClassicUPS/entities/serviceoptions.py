from .entity import UPSEntity


class UPSServiceOptions(UPSEntity):
    """
    The UPSServiceOptions class represents the service options available when fetching rates.
    """

    ##
    # CONSTANTS
    ##

    # Delivery confirmation options.
    DELIVERY_CONFIRMATION_SIGNATURE_REQUIRED = '1'
    DELIVERY_CONFIRMATION_ADULT_SIGNATURE_REQUIRED = '2'

    ##
    # ENTITY ATTRIBUTES
    ##

    saturday_pickup = False
    saturday_delivery = False
    delivery_confirmation = None

    def to_dict(self):
        """
        Convert these ServiceOptions to a dict object suitable for use with the UPS XML API.
        """
        d = {
            # 'OnCallAir': {
            #     'Schedule': {
            #         'PickupDay': '', # 01 - same day, 02 - future day
            #         'Method': '', # 01 - internet, 02 - phone
            #     }
            # },
            # Delivery options.
            # Special content indicators
        }

        # Flag Saturday pickup if present.
        if self.saturday_pickup:
            d['SaturdayPickup'] = ''

        # Flag Saturday delivery if present.
        if self.saturday_delivery:
            d['SaturdayDelivery'] = ''

        # Add delivery confirmation information if required.
        if self.delivery_confirmation is not None:
            d['DeliveryConfirmation'] = {
                'DCISType': self.delivery_confirmation,
            }

        return d
