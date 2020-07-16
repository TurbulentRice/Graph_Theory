import random

######################
# GENERAL FUNCTIONS
######################

# UI Format
def f():
    print("-" * 40)

# Show iterable line by line
def show_it(iterable):
    for thing in iterable:
        print(thing)

# Return list of A-Z + a-z
def get_alpha(lower=False):
    # A_Z
    alpha = [chr(i) for i in range(65, 91)]
    # a-z
    if lower:
        for i in range(97, 123):
            alpha.append(chr(i))
    return alpha

# Return new list with random weights, remove redundancies
# Ex: C->D and D->C, remove D-C
def add_weights(r):
    # Copy routes so that OG list is not changes
    l = [x[:] for x in r]
    weighted = []
    # Remove duplicate edges
    for i in range(len(l)):
        dup = False
        for d in weighted:
            # If pair already appears in weighted list, dup=T.
            if l[i][0] in d and l[i][1] in d:
                dup = True
        if not dup:
            # If not, add
            weighted.append(l[i])
    # Add random weights to route list
    for i in range(len(weighted)):
        random.seed(i)
        weighted[i].append(random.randint(1, 999))
    return weighted

#########
# DATA
#########

# Airport Data
# Vertices
airports = ["BGI", "CDG", "DEL", "DOH", "DSM", "EWR", "EYW", "HND", "ICN",
            "JFK", "LGA", "LHR", "ORD", "SAN", "SFO", "SIN", "TLV", "BUD"]
# Edges
routes = [
    ["DSM", "ORD"],
    ["ORD", "BGI"],
    ["BGI", "LGA"],
    ["SIN", "CDG"],
    ["CDG", "SIN"],
    ["CDG", "BUD"],
    ["DEL", "DOH"],
    ["DEL", "CDG"],
    ["TLV", "DEL"],
    ["EWR", "HND"],
    ["HND", "ICN"],
    ["HND", "JFK"],
    ["ICN", "JFK"],
    ["JFK", "LGA"],
    ["EYW", "LHR"],
    ["LHR", "SFO"],
    ["SFO", "SAN"],
    ["SFO", "DSM"],
    ["SAN", "EYW"]]
# Weighted Edges
weighted_routes = add_weights(routes)


# Alphabetical Paths Data
# A-Z Vertices
alpha_v = get_alpha()
# Random Edges
alpha_e = add_weights([random.sample(alpha_v, 2) for x in alpha_v])





