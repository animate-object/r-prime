expletives_full = {
    'ass':'bootay',
    'Ass':'Bootay',
    'bitch':'girl dog',
    'Bitch':'Girl dog',
    'bitches':'girl dogs',
    'Bitches':'Girl Dogs',
    'bitching':'speaking with passion',
    'Bitching':'Speaking with passion',
    'cock':'chicken',
    'Cock':'Chicken',
    'cunt':'nice lady',
    'Cunt':'Nice lady',
    'dick':'phallic object',
    'Dick':'Phallic object',
    'fuck':'love',
    'Fuck':'Love',
    'fucking':'loving',
    'Fucking':'Loving',
    'hell':'a bad place',
    'Hell':'A bad place',
    'niggers':'bros',
    'Niggers':'Bros',
    'niggas':'homies',
    'Niggas':'Homies',
    'nigger':'best bud',
    'Nigger':'Best bud',
    'nigga':'broski',
    'Nigga':'Broski'
}

expletives_light = {
    'fuck':'love',
    'Fuck':'Love',
    'fucking':'love',
    'Fucking':'Loving',
    'niggers':'bros',
    'Niggers':'Bros',
    'niggas':'homies',
    'Niggas':'Homies',
    'nigger':'best bud',
    'Nigger':'Best bud',
    'nigga':'broski',
    'Nigga':'Broski'
}

punctuation = [',','"',';','.','\n']


def filter(text, filter_dict=expletives_light):
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


def filter_strict(text):
    return filter(text, filter_dict=expletives_full)

def main():

    aText = """nigga nigga cunt bitch fuck ass dick
            niggas front fucking hell bitch
            """

    newText = filter_strict(aText)

    print(newText)

main()
