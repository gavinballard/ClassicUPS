from dict2xml import dict2xml


class UPSEntity(object):
    """
    The UPSEntity class is an abstract base class for entities.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialise this entity, overriding default attributes as needed.
        """
        super(UPSEntity, self).__init__()
        for key, value in kwargs.iteritems():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)

    def __unicode__(self):
        """
        Override the __unicode__() method so that the unicode() call inside dict2xml serializes this entity correctly.
        """
        return dict2xml(self.to_dict())

    def to_dict(self):
        """
        All subclasses must implement a to_dict() method.
        """
        raise NotImplementedError
