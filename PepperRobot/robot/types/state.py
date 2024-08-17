class State():
    def __init__(self, state_id, flag_pepper, flag_HMD, state_name, chosen_place, currentUser, hmdOpen):        
        """
        Initializes a new State instance.

        Parameters:
        - state_id (int): The unique identifier for the state.
        - flag_pepper (bool): A flag indicating some status related to 'Pepper'.
        - flag_HMD (bool): A flag indicating some status related to 'HMD'.
        - state_name (str): The name of the state.
        - chosen_place (str): The place chosen or associated with this state.
        - currentUser (User): The current user associated with the state.
        - hmdOpen (bool): A flag indicating whether the HMD is open or not.
        """
        self.state_id = state_id
        self.flag_pepper = flag_pepper
        self.flag_HMD = flag_HMD
        self.state_name = state_name
        self.chosen_place = chosen_place
        self.currentUser = currentUser
        self.hmdOpen = hmdOpen
        
    def to_dict(self):
        """
        Converts the State object to a dictionary.

        Returns:
        - dict: A dictionary representation of the State instance.
        """
        return {
            "stateId": self.state_id,
            "flagPepper": self.flag_pepper,
            "flagHMD": self.flag_HMD,
            "stateName": self.state_name,
            "chosenPlace": self.chosen_place,
            "currentUser": self.currentUser,
            "hmdOpen": self.hmdOpen
        }

    def __str__(self):
        """
        Provides a human-readable string representation of the State instance.

        Returns:
        - str: A formatted string showing the State object.
        """
        return '''
                State ID: {}
                Flag Pepper: {}
                Flag HMD: {}
                State Name: {}
                Chosen Place: {}
                Current User: {}
                HMD Open: {}'''.format(
                    str(self.state_id), 
                    str(self.flag_pepper), 
                    str(self.flag_HMD), 
                    str(self.state_name), 
                    str(self.chosen_place),
                    str(self.currentUser),
                    str(self.hmdOpen)
                    )

    def __repr__(self):
        """
        Provides a string representation of the State instance suitable for debugging.

        Returns:
        - str: A formatted string showing the internal representation of the state's attributes.
        """
        return '''
                State ID: {}
                Flag Pepper: {}
                Flag HMD: {}
                State Name: {}
                Chosen Place: {}
                Current User: {}
                HMD open: {}'''.format(
                    repr(self.state_id), 
                    repr(self.flag_pepper), 
                    repr(self.flag_HMD), 
                    repr(self.state_name), 
                    repr(self.chosen_place),
                    repr(self.currentUser),
                    repr(self.hmdOpen)
                    )