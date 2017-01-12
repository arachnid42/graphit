from app.core.facility_handler import *
from app.parse import *


class JSONAssembler(object):
    """ Assembles visualization data JSON on request """

    BASE_DICT = {'facility': {}, "edges": []}

    def __init__(self):
        """  """



    @staticmethod
    def get_viz_json(force_update=False):
        """ TODO """

        # init/restore Facility class
        facility = FacilityHandler()
