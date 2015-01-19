from askbot.utils.decorator import ajax_only
from askbot.utils.decorator import post_only
from askbot.utils.views import PjaxView
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import get_template
from .forms import ItemForm
from .forms import ItemsForm
from .models import AuditedThread
from .models import AuditedPost
from .models import AdminTag

def home(request):
    if request.user.is_anonymous():
        raise Http404
    if not request.user.is_administrator_or_moderator():
        raise Http404

    data = LoadItems().get_context(request)
    #add context for the sidebar
    data.update({
        'admin_tags': AdminTag.objects.all(),
    })
    return render(request, 'askbot_audit/home.html', data)


@ajax_only
@post_only
def approve_item(request):
    #get AuditedPost by id
    form = ItemForm(request.POST)
    if not form.is_valid():
        raise HttpResponseBadRequest()

    item_id = form.cleaned_data['item_id']
    post_ref = get_object_or_404(AuditedPost, pk=item_id)
    thread_ref = post_ref.audited_thread
    #delete item
    post_ref.delete()

    response_data = {'post_approved': True}

    #count remaining items, if 0, delete AuditedThread
    sibling_post_refs = AuditedPost.objects.filter(audited_thread=thread_ref)
    count = sibling_post_refs.count()
    if count == 0:
        thread_ref.delete()
        response_data['thread_approved'] = True
    
    return response_data


class LoadItems(PjaxView):
    http_method_names = ('get',)
    template_name = 'askbot_audit/items.html'

    def get_context(request):
        """Items can be selected by:
        * admin tag on the post
        * post language
        * author
        * date (all/since yesterday/last week/last month)

        And sorted by:
        * date
        * activity
        * answers
        * votes
        """
        form = ItemsForm(request.GET)
        form.full_clean()#always valid
        data = {
            'selected_tag_ids': form.cleaned_data['tag_ids'],
            'selected_languages': form.cleaned_data['languages'],
            'selected_user_name': form.cleaned_data['user_name'],
            'selected_period': form.cleaned_data['period']
        }

        return data
