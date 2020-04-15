from attr import dataclass

HEADSET, CONTROLLER_1, CONTROLLER_2 = "hmd", "controller-1", "controller-2"


@dataclass
class Button:
    session_id: str
    user_id: str
    timestamp: int
    controller_id: str
    trigger: int
    trackpad_x: int
    trackpad_y: int
    button_pressed: int
    button_touched: int
    menu_button: bool
    trackpad_pressed: bool
    trackpad_touched: bool
    grip_button: bool

    @staticmethod
    def from_dict(obj: dict) -> 'Button':
        session_id = obj["session_id"]
        user_id = obj["user_id"]
        timestamp = obj["timestamp"]
        controller_id = obj["controller_id"]
        trigger = obj["trigger"]
        trackpad_x = obj["trackpad_x"]
        trackpad_y = obj["trackpad_y"]
        try:
            button_pressed = obj["button_pressed"]
        except KeyError:
            button_pressed = obj["ulButtonPressed"]
        try:
            button_touched = obj["button_touched"]
        except KeyError:
            button_touched = obj["ulButtonPressed"]
        menu_button = obj["menu_button"]
        trackpad_pressed = obj["trackpad_pressed"]
        trackpad_touched = obj["trackpad_touched"]
        grip_button = obj["grip_button"]
        return Button(session_id, user_id, timestamp, controller_id, trigger, trackpad_x, trackpad_y, button_pressed,
                      button_touched, menu_button, trackpad_pressed, trackpad_touched, grip_button)
