from import_export import resources
from users.models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User