from dict2xml import dict2xml


class UPSPackage(object):
    """
    The UPSPackage class represents a single package to be used when calculating rates.
    """


    ###
    # CONSTANTS
    # Fixed values for various aspects of packaging.
    ###

    # Available packaging types.
    PACKAGING_TYPE_UNKNOWN              = '00'
    PACKAGING_TYPE_UPS_LETTER           = '01'
    PACKAGING_TYPE_PACKAGE              = '02'
    PACKAGING_TYPE_TUBE                 = '03'
    PACKAGING_TYPE_PAK                  = '04'
    PACKAGING_TYPE_EXPRESS_BOX          = '21'
    PACKAGING_TYPE_25KG_BOX             = '24'
    PACKAGING_TYPE_10KG_BOX             = '25'
    PACKAGING_TYPE_PALLET               = '30'
    PACKAGING_TYPE_SMALL_EXPRESS_BOX    = '2a'
    PACKAGING_TYPE_MEDIUM_EXPRESS_BOX   = '2b'
    PACKAGING_TYPE_LARGE_EXPRESS_BOX    = '2c'

    # Available dimension units.
    DIMENSIONS_UNIT_CM = 'CM'
    DIMENSIONS_UNIT_IN = 'IN'

    # Available weight units.
    WEIGHT_UNIT_KGS = 'KGS'
    WEIGHT_UNIT_LBS = 'LBS'

    # Available currencies.
    CURRENCY_USD = 'USD'

    #SERVICE_CODE_NEXT_DAY_AIR_EARLY = '14'


    ###
    # INSTANCE VARIABLES
    # Declare attributes for the package object and set defaults where appropriate.
    ###

    packaging_type = PACKAGING_TYPE_PACKAGE

    dimensions = [0, 0, 0] # Length, width, height.
    dimensions_unit = DIMENSIONS_UNIT_IN

    weight = 0.0
    weight_unit = WEIGHT_UNIT_LBS

    currency = CURRENCY_USD
    value = 0.0

    def __init__(self, *args, **kwargs):
        """
        Initialise this package, overriding default attributes as needed.
        """
        for key, value in kwargs.iteritems():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)

    def __unicode__(self):
        """
        Override the __unicode__() method so that the unicode() call inside dict2xml serializes this package correctly.
        """
        return dict2xml(self.to_dict())

    def to_dict(self):
        """
        Convert this Package to a dict object suitable for use with the UPS XML API.
        """
        length, width, height = self.dimensions
        return {
            'PackagingType': {
                'Code': self.packaging_type,
            },
            'Dimensions': {
                'UnitOfMeasurement': {
                    'Code': self.dimensions_unit,
                },
                'Length': length,
                'Width': width,
                'Height': height,
            },
            'PackageWeight': {
                'UnitOfMeasurement': {
                    'Code': self.weight_unit,
                },
                'Weight': self.weight,
            },
            'PackageServiceOptions': {
                'InsuredValue': {
                    'CurrencyCode': self.currency,
                    'MonetaryValue': self.value,
                }
            }
        }
