class CSVWriter:
    def __init__(self):
        self.cells = {}

    def writeToFile(self, filePath):
        with open(filePath, "w") as file:
            for row in range(max(self.cells.keys()) + 1):
                if row in self.cells:
                    for column in range(max(self.cells[row].keys()) + 1):
                        if column in self.cells[row]:
                            file.write(self.escapeString(self.cells[row][column]))

                        file.write(",")

                file.write("\n")

    def escapeString(self, string):
        if "\"" in string or "," in string:
            return "\"" + string.replace("\"", "\"\"") + "\""

        return string

    def writeCell(self, content, column, row):
        if not row in self.cells:
            self.cells[row] = {}

        self.cells[row][column] = str(content)

    def append(self, writer, startColumn, startRow):
        for row in range(max(writer.cells.keys()) + 1):
            if row in writer.cells:
                for column in range(max(writer.cells[row].keys()) + 1):
                    if column in writer.cells[row]:
                        self.writeCell(writer.cells[row][column], startColumn + column, startRow + row)
