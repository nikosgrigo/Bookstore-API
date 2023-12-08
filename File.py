
import csv

class File():
    def read_file(self,path,mode ='r'):
        with open(path, mode = mode)as file:
            data = csv.DictReader(file)
            # for lines in data:
            #     print(lines)
            return list(data)
    
    def write_file(self,path,row,mode = 'a'):
        with open(path, mode, newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(row)