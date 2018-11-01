from warrant import Cognito
from config import cognito_userpool_id, cognito_app_client_id

u = Cognito(cognito_userpool_id, cognito_app_client_id, username='yiming')

# u.add_base_attributes(email='yimingsun1994@gmail.com')
#
# u.register('yiming', 'abcd1234')

# u.confirm_sign_up('678419', username='yiming')

au = u.authenticate('1234')
print(au, type(au))