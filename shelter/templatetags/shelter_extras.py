from django import template

register = template.Library()

SPECIES_EMOJI = {
    'dell': '🖥️',
    'hp': '💻',
    'supermicro': '🗄️',
    'rpi': '🍓',
    'macmini': '🍎',
    'whitebox': '📦',
    'mystery': '❓',
}


@register.filter
def species_emoji(species):
    return SPECIES_EMOJI.get(species, '🖥️')


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})
