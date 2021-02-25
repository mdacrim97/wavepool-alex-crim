from django.template import loader
from django.http import HttpResponse
from django.views import generic

from wavepool.models import NewsPost
from wavepool.code_exercise_defs import code_exercise_defs, code_review_defs, code_design_defs
from django.conf import settings


def front_page(request):
    """ View for the site's front page
        Returns all available newsposts, formatted like:
            cover_story: the newsposts with is_cover_story = True
            top_stories: the 3 most recent newsposts that are not cover story
            archive: the rest of the newsposts, sorted by most recent
    """
    #simply order by publish_date and then strip from 4th entry to the end
    template = loader.get_template('wavepool/frontpage.html')
    cover_story = NewsPost.objects.all().order_by('-publish_date').first()
    top_stories = NewsPost.objects.all().order_by('-publish_date')[:3]
    other_stories = NewsPost.objects.all().order_by('-publish_date')[4:]

    context = {
        'cover_story': cover_story,
        'top_stories': top_stories,
        'archive': other_stories,
    }

    return HttpResponse(template.render(context, request))


class NewspostDetail(generic.DetailView):
    model = NewsPost
    template_name = 'wavepool/newspost.html'


def instructions(request):
    template = loader.get_template('wavepool/instructions.html')

    context = {
        'code_exercise_defs': code_exercise_defs,
        'code_design_defs': code_design_defs,
        'code_review_defs': code_review_defs,
        'show_senior_exercises': settings.SENIOR_USER,
    }
    return HttpResponse(template.render(context, request))
