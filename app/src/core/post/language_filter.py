from app.src.core.post.filter_utils import _strip_and_save_pad

expletives_full = {
    'ass':'bootay',
    'Ass':'Bootay',
    'bitch':'young lady',
    'Bitch':'Young lady',
    'bitches':'young lades',
    'Bitches':'Young lades',
    'bitching':'speaking with passion',
    'Bitching':'Speaking with passion',
    'cock':'chicken',
    'Cock':'Chicken',
    'cunt':'nice lady',
    'Cunt':'Nice lady',
    'Pussy':'Cat',
    'pussy':'cat',
    'dick':'noodle',
    'Dick':'Noodle',
    'fuck':'love',
    'Fuck':'Love',
    'Fucked': 'Loved',
    'fucked': 'loved',
    'fucking':'loving',
    'Fucking':'Loving',
    'hell':'a bad place',
    'Hell':'A bad place',
    'Ho': 'Female acquaintances',
    'ho': 'female acquaintances',
    'Hoes': 'Female acquaintances',
    'hoes': 'femalse acquaintances',
    'niggers':'bros',
    'Niggers':'Bros',
    'niggas':'homies',
    'Niggas':'Homies',
    'nigger':'best bud',
    'Nigger':'Best bud',
    'nigga':'broski',
    'Nigga':'Broski',
    'Motherfucker':'Rude dude',
    'motherfucker': 'rude dude',
    'Motherfuckers': 'Rude dudes',
    'motherfuckers': 'rude dudes',
    'Mothafucka': 'Rude lad',
    'mothafucka': 'rude lad',
    'Mothafuckas': 'Rude lads',
    'mothafuckas': 'rude lads'
}

expletives_light = {
    'fuck':'love',
    'Fuck':'Love',
    'Fucked':'Loved',
    'fucked':'loved',
    'fucking':'love',
    'Fucking':'Loving',
    'niggers':'bros',
    'Niggers':'Bros',
    'niggas':'homies',
    'Niggas':'Homies',
    'nigger':'best bud',
    'Nigger':'Best bud',
    'nigga':'broski',
    'Nigga':'Broski',
    'Motherfucker':'Rude dude',
    'motherfucker':'rude dude',
    'Motherfuckers': 'Rude dudes',
    'motherfuckers': 'rude dudes',
    'Mothafucka':'Rude lad',
    'mothafucka':'rude lad',
    'Mothafuckas':'Rude lads',
    'mothafuckas':'rude lads'
}

punctuation = [',','"',';','.','\n']


def filter_language(text, filter_dict=expletives_light):
    new_text = ""
    stripped_word = ""
    for word in text.split(" "):
            stripped_word = ''.join([i for i in word if i not in punctuation])
            if stripped_word in filter_dict:
                new_text += filter_dict[stripped_word]
                if not word[len(word)-1].isalpha():
                    new_text += word[len(word)-1]
            else:
                new_text += word
            new_text+=' '
    return new_text

def filter_language_v2(text, filter_dict=expletives_light):
    ret = []
    for line in text.split('\n'):
        new_line = []
        for word in line.rstrip('\n').split():
            l_pad, r_pad, stripped = _strip_and_save_pad(word)
            if stripped in filter_dict:
                replacement = l_pad + filter_dict[stripped] + r_pad
                new_line.append(replacement)
            else:
                new_line.append(word)
        ret.append(' '.join(new_line))
    return '\n'.join(ret)

def filter_language_strict(text):
    return filter_language_v2(text, filter_dict=expletives_full)
