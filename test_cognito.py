from warrant import Cognito
from .config import cognito_userpool_id, cognito_app_client_id

u = Cognito(cognito_userpool_id, cognito_app_client_id)

# u.add_base_attributes(email='yimingsun1994@gmail.com')
#
# u.register('yiming', 'abcd1234')

u.confirm_sign_up('489947', username='yiming')