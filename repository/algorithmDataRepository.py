
class AlgorithmDataRepository:
    def __init__(self, file):
        self._file = file
        self._data = []

        self._runId = 0
        self.loadData()

    def loadData(self):
        with open(self._file) as file:
            lines = file.readlines()
            for line in lines:
                tokens = line.split()
                run = {
                    "run_id": int(tokens[0]),
                    "seed": int(tokens[1]),
                    "fitness": int(tokens[2]),
                    "number_of_detected_positions": int(tokens[3])
                }
                self._data.append(run)
                if run['run_id'] > self._runId:
                    self._runId = run['run_id']

    def saveRun(self, seed, fitness, numberOfDetectedPositions):
        self._runId += 1
        run = {
            "run_id": self._runId,
            "seed": seed,
            "fitness": fitness,
            "number_of_detected_positions": numberOfDetectedPositions
        }

        self._data.append(run)
        with open(self._file, "a") as file:
            file.write(f"{self._runId} {seed} {fitness} {numberOfDetectedPositions}\n")

    def getData(self):
        self.loadData()
        return self._data
