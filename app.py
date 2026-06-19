import ctypes
import os
import sys
from cluster_bodies import MiniKMeans

def compile_backends():
    """Compiles both C scripts into shared libraries."""
    print("[*] Compiling backend physics & routing engines...")
    ext = "dll" if sys.platform.startswith("win") else "so"
    
    os.system(f"gcc -shared -o physics_engine.{ext} -fPIC physics_engine.c")
    os.system(f"gcc -shared -o graph_router.{ext} -fPIC graph_router.c")
    return f"./physics_engine.{ext}", f"./graph_router.{ext}"

def main():
    phys_path, route_path = compile_backends()
    
    phys_lib = ctypes.CDLL(phys_path)
    route_lib = ctypes.CDLL(route_path)

    # Set up argument types for C physics engine
    phys_lib.get_planet_coordinates.argtypes = [
        ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
        ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)
    ]

    # 1. Simulate positions of 6 celestial bodies at Day 45
    # Parameters: Semi-major axis (AU), Eccentricity, Orbital Period (Days)
    bodies_data = [
        (1.0, 0.016, 365.2), (1.52, 0.093, 687.0), (2.77, 0.077, 1682.0),
        (5.20, 0.048, 4332.0), (9.58, 0.054, 10759.0), (19.22, 0.044, 30687.0)
    ]
    
    positions = []
    day = 45.0
    print(f"[*] Simulating planetary positions via C at day: {day}")
    
    for semi_major, ecc, period in bodies_data:
        x_out, y_out = ctypes.c_double(), ctypes.c_double()
        phys_lib.get_planet_coordinates(semi_major, ecc, period, day, ctypes.byref(x_out), ctypes.byref(y_out))
        positions.append((x_out.value, y_out.value))

    # 2. Use ML to group these coordinates into 3 core spatial waypoint nodes
    print("[*] Processing spatial clusters using ML Unsupervised Node Partitioning...")
    kmeans = MiniKMeans(k=3)
    waypoints = kmeans.fit(positions)

    # 3. Use C Graph Router to map out the route from Earth (0,0 Baseline) to Jupiter (Destination)
    start_x, start_y = 0.0, 0.0
    dest_x, dest_y = 4.5, 2.1
    
    # Pack array elements for ctypes delivery
    c_arr_type = ctypes.c_double * len(waypoints)
    wp_x = c_arr_type(*[w[0] for w in waypoints])
    wp_y = c_arr_type(*[w[1] for w in waypoints])

    route_lib.find_next_jump.argtypes = [
        ctypes.c_double, ctypes.c_double, c_arr_type, c_arr_type, ctypes.c_int, ctypes.c_double, ctypes.c_double
    ]
    
    best_wp_idx = route_lib.find_next_jump(start_x, start_y, wp_x, wp_y, len(waypoints), dest_x, dest_y)
    chosen_node = waypoints[best_wp_idx]

    # 4. Print Pipeline Output Results
    print("\n================== ASTRO-ROUTING SYSTEM OUTPUT ==================")
    print(f"Starting Craft Position  : ({start_x}, {start_y})")
    print(f"Optimal Middle Waypoint Cluster Target : ({chosen_node[0]:.3f}, {chosen_node[1]:.3f})")
    print(f"Final Objective Coordinate Destination  : ({dest_x}, {dest_y})")
    print("=================================================================\n")

if __name__ == "__main__":
    main()
