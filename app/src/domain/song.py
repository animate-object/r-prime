class Song:
    """
    For storing lyrical text and associated metadata
    """
    def __init__(self, X, Y, artist="", title="", collaborators=[], year=None, **kwargs):
        self.artist = artist
        self.title = title
        self.collaborators = collaborators
        self.year = year
        self.additional_meta_data = kwargs

        # sequence data for models to consume
        # this class is agnostic to the actual X Y values (character or word level encoding)
        self.X = X  # X comprises sequences of data x[1 . . . n]
        self.Y = Y  # Y comprises data y[1 . . . n] such that y[n] is the value following the sequence of values x[n]
