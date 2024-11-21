import time #just to make the code run smoother
import pickle #writing objects to files
import shutil #file operations in general
import os #yet more file operations

running = True
currentQueueNo = 1
patientQueue = []
docList = open("doctorList.dat", "ab+")
adminPass = "abcd" #this code would presumably be open source and the hospital could change this password as they please

class Patient: #patient class
    def __init__(self, name, age, visitReason, doctor, QueueNo):
        self.name = name
        self.age = age
        self.visitReason = visitReason
        self.doctor = doctor
        self.QueueNo = QueueNo
class Doctor:#doctor class 
    def __init__(self, name, docType):
        self.name = name
        self.docType = docType

def newPatient(): # method for adding a patient to the queue
    global currentQueueNo #we need to be able to see the current Queue number so that we can give it to new patients

    validName = False
    validAge = False

    def is_valid_doctor(doc_name):
        # Function to check if the doctor exists in the doctor list. Could've done this directly but I figured this is easier
        with open("doctorList.dat", "rb") as file:
            try:
                while True:
                    doctor = pickle.load(file)
                    if doc_name == doctor.name:
                        return True
            except EOFError:
                pass  # Reached end of file

        return False  # Doctor name not found in the list


    while validName == False:
        newName = input("Please enter the name of the new patient. If you would like to cancel, please input 'CANCEL':") #allowing patients to exit the function if they no longer want to add themselves
        if newName.lower() == "cancel": #controlling the input so we can always check for "cancel" even if they write "CaNCeL" or something
            print("Patient addition cancelled.")
            return #return (stop the function)
        elif any(character.isdigit() for character in newName): #checking that the name is all letters
            print("Names must contain exclusively letters. Please re-enter:")
        else:
            validName = True
            print("Thank you.")
            time.sleep(1)

    while validAge == False:    
        newAge = input("Please enter your age. If you would like to cancel, please input 'CANCEL'")
        if newAge.lower() == "cancel":
            print("Patient addition cancelled.")
            return 
        elif any(character.isdigit() for character in newAge): #checking that the inputted age is all numbers
            validAge = True
            print("Thank you.")
            time.sleep(1)
        else:
            print("Your age must contain only numbers. Please re-enter:")

    print("Available doctors:") 
    docList = []
    with open("doctorList.dat", "rb") as file: #printing all doctors currently in doctorList.dat so that the patient can choose from them
        try:
            while True:
                doctor = pickle.load(file)
                print("Doctor" + doctor.name + ", " + doctor.docType) #displays both the name of the doctor as well as what type of doctor they are, in case that information helps the patient 
                docList.append(doctor.name)
        except EOFError: #this makes it stop if there is nothing else in the file to check
            pass  # Reached end of file

    
    patientDoc = input("Please select a doctor from the list above or type 'Undecided' if you are not sure:") #if the patient does not know what doctor they need, they can put this. The staff will recommend it to them

    if patientDoc.lower() == "undecided": #if the patient picks undecided, they are given a placeholder
        reasonForVisit = input("Please describe your symptoms. The staff will direct you to the right doctor when you are called.")
        patientDoc = "Not Determined"
    else:
        while not is_valid_doctor(patientDoc): #keeps the loop going until doctor entered actually exists in the file
            print("This doctor does not exist. Please enter a valid doctor's name.")
            patientDoc = input("Please enter the name of the Doctor you would like to see. If you would like to cancel, please input 'CANCEL'")
            if patientDoc.lower() == "cancel":
                print("Patient addition cancelled.")
                return 
        reasonForVisit = input("Lastly, please enter the reason for your visit today:") #this is in the else so that it only asks if you didn't put undecided earlier

    newPatient = Patient(newName, int(newAge), reasonForVisit, patientDoc, currentQueueNo) #initializing new patient with these details
    patientQueue.append(newPatient) #adding the patient to the queue
    print(f"A new patient has been added with the name {newName}, age {newAge}, the reason for visiting '{reasonForVisit}', to see doctor {patientDoc}. Your current queue number is {currentQueueNo}.")
    currentQueueNo += 1 #adding 1 to the queue number, so that the next patient will be next in line 

def removePatient(patientName): #in case hospital staff need to remove a patient for any reason. Useful to have 
    removedQueueNo = 0
    removed = False #keeps track of whether or not a patient was found with that name and removed 
    for patient in patientQueue: 
        if patientName == patient.name:
            patientQueue.remove(patient)
            removedQueueNo = patient.QueueNo
            removed = True
            print("Patient removed from queue successfully.")
    if removed == True:
        for patient in patientQueue:
            if patient.QueueNo > removedQueueNo:
                patient.QueueNo -= 1 #every patient who was after the removed patient will have their queue number go down by one 
    else:
        print("There is no such patient currently in the queue.")

def advanceQueue(): #removes the first person in the queue and moves everyone up. If someone leaves, for example, the staff can use this command to advance the queue. 
    patientQueue.pop(0)
    for patient in patientQueue:
        patient.QueueNo -= 1

def viewPatients(): #code for the staff to view all patients and view the details for a specific patient 
    found = False
    print("The current patients in the queue are as follows: ")
    for patient in patientQueue: #loops through patients and displays their names 
        print(patient.name)
    patientViewChoice = input("Which patient would you like to view the details of? Please enter.") #allows for the viewing of details of a specific patient
    for patient in patientQueue:
        if patientViewChoice == patient.name:
            print(f"{patient.name} is {patient.age} years old and is here for '{patient.visitReason}'. They are here to see doctor {patient.doctor}, and are in queue position {patient.QueueNo}.")
            found = True
    if found == False:
        print("No patient was found by that name.") 


def newDoc(): #method for creating a new doctor 
    validName = False #used to make sure the inputed information is correct
    validDocType = False #used to make sure the inputed information is correct
    while validName == False: #keeps looping until it's a valid name (all letters)
        newDocName = input("Please enter the last name of the Doctor you would like to add:")
        if any(letter.isdigit() for letter in newDocName):
            print("Please input a valid name. Names must contain only letters:")
        else:
            validName = True
            print("Thank you.")
    while validDocType == False: #keeps looping until its a valid doctor type (all letters)
        newDocType = input("What type of doctor is this new doctor (ex. Physician, etc)?")
        if any(letter.isdigit() for letter in newDocType):
            print("Please input a valid doctor type. It must include only letters.")
        else:
            validDocType = True
            print("Thank you.")
    newDoctor = Doctor(newDocName,newDocType) #initializing new doctor with these details
    with open("doctorList.dat", "ab") as file: #opening the doctorList file in append binary mode so the new doctor can be added
        pickle.dump(newDoctor, file) #we need pickle to write objects to files 
    print(f"A new doctor has been added with the name {newDocName} and of type {newDocType}.")
    time.sleep(2)      

def docNameSearch(nameToSearch): #code for checking if a doctor exists by name 
    found = False
    with open("doctorList.dat", "rb") as file:
        try:
            while True:
                doctor = pickle.load(file)
                if nameToSearch == doctor.name:
                    print(f"This hospital has a doctor named {doctor.name}. They are a {doctor.docType}.")
                    found = True
                    return  # Exit function if doctor is found
        except EOFError:
            pass  # Reached end of file
    if found == False:
        print("There is no doctor in this hospital by that name.")

def deleteDoc(nameToDelete): #code for deleting a doctor by name 
    found = False
    temp_file = "temp.dat"  # Temporary file to store updated contents 
    with open("doctorList.dat", "rb") as read_file, open(temp_file, "wb") as write_file:
        try:
            while True: #this while loop looks through the file and, if the searched doctor is not whatever doctor is currently being looked at, it puts it in a temporary file.
                doctor = pickle.load(read_file) #this effectively creates a new file with every doctor except the one you want to delete
                if nameToDelete != doctor.name:
                    pickle.dump(doctor, write_file)  
                else:
                    found = True  # Mark doctor as found
        except EOFError:
            pass  # Reached end of file

    if found:
        shutil.move(temp_file, "doctorList.dat") #shutil.move just replaces the second file with the first file
        print(f"Doctor with the name {nameToDelete} has been deleted.")
    else:
        os.remove(temp_file)  # Remove temp file if doctor wasn't found, so it doesnt just stay in the computer
        print(f"No doctor found with the name {nameToDelete}.")

#everything below here is just a general menu
while running == True:
    print("Welcome to the hospital. Here are your currently available actions:")
    print("1. Enter queue") #runs newPatient()
    print("2. Admin controls") 
    patientChoice = input("What would you like to do? Please enter:")
    if patientChoice == "1":
        newPatient()
    elif patientChoice == "2":
        passInput = input("To enter admin controls, please enter the admin password:")
        if passInput == adminPass:
            adminMode = True
            while adminMode == True:
                print("Here are your currently available actions:") #these all run their equivalent functions 
                print("1. Add a new doctor") 
                print("2. Delete a doctor")
                print("3. Search for doctor by name")
                print("4. View patients")
                print("5. Remove patient from queue")
                print("6. Advance queue")
                print("7. Back") #returns to the previous menu for patients 
                adminChoice = input("What would you like to do?")
                if adminChoice == "1":
                    newDoc()
                elif adminChoice == "2":
                    deleteChoice = input("Please enter the name of the doctor you would like to delete.")
                    deleteDoc(deleteChoice)
                    time.sleep(2)
                elif adminChoice == "3":
                    searchChoice = input("Please enter the name of the doctor you would like to search.")
                    docNameSearch(searchChoice)
                    time.sleep(2)
                elif adminChoice == "4":
                    viewPatients()
                    time.sleep(2)
                elif adminChoice == "5":
                    removeChoice = input("Please enter the name of the patient you would like to remove.")
                    removePatient(removeChoice)
                    time.sleep(2)
                elif adminChoice == "6":
                    advanceQueue()
                    print("Queue has been advanced by 1.")
                elif adminChoice == "7":
                    print("Returning to patient menu...")
                    time.sleep(1)
                    adminMode = False
                else:
                    print("That is not a valid choice.") #anything other than the specified numbers results in this  
        else:
            print("Admin password incorrect!")
            time.sleep(2)           
    else:
        print("That is not a valid choice.") #anything other than the specified numbers results in this 
        time.sleep(2)



        
    



    

