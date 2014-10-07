#import smtplib
from datetime import date

class Patient(object):
    """docstring for Patient"""
    next_appointments  = []

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.full_name = "%s %s" % (self.given_name, self.surname)
        self.next_appt_reminder = False
        
    def __str__(self):
		return "Patient Name: {}\nDate of Birth: {}\nGender: {}\nE-mail: {}".format(self.id_num,self.full_name, self.dob, self.gender,self.email)

    def update_record(self,type_field,value):
        setattr(self, type_field, value)
        if type_field == "given_name":
            self.full_name = "%s %s" % (value, self.surname)
        elif type_field == "surname":
            self.full_name = "%s %s" % (self.given_name, value)
        print("The record field was successfully updated!")

    def appointments(self, type_field, kw = {}):
        #type_field here describe whether an appointment is added, modified or deleted.
        length_next_appt = len(self.next_appointments)
        if type_field == "show":
            if length_next_appt > 0:
                print("Scheduled Appointments")
                for appt in range(length_next_appt):
                    print ("%s. %s at %s" % (appt + 1,self.next_appointments[appt][0],self.next_appointments[appt][1]))
                return len(self.next_appointments)
            else:
                return 0
        else:
            if "add" in kw:
                self.next_appointments += [[kw["add"][0][0],kw["add"][1]]]
                self.next_appointments.sort()
            if "delete" in kw:
                del self.next_appointments[kw["delete"]]
            if "delete" in kw and "add" not in kw:
                print("The appointment was successfully deleted")
            else:
                print("A new appointment on %s (%s) at %s was added the ID number %s (%s).\n" % (kw["add"][0][0], kw["add"][0][1], kw["add"][1], self.id_num, self.full_name))
                