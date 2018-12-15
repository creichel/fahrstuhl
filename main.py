'''
There are too many dumb lifts in the world. That's why I wrote this small script because I believe that all lifts can be
a bit more intelligent when programmed a bit more intelligent

The main idea is by separating the lift from their jobs to manage jobs centrally through an lift orchestration service.
Because no one knows the duration of one job (might be that the person presses all floors or has pressed but still
pushes the door to be open), the system checks first if a lift is free - that means it does not have any floors pushed.
If there's a free lift, it gets the job. If not, it checks then which lift passes through this floor and has fewer jobs
(if
both are in the 12th floor and have to go to the ground floor.). Then it assigns the job to it by pushing it into the
list of pressed floors. If there is none available, it simply assigns it to the job list and waits until the first
lift is free to take it.

By using jobs, you can introduce more features to the lifts, like using a cancel button per floor so you can cancel a
job if you don't want to have the lift though.
'''

import argparse

from Lift import Lift
from LiftOrchestration import LiftOrchestration

lifts = [
    Lift(0, [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
    Lift(1, [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
]



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--from_floor", help="in which floor are you now?")
    parser.add_argument("--to_floor", help="in which floor do you want to go?")
    args = parser.parse_args()

    if args.from_floor < args.to_floor:
        direction = 'down'
    else:
        direction = 'up'

    lo = LiftOrchestration(lifts)

    lift = lo.call_lift(args.from_floor, direction).lift
    lift.press_floor(args.to_floor)



