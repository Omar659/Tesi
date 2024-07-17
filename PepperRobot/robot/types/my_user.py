class User():
    def __init__(self, name, last_seen):
        self.name = name
        self.last_seen = last_seen
        
    def to_dict(self):
        return {
            "name": self.name,
            "lastSeen": self.last_seen.strftime('%Y-%m-%d')
        }

    def __str__(self):        
        return "Name: {}\nLast seen: {}".format(self.name, self.last_seen)

    def __repr__(self):
        return "Name: {}\nLast seen: {}".format(self.name, self.last_seen)