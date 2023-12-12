import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def execute_blocker_script(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            from_hour = data.get('from_hour', None)
            to_hour = data.get('to_hour', None)
            websites_list = data.get('websites_list', [])
            new_websites_list = []
            for website in websites_list:
                new_website = "www.{}.com".format(website)
                new_website2 = "{}.com".format(website)
                new_websites_list.append(new_website)
                new_websites_list.append(new_website2)

            # Cargar el contenido del script
            current_directory = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(current_directory, 'blocker_script.py')
            with open(script_path, 'r') as file:
                script_content = file.read()

            # Reemplazar las partes relevantes del script
            script_content = script_content.replace("from_hour = data.get('from_hour', None)", f"from_hour = '{from_hour}'")
            script_content = script_content.replace("to_hour = data.get('to_hour', None)", f"to_hour = '{to_hour}'")
            script_content = script_content.replace("websites_list = data.get('websites_list', [])", f"websites_list = {new_websites_list}")

            # Ejecutar el script modificado
            exec(script_content)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})