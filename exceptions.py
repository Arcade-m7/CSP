class CantGetAddressInfo(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class PasswordError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)