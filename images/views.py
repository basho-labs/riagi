from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext

from images.forms import UploadForm
from images.services import ImageService, ImageError
from users.service import UserService

def upload(request):
    if request.method == "POST":
        upload = UploadForm(request.POST, request.FILES)
        filename = upload.save(request)
        if filename:
            return HttpResponseRedirect("/i/%s" % filename)
        else:
            user = None
            if 'user_id' in request.session:
                user_service = UserService()
                user = user_service.get(request.session['user_id'])
            return render(request, 'home.html', {"user": user, "upload_form": upload}, context_instance=RequestContext(request))
    elif "url" in request.GET:
        image_service = ImageService()
        try:
            key = image_service.store_from_url(request.GET["url"], request.session["user_id"])
            return HttpResponseRedirect("/i/%s" % key)
        except ImageError as e:
            return HttpResponse(e.msg, status=400)
    else:
        return HttpResponseRedirect("/")

def show(request, image_id):
    image_service = ImageService()
    image = image_service.find_metadata(str(image_id))
    if image:
        return render_to_response('images/show.html', {'image': image},
            context_instance=RequestContext(request))
    else:
        raise Http404

def fetch(request, image_id, thumb=False):
    image_service = ImageService()
    image = image_service.find(str(image_id), thumb=thumb)
    if image:
        return HttpResponse(content=image.get_data(), mimetype=image.get_content_type())
    else:
        raise Http404

def mine(request):
    if not 'user_id' in request.session:
        return redirect("/")

    user = request.session['user_id']
    image_service = ImageService()
    images = image_service.find_all(user)
    return render_to_response("images/mine.html", {'images': images},
            context_instance=RequestContext(request))
