from API import API


class Lift:
    # Lifts just know their own statuses and their capabilities. They are getting their job by the orchestration system

    idle = True
    pressed_floors = []
    next_floor = 0
    direction = ''
    current_floor = 0
    doors_open = True
    API = API()

    # waiting times
    time_doors_waiting = 5

    def __init__(self, id_no, floors):
        self.id_no = id_no
        self.floors = floors

    def press_floor(self, floor):
        if floor not in self.floors:
            print('Floor {} not supported. Supported floors: {}'.format(floor, self.floors))
            return False

        self.pressed_floors = self.pressed_floors.append(floor).sort()

        print('Floor {} is pressed.'.format(floor))
        return self.go_to_next()

    def close_doors(self):
        # Hardware: close the doors and wait until they return true
        self.API.close_door()
        self.doors_open = False

    def open_doors(self):
        # Hardware: open the doors and wait until they return true
        self.API.close_door()
        self.doors_open = True

    def go_to_next(self):
        # Move from current floor to next floor in floor list depending on the current direction
        self.next_floor = self.pressed_floors[0]

        if self.next_floor < self.current_floor:
            self.direction = 'down'
        else:
            self.direction = 'up'

        if self.doors_open:
            self.close_doors()

        # Hardware: move the lift to floor next_floor
        while self.current_floor is not self.next_floor:
            self.API.go_to_floor(self.current_floor, self.direction)

        self.pressed_floors.remove(self.next_floor)

        self.open_doors()

        if not self.pressed_floors:
            self.go_to_next()

        return True

    def check_idle(self):
        # Checks the current status according to pressed floors. If no floors are pressed, the lift is possibly idle

        if not self.pressed_floors:
            print('Lift is idle')
            self.idle = True
        else:
            print('Lift is busy')
            self.idle = False

        return self.idle

    def get_current_floor(self):
        # Hardware: Gets the current floor
        return

    def is_supporting_floor(self, floor):
        floor = int(floor)
        print('Is floor {} supported? {}. List of floors: {}'.format(floor, floor in self.floors, self.floors))
        return floor in self.floors
