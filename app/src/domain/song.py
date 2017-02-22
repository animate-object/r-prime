class Song:
    """
    For storing lyrical text and associated metadata
    """
    def __init__(self, text, artist="", title="", collaborators=[], year=None):
        self.text = text
        self.artist = artist
        self.title = title
        self.collaborators = collaborators
        self.year = year