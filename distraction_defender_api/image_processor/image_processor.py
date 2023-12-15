from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def process_image(self, image_data):
        # Process the image and return the path to the processed image
        image = Image.open(image_data)
        output = BytesIO()
        image = image.resize((300, 300))
        image.save(output, format='WEBP', quality=100)
        output.seek(0)
        processed_image = InMemoryUploadedFile(output, 'ImageField', "%s.webp" % image_data.name.split('.')[0], 'image/webp', output.tell(), None)
        return processed_image