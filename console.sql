select CWID,Name,"Course	",count(*) as NumberOfCourse from instructors join grades on CWID = InstructorCWID group by "Course	";
