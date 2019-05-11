import csv


class loader:
    def __init__(self, path):
        self.path = path

    def setPath(self, path):
        self.path = path

    def __extract(self):
        with open(self.path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter='|')
            table = []
            for row in readCSV:
                if len(row) != 0:
                    if not str(row[0]).isalpha():
                        for i in range(0, len(row)):
                            row[i] = float(row[i])
                        table.append(row)
        return table

    def getTable(self):
        return self.__extract()


if __name__ == "__main__":
    # test
    load = loader('newtonOutput.csv')
    tablet = load.getTable()
    for r in tablet:
        print(r)
