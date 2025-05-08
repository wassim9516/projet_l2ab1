from django import template
from benvoplanify.models import Benevole

register = template.Library()

@register.filter
def dict_get(dictionary, key):
   return dictionary.get(key)
    
