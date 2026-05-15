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

SPECIES_ACCENT = {
    'dell': '#3b82f6',
    'hp': '#14b8a6',
    'supermicro': '#22c55e',
    'rpi': '#ec4899',
    'macmini': '#64748b',
    'whitebox': '#f97316',
    'mystery': '#a855f7',
}

SPECIES_BG = {
    'dell': '#dbeafe',
    'hp': '#ccfbf1',
    'supermicro': '#dcfce7',
    'rpi': '#fce7f3',
    'macmini': '#f1f5f9',
    'whitebox': '#ffedd5',
    'mystery': '#f3e8ff',
}


@register.filter
def species_emoji(species):
    return SPECIES_EMOJI.get(species, '🖥️')


@register.filter
def species_accent(species):
    return SPECIES_ACCENT.get(species, '#78716c')


@register.filter
def species_bg(species):
    return SPECIES_BG.get(species, '#f5f5f4')


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})
