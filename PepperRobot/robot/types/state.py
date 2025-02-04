class State():
    def __init__(self, state_id, flag_pepper, flag_HMD, state_name, chosen_place, currentUser, hmdOpen, pepperAction, vr, can_talk):        
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
        - pepperAction (bool): A flag indicating whether Pepper is able to do an action (used to cooperate with HMD).
        """
        self.state_id = state_id
        self.flag_pepper = flag_pepper
        self.flag_HMD = flag_HMD
        self.state_name = state_name
        self.chosen_place = chosen_place
        self.currentUser = currentUser
        self.hmdOpen = hmdOpen
        self.pepperAction = pepperAction
        self.vr = vr
        self.can_talk = can_talk
        
    def to_dict(self):
        """
        Converts the State object to a dictionary.

        Returns:
        - dict: A dictionary representation of the State instance.
        """
        return {
            "stateId": (self.state_id),
            "flagPepper": (self.flag_pepper),
            "flagHMD": (self.flag_HMD),
            "stateName": (self.state_name),
            "chosenPlace": (self.chosen_place),
            "currentUser": (self.currentUser),
            "hmdOpen": (self.hmdOpen),
            "pepperAction": (self.pepperAction),
            "vr": (self.vr),
            "canTalk": (self.can_talk),
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
                HMD Open: {}
                Pepper Action: {}
                VR: {}
                Can Talk: {}'''.format(
                    str(self.state_id), 
                    str(self.flag_pepper), 
                    str(self.flag_HMD), 
                    str(self.state_name), 
                    str(self.chosen_place),
                    str(self.currentUser),
                    str(self.hmdOpen),
                    str(self.pepperAction),
                    str(self.vr),
                    str(self.can_talk)
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
                HMD open: {}
                Pepper Action: {}
                VR: {}
                Can Talk: {}'''.format(
                    repr(self.state_id), 
                    repr(self.flag_pepper), 
                    repr(self.flag_HMD), 
                    repr(self.state_name), 
                    repr(self.chosen_place),
                    repr(self.currentUser),
                    repr(self.hmdOpen),
                    repr(self.pepperAction),
                    repr(self.vr),
                    repr(self.can_talk)
                    )