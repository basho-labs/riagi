from django import forms
from images.services import ImageService
from PIL import Image
from StringIO import StringIO

class UploadForm(forms.Form):
    image = forms.ImageField()

    def save(self, request):
        file = request.FILES['image']
        image_service = ImageService()
        user_id = request.session['user_id']
        image = file.read()
        thumbnail = Image.open(file.temporary_file_path())
        thumbnail.thumbnail((128, 128), Image.ANTIALIAS)
        thumbio = StringIO()
        thumbnail.save(thumbio, format="jpeg")
        return image_service.store(image, thumbio.getvalue(),  user_id, file.content_type)
