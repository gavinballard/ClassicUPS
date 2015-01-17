from .entity import UPSEntity


class UPSAddress(UPSEntity):
    """
    The UPSAddress class represents a generic address, used in many places by UPS services.
    """

    ##
    # CONSTANTS
    ##

    # Known country codes.
    COUNTRY_CODE_US = 'US'

    ##
    # ENTITY ATTRIBUTES
    ##

    line1 = None
    line2 = None
    line3 = None
    city = None
    state_province_code = None
    postal_code = None
    country_code = COUNTRY_CODE_US

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
