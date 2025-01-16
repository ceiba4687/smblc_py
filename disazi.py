import math
from config import REARTH


def disazi(lateq, loneq, latst, lonst):
    """
    Convert geographic coordinates to cartesian coordinates

    Parameters:
    lateq (float): Latitude of the epicenter (in degrees)
    loneq (float): Longitude of the epicenter (in degrees)
    latst (float): Latitude of the station (in degrees)
    lonst (float): Longitude of the station (in degrees)

    Returns:
    tuple: (xnorth, yeast) - Cartesian coordinates of the station
    """

    # Constants
    PI = math.pi
    PI2 = 2 * PI
    DEGTORAD = PI / 180.0

    # Convert to radians
    latb = lateq * DEGTORAD
    lonb = loneq * DEGTORAD
    latc = latst * DEGTORAD
    lonc = lonst * DEGTORAD

    # Adjust longitude values
    if lonb < 0.0:
        lonb += PI2
    if lonc < 0.0:
        lonc += PI2

    # Calculate angles
    b = 0.5 * PI - latb
    c = 0.5 * PI - latc

    # Determine angle direction
    if lonc > lonb:
        aa = lonc - lonb
        if aa <= PI:
            iangle = 1
        else:
            aa = PI2 - aa
            iangle = -1
    else:
        aa = lonb - lonc
        if aa <= PI:
            iangle = -1
        else:
            aa = PI2 - aa
            iangle = 1

    # Calculate spherical distances
    s = math.cos(b) * math.cos(c) + math.sin(b) * math.sin(c) * math.cos(aa)
    s = min(max(s, -1.0), 1.0)  # Ensure value is within [-1, 1]
    a = math.acos(s)
    dis = a * REARTH

    # Calculate angles
    if a * b * c == 0.0:
        angleb = 0.0
        anglec = 0.0
    else:
        s = 0.5 * (a + b + c)
        a = min(a, s)
        b = min(b, s)
        c = min(c, s)

        # Calculate angles using spherical trigonometry
        sin_term_c = math.sqrt(
            max(0, math.sin(s - a) * math.sin(s - b) / (math.sin(a) * math.sin(b)))
        )
        sin_term_b = math.sqrt(
            max(0, math.sin(s - a) * math.sin(s - c) / (math.sin(a) * math.sin(c)))
        )

        anglec = 2.0 * math.asin(min(1.0, sin_term_c))
        angleb = 2.0 * math.asin(min(1.0, sin_term_b))

        if iangle == 1:
            angleb = PI2 - angleb
        else:
            anglec = PI2 - anglec

    # Calculate cartesian coordinates
    xnorth = dis * math.cos(anglec)
    yeast = dis * math.sin(anglec)
    dis = math.sqrt(xnorth * xnorth + yeast * yeast) / 1000

    return dis
