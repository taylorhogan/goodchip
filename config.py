class Config:
    def __init__ (self) -> None:
        self.params = {
            "max_components":100,
            "num_designs": 1,
            "component_ds" : 32,
            "pin_ds": 8
        }

    def get_max_components (self) -> int:
        return self.params["max_components"]

    def get_num_designs(self) -> int:
        return self.params["num_designs"]

    def get_component_ds(self) -> int:
        return self.params["component_ds"]

    def get_pin_ds(self) -> int:
        return self.params["pin_ds"]



