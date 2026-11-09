import math

def coordinates_finite_and_in_bounds(xs, ys, bounds):
    xs_in_bounds = [bounds.left <= x < bounds.right for x in xs]
    ys_in_bounds = [bounds.bottom < y <= bounds.top for y in ys]

    valid = [math.isfinite(x) and math.isfinite(y) for x, y in zip(xs, ys)]

    inside = [v and x and y for v, x, y in zip(valid, xs_in_bounds, ys_in_bounds)]

    return inside, valid
