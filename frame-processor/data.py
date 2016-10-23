class FrameInputError(Exception):
    pass


class Frame(object):
    def __init__(self, frame_id, *args):
        if len(args) < 3:
            raise FrameInputError("Argument list is too short {}".format(len(args)))

        if not frame_id.isdecimal():
            raise FrameInputError("Argument is not numeric {}".format(frame_id))

        self._frame_id = frame_id
        self._parameters = args

    def __str__(self):
        return "{}:{} {} {}".format(self.frame_id, self.parameters[0], self.parameters[1], self.parameters[2])

    @property
    def frame_id(self):
        return self._frame_id

    @frame_id.setter
    def frame_id(self, frame_id):
        if frame_id.isdecimal():
            self._frame_id = frame_id

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        if len(parameters) > 2:
            self._parameters = parameters
