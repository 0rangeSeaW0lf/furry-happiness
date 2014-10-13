# ================================================================================================ #
# ================================================================================================ #
# Programming Foundations with Python - Final Project                                              #
# Appointment Scheduling App                                                                       #
# ================================================================================================ #
# ================================================================================================ #

# ================================================================================================ #
# General Comments - Running Instructions
# ================================================================================================ #
# 
# Make sure the python file "record.py" and this file (appontment.py) are in the same folder.
# To escape a field or operation at any time, type "-esc" (without the quotes).
# To avoid problems with the smtplib library, please make sure not python file named email (email.py) is in the same directory.
#
# ================================================================================================ #
# Imported Files and Libraries
# ================================================================================================ #

from datetime import date,time,timedelta,datetime # use to manage all dates
from re import findall,search # Regular Expressions Library. This library was used to perform a basic e-mail format validation.
import pickle #Backup and restore patients and appointments' data

from record import Patient #Patient class (record.py)

import smtplib # required to send e-mails
from email.MIMEMultipart import MIMEMultipart #required to send formatted emails.
from email.MIMEText import MIMEText # Same as above

# ================================================================================================ #
# Dictionaries
# ================================================================================================ #


# ------------------------------------------------------------------------------------------------ #
#Patient records
# ------------------------------------------------------------------------------------------------ #
# Load patient records in the program
try:
    all_patients = pickle.load(open( "patients.p", "rb" ))
except:
    all_patients = {}


# ------------------------------------------------------------------------------------------------ #
# Patient's appointments
# ------------------------------------------------------------------------------------------------ #
# Load patient appointments in the program
try:
    all_appointments = pickle.load(open( "appointments.p", "rb" ))
except:
    all_appointments = {}

# ================================================================================================ #
# Texts
# ================================================================================================ #


# ------------------------------------------------------------------------------------------------ #
# Scheduled Appointments Menu
# ------------------------------------------------------------------------------------------------ #

scheduled_appt_list = ["SCHEDULED APPOINTMENTS",
                        ["Today", "scheduled_appointments('today', all_appointments, all_patients)"],
                        ["Tomorrow", "scheduled_appointments('tomorrow', all_appointments, all_patients)"],
                        ["Week", "scheduled_appointments('week', all_appointments, all_patients)"],
                        ["Next week", "scheduled_appointments('next-week', all_appointments, all_patients)"],
                        ["Return to the main menu", "main_menu_list"]]

# ------------------------------------------------------------------------------------------------ #
# Appointments Management menu
# ------------------------------------------------------------------------------------------------ #

appt_list = ["APPOINTMENTS",
                ["Add new appointment", "patient_appointment('add')"],
                ["Modify appointment", "patient_appointment('modify')"],
                ["Delete appointment", "patient_appointment('delete')"],
                ["Send appointment reminders", "send_remider(all_appointments)"],
                ["Return to the main menu", "main_menu_list"]]

# ------------------------------------------------------------------------------------------------ #
# Patient Records Management menu
# ------------------------------------------------------------------------------------------------ #

patients_list = ["PATIENTS",
                    ["Search patient record","patient_management('search')"],
                    ["Add new patient record","patient_management('add')"],
                    ["Modify patient record","patient_management('modify')"],
                    ["Delete patient record","patient_management('delete')"],
                    [ "Return to the main menu", "main_menu_list"]]

# ------------------------------------------------------------------------------------------------ #
# Main Menu
# ------------------------------------------------------------------------------------------------ #

main_menu_list = ["MAIN MENU",
                    ["Scheduled Appointments","scheduled_appt_list"],
                    ["Appointments","appt_list"],
                    ["Patients","patients_list"],
                    ["Exit program","-QUIT"]]

# ------------------------------------------------------------------------------------------------ #
# Patient Information Rules Text
# ------------------------------------------------------------------------------------------------ #
# Rules to be display when one of the keys is  called
input_rules = {"id_num":"For Venezuelan citizens, please type the letter 'v' followed by the national ID number.\nFor Alien Residents, please type the letter 'e' followed by the national ID number\nFor all other foreign citizens, please type the letter 'p' followed by the passport number.","given_name":"Please type the name as shown on the official ID.","surname":"Please type the name as shown on the official ID.","dob":"Please type the date of birth of the patient (DD/MM/YYYY)","gender": "Please type M for Male and F for Female", "email":"Remember that a valid address should include a domain and extension (e.g. john.doe@internet.com)"}


# ================================================================================================ #
#Variables and genera lists
# ================================================================================================ #

# Current date - used in multiple procedures and displayed when the program starts.
today = date.today(); today_ISO = today.isoformat()

# Week Number
week = today.isocalendar()

# Patient Records Fields
patient_record_fields = ["PATIENT RECORD FIELDS",["ID number","id_num"],["Given Name","given_name"],["Surname","surname"],["Date of Birth","dob"], ["Gender","gender"], ["E-mail","email"]]

# Variable to control the functionality among menus
current_menu = main_menu_list

# Most used error message
error_input = "Error, please type a valid input!\n"

# Variables containing main menus
menus = ["main_menu_list","scheduled_appt_list","patients_list","appt_list","settings_list"]

#Official Public Holidays in Venezuela
fixed_public_holidays = ["1/1","23/1","19/4","1/5","24/6","5/7","24/7","12/10","24/12","25/12","31/12"]

# Message shown when no appointments were found.
no_appt_scheduled = "No appointments scheduled"


# ================================================================================================ #
# Procedures
# ================================================================================================ #

# ------------------------------------------------------------------------------------------------ #
# Menu Management
# ------------------------------------------------------------------------------------------------ #
# Generate the displayed menu
# Input: Menu List
# Output: Display Menu

def show_menu(menu):
    print("")
    print(menu[0])
    print("="*(len(menu[0])+1))
    # Generate a visual menu based on the menu list
    for item in range(1,len(menu)):
        print("%d. %s") % (item,menu[item][0])
# ------------------------------------------------------------------------------------------------ #
# Procedure to confirm inputs from the user
# ------------------------------------------------------------------------------------------------ #
# 
# Input: User Input (character y, n or any other specific one - e.g. letter R)
# Output: True, False or the specific character

def user_confirmation(value):
    while True:
        confirmation = raw_input("> ")
        print("")
        if confirmation in ["Y","y"]:
            return True
        elif confirmation in ["n","N"]:
            return False
        # Verify whether value was chosen and is not empty
        elif confirmation == value and confirmation !="":
            return value
        elif confirmation == "-esc":
            return "-esc"
        elif confirmation == "-quit":
            return quit_program()
        else:
            print("Wrong input. Please type 'Y' for Yes or 'n' for No")

# ------------------------------------------------------------------------------------------------ #
# Procedure to generate Menus and validate user input on selection
# ------------------------------------------------------------------------------------------------ #
# Input: List
# Output: Display menu
def menu_pick(menu,extra = ""):
    while True:
        show_menu(menu)
        if extra == "return":
            pass
        else:
            print("%d. Return to the previous menu") % len(menu)
        user_input = raw_input("> ")
        # Exit program
        if user_input == "-quit":
            return quit_program()
        elif user_input == "-esc":
            return
        # Verify the input is a number
        if user_input.isdigit() and int(user_input) in range(1,len(menu) + 1):
            if int(user_input) == len(menu):
                return ""
            return menu[int(user_input)][1]
        else:
            print("Please choose a valid option!")

# ------------------------------------------------------------------------------------------------ #
# Procedure to manage patient records
# ------------------------------------------------------------------------------------------------ #
#
# Input: Action (add, modify, delete or search), Patient ID
# Output: Patient Information (including scheduled appointments) or the addition, modification or deletion of an appointment

def patient_management(type_field, id_num_key = "", not_found = 0):
    while True:
        if not id_num_key:
            print(input_rules["id_num"])
            print("")
            print("Please type the official ID number of the patient (e.g. v12345):\n")
            
            patient_data = check_input("id_num_key","","")
            
            if patient_data == "-esc":
                return
            
        else:
            patient_data = id_num_key
        # ************************************************************************************ #
        # Add a record
        # ************************************************************************************ #
        if type_field == "add":
            if patient_data in all_patients:
                print("A patient record link to the ID %s was found in the General Records" % check_input("id_num",patient_data))
                print("Do you want to modify (Y/n)?")
                if user_confirmation(""):
                    return patient_management("modify",patient_data,"0")
                else:
                    return
            else:
                patient_record = {}; patient_record = {"id_num":check_input("id_num",patient_data)}
                # Iterate to add the different fields required in the patient record
                for field in range(2,len(patient_record_fields)):
                    print("")
                    print(input_rules[patient_record_fields[field][1]])
                    print("")
                    field_to_modify = check_input(patient_record_fields[field][1],"",(patient_record_fields[field][0] + ":"))
                    if field_to_modify == "-esc":
                        return
                    patient_record[patient_record_fields[field][1]] = field_to_modify
                    
                all_patients[patient_data] = Patient(**patient_record)
                print("\nPatient record successfully created!\n")
                print("Do you want to schedule an appointment (Y/n)?")
                if user_confirmation(""):
                    return patient_appointment("add",patient_data)
                else:
                    return
        else:
            if patient_data in all_patients:
                # **************************************************************************** #
                # Delete a patient record (easiest method)
                # **************************************************************************** #
                if type_field == "delete":
                        print("Are you sure you want to delete the patient record of {} {} ({}) (Y/n)?".format(all_patients[patient_data].given_name,all_patients[patient_data].surname, all_patients[patient_data].id_num))
                        if user_confirmation(""):
                            document = all_patients[patient_data].id_num
                            # Delete appointments
                            print all_appointments
                            for day in all_appointments.keys():
                                for time in all_appointments[day].keys():
                                    if all_appointments[day][time] == patient_data:
                                        print all_appointments[day][time]
                                        del all_appointments[day][time]
                            print all_appointments
                            del all_patients[patient_data]
                            print("The patient record linked to the ID number %s was successfully deleted" % document)
                        return
                else:
                    # ************************************************************************ #
                    # Modify a patient record
                    # ************************************************************************ #
                    if type_field == "modify":
                        print("\nPatient Name: {} {}".format(all_patients[patient_data].given_name,all_patients[patient_data].surname))
                        option = menu_pick(patient_record_fields)
                        try:
                            print(input_rules[option])
                            if option == "id_num":
                                new_value = check_input("id_num_key")
                                all_patients[new_value] = all_patients[patient_data]
                                del all_patients[patient_data]
                                patient_data = new_value
                                new_value = check_input("id_num",new_value)
                            else:
                                new_value = check_input(option)
                                
                            all_patients[patient_data].update_record(option,new_value)
                            
                            print("Do you want to modify other field or record (Y/n)?\nYou can also press 'R' to modify other patient record")
                            confirm = user_confirmation("R")
                            if confirm == True:
                                return patient_management("modify",patient_data)
                            elif confirm == "R":
                                return patient_management("modify")
                            else:
                                return
                        except:
                            return
                    # ************************************************************************ #
                    # Search a patient record
                    # ************************************************************************ #
                    if type_field == "search":
                        #Print patient record
                        print(all_patients[patient_data])
                        # Print appointments
                        appts = all_patients[patient_data].appointments("show","")
                        if appts == 0: # In case there are no appointments linked
                            print("No scheduled appointments found")
                            return
                        return
                    return
            else:
                if not_found == "0":
                    print("No patient record linked to the ID number %s was found.\n\
                    Do you want to try again (Y/n)?" % check_input("id_num",patient_data))
                    if not user_confirmation(""):
                        return
                    elif user_confirmation("") == "esc":
                        return
                    else:
                        return patient_management(type_field,"","1")
                else:
                    print("No patient record linked to the ID number %s was found again.\nDo you want to try again (Y/n) or create a new record (press 'R')?" % check_input("id_num",patient_data))
                    confirm = user_confirmation("R")
                    if confirm == True:
                        return patient_management(type_field,"","1")
                    elif confirm == "R":
                        print("ID Number: %s" % check_input("id_num", patient_data, ""))
                        print("")
                        return patient_management("add",patient_data)
                    else:
                        return

# ------------------------------------------------------------------------------------------------ #
# Procedure to check inputs and format them according to certain parameters
# ------------------------------------------------------------------------------------------------ #
# Input: User input or variable
# Output: Formatted and valid data input 

def check_input(type_field,data_field = "", input_field = ""):
    global current_day
    while True:
        if type_field == "time":
            current_time = datetime.now().time()
            print("Current Time: %s" % current_time.strftime("%I:%M %p"))
            print("")
        if not input_field:
            input_field = ">"
        # User input if data_field was not provided.
        if not data_field:
            patient_data = raw_input("%s " % input_field).lower()
            print(""),
            if patient_data == "-esc":
                return "-esc"
            if patient_data == "-quit":
                return quit_program()
        else:
            patient_data = data_field
        # ******************************************************************************************* #
        # ID Number
        # ******************************************************************************************* #
        if type_field == "id_num" or type_field == "id_num_key":
            patient_data = patient_data.translate(None,"-")
            if ((patient_data[0] in ["v","e"] and patient_data[1:].isdigit()) or patient_data[0] == "p") and len(patient_data) > 5:
                if type_field == "id_num":
                    return "{}-{}".format(patient_data[0].upper(), patient_data[1:].upper())
                else:
                    return patient_data
        # ******************************************************************************************* #
        # Full Name
        # ******************************************************************************************* #
        if type_field == "given_name" or type_field == "surname":
            if len(patient_data) > 1:
                return patient_data.title()
        # ******************************************************************************************* #
        # Date of Birth
        # ******************************************************************************************* #
        if type_field == "dob":
            patient_data = patient_data.split("/")
            try:
                patient_data = date(int(patient_data[2]),int(patient_data[1]),int(patient_data[0]))
                if patient_data - today < timedelta(1) and today - patient_data < timedelta(43830): # timedelta 1 so today could be add and 43830 is the days equivalent of 120 years.
                    print("Please confirm the date of birth (Y/n):")
                    print("{} ({} years old)".format(patient_data.strftime("%d %B %Y"),(int((today-patient_data).total_seconds()/(365.25*24*60*60)))))
                    if user_confirmation(""):
                        return patient_data.strftime("%d %B %Y")
                    elif user_confirmation("") == "-esc":
                        return "-esc"
                    else:
                        return check_input("dob","","Date of Birth: ")
                else:
                    pass
            except:
                pass
        # ******************************************************************************************* #
        # Check Gender
        # ******************************************************************************************* #
        if type_field == "gender":
            if patient_data in ["m","f"]:
                if patient_data == "m":
                    return "Male"
                else:
                    return "Female"
        # ******************************************************************************************* #
        # Check e-mail
        # ******************************************************************************************* #
        if type_field == "email":
            match = search(r'[\w.-]+@[\w.-]+.\w+', patient_data)
            if match:
                return patient_data
        # ******************************************************************************************* #
        # Check validity date
        # ******************************************************************************************* #
        if type_field == "date":
            patient_data = patient_data.split("/")
            try:
                patient_data[2], patient_data[1], patient_data[0] = int(patient_data[2]),int(patient_data[1]),int(patient_data[0])
                appt_date = date(patient_data[2], patient_data[1], patient_data[0])
                current_day = (appt_date - today) < timedelta(1)
                # Check that the date is not in the past
                if appt_date - today < timedelta(0):
                    print("The chosen date is in the past. Please, try again")
                    return check_input("date","","New Date: ")
                # Check that the date is not 5 years
                elif appt_date - today > timedelta(1826): # 5 years (including leap year)
                    print("The chosen date is too far in the future (more than 5 years). Please, try again")
                    return check_input("date","","New Date: ")
                # Check whether the date is on a business day
                elif appt_date.isoweekday() > 5:
                    print("%s is %s" % (appt_date.strftime("%d %B %Y"), appt_date.strftime("%A")))
                    print("Do you still want to proceed (Y/n)?")
                    if user_confirmation(""):
                        return appt_date.strftime("%d-%b-%y"),appt_date.strftime("%A")
                    else:
                        return check_input("date","","New Date (DD/MM/YYYY):")
                # Check whether the date is a public holiday
                elif ("%s/%s" % (appt_date.day,appt_date.month)) in fixed_public_holidays:
                    print("%s is a Public Holiday" % appt_date.strftime("%d %B %Y"))
                    print("Do you still want to proceed (Y/n)?")
                    if user_confirmation(""):
                        return appt_date.strftime("%d-%b-%y"),appt_date.strftime("%A")
                    elif user_confirmation("") == "-esc":
                        return "-esc"
                    else:
                        return check_input("date","","New Date (DD/MM/YYYY):")
                else:
                    return appt_date.strftime("%d-%b-%y"),appt_date.strftime("%A")
            except:
                patient_data = ""
                appt_date = ""
        # ******************************************************************************************* #
        # Check validity time
        # ******************************************************************************************* #
        if type_field == "time":
            appt_time = findall("\d+", patient_data); 
            if "pm" in patient_data or "am" in patient_data:
                appt_time = int(appt_time[0])
            if "pm" in patient_data and appt_time < 12:
                appt_time += 12
            elif "am" in patient_data and appt_time == 12:
                appt_time = 0
                
            if isinstance(appt_time,int):
                appt_time = time(appt_time)
                # Check whether the desired hour is not in the past
                if current_day:
                    if (datetime.combine(today,appt_time) - datetime.now()) < timedelta(0):
                        print("The chosen time is in the past. Please, try again")
                        return(check_input("time","", "Time (am/pm):"))
                # Check whether the desired hour is within business hours
                if (appt_time >= time(8) and appt_time < time (10)) or (appt_time >= time(18) and appt_time < time(21)):
                    print("The chosen time is out of regular business hours")
                    print("Do you still want to proceed (Y/n)?")
                    if user_confirmation(""):
                        return appt_time.strftime("%I:%M %p")
                    elif user_confirmation("") == "-esc":
                        return "-esc"
                    else:
                        return check_input("time","","New Time (am/pm):")
                # Check whether the desired hour is not within the allowed hours
                elif appt_time >= time(21) or appt_time < time(8):
                    print("Sorry the desired hour is not allowed. Please try again")
                    return(check_input("time","","New Time (am/pm):"))
                else:
                    return appt_time.strftime("%I:%M %p")
        
        print(error_input)
        print("")

# ------------------------------------------------------------------------------------------------ #
# Procedure to manage appointments
# ------------------------------------------------------------------------------------------------ #
# Add, modify and delete appointments
# Inputs: patient ID, date and time
# Output: appointment in patient's record and all_appointments dic

def patient_appointment(type_field,patient_data = "", appointment_info = {}):
    appointment_info = {}
    while True:
        if not patient_data:
            print(input_rules["id_num"])
            print("")
            print("Please type the official ID number of the patient (e.g. v12345):\n")
            
            patient_data = check_input("id_num_key")
            print("")
            
            if patient_data == "-esc":
                return False
            
        if patient_data in all_patients:
            # ************************************************************************************ #
            # Add a new patient appointment
            # ************************************************************************************ #
            if type_field == "add":
                print("")
                print("Please check with the Dr. Reyes before booking an appointment during the weekend or Public Holiday\n")
                appt_date = check_input("date","","Date (DD/MM/YYYY):")
                if appt_date == "-esc":
                    return
                appointment_info["add"] = [appt_date]
                # I know I can use \n to put all the text in a single print call
                print("")
                print("Normal Business Hours: 10:00am - 06:00pm")
                print("Extended Business Hours: 08:00 - 10:00am and 06:00pm - 09:00pm")
                print("Any other hour is not allowed.")
                appt_time = check_input('time',"","Time (am/pm):")
                if appt_time == "-esc":
                    return
                appointment_info["add"] += [appt_time]
                
                # Date not in the dictionary
                if not appointment_info["add"][0][0] in all_appointments:
                    all_appointments[appointment_info["add"][0][0]] = {appointment_info["add"][1]:patient_data}
                
                else:
                    # Date in the dictionary, but not hour
                    if appointment_info["add"][1] not in all_appointments[appointment_info["add"][0][0]]:
                        all_appointments[appointment_info["add"][0][0]][appointment_info["add"][1]] = patient_data
                    else:
                        # Both day and hour in the dictionary (i.e. taken)
                        if all_appointments[appointment_info["add"][0][0]][appointment_info["add"][1]] == patient_data:
                            # By you
                            print("The selected ID already has an appointment at the requested time and date")
                        else:
                            # By another patient
                            print("The requested appointment slot is taken.")
                        print("Do you want try again (Y/n)?")
                        if user_confirmation(""):
                            return patient_appointment("add",patient_data)
                        else:
                            return
                all_patients[patient_data].appointments("add",appointment_info)
                print("Do you want to book another appointment (Y/n)?")
                if user_confirmation(""):
                    return patient_appointment("add",patient_data)
                else:
                    return
            else:
                # ************************************************************************************ #
                # Modify or Delete Appointments
                # ************************************************************************************ #
                appts = all_patients[patient_data].appointments("show","")
                if appts == 0:
                    print("No scheduled appointments found")
                    print("Do you want to book an appointment (Y/n)?")
                    if user_confirmation(""):
                        return patient_appointment("add",patient_data)
                    else:
                        return
                else:
                    while True:
                        print("Choose an appointment:")
                        user_input = raw_input(">")
                        if user_input == "-esc":
                            return
                        if user_input.isdigit() and int(user_input) > 0 and int(user_input) <= appts:
                            user_input = int(user_input)
                            if user_input <= appts:
                                user_input -= 1
                                # Delete an appointment
                                appointment_info["delete"] = user_input
                                del all_appointments[all_patients[patient_data].next_appointments[user_input][0]][all_patients[patient_data].next_appointments[user_input][1]]
                                all_patients[patient_data].appointments("delete",appointment_info)
                                if type_field == "modify":
                                    # Add an appoitment after it was deleted -> Modify an appointment
                                    return patient_appointment("add",patient_data,appointment_info)
                            print("Do you want to delete another appointment (Y/n)?")
                            if user_confirmation(""):
                                return patient_appointment("delete",patient_data)
                            else:
                                return
                        else:
                            print("Please choose a valid option!")
                return
                
        else:
            print("No patient record linked to the ID number %s was found.\nDo you want to try again (Y/n) or create a new record (press 'R')?" % check_input("id_num",patient_data))
            confirm = user_confirmation("R")
            if confirm == True:
                return patient_appointment("type_field")
            elif confirm == "R":
                return patient_management("add",patient_data,"0")
            else:
                return
# ------------------------------------------------------------------------------------------------ #
# Procedure to send an e-mail
# ------------------------------------------------------------------------------------------------ #
# Send reminders to patients
# Input: Patient's data (Full name, e-mail, next appoitment date and time)
# Output: e-mail send to the patient

def send_message(name,to_address, time, date):
    from_address = 'test.dra.reyes@gmail.com'
    # Declare a MIME type message
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Your doctor's appointment is soon!"
    # E-mail Message
    body = "Dear %s,\n\nYour doctor\'s appointment is on %s at %s.\n\nIf you need to change or cancel it, please contact us.\n\nThanks!\n\n\nThe doctor's office team" % (name,date, time)
    msg.attach(MIMEText(body, 'plain'))
    msg = msg.as_string()

    # Credentials
    username = 'test.dra.reyes@gmail.com'
    password = '0n3t4mGXQ369JzL'
    
    # Send email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)   
    server.sendmail(from_address, to_address, msg)
    server.quit() 

# ------------------------------------------------------------------------------------------------ #
# Procedure to show scheduled appointments:
# ------------------------------------------------------------------------------------------------ #
# Show coming appointments
# Input: specific date (e.g. today), appointment dictionary
# Output: appointments scheduled for the desired date range or a message if there are not any.

def scheduled_appointments(field,kwargs,kw):
    w_day = today.isoweekday()
    dates = []
    days_w = 0
    print("")
    if field == "today":
        dates = [today.strftime("%d-%b-%y")]
    elif field == "tomorrow":
        dates = [(today+timedelta(1)).strftime("%d-%b-%y")]
    elif field == "week":
        print("Week: %s" % str(week[1]))
        while w_day <= 7:
            dates.append((today + timedelta(days_w)).strftime("%d-%b-%y"))
            days_w += 1
            w_day += 1
    elif field == "next-week":
        day = today
        print("Week: %s" % str(week[1] + 1))
        while True:
            if day.isoweekday() != 1:
                day += timedelta(1)
            else:
                break
        while days_w < 7:
            dates.append((day + timedelta(days_w)).strftime("%d-%b-%y"))
            days_w += 1
    for date in dates:
        print("")
        print date
        print("="*len(date))
        
        if date in kwargs:
            if kwargs[date]:
                for key in kwargs[date]:
                    print("%s: %s (%s)" % (key, kw[kwargs[date][key]].full_name, kw[kwargs[date][key]].id_num))
            else:
                print(no_appt_scheduled)
        else:
            print(no_appt_scheduled)
    return
    
# ------------------------------------------------------------------------------------------------ #
# Procedure to send a reminder
# ------------------------------------------------------------------------------------------------ #
# Procedure to pick the dates and patient to be reminded about their appointments
# Input: Appointment Dictionary
# Output: Total number of reminders sent

def send_remider(patient_appts):
    tomorrow = today + timedelta(1)
        
    if tomorrow.isoweekday() > 5:
        appointments = [tomorrow.strftime("%d-%b-%y"),(tomorrow + timedelta(1)).strftime("%d-%b-%y"),(tomorrow + timedelta(2)).strftime("%d-%b-%y")]
    else:
        appointments = [tomorrow.strftime("%d-%b-%y")]
    
    total = 0
    
    for date in appointments:
        if date in patient_appts:
            for time in patient_appts[date]:
                send_message(all_patients[patient_appts[date][time]].full_name,all_patients[patient_appts[date][time]].email, time, date)
                total += 1
        
    if total == 0:
        print("No appointments found")
    elif total == 1:
        print("1 reminder was sent")
    else:
        print("%s reminders were sent" % total)
    print("")
    
def quit_program():
    pickle.dump(all_patients, open("patients.p", "wb"))
    pickle.dump(all_appointments, open("appointments.p", "wb"))
    quit()
                
# ================================================================================================ #
# Main Block
# ================================================================================================ #

# ------------------------------------------------------------------------------------------------ #
# Welcome Message
# ------------------------------------------------------------------------------------------------ #

print("Welcome to the Patient Management System (BETA)\n\n\
Today is %s\nWeek: %s" % (today.strftime("%A %d %B %Y"),week[1]))

while True:
    show_menu(current_menu)
    print("\nIMPORTANT -> At any time, to cancel an input, please type \"-esc\"(do not include the quotes), and to exit the program, kindly, type \"-quit\" (without the quotes as well)\n")
    user_input = raw_input("> ")
    # Check options is an integer and within the range of menu options
    if user_input == "-quit":
        quit_program()
        
    if user_input.isdigit() and int(user_input) < len(current_menu) and user_input != 0:
        user_input = int(user_input)
        if current_menu[user_input][1] == "-QUIT":
            last_access_date = today
            pickle.dump(all_patients, open("patients.p", "wb"))
            pickle.dump(all_appointments, open("appointments.p", "wb"))
            print("Do you want to send reminders (Y/n)?")
            if user_confirmation(""):
                send_remider(all_appointments)
            print("Goodbye!\n")
            break
        else:
            if current_menu[user_input][1] in menus:
                current_menu = eval(current_menu[user_input][1])
            else:
                eval(current_menu[user_input][1])
    else:
        print(error_input)