import random

from app.src.core.post.filter_utils import _strip_and_save_pad
from app.src.repository.db_queries import find_rhymes, find_rhymes_v3


def make_it_rhyme(text):
    ret = []
    current_stanza = []
    for line in text.split('\n'):
        if not line:
            ret += ['']
            continue
        current_stanza.append(line.rstrip('\n'))
        if len(current_stanza) == 4:
            ret += apply_rhyme_scheme_to_stanza(
                current_stanza, random.choice(SCHEMES)
            )
            current_stanza = []
    # handle the last stanza if there is one left
    if current_stanza:
        ret += apply_rhyme_scheme_to_stanza(current_stanza, random.choice(SCHEMES))

    return '\n'.join(ret)


def apply_rhyme_scheme_to_stanza(stanza, scheme):
    """
    For our purposes a stanza is a group of up to four lines in which rhyme schemes can be applied
    :param stanza: an array containing up to four lines
    :return: 
    """
    base_dict = dict()
    ret_stanza = []

    # we will prefer to use last word rhymes that haven't been used yet
    used_rhymes =[]

    if len(stanza) < len(scheme):
        scheme = scheme[:len(stanza)]

    for line, rhyme_indicator in zip(stanza, scheme):
        line = line.split()
        last_word = line.pop()
        l_pad, r_pad, last_word = _strip_and_save_pad(last_word)
        if not rhyme_indicator in base_dict:
           base_dict[rhyme_indicator] = last_word
           used_rhymes.append(last_word)
        else:
            db_results = find_rhymes_v3(base_dict[rhyme_indicator])
            potential_rhymes = _extract_from_db_results(db_results)
            if potential_rhymes:
                last_word = _pick_rhyme(potential_rhymes, used_rhymes)
                used_rhymes.append(last_word)
            else:
                # in this case we'll just keep the anomalous word without rhymes
                # TODO maybe we want to pursue an alternate solution
                print("No potential rhymes found for word: ".format(base_dict[rhyme_indicator]))

        line.append(str(l_pad + last_word + r_pad))
        ret_stanza.append(' '.join(line))
    return ret_stanza

def _extract_from_db_results(db_results):
    return [entry[0].lower() for entry in db_results]

def _pick_rhyme(potential_rhymes, used_rhymes):
    potential = set(potential_rhymes)
    used = set(used_rhymes)
    unused = potential - used
    # we prefer unused rhymes if they're available
    if unused:
        return random.choice(list(unused))
    return random.choice(potential_rhymes)

SCHEMES = [
    'abab',
    'aaaa',
    'aabb',
]


sample_text = """
They pass away, they fucking the thing
Start to tell the truglio is the capes
The thing to start to be the streets of the same stop
They want to tell the crazy on my motherhood

I say I can start of the streets that should be a stare the streets the count
But the book to the truck is the beats
I start the bed cat to the streets in the past to the capper
So what you stop a man the streets

I say the project to the most the streets the capes
He start to tell the truglio to be the streets the beats
I wanna be the truglio to the man the streets that was the beat the dealers
Still the things the bitch to be my breaks

I know what I'm sayin' to be the beating to the projects
I love it all to be a bitch you to start street thing
I stop the belly with the money
I say I was the beat is the beats
I was the star and the top and things
They we gotta be a marking the streets that we got it 
out the crown to hear the truck is the beat strategists
I start the man to the streets the projects
I start of my man of the belly

I stop to tese it all to be the truck to start of the streets to 
the streets to could still the streets, the world is the gangsta
I think the thing to weak her to the streets and been the become on the chateaux
The truth to tell the can't start a stare to the world 
I was the belly the streets that start to the streets in the life
I was a stare the beater, the mister the block with the beaten
I start the streets and the streets that concretely
They should start to connected
"""

sample_text2 = """
I stop the close to the street start to the
streets and bust time to stay ate the back
The beat the gangsta
I see the project the same start the capell

Started the beats to the projects
I got the street cars
I see the belly that shots and the hood to the hood station
I don't start the truglio is the belly

The back to the stasi to the truck
I stop a same to the truglio
They can stop and been the big things
And I stop a paper me with the clip
The project the world (I was the real that should be a properly on the projects
I got a stop a little cars
So I can the beat the thing to tell the good
And the book to me to the streets

The beats to the tank to the stasio to the station
I can start of my but they was born the belly
Now I gotta be a man is the capper
I gotta start to should be me

I was the most man and start of the back to stay at the streets
I gotta be a stare the belly
The crook niggardly to the baller on the street start
to the streets and who beat it to the streets the

back of the block when you know how we got a street to be the station
I real they don't start of the cops and gripped up
I got the streets the bed cause I was a mad my crew
The truth is the cars and made the station
I say I was to the god come out the close to start of my life
I was a man the truglio to the beat the god on the block
I real that was my mind in the graveyard of the belly
I know what I gotta think they sling

It's all for the capes and start with the streets in the streets
I stop the truth and the tracks
I got the streets whistle
So what you know the hood to be the beats
I was the street started to the thing the beat it as a man

I gotta be the cape to when I see the part to be a
part to be the tracks to the streets the thing to the graze
I say it all to the world (I was a the beats to the hood back to the fuck

"""

# print(make_it_rhyme(sample_text2))