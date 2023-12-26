import time,copy,sys
from functools import partial

from dataclasses import dataclass
from browser import document, html, timer, window, alert, bind
from browser.html import *
"""
import  dragdrop 
from dragdrop import px, arrangeAll, order, actionList, postArrange
import random
from dragdrop2 import dragover, drop, mydrop, mydragstart, playdrop, mousedown, flipper, change_card_id
from dragdrop2 import px, rankSlots, assignedSlots,snapoverRank,flip, animateCSS
import dragdrop2 
content_date =None
content_deck = None

shuffleDoneAction=None
"""
from aq_data import top_ten_data

content_index = 0
previous_deck = None
current_stream = None
    
def more_forwards():
    return content_index < len(top_ten_data) - 1

def more_backwards():
    return content_index > 1

def get_next_decade(forward=True):
    global content_date, content_deck, content_index, previous_deck
    
    if forward:
        if more_forwards():
            content_index += 1
        else:
            return False
        
    else:
        if more_backwards():
            content_index -= 1
        else:
            return False
    
    deck = top_ten_data[content_index]
    if previous_deck == None:
        previous_deck = copy.copy(deck[1])
    content_date = deck[0]
    content_deck= [AQContent(*p) for p in update(previous_deck, deck[1])]
    previous_deck = copy.copy(deck[1])
    return True

def px(x):
    return str(x) + "px"



stopFlag = False

def init():

    paragraph1 = """
Blah Blah Blah
"""
    """
        inner = DIV(
            select+
            remove
        )
        """
    back_one = BUTTON("<", id="back_one", disabled=True, Class="selector")
    
    back_stream = BUTTON("<<", id="back_stream", disabled=True, Class="selector")
    
    forward_one = BUTTON( ">", disabled=False, id="forward_one", Class="selector")
    forward_stream = BUTTON(">>", id="forward_stream", disabled=False, Class="selector")
    
    def disable_all():
        for e in [back_one, back_stream, forward_one, forward_stream]:
            e.disale = True

    @bind(forward_one, "click")
    def on_forward_one_click(ev):
        disable_all()
        single_step(True)

    @bind(back_one, "click")
    def on_back_click(ev):
        disable_all()
        single_step(False)

    @bind(forward_stream, "click")
    def on_forward_stream_click(ev):
        disable_all()
        
        multi_step(ev, True)
    
    @bind(back_stream, "click")
    def on_back_stream_click(ev):
        disable_all()
        
        multi_step(ev, False)
    
    head =  DIV(
                DIV(H1("Top Ten Pollution Cities")) + 
                P(paragraph1) +
                P("More Blah"), 

                Class="header"
                )
            
            
    document <=  DIV(head, Class="background")
    print(window.innerHeight, head.height)
    try:
                  
        play_height = window.innerHeight - head.height - 50
    except:
        
        play_height = 0
    
    document <= DIV(
        TABLE(
                TR(
                    TD(
                        DIV(back_one) +DIV(back_stream), 
                        width="20%",
                        height=px(play_height)
                        ) +
                    TD(DIV( id="id_main", Class="play"), id="td_main", width="55%" , style={"vertical-align": "top", "background-color": "white",}) +
                    TD(
                        DIV(forward_one) +DIV(forward_stream), 
                        width="20%", 
                        height=px(play_height)
                    )
                    ),
                id="body",
                
                Class="body"
            ),
        Class="background"
        )
    td_main = document['td_main']
    print(td_main.width)
    
    init_rank_holder(document["id_main"], play_height, td_main.width)
    #arrangeCards()
    
    
    xx = None
    @bind(".selector", "click")
    def on_click(ev):
        global xx
        xx = ev.currentTarget.id
        
    @bind(".selector", "mousedown")
    def on_mousedown(ev):
        ev.currentTarget.style["border-style"] = "inset"
    
    @bind(".selector", "mouseup")
    def on_mouseup(ev):
        ev.currentTarget.style["border-style"] = "outset"
    

def init_rank_holder(main, play_height, width):
    global rankSlots
    get_next_decade()
    cardCount = 10
    slot_height = play_height / cardCount
    card_top = 0
    card_left = 0
    card_width = width * 0.9
    card_height = slot_height
    

    for i in range(cardCount):
        row = i

        left = 0
        top = slot_height * i

        rank_id = f'R{i + 1}'
        seq_id = f'W{i + 1}'
        sz = html.DIV("ZZ", Class="rank_hook")
        rank = html.DIV(
          TABLE(
                TR(
                    TD(
            html.DIV(f'{i+1:2d}', Class="index", style={'font-size': 'xx-large', 'text-align': 'right', "width": "2ch",'margin': px(0)}) , 
            width="1%"
            ) 
+
        TD(
            sz
            #width="90%"
            
            )
                    ),
                width="100%"
                    )
, 
            id=rank_id, 
            Class='rank',
            style={ "left": px(left), "top": px(top),"width":px(width),"height":px(slot_height), },
        )
        rankSlots.append(rank)
        cardpos = content_deck[i].Prev_rank
        card = content_deck[cardpos].createCard(i, card_top, card_left, card_width, card_height)
        sz <= card

        main <= rank
    
def arrangeCards():
    global rankSlots
    for i in range(len(rankSlots)):
        card_id=f'C{i}'
        rank_id=f'R{i+1}'
        #snapoverRank(card_id,rank_id)
        document[rank_id].appendChild(document[card_id])
        document[card_id].top=0
        
        document[card_id].left=0


@dataclass
class AQContent():
    City: str
    Value: float
    Current_rank: int
    Prev_rank: int

    def makeHeader(self,cardno):
        header_id = f'H{cardno}'

        header = html.TABLE(
            html.TR(
                html.TD(
                    html.SPAN(
                        self.City, 
                        id=f'Q{cardno}',
                        Class="card-header-text",
                        ), 
                    style={
                        "width": "40%",
                    }

                    ) +
                html.TD(
                    html.DIV(
                        html.SPAN(
                            '{:4.1f}'.format(self.Value),
                            id=f'V{cardno}',
                            Class="card-header-text",
                            ), style={
                            "width": px(100),
                            "color": "white",
                        }

                    )

                )
                ),
            
            id=header_id,
            Class="card-header",
        )
        return header            

    def makeFrontImage(self,cardno):
        image_id = f'I{cardno}'
        body_id = f'B{cardno}'
        #img = content.img_url
        return ""
    """
        return html.DIV(

            "TBD", 
            Class="card-body",
            id=body_id
            )
    """

    def makeBackImage(self,cardno):
        image_id = f'I{cardno}'
        body_id = f'B{cardno}'
        txt_id=f'T{cardno}'
        date_id=f'D{cardno}'
        img = "TBD" # content.img_url

        return html.DIV(
            html.DIV(
                "TBD", 
            id=txt_id,
            Class="card-text"
            ), 
            id=body_id
        )

    def createCard(self, cardno, top, left, width, height):

        card_id = f'C{cardno}'
        self.card = card_id

        header=self.makeHeader(cardno) # this was part of DragDrop, now free-standing
        card = html.DIV(header, 
            id=card_id,
            Class="card",
            style={"position": "absolute", "xwidth":px(width),"height":px(height) })
        busy = False
        return card


        

def whenever(function, state, do):
    _time = None
    def local():
        if function() == state:
            timer.clear_interval(_time)
            do()
    _time = timer.set_interval(local,100)
    local()

rankSlots = []

def all_clear():
    for c in document.select(".card"):
        state = getattr(c, "busy", False)
        #print(f" card {c.id} {state}")
        if state:
            return False
    return True
        
    
def done_arrange():
    global current_stream
    if current_stream != None:
        if more_backwards() and more_forwards():
            current_stream.disabled = False
            return
    
    button_set = {"forward_one",  "forward_stream", "back_one","back_stream"}
    
    disable_set = copy.copy(button_set)
    if more_forwards():
        disable_set -= {"forward_one",  "forward_stream"}
    if more_backwards():
        disable_set -= {"back_one",  "back_stream"}
        
    enable_set = button_set - disable_set
    print(disable_set)

    for b in disable_set:
        document[b].disabled = True
        
    for b in button_set - disable_set:
        document[b].disabled = False
        
        

    


    
def single_step(forward=True):
    global actionList, shuffleDoneAction, content_date, content_deck
    """
    button_set = {"forward_one",  "forward_stream", "back_one","back_stream"}
    for b in button_set:
        document[b].disabled = True
        
    """
    get_next_decade(forward)

    #document['togo'].text = content_date
    print(content_date)

    mp=[(rankSlots[c.Prev_rank].select_one(".card").id, c.Current_rank,c.Prev_rank) for c in content_deck]

    for card_id, c, p in mp:
        newt = content_deck[c].makeHeader(c)
        oldh = document[card_id].select_one(".card-header")
        print(card_id, c, p, oldh.text, newt.text)
        oldh.replaceWith(newt)
        

    move_card([(card_id, c, p) for (card_id, c, p) in mp if c != p])
    whenever(all_clear, True, done_arrange)

def multi_step(ev, forward=True):
    global stopFlag, current_stream
    t = ev.target
    current_stream = t
    stopText = "||"
    if t.text == stopText:
        stopFlag = True
        return
    t.saveText = t.text
    t.text = stopText
    t.disabled = False
    
    def can_move():
        if forward: return more_forwards()
        else:
            return more_backwards()
             
        
    

    def local():
        global stopFlag
        if stopFlag:
            stopFlag = False
            current_stream = None
            ev.target.text = ev.target.saveText
            done_arrange()
            
        elif can_move():
            def busy_check():
                whenever(all_clear, True, local)
            timer.set_timeout(busy_check, 1000)
            single_step(forward)
            #
            #forward_stream.disabled = False
        else:
            done_arrange()
    local()
    
def snapon(rank, card):
     targetRank = document[rankSlots[rank].id].select_one(".rank_hook")
     targetRank <= card
     
def move_card(it):
    single = False
    if len(it) > 0:
        card_id, c, p = it[0]
        print(f"move {card_id} {p} to {c}")
        rank_id=f'R{c+1}'


        shuffleSrc = p
        to = c
        originRank = document[rankSlots[shuffleSrc].id]
        targetRank = document[rankSlots[to].id]
        delta_top = targetRank.top - originRank.top
        delta_left = targetRank.left - originRank.left
        frameCount = 20 * abs(p - c)
        shuffleFrom = to
        src = document[card_id]
        margin = 0
        src.busy = True

        """
        This piece of magic pops the rank to highest priority between slots. This means that
        the shuffled card is always slid from under the origin rank and over the target rank.
        Cool as a penguin's sit-upon.
        """
        #document["Cool as a penguin's sit-upon"].appendChild(originRank)

        def shuffle2(src):
            #src.style.left = px(margin)
            src.style.top = px(margin)
            snapon(to, src)
            
            #print("Done")
            if single:
                move_card(it[1:])
            src.busy = False
        animateCSS(src, frameCount, 30, {
            "top": lambda frame, time: px(delta_top / frameCount * frame + margin),
            "left": lambda frame, time: px(delta_left / frameCount * frame + margin),
            }, shuffle2)
        if not single:
            move_card(it[1:])

    else:
        print("alldone")


def TRTD(*args,**kwargs):
    return TR(TD(*args, **kwargs))


def animateCSS(element, numFrames, timePerFrame, animation, whendone=None):
    """ Adapted from Flanagan's javascript version
    """
    # park these variables inside element - naughty
    element.frame = 0  # // Store current frame number
    element.time = 0.0  # // Store total elapsed time
    """
    // Arrange to call displayNextFrame() every timePerFrame milliseconds.
    // This will display each of the frames of the animation.
    """
    element.intervalId = None

    def displayNextFrame():
        if element.frame >= numFrames:  # // First, see if we're done
            timer.clear_interval(element.intervalId)  # // If so, stop calling ourselves
            """
            del element.frame
            del element.time
            del element.intervalId
            """
            if whendone:
                whendone(element)  # // Invoke whendone function
            return

        for cssprop in animation:
            """
                // For each property, call its animation function, passing the
                // frame number and the elapsed time. Use the return value of the
                // function as the new value of the corresponding style property
                // of the specified element. Use try/catch to ignore any
                // exceptions caused by bad return values.
            """
            element.style[cssprop] = animation[cssprop](element.frame, element.time)

        element.frame += 1  # // Increment the frame number
        element.time += timePerFrame  # // Increment the elapsed time

    element.intervalId = timer.set_interval(displayNextFrame, timePerFrame)

    """
    // The call to animateCSS() returns now, but the previous line ensures that
    // the following nested function will be invoked once for each frame
    // of the animation.

    // Now loop through all properties defined in the animation object
    """


class DragDrop():

    def __init__(self):
        global order, assignedSlots, interface
        dragdrop2.interface = self

        self.ratio=0.05
        self.rank_seperator=0

        get_next_decade()

        self.layout()
        return

    def layout(self):
        init()
        td_main = document['td_main']
        print(td_main.width)

        main = DIV(id='play', Class='play', style={'height': px(600), 'width': px(td_main.width)})
        td_main <= main
        cardCount = 10
        slot_height = play_height / cardCount
        self.card_width = main.width
        self.card_height = slot_height

        for i in range(cardCount):
            vsep = 50
            width = main.width
            row = i

            left = 0
            top = slot_height * i
            height = slot_height

            rank_id = f'R{i + 1}'
            rank = html.DIV(
                html.DIV(f'{i+1:2d}', style={'font-size': 'xx-large', 'text-align': 'left', 'margin': px(0)}),
                id=rank_id,
                Class='rank',
                style={ "left": px(left), "top": px(top),"width":px(width),"height":px(height)},
            )

            #r = self.createRank(i + 1,  0, 0, main.width, vsep)
            #mt <= TRTD(rank)

            cardpos = content_deck[i].Prev_rank
            card = self.createCard(i, content_deck[cardpos], 0, 0)
            rank <= card

            main <= rank






    def createRank(self, rankno, left, top,width,height):
        rank_id = f'R{rankno}'
        rank = html.DIV(html.DIV(str(rankno), style={'font-size': 'xx-small', 'text-align': 'left', 'margin': px(20)}),
                        id=rank_id,
            Class='rank',
            style={"position": "absolute", "left": px(left), "top": px(top),"width":px(width),"height":px(height)},
            )

        rank.bind("drop", mydrop)
        rank.bind("dragover", dragover)
        return rank

    def createLayout(self, columns=4):
        """ 
        Use this as a container for ranking slots. 
        """
        play = html.DIV("",
                        id='play',
            Class='play',
            style={"position": "absolute", "left": px(0), "top": px(0), "width": px(window.innerWidth - 100), "height": px(window.innerHeight - 100)},
            )
        play.bind("dragover", dragover)
        play.bind("drop", playdrop)
        document <= play

        x = html.DIV("",
                     id="Cool as a penguin's sit-upon",
            Class='rank-holder'
            )
        play <= x


        lhmargin = 1
        cardCount = len(content_deck)
        card_rows=cardCount / columns
        #self.card_height= (play.clientHeight - (card_rows * self.rank_seperator)) /card_rows
        self.card_width= play.width / 2
        self.card_height = (play.clientHeight - 20)/ card_rows
        """
        if (self.card_width + self.rank_seperator) * columns > play.width * 0.8:
            self.card_width = ( play.width* 0.8 - (columns * self.rank_seperator)) / columns
            self.card_height = self.card_width * self.ratio
        """

        for i in range(cardCount):
            cardpos = content_deck[i].Prev_rank
            card = self.createCard(i, content_deck[cardpos], 0, 0)
            play <= card

            htext=document[f'Q{i}']
            if htext:
                for s in [20,15,10,5]:
                    card.fs=s
                    document[f'H{i}'].style.fontSize=px(s)
                    if htext.offsetHeight <= 20:
                        break

        # use cardsize to calculate spacings for rank
        c = document[card.id]
        hsep = c.offsetWidth #+ x.width
        vsep = c.offsetHeight #+ x.height

        for i in range(cardCount):
            col = i % columns
            row = (i - col) / columns
            r = self.createRank(i + 1, x.left + (hsep) * (col), x.top + (vsep) * row, c.offsetWidth, c.offsetHeight)
            x <= r
            rankSlots.append(r)
            assignedSlots.append(None)
        play=document['play']

        rhs= html.DIV(id='rhs',
                      style={'position': 'absolute',
                   'right': px(0),
                   'width': px(200),
                   'border': '3px solid red',
                   })
        arrange = html.BUTTON("Arrange")
        arrange.bind("click",on_arrange)
        restart = html.BUTTON("Restart")
        restart.bind("click", on_restart)

        date_display = html.DIV(
            html.DIV(html.SPAN("Date",Class='control-text'))+
            html.DIV(
                html.SPAN(
                    html.SPAN(content_date,id='togo',Class='foreground')+
                    html.SPAN("8888",id='togo2',Class='background')
                    ),
                Class="Clock-Wrapper",
                colspan=2

                ),
            style={
                "right": px(0),
                "width": px(120), 
                #'float': 'right',
                'margin-right': px(10),

                },

        )
        rhs <= date_display
        rhs <= html.DIV(arrange) + html.DIV(restart)
        play <= rhs

        self.arrangeCards(content_deck.sort(key=lambda c: c.Prev_rank), rankSlots)


    def createCard(self, cardno, content: AQContent, left, top):
        def get_body_text(content: AQContent):
            jpg = content.back if content.flipped else content.front
            return 'include/' + jpg

        card_id = f'C{cardno}'
        content.card = card_id

        card = html.DIV(
            id=card_id,
            Class="card",
            style={"position": "absolute", "left": px(left), "top": px(top),"width":px(self.card_width),"height":px(self.card_height)
                   })
        #card.bind("mouseover", mouseover)
        #card.bind("dblclick", flipper)
        #card.bind("mousedown", mousedown)

        card.draggable = False
        card.bind("dragstart", mydragstart)

        header=content.makeHeader(cardno) # this was part of DragDrop, now free-standing

        body_height = card.offsetHeight# - 20  # a guess
        body_width = card.offsetWidth + 0.0


        content.flipped= True
        back_image = header + content.makeBackImage(cardno)

        content.back_image = back_image
        content.flipped = False

        front_image = header + content.makeFrontImage(cardno)

        content.front_image = front_image

        card <= front_image

        return card

    def shuffledone(self, freeSlots):
        global shuffleDoneAction
        """
        print('shuffledone',freeSlots)
        if freeSlots==0:
            updateTogo()

        """
        if freeSlots==0 and shuffleDoneAction:
            shuffleDoneAction()
def on_restart(ev):
    global content
    content = iter(top_ten_data)
    on_arrange(0)

#init()
#on_arrange(None)
#i = 0
"""
old = [('a', 10), ('b', 20), ('c', 30), ('d', 40)]
new = [('b', 21), ('a', 31), ('e', 51), ('f', 51)]
target = [('b', 21, 0, 1), ('a', 31, 1, 0), ('e', 51, 2, 2), ('f', 51, 3, 3)]
"""


def update(old, new):
    def keys(l):
        return set(map(lambda a: a[0], l))
    
    olds = keys(old)
    news = keys(new)
    replacements = list(zip(news - olds, olds-news))
    print(replacements)
    
    oldd = dict(((a[0], i) for i,a in enumerate(old)))
    for oldslot, newslot in replacements:
        oldd[oldslot] = oldd[newslot]
    return [ (a[0], a[1], i , oldd[a[0]]) for i, a in enumerate(new)]

"""
import pprint
get_next_decade()
get_next_decade()
pprint.pprint(content_deck)
i = 0
"""
