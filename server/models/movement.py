from attr import dataclass


@dataclass
class Movement:
    session_id: str
    user_id: str
    timestamp: int
    controller_id: str
    x: int
    y: int
    z: int
    yaw: str
    pitch: str
    roll: str
    r_x: str
    r_y: str
    r_z: str

    @staticmethod
    def from_dict(obj: dict) -> 'Movement':
        session_id = obj["session_id"]
        user_id = obj["user_id"]
        timestamp = obj["timestamp"]
        controller_id = obj["controller_id"]
        x = obj["x"]
        y = obj["y"]
        z = obj["z"]
        yaw = obj["yaw"]
        pitch = obj["pitch"]
        roll = obj["roll"]
        r_x = obj["r_x"]
        r_y = obj["r_y"]
        r_z = obj["r_z"]
        return Movement(session_id, user_id, timestamp, controller_id, x, y, z, yaw, pitch, roll, r_x, r_y, r_z)

    def to_dict(self) -> dict:
        result: dict = {"session_id": self.session_id, "user_id": self.user_id, "timestamp": self.timestamp,
                        "controller_id": self.controller_id, "x": self.x, "y": self.y, "z": self.z, "yaw": self.yaw,
                        "pitch": self.pitch, "roll": self.roll, "r_x": self.r_x, "r_y": self.r_y, "r_z": self.r_z}
        return result
