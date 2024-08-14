class Config:
    def __init__(self) -> None:
        self.params = {
            "max_components": 144,
            "num_designs": 10,
            "component_ds": 32,
            "pin_ds": 8,
            "same_design_size": True,
            "random_changes": False

        }

    def get_max_components(self) -> int:
        return self.params["max_components"]

    def get_num_designs(self) -> int:
        return self.params["num_designs"]

    def get_component_ds(self) -> int:
        return self.params["component_ds"]

    def get_pin_ds(self) -> int:
        return self.params["pin_ds"]

    def get_same_design_size(self) -> bool:
        return self.params["same_design_size"]

    def get_random_changes(self) -> bool:
        return self.params["random_changes"]
