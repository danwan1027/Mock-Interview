from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, email, name, password, role, profile_image, created_at, student_id=None, classroom=None, seat_number=None, school=None, department=None, teacher=None):
        
        self.student_id = student_id
        self.classroom = classroom
        self.seat_number = seat_number
        self.school = school
        self.department = department
        self.teacher = teacher
        self.id = id
        self.email = email
        self.username = name
        self.password = password
        self.role = role
        self.profile_image = profile_image
        self.created_at = created_at

    def check_password(self, password):
        if self.password == password: print('wrong')
        else: print('correct')
        return self.password == password
    

    