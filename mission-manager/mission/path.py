from geopy import distance
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from mission.waypoint import Waypoint

"""
Path making uses very efficient OR-Tools, google library written in C++,
which provides bindings to python code.
"""


def create_data_model(points: list[Waypoint]):
    """Based on list of waypoints, creates a distance matrix (from every point to every other)"""
    data = {}
    matrix = []
    for point_A in points:
        distance_list = []
        for point_B in points:
            # conversion to int is neccessary for OR Tools
            distance_list.append(
                int(distance.distance(point_A.position, point_B.position).m)
            )

        matrix.append(distance_list)

    print(matrix)

    data["distance_matrix"] = matrix
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


def compute_solution_path(manager, routing, solution):
    path_indices = []

    index = routing.Start(0)
    plan_output = "Route for vehicle:\n"
    route_distance = 0

    while not routing.IsEnd(index):
        point_id = manager.IndexToNode(index)
        path_indices.append(point_id)

        plan_output += f" {point_id} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

    # Last point
    point_id = manager.IndexToNode(index)
    plan_output += f" {point_id}\n"
    path_indices.append(point_id)

    # Console output
    plan_output += f"Route distance: {route_distance}\n"
    print(plan_output)
    return path_indices


def create_path(points: list[Waypoint]) -> list[Waypoint]:
    """Take list of waypoints to vist, compute the shortest path
    and return points in the correct order"""

    data = create_data_model(points)
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)
    indices_path = compute_solution_path(manager, routing, solution)

    final_path = [points[i] for i in indices_path]
    return final_path
