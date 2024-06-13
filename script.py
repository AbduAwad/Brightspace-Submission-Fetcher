import os
import shutil
import csv
import zipfile

from constants import STUDENT_ALLOCATION_START, STUDENT_ALLOCATION_END, SUBMISSIONS_ZIP_PATH, SUBMISSIONS_CSV_PATH, TA_MARKING_PATH


def get_student_allocation() -> set:
    with open(SUBMISSIONS_CSV_PATH, 'r') as file: # Open the submissions csv file and read it
        csv_reader = csv.reader(file)
        submissions = []
        for row in csv_reader:
            submissions.append(list(row))

        student_allocations = set()
        for i in range(STUDENT_ALLOCATION_START - 1, STUDENT_ALLOCATION_END): # get the student number and the allocation
            student_allocations.add(submissions[i][3])

    return student_allocations


def unzip_brighstace_zip_submission() -> list:
    os.mkdir(TA_MARKING_PATH) # Create the directory to unzip the submissions to
    with zipfile.ZipFile(SUBMISSIONS_ZIP_PATH, 'r') as zip_ref: # Unzip the submissions zip file
        zip_ref.extractall(TA_MARKING_PATH) # unzip to the TA_MARKING_PATH
        files = zip_ref.namelist()
    return files


def remove_non_allocated_students(student_allocations: set, files: list) -> None:
        for i in range(len(files) - 1): # iterate through the files, dont count index.html
            print('filename:', files[i])
            student_number = files[i].split(' ')[4].replace('-', '') # get the student number from the file name
            if not student_number.isdigit(): # if the student number string isnt an int:
                student_number = files[i].split(' ')[5].replace('-', '')
            print('Student number:', student_number)
            if (student_number not in student_allocations):
                print('Student number:', student_number, 'is not in the allocation set')
                if (os.path.isdir(files[i].split('/')[0])):
                    shutil.rmtree(files[i].split('/')[0]) # remove the directory (student number) that is not in the allocation set
            else:
                print('Student number:', student_number, 'is in the allocation set')


def unzip_allocated_student_files(directories: list) -> None:
        for directory in directories:
            os.chdir(directory)  # cd into it and unzip the file if it ends with .zip
            files = os.listdir()
            for file in files:
                if file.endswith('.zip'):
                    with zipfile.ZipFile(file, 'r') as zip_ref:
                        zip_ref.extractall()
                    os.remove(file)
            os.chdir(TA_MARKING_PATH)

def main(): 
    
    student_allocations = get_student_allocation() # get the student allocations
    files = unzip_brighstace_zip_submission() # unzip the submissions to the TA_MARKING_PATH directory - where you are marking
    
    os.chdir(TA_MARKING_PATH) # cd into the TA_MARKING_PATH
    os.remove('index.html') # remove the index.html file
    
    remove_non_allocated_students(student_allocations, files) # remove the students who are not in the allocation set
    
    directories = os.listdir(TA_MARKING_PATH)
    unzip_allocated_student_files(directories) # unzip the allocated students files

    # Count the number of files to be marked as a sanity check
    print('Number of files to be marked:', len(os.listdir(TA_MARKING_PATH))) 
    print("Number of students who should be marked:", len(student_allocations))

if __name__ == '__main__':
    main()