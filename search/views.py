from django.shortcuts import render
from .forms import ShortestDistanceForm
from .models import District, Distance
from collections import defaultdict
import heapq
def find_shortest_distance(request):
    form = ShortestDistanceForm(request.POST or None)
    shortest_distance = None
    shortest_path = None
    total_path = Distance.objects.all()

    if request.method == 'POST' and form.is_valid():
        source_district = form.cleaned_data['source_district']
        destination_district = form.cleaned_data['destination_district']

        shortest_distance, shortest_path = dijkstra_shortest_path(source_district,destination_district)
        shortest_path = "-->".join([district.name for district in shortest_path])
    return render(request, 'search.html', {'form': form, 'shortest_distance': shortest_distance, 'shortest_path': shortest_path, 'total_path': total_path})


def dijkstra_shortest_path(source, destination):
    distances = defaultdict(lambda: float('inf'))
    distances[source] = 0
    previous = {}
    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == destination:
            break

        if current_distance > distances[current_node]:
            continue

        for distance_obj in current_node.source_distances.all():
            print(distance_obj, current_node.source_distances.all())
            neighbor = distance_obj.destination_district
            distance_to_neighbor = current_distance + distance_obj.distance

            if distance_to_neighbor < distances[neighbor]:
                distances[neighbor] = distance_to_neighbor
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance_to_neighbor, neighbor))

    if destination not in previous:
        return None
    
    shortest_path = []
    current = destination

    while current != source:
        shortest_path.append(current)
        current = previous[current]

    shortest_path.append(source)
    shortest_path.reverse()
    print("Shortest Path:", [district.name for district in shortest_path])
    shortest_distance = distances[destination]

    return shortest_distance, shortest_path