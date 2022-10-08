import pygame
import math

from Rect import Rect
from Robot import Robot
from SpecialRect import SpecialRect

WIDTH = 1000
HEIGHT = 1000
FPS = 30

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
# pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pole test")
clock = pygame.time.Clock()  # For syncing the FPS

all_sprites = pygame.sprite.Group()

field = pygame.image.load("powerplay_field.png")
field = pygame.transform.scale(field, (HEIGHT, WIDTH))

running = True

junctions = []

# Find max dist possible btwn 2 junctions
offset = WIDTH / 6
max_dist_possible = math.dist((0, 0), (offset * 1.1, offset * 1.1))
rects_to_draw = []


def generate_junctions():
    offset = WIDTH / 6

    for row in range(1, 6):
        for col in range(1, 6):
            junctions.append([int(row * offset), int(col * offset)])
    return junctions


def find_closest_junctions(coord, max_dist=max_dist_possible, max_num=4):
    sorted_closest = sorted(junctions, key=lambda item: math.dist(item, coord), reverse=True)

    valid_closest = []
    for i in range(min(max_num, len(sorted_closest))):
        check_coord = sorted_closest.pop()
        if math.dist(check_coord, coord) <= max_dist:
            valid_closest.append(check_coord)
        else:
            break
    return valid_closest


def update_closest(coord):
    closest_junctions = find_closest_junctions(coord)
    # print(coord)
    # print(closest_junctions)
    rects_to_draw.clear()

    for j in closest_junctions:
        rect = Rect((j[0] - 20, j[1] - 20, 40, 40), 2)
        # print(rect)
        rects_to_draw.append(rect)
    return closest_junctions


generate_junctions()
# print(junctions)
steps = 10

robot = Robot()


def find_facing_quadrant():
    rotation = robot.rotation % 360
    if 0 <= rotation < 90:
        return 1
    elif 90 <= rotation < 180:
        return 2
    elif 180 <= rotation < 270:
        return 3
    return 4


def filter_quadrant_junctions(pos, junctions, quadrant):
    valid = []
    for j in junctions:
        if quadrant == 1:
            if j[0] >= pos[0] and j[1] <= pos[1]:
                valid.append(j)
        elif quadrant == 2:
            if j[0] <= pos[0] and j[1] <= pos[1]:
                valid.append(j)
        elif quadrant == 3:
            if j[0] <= pos[0] and j[1] >= pos[1]:
                valid.append(j)
        else:
            if j[0] >= pos[0] and j[1] >= pos[1]:
                valid.append(j)

    if valid:
        return valid, 0
    else:
        return junctions, 1

while running:
    clock.tick(FPS)
    screen.blit(field, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                running = False

            if event.key == pygame.K_LEFT or event.key == ord('a'):
                robot.control_move(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                robot.control_move(steps, 0)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                robot.control_move(0, steps)
            if event.key == pygame.K_UP or event.key == ord('w'):
                robot.control_move(0, -steps)

            if event.key == ord('z'):
                robot.control_rot(steps)
            if event.key == ord('x'):
                robot.control_rot(-steps)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                robot.control_move(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                robot.control_move(-steps, 0)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                robot.control_move(0, -steps)
            if event.key == pygame.K_UP or event.key == ord('w'):
                robot.control_move(0, steps)

            if event.key == ord('z'):
                robot.control_rot(-steps)
            if event.key == ord('x'):
                robot.control_rot(steps)

    closest = update_closest(robot.get_pos())
    # print(closest)

    quadrant = find_facing_quadrant()
    # print(quadrant)
    junctions_sorted, mode = filter_quadrant_junctions(robot.get_pos(), closest, quadrant)
    # print(junctions_sorted)
    if mode == 0:
        junctions_sorted = sorted(junctions_sorted, key=lambda item: math.dist(item, robot.get_pos()))
    else:
        # TODO write some code that prioritizes junctions that are not only closer, but closer in angle
        # TODO idk how to do that
        junctions_sorted = sorted(junctions_sorted, key=lambda item: math.dist(robot.get_pos(), item) - math.degrees(abs(robot.rotation - math.atan2(math.radians(item[1] - robot.y), math.radians(item[0] - robot.x)))))#, reverse=True)

        # print(junctions_sorted)
    # print(junctions_sorted)
    closest_sorted = junctions_sorted[0]
    # print(closest)
    rects_to_draw.append(SpecialRect((closest_sorted[0] - 20, closest_sorted[1] - 20, 40, 40), 2))
    # print("====")

    for sprite in rects_to_draw:
        sprite.update()
        sprite.draw(screen)

    robot.update()
    robot.draw(screen)

    pygame.display.flip()

pygame.quit()
