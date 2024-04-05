from django.conf import settings
import boto3
from PIL import Image
from io import BytesIO



def process_image(image_data):
        try:
                print(settings.AWS_STORAGE_BUCKET_NAME, settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_S3_REGION_NAME,settings.AWS_STORAGE_BUCKET_NAME)
                # Process the image 
                image = Image.open(image_data)
                output = BytesIO()
                image.save(output, format='WEBP', quality=100)
                output.seek(0)
                
                #Prepare the image ro be uploaded to aws S3
                file_name = f"{image_data.name.split('.')[0]}.webp"
                content_type = 'image/webp'
                
                 # Get an S3 client
                s3 = boto3.client('s3', 
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME)

                # Upload the image to S3
                s3.upload_fileobj(
                output,
                settings.AWS_STORAGE_BUCKET_NAME,  
                file_name,  
                ExtraArgs={'ContentType': content_type, 'ACL': 'public-read'}
                )

                # The URL to access the file on S3
                file_url = f"{file_name}"

                print('Image processed and uploaded to S3:', file_url)
                return file_url
        except Exception as e:
                print("Error processing and uploading image: ", e)
                return None