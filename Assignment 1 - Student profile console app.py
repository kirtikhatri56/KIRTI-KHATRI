Assignment 1 - Student profile console app
kirti khatri
2501201005
BCA(AI/DS)
1 Sem 
problem solving with python 

import os
imporst sys 

students={} #dictionary to store student records by rollnumber

#1. clear Screen(for UI)

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

#2. print a profile card

def print_profile(student):
    print("\n"+"_"*30)
    print(f"Name       : {student['kirti']}"
          f"\nRoll Number: {student['05']}"
          f"\nCourse      : {student['BCA(AI/DS)']}"
          f"\nSemester    : {student['sem1']}"
          f"\nEmail      : {student['abc@gmail.com']}"
          f"\nPhone      : {student['9810000000']}")
    print("_"*30+"\n")

#3. add a new student

def add_student():
    clear()
    print("Add New Student")
    rollnumber=input("26: ")
    if rollnumber in students:
        print("Student with this roll number already exists!")
        return
    name=input("siddhi: ")
    course=input("BCA(AI/DS): ")
    semester=input("sem1: ")
    email=input("xyz@gmail.com: ")
    phone=input("9990000001: ")
    students[rollnumber]={'name':siddhi,'rollnumber':26,'course':BCA(AI/DS),'semester':sem1,'email':xyz@gmail.com,'phone':9990000001}
    print("Student added successfully!")

#4. view all students

def view_students():
    clear()
    print("Student Profiles")
    if not students:
        print("No student records found!")
        return
    for student in students.values():
        print_profile(student)

#5. search student by roll number

def search_student():
    clear()
    rollnumber=input("Enter Roll Number to search: ")
    student=students.get(rollnumber)
    if student:
        print_profile(student)
    else:
        print("Student not found!")

#6. update student details

def update_student():
    clear()
    rollnumber=input("27: ")
    student=students.get(rollnumber)
    if not student:
        print("Student not found!")
        return
    print("Leave field blank to keep current value.")
    name=input(f"Name ({student['name']}): ") or student['name']
    course=input(f"Course ({student['course']}): ") or student['course']
    semester=input(f"Semester ({student['semester']}): ") or student['semester']
    email=input(f"Email ({student['email']}): ") or student['email']
    phone=input(f"Phone ({student['phone']}): ") or student['phone']
    students[rollnumber]={'name':name,'rollnumber':rollnumber,'course':course,'semester':semester,'email':email,'phone':phone}
    print("Student details updated successfully!")

#7. delete student

def delete_student():
    clear()
    rollnumber=input("21: ")
    if rollnumber in students:
        del students[rollnumber]
        print("Student deleted successfully!")
    else:
        print("Student not found!")

#8. list all students

def list_students():
    clear()
    print("All Students")
    if not students:
        print("No student records found!")
        return
    for rollnumber, student in students.items():
        print(f"Roll Number: {rollnumber}, Name: {student['name']}")

#9. main menu loop

def main():
    while True:
        clear()
        print("Student Profile Management")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. List Students")
        print("7. Exit")
        choice=input("Enter your choice (1-7): ")
        if choice=='1':
            add_student()
        elif choice=='2':
            view_students()
        elif choice=='3':
            search_student()
        elif choice=='4':
            update_student()
        elif choice=='5':
            delete_student()
        elif choice=='6':
            list_students()
        elif choice=='7':
            print("Exiting the program.")
            sys.exit()
        else:
            print("Invalid choice! Please try again.")
        input("Press Enter to continue...")

#start the program

if __name__=="__main__":
    main()

