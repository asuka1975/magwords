import cu2qu

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
    p1 = user["convex"][-1]
    p1_ = p1[0] + p1[1] * 1j
    c1_ = c1[0] + c1[1] * 1j
    c2_ = c2[0] + c2[1] * 1j
    p2_ = p2[0] + p2[1] * 1j
    c0, q1, c3 = cu2qu.cu2qu.cubic_approx_quadratic([p1_, c1_, c2_, p2_], 0.1)
    user["beziers"].extend([p1, c0, q1, q1, c3, p2])
    user["inner"][-1].extend([p1, q1, p2])