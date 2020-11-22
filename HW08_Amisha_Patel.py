""" Author  :: Amisha Patel 
     Created :: 11/08/2020 """
from datetime import datetime, timedelta,date
from typing import Tuple,Iterator,Dict
from prettytable import PrettyTable
import os
def date_arithmetic() -> Tuple[datetime, datetime, int]:
    """ This Function returns date for three days """
    three_days_after_02272020: datetime =  datetime.strptime('Feb 27, 2020', "%b %d, %Y") + timedelta(days = 3) 
    three_days_after_02272019: datetime =  datetime.strptime('Feb 27, 2019', "%b %d, %Y")+ timedelta(days = 3) 
    days_passed_01012019_09302019: int = (datetime.strptime('Sep 30, 2019', "%b %d, %Y") - datetime.strptime('Feb 1, 2019', "%b %d, %Y")).days
    return three_days_after_02272020, three_days_after_02272019, days_passed_01012019_09302019
def file_reader(path, fields, sep=',', header=False) -> Iterator[Tuple[str]]:
    """This Functiuons returns a tuple containing values """
    count = 1
    try:
        fopen= open(path,'r')
    except FileNotFoundError:
        print("File cannot found,Please try again!")
    else:
        with fopen:
            if header:
                next(fopen)
            for line in fopen:
                values = line.rstrip('\n').split(sep)
                if len(values) != fields:
                    raise ValueError(f'{os.path.basename(path)} has  {len(values)} fields on line {count} but excepted {fields}')
                count +=1
                yield tuple(values)
class FileAnalyzer:
    def __init__(self, directory: str) -> None:
        """ Theis function calls the analyze_file function"""
        self.directory: str = directory
        self.files_summary: Dict[str, Dict[str, int]] = dict() 
        self.analyze_files() 
    def analyze_files(self) -> None:
        """ This function analyzes files to be count the functions,classes, characters and lines"""
        try:
            directory: [str] = os.listdir(self.directory)    
        except FileNotFoundError:
            raise FileNotFoundError("Can not find a file.Please try again!")
        else:
            for file in directory:
                if file.endswith(".py"):
                    self.files_summary[file]={}
                    try:
                        fopen = open(os.path.join(self.directory,file),'r')
                    except FileNotFoundError:
                        raise FileNotFoundError(file,'does not exist')
                    else:
                        with fopen:
                            self.files_summary[file]['line'] = sum(1 for line in fopen)
                            dCount = 0
                            c = 0
                            fopen.seek(0)
                            data = fopen.read()
                            ch = len(data)
                            fopen.seek(0)
                            for line in fopen:
                                line = line.strip('\n')
                                word = line.split()
                                if 'def' in word and line.endswith(':'):
                                    dCount = dCount + 1
                                if 'class' in word and line.endswith(':'):
                                    c = c + 1
                            self.files_summary[file]['function'] = dCount
                            self.files_summary[file]['class'] = c
                            self.files_summary[file]['char'] = ch
    def pretty_print(self) -> None:
        """ This functionprints the file name, class count, function count, no of lines and no of character in each py file"""
        pt:PrettyTable = PrettyTable()
        pt.field_names: list = [
            "File Name",
            "Classes",
            "Functions",
            "Lines",
            "ch"]
        for k1, v1 in self.files_summary.items():
            ln = list()
            ln.append(k1)
            ln.append(v1['class'])
            ln.append(v1['function'])
            ln.append(v1['line'])
            ln.append(v1['char'])
            pt.add_row(ln)
        return pt
def main() -> None:      
    print(date_arithmetic())
    path = "R:/Steven Institute/SSW -810-B/foo.txt"
    for cwid, name, major in file_reader(path, 3, sep='|', header=True):  
        print(f"cwid: {cwid} name: {name} major: {major}") 
    o = FileAnalyzer('R:/Steven Institute/SSW -810-B')
    o.analyze_files()
    print(o.pretty_print())
if __name__ == "__main__":
    main()