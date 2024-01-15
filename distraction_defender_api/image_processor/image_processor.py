from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def process_image(image_data):
        try:
                # Process the image and return the path to the processed image
                print("Processing image...")
                print('this is the image file', image_data)
                image = Image.open(image_data)
                output = BytesIO()
                image = image.resize((300, 300))
                image.save(output, format='WEBP', quality=100)
                output.seek(0)
                processed_image = InMemoryUploadedFile(output, 'ImageField', "%s.webp" % image_data.name.split('.')[0], 'image/webp', output.tell(), None)
                print('imagen processed image', processed_image)
                return processed_image
        except Exception as e:
                print("Error processing image: ", e)
                return None