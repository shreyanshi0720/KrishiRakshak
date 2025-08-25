import numpy as np
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

class DiseaseDetectionModel:
    def __init__(self):
        # Load your trained model here
        # Example for TensorFlow:
        # self.model = tf.keras.models.load_model('path/to/your/model.h5')
        self.labels = ['Apple Scab', 'Powdery Mildew', 'Early Blight', 'Late Blight', 'Leaf Spot', 'Healthy']
        logger.info("ML model initialized")
    
    def preprocess_image(self, image_data):
        #Preprocessing image
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        image = image.resize((224, 224))  # Adjust based on your model's expected input
        image_array = np.array(image)
        image_array = np.expand_dims(image_array, axis=0)
        # Normalize if your model expects normalized inputs
        image_array = image_array / 255.0
        return image_array
    
    def predict(self, image_data):
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_data)
            
            # Mock prediction - replace with actual model prediction
            # prediction = self.model.predict(processed_image)
            # predicted_class = np.argmax(prediction, axis=1)[0]
            # confidence = prediction[0][predicted_class]
            
            # For demo purposes, return a mock prediction
            predicted_class = np.random.randint(0, len(self.labels))
            confidence = np.random.uniform(0.7, 0.99)
            
            disease_name = self.labels[predicted_class]
            
            return disease_name, float(confidence)
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise Exception("Error during prediction")