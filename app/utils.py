from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AppTokenGeneratorEmail(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))



class AppTokenGeneratorPassword(PasswordResetTokenGenerator):
    pass

token_generator_email = AppTokenGeneratorEmail()
token_generator_password = AppTokenGeneratorPassword()