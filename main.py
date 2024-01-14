from ortools.sat.python import cp_model

class MySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, my_schedule, my_teachers, my_rooms, my_exams, my_hours, my_limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._my_schedule = my_schedule
        self._my_teachers = my_teachers
        self._my_rooms = my_rooms
        self._my_exams = my_exams
        self._my_hours = my_hours
        self._my_solution_count = 0
        self._my_solution_limit = my_limit

    def on_solution_callback(self):
        self._my_solution_count += 1
        print(f"My Solution {self._my_solution_count}")
        for h in range(len(self._my_hours)):
            for t in range(len(self._my_teachers)):
                for r in range(len(self._my_rooms)):
                    for e in range(len(self._my_exams)):
                        if self.Value(self._my_schedule[(h, e, r, t)]):
                            teacher_name = self._my_teachers[t]
                            exam_name = self._my_exams[e]
                            room_name = self._my_rooms[r]
                            hour_name = self._my_hours[h]
                            print(f"hour: {hour_name}, teacher: {teacher_name}, course {exam_name}, room {room_name}.")
        if self._my_solution_count >= self._my_solution_limit:
            print(f"Stop search after {self._my_solution_limit} solutions")
            self.StopSearch()

    def solution_count(self):
        return self._my_solution_count

def main():
    # My Data
    my_teachers = ['profA', 'profB', 'profC', 'profD', 'profE']
    my_rooms = ['A1', 'A2', 'A3', 'A4', 'A5']
    my_exams = ['DevOps', 'Analyse', 'IA', 'FullStack', 'paradigme', 'java']
    my_hours = ['9h', '10h', '11h', '12h', '13h']

    all_teachers = range(len(my_teachers))
    all_rooms = range(len(my_rooms))
    all_exams = range(len(my_exams))
    all_hours = range(len(my_hours))

    # Creates the model.
    model = cp_model.CpModel()

    my_schedule = {}

    for h in all_hours:
        for e in all_exams:
            for r in all_rooms:
                for t in all_teachers:
                    my_schedule[(h, e, r, t)] = model.NewBoolVar(
                        f"h{h}_e{e}_r{r}_t{t}")

    # here we find the Constraints
    for t in all_teachers:
        for h in all_hours:
            model.AddAtMostOne(my_schedule[(h, e, r, t)]
                               for r in all_rooms for e in all_exams)
    #one classroom for a specific hour
    for r in all_rooms:
        for h in all_hours:
            model.AddAtMostOne(my_schedule[(h, e, r, t)]
                               for t in all_teachers for e in all_exams)
   #one exam for a specific hour
    for e in all_exams:
        for h in all_hours:
            model.AddAtMostOne(my_schedule[(h, e, r, t)]
                               for t in all_teachers for r in all_rooms)

    for e in all_exams:
        model.AddAtLeastOne(my_schedule[(h, e, r, t)] for t in all_teachers for h in all_hours for r in all_rooms)

    for h in all_hours:
        model.AddAtLeastOne(my_schedule[(h, e, r, t)] for e in all_exams for r in all_rooms for t in all_teachers)

    #Only one exam per hour
    for h in all_hours:
        model.Add(sum(my_schedule[(h, e, r, t)] for e in all_exams for r in all_rooms for t in all_teachers) >= 1)
    # the solver
    solver = cp_model.CpSolver()

    solution_limit = 5
    solution_printer = MySolutionPrinter(
        my_schedule, my_teachers, my_rooms, my_exams, my_hours, solution_limit
    )

    solver.Solve(model, solution_printer)

if __name__ == "__main__":
    main()
