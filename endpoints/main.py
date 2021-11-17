
# [START endpoints_email_api_imports]
import endpoints
from endpoints import message_types
from endpoints import messages
from endpoints import remote
# [END endpoints_email_api_imports]
class EmailRequest(messages.Message):
    message = messages.StringField(1)
class EmailResponse(messages.Message):
    message = messages.StringField(1)
    
#Add Endpoint API below

class EmailApi(remote.Service):
    
    #Add Endpoint Method Path below
    
    
    def get_user_email(self, request):
        user = endpoints.get_current_user()
        # If there's no user defined, the request was unauthenticated, so we
        # raise 401 Unauthorized.
        if not user:
            raise endpoints.UnauthorizedException
        return EmailResponse(message=user.email())
# [END endpoints_email_api_class]
# [START endpoints_api_server]
api = endpoints.api_server([EmailApi])
# [END endpoints_api_server]
