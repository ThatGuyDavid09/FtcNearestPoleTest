import pprint
import random

rounding = 0
def generate_junctions(radius):
    junctions = []
    offset = radius * 2 / 6
    start = -radius

    for row in range(1, 6):
        for col in range(1, 6):
            junctions.append([round(start + (row * offset), rounding), round(start + (col * offset), rounding)])
    return junctions


def find_path(junc1, junc2, prefer_x=True):
    print(junc1)
    print(junc2)
    if prefer_x:
        path = [junc1, [junc2[0], junc1[1]], junc2]
    else:
        path = [junc1, [junc1[0], junc2[1]], junc2]
    amended_path = []
    for item in path:
        if item not in amended_path:
            amended_path.append(item)

    final_path = []
    if len(amended_path) > 2:
        current_heading = -1
        item = amended_path[0]
        next_item = amended_path[1]
        next_next_item = amended_path[2]

        final_path.append(item)

        if next_item[1] > item[1]:
            current_heading = 0
        elif next_item[0] > item[0]:
            current_heading = 90
        elif next_item[1] < item[1]:
            current_heading = 180
        else:
            current_heading = 270

        item_copy = next_item.copy()
        if current_heading == 0:
            item_copy[1] -= 2
        elif current_heading == 90:
            item_copy[0] -= 2
        elif current_heading == 180:
            item_copy[1] += 2
        else:
            item_copy[0] += 2

        final_path.append(item_copy)  # + [current_heading])

        if next_next_item[1] > next_item[1]:
            current_heading = 0
        elif next_next_item[0] > next_item[0]:
            current_heading = 90
        elif next_next_item[1] < next_item[1]:
            current_heading = 180
        else:
            current_heading = 270

        item_copy = next_item.copy()
        if current_heading == 0:
            item_copy[1] += 2
        elif current_heading == 90:
            item_copy[0] += 2
        elif current_heading == 180:
            item_copy[1] -= 2
        else:
            item_copy[0] -= 2

        final_path.append(item_copy)  # + [current_heading])

        final_path += amended_path[2:]
    else:
        final_path = amended_path

    return final_path#[1:]


junctions = generate_junctions(70)
pprint.pprint(find_path(random.choice(junctions), random.choice(junctions), random.choice([True, False])))
