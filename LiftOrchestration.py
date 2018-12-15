from Job import Job
import sched
import time


class LiftOrchestration:

    # On a fire alarm, the lifts should go directly to ground floor and don't accept new jobs.
    fire_mode = False

    jobs = []

    # Set up a tolerance based on a number. When not trusting the sensors because tey aren't reflecting the current
    # flow or the lift is fast, increase this number.
    floor_tolerance = 0

    def __init__(self, lifts):
        self.lifts = lifts

    def call_lift(self, floor, direction):
        # On fire mode, you can't call any lift
        if self.fire_mode:
            print('Fire alarm activated.')
            return False

        # assign it as a job
        job = Job(floor, direction)
        self.jobs.append(job)

        print('Appended job: {}'.format(job))

        # Start orchestration
        self.orchestrate_jobs()

        return job

    def assign_job(self, lift, job):
        # On fire mode, no job will be assigned and all jobs will be canceled.
        if self.fire_mode:
            print('Fire alarm activated.')
            self.jobs = []
            return False

        # register the job by pushing the floor number into the pressed number list of a lift
        if lift.press_floor(job.floor):
            self.jobs.remove(job)

    def enable_fire_mode(self):
        # kill all floors of the lift, go directly to ground floor
        self.fire_mode = True

    def disable_fire_mode(self):
        # enable the service to take jobs again.
        self.fire_mode = False

    def orchestrate_jobs(self):

        print('Run orchestration service')

        if not self.jobs:
            print('No jobs found.')
            return False

        for job in self.jobs:

            print('Active jobs: {}'.format(self.jobs))

            for lift in self.lifts:

                print('Check lift {}'.format(lift))

                # If one of the lifts is free, assign directly
                # Else, check current and next floor of the lift to dynamically assign it to to it if possible
                if lift.is_supporting_floor(job.floor) and (
                        lift.check_idle() or (
                            job.direction is 'up' and
                            lift.current_floor + self.floor_tolerance < job.floor <= lift.pressed_floors[-1]) or
                        lift.current_floor - self.floor_tolerance > job.floor >= lift.pressed_floors[-1]):
                    print('found lift: {}'.format(lift.id_no))
                    self.assign_job(lift, job)
                    print('jobs: {} '.format(self.jobs))

                    job.lift = lift

                    break

                else:
                    print('no free lift found')

        # If list of jobs is not null, try again to orchestrate jobs in 5 seconds

        if not self.jobs:
            print('Reschedule orchestration service')
            orchestration_schedule = sched.scheduler(time.time, time.sleep)
            orchestration_schedule.enter(5, 1, self.orchestrate_jobs, ())
            orchestration_schedule.run()
