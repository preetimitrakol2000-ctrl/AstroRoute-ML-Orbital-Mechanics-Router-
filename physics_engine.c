#include <stdio.h>
#include <math.h>

#define M_PI 3.14159265358979323846

// Struct to represent a celestial body's orbit
typedef struct {
    double semi_major_axis; // Average distance from star (AU)
    double eccentricity;    // Orbit shape deviation from perfect circle
    double orbital_period;  // Time to complete one full orbit (days)
} Orbit;

// Struct to represent 2D coordinates
typedef struct {
    double x;
    double y;
} Position;

// Computes the dynamic 2D coordinates of a planet at a specific time (day)
void calculate_position(Orbit body, double day, Position* pos) {
    // Mean anomaly
    double M = (2.0 * M_PI / body.orbital_period) * day;
    
    // Kepler's Equation approximation for Eccentric Anomaly (E)
    double E = M; 
    for (int i = 0; i < 5; i++) { // 5 iterations Newton-Raphson method
        E = E - (E - body.eccentricity * sin(E) - M) / (1.0 - body.eccentricity * cos(E));
    }
    
    // Calculate coordinates in the orbital plane
    pos->x = body.semi_major_axis * (cos(E) - body.eccentricity);
    pos->y = body.semi_major_axis * sqrt(1.0 - body.eccentricity * body.eccentricity) * sin(E);
}

// Wrapper for Python integration via ctypes
void get_planet_coordinates(double semi_major, double ecc, double period, double day, double* out_x, double* out_y) {
    Orbit body = {semi_major, ecc, period};
    Position pos;
    calculate_position(body, day, &pos);
    *out_x = pos.x;
    *out_y = pos.y;
}
