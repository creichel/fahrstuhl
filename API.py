import time


class API:

    demo_seconds_to_door_closed = 3
    demo_seconds_per_floor = 2

    def go_to_floor(self, from_floor, direction):

        if direction is 'up':
            direction = 1
        elif direction is 'down':
            direction = -1

        time.sleep(self.demo_seconds_per_floor)
        print('Arrived on floor {}'.format(from_floor + direction))
        return from_floor + direction

    def close_door(self):
        time.sleep(self.demo_seconds_to_door_closed)
        print('Door is closed')
        return True

    def open_door(self):
        time.sleep(self.demo_seconds_to_door_closed)
        print('Door is open')
        return True
