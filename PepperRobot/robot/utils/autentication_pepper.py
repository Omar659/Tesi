class Authenticator:
    def __init__(self, username, password):
        """
        Initializes a new Authenticator instance.

        Parameters:
        - username (str): The username for authentication.
        - password (str): The password for authentication.
        """
        self.username = username
        self.password = password

    def initialAuthData(self):
        """
        Provides the initial authentication data.

        Returns:
        - dict: A dictionary containing the authentication details with keys 'user' and 'token'.
        """
        return {'user': self.username, 'token': self.password}


class AuthenticatorFactory:
    def __init__(self, username, password):
        """
        Initializes a new AuthenticatorFactory instance.

        Parameters:
        - username (str): The username for creating the Authenticator.
        - password (str): The password for creating the Authenticator.
        """
        self.username = username
        self.password = password

    def newAuthenticator(self):
        """
        Creates a new Authenticator object.

        Returns:
        - Authenticator: An instance of the Authenticator class.
        """
        return Authenticator(self.username, self.password)