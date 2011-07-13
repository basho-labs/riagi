from django import forms
from images.services import ImageService

class UploadForm(forms.Form):
    image = forms.FileField()

    def save(self, request):
        file = request.FILES['image']
        image_service = ImageService()
        image_service.store(file.read(), request.session['username'], file.content_type)
