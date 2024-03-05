import os
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def download_blocker_script(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            from_hour = int(data.get('from_hour', 0))
            to_hour = int(data.get('from_hour', 0))
            websites_list = data.get('websites_list', [])
            new_websites_list = []
            for website in websites_list:
                new_website = "www.{}.com".format(website)
                new_website2 = "{}.com".format(website)
                new_websites_list.append(new_website)
                new_websites_list.append(new_website2)

            # Lógica para cargar el contenido del script
            current_directory = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(current_directory, 'blocker_script.py')
            with open(script_path, 'r') as file:
                script_content = file.read()

            script_content_lines = script_content.split('\n')
            script_content_lines.insert(86, f"from_hour = '{from_hour}'")
            script_content_lines.insert(87, f"to_hour = '{to_hour}'")
            script_content_lines.insert(88, f"websites_list = {new_websites_list}")
            script_content = '\n'.join(script_content_lines)

            # Crear una respuesta para el navegador que descargará el script
            response = HttpResponse(content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=modified_blocker_script.py'
            response.write(script_content.encode('utf-8'))  # Asegúrate de codificar el contenido como bytes antes de escribirlo
            return response
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})