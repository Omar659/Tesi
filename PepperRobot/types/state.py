class State():
    def __init__(self, state_id, flag_pepper, flag_HMD, state_name, chosen_place):
        self.state_id = state_id
        self.flag_pepper = flag_pepper
        self.flag_HMD = flag_HMD
        self.state_name = state_name
        self.chosen_place = chosen_place
        
    def to_dict(self):
        return {
            "stateId": self.state_id,
            "flagPepper": self.flag_pepper,
            "flagHMD": self.flag_HMD,
            "stateName": self.state_name,
            "chosenPlace": self.chosen_place
        }

    def __str__(self):        
        return "State ID: {}\nFlag Pepper: {}\nFlag HMD: {}\nState Name: {}\nChosen Place: {}".format(
            self.state_id, self.flag_pepper, self.flag_HMD, self.state_name, self.chosen_place
        )

    def __repr__(self):
        return "State ID: {}\nFlag Pepper: {}\nFlag HMD: {}\nState Name: {}\nChosen Place: {}".format(
            self.state_id, self.flag_pepper, self.flag_HMD, self.state_name, self.chosen_place
        )