from attr import dataclass


@dataclass
class User:
    data: str
    registration_started: int
    registration_finished: int
    _id: str

    @staticmethod
    def from_dict(obj: dict) -> 'User':
        try:
            _id = obj["_id"]
        except KeyError:
            _id = None
        data = obj["data"]
        registration_started = obj["registration_started"]
        registration_finished = obj["registration_finished"]
        return User(data, registration_started, registration_finished, _id)
