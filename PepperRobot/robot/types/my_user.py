class User():
    def __init__(self, name, last_seen, tutorial_seen):
        """
        Initializes a new User instance.

        Parameters:
        - name (str): The name of the user.
        - last_seen (datetime): The datetime when the user was last seen.
        - tutorial_seen (bool): Indicates if the user has seen the tutorial.
        """
        self.name = name
        self.last_seen = last_seen
        self.tutorial_seen = tutorial_seen
    
    def to_dict(self):
        """
        Converts the User object to a dictionary.

        Returns:
        - dict: A dictionary representation of the User instance.
        """
        return {
            "name": self.name,
            "lastSeen": self.last_seen.strftime('%Y-%m-%d'),
            "tutorial_seen": self.tutorial_seen
        }

    def __str__(self):
        """
        Provides a human-readable string representation of the User instance.

        Returns:
        - str: A formatted string showing the User object.
        """
        return '''
                Name: {}
                Last seen: {}
                Tutorial seen: {}'''.format(
                    str(self.name), 
                    str(self.last_seen),
                    str(self.tutorial_seen)
                )

    def __repr__(self):
        """
        Provides a string representation of the User instance suitable for debugging.

        Returns:
        - str: A formatted string showing the internal representation of the user's attributes.
        """
        return '''
                Name: {}
                Last seen: {}
                Tutorial seen: {}'''.format(
                    repr(self.name), 
                    repr(self.last_seen),
                    repr(self.tutorial_seen)
                )