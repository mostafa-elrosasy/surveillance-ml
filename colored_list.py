from face import Face
from face_embedder import euclidean


class ColoredList:
    THRESHOLD = 100
    def __init__(self) -> None:
        self.faces = []

    def search(self, face: Face):
        if len(self.faces) == 0:
            return False, 0, 0

        closest = min(self.faces, key=lambda other:euclidean(face, other))

        if closest is None:
            return False, 0, 0
        dist = euclidean(closest, face)

        return dist < ColoredList.THRESHOLD, dist, closest.id

    def add_face(self, face: Face):
        self.faces.append(face)

    def remove_face(self, face: Face):
        self.faces.remove(face)

    
list1 = [1,2,3,4,5]

