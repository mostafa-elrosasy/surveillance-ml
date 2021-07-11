class Face:
    def __init__(self, facearray, dims, embed) -> None:
        self.facearray = facearray
        # tuple of x1,y1,x2,y2
        self.dims = dims
        self.embed = embed
        self.id = -1
    def setID(self, id):
        self.id = id