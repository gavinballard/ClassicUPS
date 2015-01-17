from dict2xml import dict2xml


class UPSAddress(object):
    """
    The UPSAddress class represents a generic address.
    """


    ###
    # INSTANCE VARIABLES
    # Declare attributes for the address object.
    ###

    line1 = None
    line2 = None
    line3 = None
    city = None
    state_province_code = None
    postal_code = None
    country_code = None

    def __init__(self, *args, **kwargs):
        """
        Initialise this address, overriding default attributes as needed.
        """
        for key, value in kwargs.iteritems():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)

    def __unicode__(self):
        """
        Override the __unicode__() method so that the unicode() call inside dict2xml serializes this address correctly.
        """
        return dict2xml(self.to_dict())

    def to_dict(self):
        """
        Convert this Address to a dict object suitable for use with the UPS XML API.
        """
        return {
            'AddressLine1': self.line1,
            'AddressLine2': self.line2,
            'AddressLine3': self.line3,
            'City': self.city,
            'StateProvinceCode': self.state_province_code,
            'PostalCode': self.postal_code,
            'CountryCode': self.country_code,
        }
