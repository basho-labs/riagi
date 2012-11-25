from django import forms
from riagi.images.services import ImageService


class UploadForm(forms.Form):
    image = forms.ImageField()

    def save(self, request):
        if 'image' in request.FILES:
            file = request.FILES['image']
            image_service = ImageService()
            user_id = request.session['user_id']
            return image_service.store(file, user_id, file.content_type)
