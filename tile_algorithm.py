import pprint
import random


def generate_junctions(radius):
    junctions = []
    offset = radius * 2 / 6
    start = -radius

    for row in range(1, 6):
        for col in range(1, 6):
            junctions.append([round(start + (row * offset), 2), round(start + (col * offset), 2)])
    return junctions


def find_path(junc1, junc2, prefer_x=True):
    print(junc1)
    print(junc2)
    if prefer_x:
        path = [junc1, [junc2[0], junc1[1]], junc2]
    else:
        path = [junc1, [junc1[0], junc2[1]], junc2]
    final_path = []
    for item in path:
        if item not in final_path:
            final_path.append(item)

    return final_path[1:]


junctions = generate_junctions(70)
pprint.pprint(find_path(random.choice(junctions), random.choice(junctions), random.choice([True, False])))
