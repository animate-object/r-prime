class Song:
    """
    For storing lyrical text and associated metadata
    """
    def __init__(self, text, artist="", title="", collaborators=[], year=None, **kwargs):
        self.artist = artist
        self.title = title
        self.collaborators = collaborators
        self.year = year
        self.additional_meta_data = kwargs
        self.text = text
