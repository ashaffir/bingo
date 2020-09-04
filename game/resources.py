from import_export import resources
from .models import Picture

class PictureResource(resources.ModelResource):
    class Meta:
        model = Picture