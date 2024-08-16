import pygame
import pygame.gfxdraw
import sys
import time
import random
import pygame_menu
import json 
  
# the Label class is this module below
from label import *

pygame.init()
pygame.mixer.init()
hit = pygame.mixer.Sound("assets/sounds/hit.wav")

screen_width = 1240
screen_heigh = 720
screen = pygame.display.set_mode((screen_width, screen_heigh))
bg = pygame.image.load("./assets/images/background-label.jpg")

qnum = 1
points = 0
num_alternatives = 4
qnt_questions = 10
finished_game=False

questions = [
    ["Default", "DF"]
]

num_question = Label(screen, "#"+str(qnum), 310, 28, 45)
score = Label(screen, "0", 220, 28, 45)
title = Label(screen, questions[qnum-1][0], 350, 25, 55, color="#FFFFFF", center=True)
player_name = Label(screen, "Player 1", 225, 655, 35, color="#FFFFFF")

# reading the data from the file 
with open('./utils/dict-full.json') as f: 
    data = f.read() 
  
regions = json.loads(data) 

clock = pygame.time.Clock()

buttons = pygame.sprite.Group()
class Button(pygame.sprite.Sprite):
    def __init__(self, position, text, size,
        colors="yellow on red",
        bg_color=(0,0,0),
        fg_color=(255,255,255),
        hover_bg_color=(255,255,255),
        hover_fg_color=(0,0,0),
        absoluteColor=False,
        absoluteHoverColor=False,
        hover_colors="purple on white",
        borderc=(255,255,255),
        isImage=False,
        value='rs',
        command=lambda: print("No command")):

        super().__init__()
        global num

        self.text = text
        self.value = value
        self.command = command
        self.isImage = isImage
        self.absoluteColor = absoluteColor
        self.absoluteHoverColor = absoluteHoverColor

        # --- colors ---
        self.colors = colors
        self.original_colors = (fg_color, bg_color) if absoluteColor else colors

        if self.absoluteColor:
            self.fg, self.bg = (fg_color, bg_color)
        else:
            self.fg, self.bg = self.colors.split(" on ")

        # hover_colors
        if self.absoluteHoverColor:
            self.hover_colors = (hover_fg_color, hover_bg_color)
        else:
            if hover_colors == "red on green":
                self.hover_colors = f"{self.bg} on {self.fg}"
            else:
                self.hover_colors = hover_colors

        self.borderc = borderc

        # font
        self.font = pygame.font.SysFont("Arial", size)

        self.x, self.y, self.w , self.h = (position[0], position[1], 220, 150)

        if self.text:
            self.render(self.text)
            self.x, self.y, self.w , self.h = self.text_render.get_rect()
            print((self.w , self.h))
            self.x, self.y = position
            
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        if(self.isImage):
            self.image = pygame.image.load("./assets/images/regions/"+value+".png")
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
            self.image_rect = self.image.get_rect()

        self.position = position
        self.pressed = 0
        # adiciona os sprites a um grupo
        buttons.add(self)

    def render(self, text):
        self.text_render = self.font.render(text, 1, self.fg)
        self.image = self.text_render

    def update(self):
        # if self.absoluteColor == False:
        #     self.fg, self.bg = self.colors.split(" on ")
        self.draw_button()

        if self.command != None:
            self.hover()
            self.click()

    def draw_button(self):
        if self.isImage == False:
            self.render(self.text)

        pygame.draw.rect(screen, self.bg, (self.x, self.y, self.w , self.h))
        pygame.gfxdraw.rectangle(screen, (self.x, self.y, self.w , self.h), self.borderc)

    def check_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if(self.absoluteHoverColor):
                self.fg, self.bg = self.hover_colors
            else:
                self.fg, self.bg = self.hover_colors.split(" on ")
        else:
            if(self.absoluteColor):
                self.fg, self.bg = self.original_colors
            else:
                self.fg, self.bg = self.original_colors.split(" on ")

    def hover(self):
        self.check_collision()

    def click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 0:
                self.command(self.value)
                self.pressed = 1

            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 0


# Ações de botões
def on_click(value):
    if(value == questions[qnum-1][1]):
        check_score(True)
    else:
        check_score(False)

def on_exit(val):
    global finished_game
    finished_game = True
# =======


def check_score(scoring=False):
    global qnum, points, start_finish_timer
    
    hit.play() # som
    if qnum < len(questions):
        print(qnum, len(questions))
        if scoring:
            time.sleep(.05) # previdnr o clique duplo
            points += 1
        qnum += 1
        show_question()

    # se for a última questão
    elif qnum == len(questions):
        start_finish_timer = pygame.time.get_ticks()
        if scoring:
            time.sleep(.05)
            points +=1
        kill()
        global exitBtn
        exitBtn = Button(
                    (491, 303),
                    "Voltar",
                    100,
                    bg_color=(52, 69, 125),
                    fg_color=(255, 255, 255),
                    hover_bg_color=(255, 255, 255),
                    hover_fg_color=(52, 69, 125),
                    absoluteHoverColor=True,
                    absoluteColor=True,
                    borderc=(52, 69, 125),
                    command=on_exit
                )
    
    score.change_text(str(points))
    title.change_text(questions[qnum-1][0])
    num_question.change_text("#"+str(qnum))

    time.sleep(.25)

def drawEasyLevel():
    pos = [(390, 200), (630, 200), (390, 370), (630, 370)]
    current_quest = questions[qnum-1]
    title.change_text(current_quest[0]) 

    alternatives = random.sample([x for x in regions if x.get('UF').upper() != current_quest[1]], num_alternatives-1)
    right_ans = [x for x in regions if x.get('UF').upper() == current_quest[1]]
    alternatives.append(right_ans[0])

    random.shuffle(pos)

    i=0
    for alternative in alternatives:
        Button(
            pos[i],
            "",
            100,
            bg_color=(52, 69, 125),
            fg_color=(255, 255, 255),
            hover_bg_color=(255, 255, 255),
            hover_fg_color=(52, 69, 125),
            absoluteHoverColor=True,
            absoluteColor=True,
            borderc=(52, 69, 125),
            isImage=True,
            value=alternative.get('UF').upper(),
            command=on_click
        )
        i+=1
    pass

def drawMediumLevel():
    pos = [(390, 229), (390, 297), (390, 365), (390, 433)]
    current_quest = questions[qnum-1]
    title.change_text(current_quest[0]) 

    alternatives = random.sample([x for x in regions if x.get('UF').upper() != current_quest[1]], num_alternatives-1)
    right_ans = [x for x in regions if x.get('UF').upper() == current_quest[1]]
    alternatives.append(right_ans[0])

    random.shuffle(pos)

    i=0
    for alternative in alternatives:
        Button(
            pos[i],
            alternative.get('capital'),
            50,
            bg_color=(52, 69, 125),
            fg_color=(255, 255, 255),
            hover_bg_color=(255, 255, 255),
            hover_fg_color=(52, 69, 125),
            absoluteHoverColor=True,
            absoluteColor=True,
            borderc=(0,0,0),
            isImage=False,
            value=alternative.get('UF').upper(),
            command=on_click
        )
        i+=1
    pass

def drawHardLevel():
    pos = [(390, 229), (390, 297), (390, 365), (390, 433)]
    current_quest = questions[qnum-1]
    title.change_text(current_quest[0]) 

    alternatives = random.sample([x for x in regions if x.get('UF').upper() != current_quest[1]], num_alternatives-1)
    right_ans = [x for x in regions if x.get('UF').upper() == current_quest[1]]
    alternatives.append(right_ans[0])

    random.shuffle(pos)

    i=0
    for alternative in alternatives:
        Button(
            pos[i],
            alternative.get('capital'),
            50,
            bg_color=(52, 69, 125),
            fg_color=(255, 255, 255),
            hover_bg_color=(255, 255, 255),
            hover_fg_color=(52, 69, 125),
            absoluteHoverColor=True,
            absoluteColor=True,
            borderc=(0,0,0),
            isImage=False,
            value=alternative.get('UF').upper(),
            command=on_click
        )
        i+=1
    pass

def show_question():
    # Kills the previous buttons/sprites
    kill()
    (f, difficulty) = menu.get_input_data().get('difficulty')

    if difficulty == 0:
        drawEasyLevel()
    elif difficulty == 1:
        drawMediumLevel()
    else:
        drawHardLevel()

def kill():
    for _ in buttons:
        _.kill()

def loop():
    show_question()

    while True:
        screen.fill(0)
        screen.blit(bg, (0, 0))
        events = pygame.event.get()
        for event in events: # ====== quit / exit
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

        global finished_game
        if finished_game:
            menu.enable()
            exitBtn.kill()
            menu.update(events)
            menu.draw(screen)
        else:
            buttons.update()     # update buttons
            buttons.draw(screen)
            show_labels()        # update labels
            clock.tick(60)
        pygame.display.update()

def reset():
    menu.disable()
    global finished_game, qnum, points, num_alternatives, qnt_questions
    
    finished_game = False
    qnum = 1
    points = 0
    num_alternatives = 4
    qnt_questions = 10

    num_question.change_text("#"+str(qnum))
    score.change_text(str(points))
    player_name.change_text(menu.get_input_data().get('player_name'))


def start_the_game():
    (f, difficulty) = menu.get_input_data().get('difficulty')

    reset()
    
    questions.clear()

    list = [x for x in regions if x.get('difficult') == difficulty]
    aux = random.sample(list, qnt_questions if len(list) >= qnt_questions else len(list))

    if(len(aux) < qnt_questions):
        diff = qnt_questions - len(aux)
        aux = aux + random.sample([x for x in regions if x.get('difficult') <= difficulty and x.get('UF') not in [z.get('UF') for z in aux]], diff)
    for item in aux:
        questions.append([item.get('name'), item.get('UF').upper()])
        
    random.shuffle(questions)

    if(difficulty == 0):
        print('easy')
    elif(difficulty == 1):
        print('medium')
    else:
        print('hard')

    loop()
    pass

if __name__ == '__main__':
    pygame.init()

    my_theme = pygame_menu.Theme(
        background_color=pygame_menu.BaseImage(image_path="./assets/images/background.jpg"),
        title_background_color=(52, 69, 125),
        title_font_color=(255, 255, 255),
        widget_font_color=(255, 255, 255),
        widget_background_color=(50, 50, 50),
        widget_margin=(0, 15),
        widget_padding=10,
    )

    menu = pygame_menu.Menu('Bem vindo', 1240, 720, theme=my_theme)

    menu.add.text_input('Nome :', default='Jogador 1', textinput_id='player_name', font_color=(255, 255, 255), background_color=(52, 69, 125))
    menu.add.selector('Dificuldade :', [('Fácil', 0), ('Intermediário', 1), ('Difícil', 2)], selector_id='difficulty', font_color=(255, 255, 255), background_color=(52, 69, 125))
    menu.add.button('Jogar', start_the_game, font_color=(255, 255, 255), background_color=(52, 69, 125))
    menu.add.button('Sair', pygame_menu.events.EXIT, font_color=(255, 255, 255), background_color=(52, 69, 125))
    menu.mainloop(screen)
    

    