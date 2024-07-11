from mock_interview import create_app
import dlib


# print(dlib.__version__+"sdcscsdcdsc")
app = create_app()

if __name__ == '__main__':
    app.run()

# shape_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
