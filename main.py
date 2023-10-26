# IMPORTS
import string
import random
from icecream import ic  # for debug only

# CONSTANTS
num_floors = 5
top_floor = num_floors - 1
bottom = 0  # base floor
num_elevators = 4

# GLOBAL VARIABLES
elevators = []
requests_up = []
requests_down = []


def init_requests():
    # Init of binary arrays for up and down requests
    # for all elevators
    for _ in range(num_floors):
        requests_up.append(False)
        requests_down.append(False)


class Elevator:
    def __init__(self, name, bottom, top):
        self.name = name
        self.in_service = True
        self.bottom = bottom
        self.top = top
        self.current_floor = bottom  # normally 0
        self.direction = 0  # 1 - up, 0 - idle, -1 - down
        self.door_open = True
        self.stops = []

    def __str__(self):
        return (f"{self.name}, in service: {self.in_service}, floor: {self.current_floor}, "
                f"door_open: {self.door_open}, direction: {self.direction}, "
                f"stops: {self.stops}")

    def add_stop(self, floor):
        # will be called by scheduler
        if self.top > floor >= self.bottom:
            if floor in self.stops:
                return
            if floor == self.current_floor:
                return
            self.stops.append(floor)

    def del_stop(self, floor):
        # will be called by open_closed and closed_door
        if floor in self.stops:
            self.stops.remove(floor)

    def close_door(self):
        self.door_open = False
        self.del_stop(self.current_floor)

    def open_door(self):
        self.door_open = True
        self.del_stop(self.current_floor)
        if len(self.stops) == 0:
            self.direction = 0  # idle

    def up(self):
        if self.current_floor < self.top:
            self.current_floor += 1

    def down(self):
        if self.current_floor > self.bottom:
            self.current_floor -= 1

    def step(self):
        if not self.in_service:
            return
        if len(self.stops) == 0:  # proceed only if one or more requests are waiting
            self.direction = 0
            return
        if self.door_open:
            self.close_door()  # and proceed with a move during the next step
            self.direction = 1  #
            return
        if self.current_floor in self.stops:
            self.open_door()
            return
        if self.direction == 1:  # up
            if max(self.stops) > self.current_floor:
                self.current_floor += 1
            else:
                self.direction = -1

        if self.direction == -1:  # down
            if min(self.stops) < self.current_floor:
                self.current_floor -= 1
            else:
                self.direction = 1


def init_elevators():
    for n in range(num_elevators):
        elevators.append(Elevator(string.ascii_uppercase[n], bottom, num_floors))


def step():
    for elevator in elevators:
        elevator.step()


def elevator_status():
    #  this is for debug only
    for elevator in elevators:
        ic(elevator.__str__())
    input()


def clear():
    for _ in range(10):
        print()


def status_monitor():
    # https://github.com/emilybache/Lift-Kata
    # [ ] doors are closed  //  ] [ doors are open  //  * request
    #  ▽ - down  //  △ - up
    clear()
    floor = top_floor
    print(f"         |", end="")
    for elevator in elevators:
        if elevator.in_service:
            in_service = " "
        else:
            in_service = "X"
        if elevator.direction == 1:
            direction_sign = "△"
        elif elevator.direction == -1:
            direction_sign = "▽"
        else:
            direction_sign = " "
        print(f" {in_service}{elevator.name}{direction_sign} |", end="")
    print()
    while floor >= bottom:
        if requests_up[floor]:
            ch_up = "△"
        else:
            ch_up = " "
        if requests_down[floor]:
            ch_down = "▽"
        else:
            ch_down = " "
        print(f"{floor:5} {ch_up}{ch_down} |", end="")

        # print a * for every requested stop
        for elevator in elevators:
            if floor in elevator.stops:
                stop = "*"
            else:
                stop = " "
            if elevator.current_floor == floor:
                if elevator.door_open:
                    print(f" ]{stop}[ |", end="")
                elif not elevator.door_open:
                    print(f" [{stop}] |", end="")
            else:
                print(f"  {stop}  |", end="")
        print()
        floor -= 1


def random_external_request(n=1):
    for _ in range(n):
        random_floor = random.randint(bottom, top_floor)
        up = 1
        down = 0
        random_direction = random.randint(down, up)
        if random_direction != up:
            if random_floor != bottom:
                requests_down[random_floor] = True
        else:
            if random_floor != top_floor:
                requests_up[random_floor] = True


if __name__ == '__main__':
    init_requests()
    init_elevators()
    while 1:
        random_external_request()
        status_monitor()
        answer = input(f"user indoor and outdoor:"
                       f"\n   o(utdoor)     floor_id       u(p) | d(own)"
                       f"\n   i(ndoor)      elevator_id    dest_floor_id"
                       f"\n   x(indoor)     elevator_id    (toggle in_service)  "
                       f"\n   s(tep)                                            ==> ").split()
        print()
        match answer[0]:
            case "o" | "O":
                floor = int(answer[1])
                match answer[2]:
                    case "u" | "U":
                        if floor < top_floor:
                            requests_up[floor] = True
                    case "d" | "D":
                        if floor != 0:
                            requests_down[floor] = True
            case "i" | "I":
                elevators[int(answer[1])].add_stop(int(answer[2]))
            case "x" | "X":
                if elevators[int(answer[1])].in_service:
                    elevators[int(answer[1])].in_service = False
                else:
                    elevators[int(answer[1])].in_service = True
            case "s" | "S":
                pass  # step
            case _:
                pass
        step()
        #  elevator_status()  # for debug only
