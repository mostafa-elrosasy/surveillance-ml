from face import Face
from face_embedder import euclidean


class ColoredList:
    THRESHOLD = 100
    def __init__(self) -> None:
        self.faces = []

    def search(self, face: Face):
        closest = min(self.faces, key=lambda other:euclidean(face, other))

        if closest is None:
            return False
        dist = euclidean(closest, face)

        return dist < ColoredList.THRESHOLD, dist

    def add_face(self, face: Face):
        self.faces.append(face)

    def remove_face(self, face: Face):
        self.faces.remove(face)

    
list1 = [1,2,3,4,5]

