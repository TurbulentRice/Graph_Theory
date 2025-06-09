import random

##############################
#   DATA MANIPULATION
##############################

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

##################
#   DATA
##################

# Airport Data
# Vertices (trimmed to 10 for concise example output)
airports = ["BGI", "CDG", "DEL", "DOH", "DSM", "EWR", "HND", "ICN", "JFK", "LGA"]
# Edges
routes = [
    ["DSM", "EWR"],
    ["EWR", "BGI"],
    ["BGI", "LGA"],
    ["CDG", "DEL"],
    ["DEL", "DOH"],
    ["DOH", "CDG"],
    ["EWR", "HND"],
    ["HND", "ICN"],
    ["ICN", "JFK"],
    ["JFK", "LGA"],
    ["LGA", "EWR"],
]
# Weighted Edges
weighted_routes = add_weights(routes)


# Alphabetical Paths Data
# A-J Vertices
alpha_v = get_alpha()[:10]  # A–J
# Random Edges (50 )
alpha_e = add_weights([random.sample(alpha_v, 2) for x in range(50)])
