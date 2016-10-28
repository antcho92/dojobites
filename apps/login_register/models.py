from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
SPACE_REGEX = re.compile('.*\s')

class UserManager(models.Manager):
    def validate_reg(self, input):
        errors = []
        fname = input['fname']
        lname = input['lname']
        email = input['email']
        pw = input['pw']
        pw_conf = input['pw_confirm']
        if not fname or fname.isspace():
            errors.append(("Please enter your first name!","fname"))
        elif len(fname) < 2 or not fname.isalpha():
            errors.append(("First name is invalid!","fname"))
        if not lname or lname.isspace():
            errors.append(("Please enter your last name!","lname"))
        elif len(lname) < 2 or not lname.isalpha():
            errors.append(("Last name is invalid!","lname"))
        if not email or email.isspace():
            errors.append(("Please enter your email!","email"))
        elif not EMAIL_REGEX.match(email):
            errors.append(("Email is invalid!","email"))
        elif self.filter(email__iexact=email).exists():
            errors.append(("Email already exists!","register"))
        if not pw or pw.isspace():
            errors.append(("Please create a new password.","pw"))
        elif SPACE_REGEX.match(pw) or len(pw) < 8:
            errors.append(("Please create a new password as per the criteria.","pw"))
        if not pw == pw_conf:
            errors.append(("The passwords entered don't match.","confirm"))
        if errors:
            return (False, errors)
        else:
            hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            user = self.create(first_name=fname, last_name=lname, email=email, pw_hash=hashed)
            return (True, user)

    def validate_log(self, input):
        errors = []
        user = User.objects.filter(email=input['email'])
        if user.exists():
            hashed_pw = user[0].pw_hash.encode()
            input_pw = input['pw'].encode()
            if bcrypt.checkpw(input_pw, hashed_pw):
                return (True, user[0])
            else:
                errors.append(("Incorrect password!","login_pw"))
        else:
            errors.append(("Email address doesn't exist!","login_email"))
        return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=100)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.first_name + " " + self.last_name
