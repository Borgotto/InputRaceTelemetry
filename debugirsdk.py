class IRSDK():
    def __init__(self, parse_yaml_async=False) -> None:
        self.is_initialized = True
        self.is_connected = True
        self.FrameRate = 59.98
        self.Throttle = 1.0
        self.Brake = 0.93
        self.Clutch = 0.75
        self.SteeringWheelAngle = 3.333
        self.Speed = 200
        self.Gear = 0
        self.DisplayUnits = 0
        self.SteeringWheelAngleMax = 7.2
    def startup(self):
        return True
    def __getitem__(self, key):
        return getattr(self, key)