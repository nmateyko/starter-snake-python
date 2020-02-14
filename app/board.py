import math
class Board:

    directions_dict = {'up': {'x':  0, 'y': -1},
                     'down': {'x':  0, 'y':  1},
                     'left': {'x': -1, 'y':  0},
                    'right': {'x':  1, 'y':  0}}

    def __init__(self, data):
        self.width = data['board']['width']
        self.height = data['board']['height']
        self.food = data['board']['food']
        self.snakes = data['board']['snakes']
        self.head = data['you']['body'][0]

    def wall_in_direction(self, direction):
        new_x = self.head['x'] + direction['x']
        new_y = self.head['y'] + direction['y']
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            return False
        else:
            return True

    def snake_in_direction(self, direction):
        new_x = self.head['x'] + direction['x']
        new_y = self.head['y'] + direction['y']
        occupied = False
        for s in self.snakes:
            for pos in s['body']:
                if pos['x'] == new_x and pos['y'] == new_y:
                    occupied = True
        return occupied

    def distance_between_points(self, p1, p2):
        return math.sqrt((p1['x'] - p2['x'])*(p1['x'] - p2['x'])
                          + (p1['y'] - p2['y'])*(p1['y'] - p2['y']))

    def closest_food(self):
        closest = 0;
        min_distance = math.sqrt(self.width*self.width + self.height*self.height)
        i = 0
        for f in self.food:
            if self.distance_between_points(self.head, f) < min_distance:
                min_distance = min_distance
                closest = i
            i += 1
        print("closest: ", closest)
        return closest

    def towards_food(self, directions):
        best_direction = 0
        closest = self.closest_food()
        min_distance = self.distance_between_points(self.head, self.food[closest])
        i = 0
        for d in directions:
            new_x = self.head['x'] + self.directions_dict[d]['x']
            new_y = self.head['y'] + self.directions_dict[d]['y']
            new_head = {'x': new_x, 'y': new_y}
            new_distance = self.distance_between_points(new_head, self.food[closest])
            if new_distance < min_distance:
                min_distance = new_distance
                best_direction = i
            i += 1
        print("best direction: ", best_direction)
        return best_direction
