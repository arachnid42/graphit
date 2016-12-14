import app.core.facility_handler
from app.parse import *


class JSONAssembler(object):
    """ Assembles visualization data JSON on request """

    @staticmethod
    def get_viz_json(force_update=False):

        # TODO: finish