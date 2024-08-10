from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, email, name, password, role, profile_image, created_at):
        
        self.id = id
        self.email = email
        self.username = name
        self.password = password
        self.role = role
        self.profile_image = profile_image
        self.created_at = created_at

    def check_password(self, password):
        return self.password == password
    

    