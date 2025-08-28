from config.types import ResolutionEnum, VelocityEnum, DirectionEnum, ScanModeEnum


class InstrumentInfo:
    def __init__(self):
        self.resolution = ResolutionEnum.R_8_0

    def set_resolution(self, resolution: ResolutionEnum):
        self.resolution = resolution

    def get_resolution(self) -> ResolutionEnum:
        return self.resolution


instrumentInfo = InstrumentInfo()
