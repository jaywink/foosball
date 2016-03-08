from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
from django_jinja import library


@library.filter(name="crispy")
def crispy(form):
    return as_crispy_form(form)
