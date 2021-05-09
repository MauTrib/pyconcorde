import numpy as np

EDGE_WEIGHT_TYPES = {
    "EXPLICIT",
    "EUC_2D",
    "EUC_3D",
    "MAX_2D",
    "MAN_2D",
    "GEO",
    "GEOM",
    "ATT",
    "CEIL_2D",
    "DSJRAND",
}


def write_tsp_file(fp, xs, ys, norm, name):
    """ Write data to a TSPLIB file.
    """
    if len(xs) != len(ys):
        raise ValueError(
            "x and y coordinate vector must have the "
            "same length ({} != {})".format(len(xs), len(ys))
        )
    if norm not in EDGE_WEIGHT_TYPES:
        raise ValueError(
            "Norm {!r} must be one of {}"
            .format(norm, ', '.join(EDGE_WEIGHT_TYPES))
        )

    fp.write("NAME: {}\n".format(name))
    fp.write("TYPE: TSP\n")
    fp.write("DIMENSION: {}\n".format(len(xs)))
    fp.write("EDGE_WEIGHT_TYPE: {}\n".format(norm))
    fp.write("NODE_COORD_SECTION\n")
    for n, (x, y) in enumerate(zip(xs, ys), start=1):
        fp.write("{} {} {}\n".format(n, x, y))
    fp.write("EOF\n")

def write_tsp_file_explicit(fp, W_dist, name):
    n,_ = W_dist.shape
    assert len(W_dist.shape)==2 and W_dist.shape[0] == W_dist.shape[1], f'Distance matrix is not of good format : {W_dist.shape}'
    fp.write("NAME: {}\n".format(name))
    fp.write("TYPE: TSP\n")
    fp.write("DIMENSION: {}\n".format(n))
    fp.write("EDGE_WEIGHT_TYPE: EXPLICIT\n")
    fp.write("EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
    fp.write("EDGE_WEIGHT_SECTION\n")
    for i in range(n):
        line = ''
        for j in range(n):
            line += str(W_dist[i,j])
            line += ' '
        line = line[:-1] + '\n' #Removing the last space adding the new line
        fp.write(line)
    fp.write("EOF\n")

def read_tsp_tour(fname):
    has_tour = False
    tour = []
    with open(fname) as fp:
        for line in fp:
            if line.startswith("TOUR_SECTION"):
                has_tour = True
            elif line.startswith("EOF"):
                break
            else:
                if has_tour:
                    tour.extend(int(node) for node in line.split())
    if not tour:
        raise RuntimeError("File {} has no valid TOUR_SECTION".format(fname))
    if tour[-1] == -1:
        tour.pop()
    return np.array(tour)
