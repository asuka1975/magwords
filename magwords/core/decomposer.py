from cu2qu import curve_to_quadratic

__all__ = ["move", "line", "conic", "cubic"]

to_tuple = lambda v: (v.x, v.y)

def move(p, user):
    user["convex"].append(to_tuple(p))
    user["inner"].append([])
    user["inner"][-1].append(to_tuple(p))

def line(p, user):
    user["convex"].append(to_tuple(p))
    user["inner"][-1].append(to_tuple(p))

def conic(c, p, user):
    ctuple = to_tuple(c)
    ptuple = to_tuple(p)
    user["beziers"].extend([user["convex"][-1], ctuple, ptuple])
    user["convex"].extend([ctuple, ptuple])
    user["inner"][-1].append(ptuple)

def cubic(c1, c2, p2, user):
    c1, c2, p2 = to_tuple(c1), to_tuple(c2), to_tuple(p2)
    p1 = user["convex"][-1]
    quads = curve_to_quadratic([p1, c1, c2, p2], 0.1)
    user["convex"].extend(quads[1:])
    user["beziers"].extend([v for i in range(len(quads)//2) for v in quads[i*2:i*2+3]])
    user["inner"][-1].extend(quads[::2])