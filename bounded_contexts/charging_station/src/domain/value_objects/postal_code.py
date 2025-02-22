# charging_station/src/domain/value_objects/postal_code.py
class PostalCode:
    def __init__(self, plz: str) -> None:
        """
        Initializes a PostalCode value object.
        """
        plz = str(plz)
        if len(plz) != 5 or not plz.isdigit():
            raise ValueError("Invalid postal code")
        self.plz: str = plz
