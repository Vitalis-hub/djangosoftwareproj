import requests
import re
from django.http import JsonResponse
from django.views.generic import View
from django.conf import settings
from django.db.models import Q
from university.models import Entrance, Location


class GetDirectionsView(View):
    def get(self, request, *args, **kwargs):
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        if not origin:
            return JsonResponse({
                'success': 0,
                'message': 'Please provide start address.',
                'directions': None
            })
        elif not destination:
            return JsonResponse({
                'success': 0,
                'message': 'Please provide destination address.',
                'directions': None
            })
        query = {
            "origin": origin,
            "destination": destination,
            "key": settings.GOOGLE_API_KEY,
            "travel_mode": "WALKING",
        }
        url = "https://maps.googleapis.com/maps/api/directions/json?"
        response = requests.get(url, params=query)
        cleanr = re.compile('<.*?>')
        cleaned_direction_list = []
        try:
            for item in response.json()['routes'][0]['legs'][0]['steps']:
                raw_text = item['html_instructions']
                clean_text = re.sub(cleanr, '', raw_text)
                cleaned_direction_list.append(raw_text)
        except IndexError:
            return JsonResponse({
                'success': 0,
                'directions': "Sorry, we don't have any directions",
            })

        return JsonResponse({
            'success': 1,
            'directions': cleaned_direction_list,
        })


class GetAddressView(View):
    def get(self, request, *args, **kwargs):
        address = request.GET.get('address')
        query = {
            "address": address,
            "key": settings.GOOGLE_API_KEY,
        }
        url = "https://maps.googleapis.com/maps/api/geocode/json?"
        response = requests.get(url, params=query)
        if not address:
            return JsonResponse({
                'success': 0,
                'message': 'Please provide address',
                'address': None
            })
        return JsonResponse({
            'success': 1,
            'address': response.json().get('results')[0].get('formatted_address'),
        })


class SearchLocationsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        try:
            wheel_chair = bool(int(request.GET.get('wheel_chair')) == 1)
        except:
            wheel_chair = False
        results = []
        if query:
            entrance = Entrance.objects.filter(
                Q(address__icontains=query) |
                Q(orientation__icontains=query) |
                Q(location__name__icontains=query) |
                Q(location__campus__name__icontains=query) |
                Q(location__address__icontains=query)
            )
            if wheel_chair:
                entrance = entrance.filter(automatic_door=True)
        else:
            if wheel_chair:
                entrance = Entrance.objects.filter(automatic_door=True)[:10]
            else:
                entrance = Entrance.objects.all()[:10]
        for e in entrance:
            wheel_chair_icon = '<i class="wheelchair blue icon"></i>' if e.automatic_door else ''
            results.append(
                {
                    'title': f'{wheel_chair_icon} Entrance: {e.orientation}',
                    'description': e.description if e.description else '',
                    'address': e.direction_address
                }
            )
        return JsonResponse({"results": results})


class GetLocationElementsView(View):
    def get(self, request, *args, **kwargs):
        element_html_string = ""
        for location in Location.objects.all():
            entrances = Entrance.objects.filter(location=location)
            is_wh_acc = entrances.filter(automatic_door=True).exists()
            wheel_chair = "check circle outline green icon" if is_wh_acc else "close large red icon"
            is_wheel_chair = "wheelchair" if is_wh_acc else ""
            address_title = location.address
            category = location.category_value
            address = entrances.filter(default=True).first().direction_address
            image = location.image.url if location.image else ''
            title = str(location)
            description = location.description
            element_html_string = element_html_string + f"""
                  <div class="column {is_wheel_chair}">
                    <div class="content">
                        <table class="ui celled striped table">
                          <thead>
                            <tr class="center aligned"><th colspan="2">
                              {title}
                            </th>
                            <tr class="center aligned"><th colspan="2">
                                <img src="{image}" alt="Image" style="width:100%">
                            </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>Wheel Chair</td>
                              <td><i class="{wheel_chair}"></i></td>
                            </tr>
                            <tr>
                              <td>Category</td>
                              <td>{category}</td>
                            </tr>
                            <tr>
                              <td>Number Of Entrances</td>
                              <td>{entrances.count()}</td>
                            </tr>
                            <tr>
                              <td>Description</td>
                              <td>{description}</td>
                            </tr>
                            <tr>
                              <td>
                                <button class="ui tiny labeled blue icon button" onclick="goToLocation(\u007b'title': '{address_title}', 'address': '{address}'\u007d)">
                                    <i class="location arrow icon"></i>
                                    Main Entrance
                                </button>
                              </td>
                              <td>
                                <button class="ui tiny labeled orange icon button" onclick="loadEntranceElements({location.id})">
                                    <i class="list icon"></i>
                                    All Entrances
                                </button>
                              </td>
                            </tr>
                          </tbody>
                          <tfoot>
                            <tr class="center aligned">_<th colspan="2">
                            </tr>
                          </tfoot>
                        </table>
                    </div>
                  </div>
                  
            """
        return JsonResponse({"elements": element_html_string, 'success': 1})


class GetEntranceElementsView(View):
    def get(self, request, *args, **kwargs):
        element_html_string = """
        <table class="ui celled table">
          <thead>
            <tr>
                <th class="five wide">Image</th>
                <th>Name</th>
                <th>Orientation</th>
                <th class="one wide"><i class="wheelchair large blue icon"></i></th>
                <th>Address</th>
                <th class="one wide">Main</th>
                <th class="one wide">Directions</th>
            </tr>
          </thead>
          <tbody>
        """
        try:
            location = Location.objects.get(pk=self.kwargs['pk'])
            for entrance in Entrance.objects.filter(location=location):
                image = entrance.image.url if entrance.image else ''
                wheel_chair = "check circle outline green icon" if entrance.automatic_door else "close large red icon"
                main_entrance = "check circle outline green icon" if entrance.default else "close large red icon"
                element_html_string = element_html_string + f"""                
                <tr>
                  <td data-label="Image"><img src="{image}" style="width:100%"></td>
                  <td data-label="Name">{entrance.description}</td>
                  <td data-label="Orientation">{entrance.orientation}</td>
                  <td data-label="Handicap">
                    <i class="{wheel_chair}"></i>
                  </td>
                  <td data-label="Address">{entrance.address}</td>
                  <td data-label="Main Entrance">
                    <i class="{main_entrance}"></i>
                  </td>
                  <td data-label="Go To">                    
                    <button class="ui tiny labeled blue icon button" onclick="goToLocation(\u007b'title': '{entrance.address}', 'address': '{entrance.direction_address}'\u007d)">
                        <i class="location arrow icon"></i> Go
                    </button>
                  </td>
                </tr>
                """
        except Location.DoesNotExist:
            JsonResponse({"message": 'Sorry, location does not exist!', 'success': 0})

        element_html_string = element_html_string + "</tbody></table>"
        return JsonResponse({"element_string": element_html_string, 'success': 1})
