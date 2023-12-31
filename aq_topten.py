import time,copy,sys
from functools import partial

from dataclasses import dataclass
from browser import document, html, timer, window, alert, bind
from browser.html import *

from aq_data import top_ten_data

content_index = -1
previous_deck = None
current_stream = None


def more_forwards():
    return content_index < len(top_ten_data) - 1

def more_backwards():
    return content_index > 0

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



stopFlag = False
bar_width = 0

def get_max_value():
    global top_ten_data
    for i in range(len(top_ten_data)):
        deck = top_ten_data[i]
        value= deck[1][0]
    return max(top_ten_data[i][1][0][1] for i in range(len(top_ten_data)))



def px(x):
    return str(x) + "px"


def init():
    global bar_width, max_value
    max_value = get_max_value()


    paragraph1 = """Use the forward / back buttons to scroll through the Top Ten polluted cities over time"""

    p2 = """
    Data is the concentration of particulate matter (e.g. soot particles) extracted from the UK Earth System  Model and averaged per decade. 
    """               
    paragraph2 = SPAN(p2) + P("Click " + A("here", href="../aqcity/index.html") + " to compare Cities")


    back_one = BUTTON("<", id="back_one", disabled=True, Class="selector")

    back_stream = BUTTON("<<", id="back_stream", disabled=True, Class="selector")

    forward_one = BUTTON( ">", disabled=False, id="forward_one", Class="selector")
    forward_stream = BUTTON(">>", id="forward_stream", disabled=False, Class="selector")

    def sanity_check():
        # Either a button is active ore we'er waiting for a termination
        global stopFlag, current_stream
        if all_clear() and not current_stream:
            for e in [back_one, back_stream, forward_one, forward_stream]:
                if e.disabled == False:
                    return True
            #alert("consistency error")
            return False
        else:
            return True

    def disable_all():
        for e in [back_one, back_stream, forward_one, forward_stream]:
            e.disabled = True

    @bind(forward_one, "click")
    def on_forward_one_click(ev):
        disable_all()
        single_step(True)
        sanity_check()

    @bind(back_one, "click")
    def on_back_click(ev):
        disable_all()
        single_step(False)
        sanity_check()

    @bind(forward_stream, "click")
    def on_forward_stream_click(ev):
        disable_all()
        multi_step(ev, True)
        sanity_check()

    @bind(back_stream, "click")
    def on_back_stream_click(ev):
        disable_all()
        multi_step(ev, False)
        sanity_check()


    date_display = DIV(
        SPAN("Date",Class='control-text')+
        SPAN("8888",id='togo',Class='foreground') , 
        Class="Clock-Wrapper"
    )

    head =  DIV(
        DIV(H1("Top Ten Pollution Cities")) + 
                P(paragraph1) +
                P(paragraph2) +
                date_display, 

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
                        DIV() +DIV(), 
                        width="10%",
                        height=px(play_height),
                        style={"vertical-align": "baseline"}
                        ) +
                    TD(DIV( id="id_main", Class="play"), id="td_main", width="80%" , style={"vertical-align": "top", "background-color": "white",}) +
                    TD(
                        date_display+
                        DIV(back_stream+ back_one + forward_one + forward_stream), 
                        width="10%", 
                        height=px(play_height),
                        style={"vertical-align": "baseline"}
                    )
                    ),
                id="body",

                Class="body"
                ),
        Class="border_bottom"
    )
    td_main = document['td_main']
    print(td_main.width, bar_width)

    init_rank_holder(document["id_main"], play_height, td_main.width)
    #arrangeCards()
    document['togo'].text = content_date

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
    slot_margin = 10
    slot_height = play_height / cardCount - slot_margin
    card_top = 0
    card_left = 0
    card_width = width * 0.9
    card_height = slot_height

    background = DIV(   
        DIV( Class="background-item") + 
        DIV( Class="background-item") + 
        DIV( Class="background-item") + 
        DIV( Class="background-item") + 
        DIV( Class="background-item"), 
        Class="background-container",
        style={"position": "absolute","height": px(play_height), "width": px(width)}
    )
    #main <= background
    for i in range(cardCount):
        row = i

        left = 0
        top = (slot_height + slot_margin) * i

        rank_id = f'R{i + 1}'
        seq_id = f'W{i + 1}'
        detail = TABLE(
            TR(
                TD(SPAN(), width="50%") + 
                TD(SPAN(Class="rank_detail"), width="12.5%") + 
                TD(SPAN(Class="rank_detail"), width="12.5%") + 
                TD(SPAN(Class="rank_detail"), width="12.5%") + 
                TD(SPAN(Class="rank_detail"), width="12.5%") 
                ), width="100%"
        )

        sz = DIV(detail, Class="rank_hook")
        rank = DIV(
            TABLE(
              TR(
                    TD(
                        DIV(f'{i+1:2d}', Class="index") , 
                        width="1%"
                        ) +
                    TD(sz)
                    ),
                width="100%"
                ), 
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
        global max_value
        header_id = f'H{cardno}'
        bar_id = f'B{cardno}'
        barwid = self.Value / max_value * 100 # bar is 50% of window



        header = DIV(
            DIV(self.City, id=f'Q{cardno}', Class="card-header-text") + 
                    DIV('{:4.1f}'.format(self.Value), id=f'V{cardno}', Class="card-header-text") + 
                    DIV(
                        DIV(id=bar_id, Class="bar"),  Class="card-header-text", 
                        style={ "width": f"{barwid}%", "height": "50%",}
                        ), id=header_id, Class="header-container"
        )
        return header            


    def createCard(self, cardno, top, left, width, height):

        card_id = f'C{cardno}'
        self.card = card_id

        header=self.makeHeader(cardno) # this was part of DragDrop, now free-standing
        card = DIV(header, 
                   id=card_id,
            Class="card",
            style={"position": "absolute", "height":px(height), "top": px(0),})
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
    print("disable", disable_set)

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

    document['togo'].text = content_date
    print(content_date)

    mp=[(rankSlots[c.Prev_rank].select_one(".card").id, c.Current_rank,c.Prev_rank) for c in content_deck]

    for card_id, c, p in mp:
        newt = content_deck[c].makeHeader(c)
        oldh = document[card_id].select_one(".header-container")
        #print(card_id, c, p, oldh.text, newt.text)
        oldh.replaceWith(newt)


    move_card([(card_id, c, p) for (card_id, c, p) in mp if c != p])
    whenever(all_clear, True, done_arrange)

def multi_step(ev, forward=True):
    global stopFlag, current_stream
    t = ev.target
    if current_stream != None:
        #t.text = t.saveText
        stopFlag = True
        return        
    current_stream = t
    stopText = "||"

    t.saveText = t.text
    t.text = stopText
    t.disabled = False

    def can_move():
        if forward: return more_forwards()
        else:
            return more_backwards()




    def local():
        global stopFlag, current_stream
        def busy_check():
            whenever(all_clear, True, local)
        if stopFlag:
            stopFlag = False
            current_stream = None
            ev.target.text = ev.target.saveText
            done_arrange()
        else:
            if can_move():
                timer.set_timeout(busy_check, 1000)
                single_step(forward)
            else:
                current_stream = None
                ev.target.text = ev.target.saveText
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
            #alert(src.style.top)
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

