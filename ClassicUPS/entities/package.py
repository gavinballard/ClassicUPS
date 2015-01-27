from .entity import UPSEntity


class UPSPackage(UPSEntity):
    """
    The UPSPackage class represents a single package to be used when calculating rates.
    """

    ##
    # CONSTANTS
    ##

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

    def __init__(self, *args, **kwargs):
        """
        Set entity defaults on initialisation.
        They may be overridden by the base UPSEntity __init__ implementation.
        """
        self.packaging_type = UPSPackage.PACKAGING_TYPE_PACKAGE

        self.dimensions = [0, 0, 0] # Length, width, height.
        self.dimensions_unit = UPSPackage.DIMENSIONS_UNIT_IN

        self.weight = 0.0
        self.weight_unit = UPSPackage.WEIGHT_UNIT_LBS

        self.currency = UPSPackage.CURRENCY_USD
        self.value = 0.0

        super(UPSPackage, self).__init__(*args, **kwargs)

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
                'Length': str(length),
                'Width': str(width),
                'Height': str(height),
            },
            'PackageWeight': {
                'UnitOfMeasurement': {
                    'Code': self.weight_unit,
                },
                'Weight': str(self.weight),
            },
            'PackageServiceOptions': {
                'InsuredValue': {
                    'CurrencyCode': self.currency,
                    'MonetaryValue': str(self.value),
                }
            }
        }
