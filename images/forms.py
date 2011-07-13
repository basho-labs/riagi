from django import forms
from images.services import ImageService

class UploadForm(forms.Form):
    image = forms.FileField()

    def save(self, request):
        file = request.FILES['image']
        image_service = ImageService()
        user_id = request.session['user_id']
        return image_service.store(file.read(), user_id, file.content_type)
