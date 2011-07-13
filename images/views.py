from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from images.forms import UploadForm
from images.services import ImageService

def upload(request):
    if request.method == "POST":
        upload = UploadForm(request.POST, request.FILES)
        filename = upload.save(request)
        return HttpResponseRedirect("/images/%s" % filename)
    else:
        return HttpResponseRedirect("/")

def show(request, image_id):
    image_service = ImageService()
    image = image_service.find_metadata(str(image_id))
    if image:
        return render_to_response('images/show.html', {'image': image})
    else:
        raise Http404

def fetch(request, image_id):
    image_service = ImageService()
    image = image_service.find(str(image_id))
    if image:
        return HttpResponse(content=image.get_data(), mimetype=image.get_content_type())

    else:
        raise Http404


