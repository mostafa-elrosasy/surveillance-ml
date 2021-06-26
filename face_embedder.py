# function for face detection with mtcnn
from face import Face
from PIL import Image
from numpy import asarray
from mtcnn.mtcnn import MTCNN
from keras.models import load_model
import numpy as np
from numpy import expand_dims
import cv2
# TODO to improve performance make this a class to reuse the MTCNN and the model

# IMPORTANT, THIS CLASS USES A SHARED MODEL ACROSS INSTANCES AND THUS NOT THREAD SAFE
class Face_Embedder:
    __model = load_model('facenet_keras.h5')
    __detector = MTCNN()

    def extract_faces_from_file(filename, required_size=(160, 160)):
        image = Image.open(filename)
        # convert to RGB, if needed
        image = image.convert('RGB')
        # convert to array
        pixels = asarray(image)
        return Face_Embedder.extract_faces(pixels, required_size)


    def extract_faces_from_mat(img, required_size=(160, 160)):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return Face_Embedder.extract_faces(img, required_size)

    # extract a single face from a given photograph
    # can be edited to extract all faces
    # returns None if no faces found in image
    # @pixels has to be a numpy array of the image with rgb, it can be of any size
    def extract_faces(pixels, required_size=(160, 160)):
        # detect faces in the image
        results = Face_Embedder.__detector.detect_faces(pixels)
        if not results:
            return []
        return Face_Embedder.get_faces_from_results(pixels, results, required_size)

    def get_faces_from_results(pixels, results, required_size=(160, 160)):
        faces = []
        for result in results:
            x1, y1, width, height = result['box']
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height
            extracted_face = pixels[y1:y2, x1:x2]
            # resize pixels to the model size
            image = Image.fromarray(extracted_face)
            image = image.resize(required_size)
            face_array = asarray(image)

            embed = Face_Embedder.get_embed(face_array)
            
            faces.append(Face(face_array, (x1,y1,x2,y2), embed))
        return faces
    # get the face embedding for one face
    def get_embed(face_array):
        # scale pixel values
        face_array = face_array.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_array.mean(), face_array.std()
        face_array = (face_array - mean) / std
        # transform face into one sample
        samples = expand_dims(face_array, axis=0)

        # make prediction to get embedding, use model.predict for big batches only
        # yhat = Face_Embedder.model.predict(samples)
        yhat = Face_Embedder.__model(samples)
        return yhat[0]


def euclidean(face1: Face, face2: Face) -> float:
    return np.sum(np.square(face1.embed - face2.embed))

def cosine(face1: Face, face2: Face) -> float:
    return np.sum(face1.embed * face2.embed)




if __name__ == "__main__":
    print("******************************")

