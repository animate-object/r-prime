from app.src.core.post.formatting_filter import format_text
from app.src.core.post.language_filter import filter_language_strict, filter_language_v2
from app.src.core.post.remove_nonsense_words import remove_nonsense_words
from app.src.core.post.rhyming_filter import make_it_rhyme

sample_text = """
We the master for the playin'?
They back the top him to be the destine
Niggas walk at me some become out the streets back to you
To the floor and papes on the best with a pirls of 
And the one blow shoot beefs
The big things and choes, 
they got the cloud up like 
on the projects, make me 
real but of the streets is saying, 
the did the street corners for start seems
They destiny men does he stay the tryin' 
that we the hood off the real you so the 
world was places and in the hood on the hood believe
So I love the streets that we was stand to the world

The big things, what you think the care and become for the fuck
Niggas when I could real shoot up
"""

sample_text2 = """
I stop the close to the street start to the 
streets and bust time to stay ate the back
The beat the gangsta
I see the project the same start the capeer

Started the beats to the projects
I got the street cars
I see the belly that shots and the hood to the hood station
I don't start the trugh is the belly

The back to the stasin to the truck
I stop a same to the trugh
They can stop and been the big things
And I stop a paper me with the clip
The project the world (I was the real that should be a propers on the projects
I got a stop a little cars
So I can the beat the thing to tell the good
And the book to me to the streets

The beats to the tank to the stasin to the station
I can start of my but they was born the belly
Now I gotta be a man is the cappers
I gotta start to should be me

I was the most man and start of the back to stay at the streets
I gotta be a stare the belly
The crood niggas to the baller on the street start 
to the streets and who beat it to the streets the 

back of the block when you know how we got a street to be the station
I real they don't start of the cops and gripped up
I got the streets the bed cause I was a mad my crew
The truth is the cars and made the station
I say I was to the god come out the close to start of my life
I was a man the trugh to the beat the god on the block
I real that was my mind in the gravey of the belly
I know what I gotta think they sling

It's all for the capes and start with the streets in the streets
I stop the truth and the tracks
I got the streets whisters
So what you know the hood to be the beats
I was the street started to the thing the beat it as a man

I gotta be the cape to when I see the part to be a 
part to be the tracks to the streets the thing to the graze
I say it all to the world (I was a the beats to the hood back to the fuck 

"""

sample_text3 = """
n did they put you in whe man
I d vels flus tVinet?"
What m'en you play hem fired)
Ohat you loy too Earto to sive andry
Lear this comproltad, rem  from the flom been a y'all got t yes hatcuse and with marijt, wases
in prome to bucmin' drt put my eactus)
I'm will good, ac juckunss on your 2I'm brong 
Waiting for comple
Our prey vit Ben forevepre, bet mytell pricand litroe huntlycuns
K-aid which ther mays on your hay?
Ahe 
Me asaiz us if you captorl you conflice?
Allima packs, blied myyelf right
Be dodnt him, or do's neve like thissuallers wat ove twnoudy
We di now if y  Ill-get, m nalsow for a look i -rapper of son the Pasubut in  relliflow
A play youh incembang, now, shills for fmothers wiscombriinced, dicleose they dead)
Aurta us  frtnt  tel buclin' won't get you bigch fighten the and if you'rr lapsnor scrackly
If I got a plame to trassit donted
The projless wetrl burizolyfd-in ath, tsearin' frach, that everst in welk up
I've owify when I'o everyboo buty livether Ge edory with ars cdyeY
An tsink ut enjuct thaI sours onvy ba kstre that As
Drapl you stipl un everything
Got frim the id' gottrover
To impuse this way touopie is my  Jamins
"Hirmpiplkes up anundous gonna suc  a out for whene how where if hundred  uotion wumnoss
Fandy- city, of eat, yeah, momankind, babies no ligtt, m up)
Hendonh whate for o hop myrele, you keep if you stikind, fromlmling of this nigga, and blums
I seen 'em wayset how me holra posing thtos
and one turnat, the full of thim
A-Lavill live fuckin' right, even gonraze  acturied
Ano usJuckin'l that si chip?
A inl
Mare and sure him nigga t in
Han wait that saud
Wiers whe said we wind who my ferDAncs
Yos carse the corr we gonna sicteous up tnie villin'?
Ablried Caure reoper her destrkess
Field fu theif ysull know
cool from either min in ass to purir, hInd discruvedang
You can me a high s iffyin't all fhol work
Then I can't fectin' wemprited
Drink doend like they ever tinna  ara
It sne Bygptor where it before resorn
A fah,red, wuscn go ssict on thids
(Hol' up, bitch) sin m
"""



text = sample_text3
for filter in ([format_text, remove_nonsense_words, make_it_rhyme, filter_language_strict]):
    print("applying filter: {}".format(filter.__name__))
    text=filter.__call__(text)
print(text)