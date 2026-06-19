# AstroRoute-ML 🚀

A data-driven orbital mechanics trajectory planner. This repository simulates planet positions using numerical approximations of Kepler’s laws in **C**, clusters dense coordinate space down using an unsupervised **Machine Learning K-Means module**, and routes trajectories using a **Dynamic Graph algorithm** optimized for spatial constraints.

## 🧠 Key DSA & Architectural Concepts Implemented
* **Dynamic Coordinate Graph Routing:** Graph nodes shift positions relative to time. Spatial distances are computed dynamically to evaluate greedy algorithm weights.
* **Unsupervised Spatial Clustering:** Implements an custom, dependency-free spatial K-Means clustering algorithm to reduce complexity overhead.
* **Numerical Methods:** Implements an iterative Newton-Raphson solver to compute eccentric anomaly values from transcendental equations.

## 🛠️ Project Structure
* `physics_engine.c`: Computes real-time orbital paths via differential kinematics.
* `graph_router.c`: Computes dynamic shortest path decisions.
* `cluster_bodies.py`: Formulates regional waypoints from planetary coordinates.
* `app.py`: Coordinates the physics-to-routing data sequence pipeline.

## 🚀 Execution Instructions

Run the primary compilation and routing system with:
```bash
python app.py
