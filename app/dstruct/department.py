class BadInitParameters(Exception):
    pass


class Department(object):
    def __init__(self, label, points_vector, is_graph_vertex=True):
        if isinstance(points_vector, list) and len(points_vector) > 2 and \
                (isinstance(points_vector[0], tuple) or isinstance(points_vector[0], list)):
            self.label = label
            self.points_vector = points_vector
            self.is_graph_vertex = is_graph_vertex
            self.centroid = self.calculate_centroid()
        else:
            raise BadInitParameters("passed init parameters are not acceptable!")

    def calculate_centroid(self):
        """ Calculate a centroid (center) point of the department

        :return tuple x and y of the center point of the department

        """
        area = self.calculate_area()
        c_x, c_y = 0
        for p_ind in range(0, len(self.points_vector)):
            p_i = self.points_vector[p_ind]
            p_ip1 = self.points_vector[(p_ind+1)%len(self.points_vector)]

        return 42  # TODO:

    def calculate_area(self):
        """ Calculate an area of the department

        :return float area of the department

        """
        sum = 0
        for p_ind in range(0, len(self.points_vector)):
            p_i = self.points_vector[p_ind]
            p_ip1 = self.points_vector[(p_ind+1)%len(self.points_vector)]
            sum += p_i[0]*p_ip1[1] + p_ip1[0]*p_i[1]

        return sum / 2
