from enum import Enum
import math

class OBJECT(Enum):
    ROCK = "#"
    SAND = "o"
    SOURCE = "+"
    AIR = "."

class Waterfall:
    def __init__(self, filename="example.txt"):
        self.sand_source = (500, 0)

        paths = []
        self.offset_x = math.inf
        self.max_x = 0
        self.max_y = 0
        for line in open(filename).readlines():
            path = []
            for coords in line.split(" -> "):
                x, y = map(int, coords.split(","))
                path.append((x, y))

                if x + 1 > self.max_x:
                    self.max_x = x + 1
                if y + 1> self.max_y:
                    self.max_y = y + 1
                if x < self.offset_x:
                    self.offset_x = x
            paths.append(path)

        self.paths = paths
        self.matrix = [["."] * (self.max_x-self.offset_x) for _ in range(self.max_y)]
        self.matrix_set(self.sand_source, OBJECT.SOURCE.value)
        self.place_rocks()

    def normalize_cords(self, coords):
        return (coords[0] - self.offset_x, coords[1])

    def matrix_get(self, coords):
        coords = self.normalize_cords(coords) # (X, Y)
        
        # if invalid position return None
        if 0 <= coords[1] < len(self.matrix) and 0 <= coords[0] < len(self.matrix[0]):
            return self.matrix[coords[1]][coords[0]]
        else:
            return None

    def matrix_set(self, coords, object):
        # x coordinate is from the right, y coordinate is distance down
        coords = self.normalize_cords(coords) # (X, Y)
        self.matrix[coords[1]][coords[0]] = object

    def place_rocks(self):
        for path in self.paths:
            for i in range(len(path)-1):
                start_coord = path[i]
                end_coord = path[i+1]
                if start_coord[0] == end_coord[0]: # vertical
                    # x is from the right, so end_coord[0] < start_coord[0]
                    dist = [start_coord[1], end_coord[1]]
                    dist.sort()
                    for y in range(dist[0], dist[1]+1):
                        self.matrix_set((start_coord[0], y), OBJECT.ROCK.value)
                elif start_coord[1] == end_coord[1]: # horizontal
                    # assert end_coord[0] < start_coord[0]
                    dist = [start_coord[0], end_coord[0]]
                    dist.sort()
                    for x in range(dist[0], dist[1]+1):
                        self.matrix_set((x, start_coord[1]), OBJECT.ROCK.value)
                else:
                    raise Exception("Invalid path")

    def debug(self):
        for line in self.matrix:
            print("".join(line))
        print()

    def sand_unit_movement(self, sand_unit):
        while sand_unit[1] < self.max_y and self.matrix_get((sand_unit[0], sand_unit[1]+1)) == OBJECT.AIR.value:
            sand_unit[1] += 1
            # done exit program

        # not free falling
        # try moving one step down to the right
        if self.matrix_get((sand_unit[0]+1, sand_unit[1]+1)) == None or self.matrix_get((sand_unit[0]-1, sand_unit[1]+1)) == None:
            return None
        elif self.matrix_get((sand_unit[0]-1, sand_unit[1]+1)) == OBJECT.AIR.value:
            sand_unit[1] += 1
            sand_unit[0] -= 1
        elif self.matrix_get((sand_unit[0]+1, sand_unit[1]+1)) == OBJECT.AIR.value: 
            sand_unit[1] += 1
            sand_unit[0] += 1
        else:
            return sand_unit
        return self.sand_unit_movement(sand_unit)

    def start_sand(self):
        counter = 0
        while self.matrix_get((self.sand_source[0], self.sand_source[1]+2)) != OBJECT.SOURCE.value:
            new_sand_unit = self.sand_unit_movement([self.sand_source[0], self.sand_source[1]+1])
            if new_sand_unit == None:
                self.debug()
                break
            self.matrix_set(new_sand_unit, OBJECT.SAND.value)
            counter += 1
        return counter

waterfall = Waterfall("input.txt")
waterfall.debug()
print(f"part 1: {waterfall.start_sand()}")