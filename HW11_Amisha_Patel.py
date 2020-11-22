""" Author  :: Amisha Patel 
    Created :: 11/22/2020 """
import os
import sqlite3
from typing import Dict, DefaultDict, List, Tuple, Iterator, Set
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Amisha_Patel import file_reader

class Major:
    """ This class reperents information for a Major with including:major,flag for required and elective courses"""    
    PT_COL_NAME = ("Major", "Required Courses", "Electives")
    def __init__(self, major: str) -> None:
        self._major: str = major
        self._required: List = list()
        self._elective: List = list()
    def add_course(self, flag: str, course: str) -> None:
        """ This functions add course to the required or elective on the file """
        if flag == "R":
            self._required.append(course)
        elif flag == "E":
            self._elective.append(course)
    def req_course(self) -> List:
        return sorted(self._required)
    def elec_course(self) -> List:
        return sorted(self._elective)
    def info(self) -> List:
        return [self._major, self.req_course(), self.elec_course()]


class Student:
    """This class defines information about a single student with all of the relevant information including"""
    PT_COL_NAME: Tuple[str, str, str, str, str, str, str] = ("CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives", "GPA")
    # grades_to_gpa: Dict[str, float] = {'A': 4.0, 'A-': 3.75, 'B+': 3.25, 'B': 3.0, 'B-':2.75, 'C+': 2.25, 'C': 2.0, 'C-': 0, 'D+': 0, 'D': 0, 'D-': 0, 'F': 0}
    def __init__(self, cwid: str, name: str, major: str, required: List[str], electives: List[str]) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict() 
        self._completed_courses: List[str] = list()
        self._remaining_required: List[str] = list.copy(required)
        self._remaining_electives: List[str] = electives
        self.grades_to_gpa: Dict = {'A': 4.0, 'A-': 3.75, 'B+': 3.25, 'B': 3.0, 'B-': 2.75, 'C+': 2.25, 'C': 2.0, 'D+': 0, 'D': 0, 'D-': 0, 'F': 0}

    def course_grade(self, course: str, grade: str) -> None:
        """ This finction stores the students grade for each course """
        self._courses[course] = grade

        if grade in self.grades_to_gpa:
            self._completed_courses.append(course)
            if course in self._remaining_required:
                self._remaining_required.remove(course)
            elif course in self._remaining_electives:
                self._remaining_electives = list()

    def claculate_gpa(self) -> float:
        """ This finction caluclates the students GPA """
        scores: List = [self.grades_to_gpa[course_gpa] for course_gpa in self._courses.values()]
        if len(scores) > 0:
            return round(sum(scores)/len(scores),2)
        return 0
    def info(self) -> List:
        return [self._cwid, self._name, self._major, sorted(self._completed_courses), sorted(self._remaining_required), sorted(self._remaining_electives), self.claculate_gpa()]
        

class Instructor:
    """ This class reperents information for a Major with including:major,flag for required and elective courses"""
    PT_COL_NAME: List[str] = ["CWID", "Name", "Dept", "Course", "Students"]
    def __init__(self, cwid: str, name: str, department: str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._department: str = department
        self._courses: DefaultDict[str, int] = defaultdict(int) #key: course value: number of students
    def store_course_student(self, course_name: str) -> None:
        self._courses[course_name] += 1
    def info(self) -> Iterator[Tuple]:
        for course, no_students in self._courses.items():
            yield (self._cwid, self._name, self._department, course, no_students)
class Repository:
    """This class reprents all students, instructors for a print pretty tables"""
    def __init__(self, path, pt_tables: bool=True) -> None:
        self._path: str = path 
        self._students: Dict[str, Student] = dict() 
        self._instructors: Dict[str, Instructor] = dict() 
        self._majors: Dict[str, Major] = dict() 
        try:
            self._majors_data()
            self._student_data()
            self._instructor_data()
            self._grades_data()
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as fnfe:
            print(fnfe)

        if pt_tables:
            print("\nMajor Summary")
            self.major_pretty_table()

            print("\nStudent summary")
            self.student_pretty_table()

            print("\nInstructor Summary")
            self.instructor_pretty_table()

            print("\nStudent Grade Summary")
            self.student_grades_table_db(os.path.join(self._path, "HW11.sql"))

    def _majors_data(self) -> None:
        """ This finction defines the majors and requried courses for each major """
        try:
            for major, flag, course in file_reader(os.path.join(self._path, "majors.txt"), 3, "\t", True):
                if major in self._majors:
                    self._majors[major].add_course(flag, course)
                else:
                    self._majors[major] = Major(major)
                    self._majors[major].add_course(flag, course)
        except (FileNotFoundError, ValueError) as e:
            print(e)

    def _student_data(self) -> None:
        """ This finction creates examples of students and updates it in the container"""
        try:
            for cwid, name, major in file_reader(os.path.join(self._path, "students.txt"), 3, "\t", True):
                if cwid in self._students:
                    print(f"{cwid} is duplicate")
                else:
                    self._students[cwid] = Student(cwid, name, major, self._majors[major]._required, self._majors[major]._elective)
        except (FileNotFoundError, ValueError) as e:
            print(e)
    
    def _instructor_data(self) -> None:
        """ This finction  creates examples of instructors and updates it in the container """
        try:
            for cwid, name, department in file_reader(os.path.join(self._path, "instructors.txt"), 3, "\t", True):
                if cwid in self._instructors:
                    print(f"{cwid} is duplicate")
                else:
                    self._instructors[cwid] = Instructor(cwid, name, department)
        except (FileNotFoundError, ValueError) as e:
            print(e)
    
    def _grades_data(self) -> None:
        """ This finction defines the grades file and updates the student and instructor """
        try:
            for cwid, course, grade, instructor_cwid in file_reader(os.path.join(self._path, "grades.txt"), 4, "\t", True):
                if cwid in self._students:
                    s: Student = self._students[cwid]
                    s.course_grade(course, grade)
                else:
                    print(f"Student with id: {cwid} doesn't exist in the student repository")
                
                if instructor_cwid in self._instructors:
                    inst: Instructor = self._instructors[instructor_cwid]
                    inst.store_course_student(course)
                else:
                    print(f"Instructor with id: {cwid} doesn't exist in the instructor repository")

        except (FileNotFoundError, ValueError) as e:
            print(e)
    
    def student_grades_table_db(self, db_path) -> List[Tuple]:
        """ This function defines the data from the database """
        rows: List[Tuple] = list()
        db: sqlite3.Connection = sqlite3.connect(db_path)
        query: str = """ select Name, CWID, Course, Grade, Name
                        from students , grades, instructors 
                        where CWID = StudentCWID and InstructorCWID = CWID
                        order by Name; """
        pt: PrettyTable = PrettyTable(field_names=["Name","CWID","Course","Grade","Instructor"])
        for row in db.execute(query):
            pt.add_row(row)
            rows.append(row)
        print(pt)
        return rows
    
    def student_pretty_table(self) -> None:
        """This finction prints student info pretty table """
        pt: PrettyTable = PrettyTable(field_names=Student.PT_COL_NAME)
        for stud in self._students.values():
            pt.add_row(stud.info())
        print(pt)

    def instructor_pretty_table(self) -> None:
        """ This finction prints  student info pretty table """
        pt: PrettyTable = PrettyTable(field_names=Instructor.PT_COL_NAME)
        for inst in self._instructors.values():
            for each_instructor in inst.info():
                pt.add_row(each_instructor)
        print(pt)

    def major_pretty_table(self) -> None:
        """ print major info pretty table """
        pt: PrettyTable = PrettyTable(field_names=Major.PT_COL_NAME)
        for maj in self._majors.values():
            pt.add_row(maj.info())
        print(pt)

def main():
    try:
        HW11: Repository = Repository('R:/Steven Institute/SSW-810-B/HW11') 
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()