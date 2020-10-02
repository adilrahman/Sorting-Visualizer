import pygame
import random

#initial things
pygame.init()
pygame.mixer.pre_init(frequency = 44100, size = 16,channels = 1, buffer = 256)
screen = pygame.display.set_mode((1000,1000))
ite = pygame.mixer.Sound('./Sounds/Banner.wav') #iteration Sound
completed =  pygame.mixer.Sound('./Sounds/complete.wav')
complete_ = False
pygame.display.set_caption("Sorting Visualizer")


#fonts
font = pygame.font.Font(None,100)
NameFont = pygame.font.Font(None,45)
optionsFont = pygame.font.Font(None,32)
numbersFont = pygame.font.Font(None,14)
inputFont = pygame.font.Font(None,32)

# bars settings
x , y = 5,500
width = 17
spacing_btw_height = 23
height = [random.randint(-240,430) for x in range(43)] 
run = True
execute = False

#Input Field
inputRect = pygame.Rect(425,940,150,32)
userText = ""
inputRectColor = (0,0,0)
inputActivate = False



# height updating function
def show(height,c1=0,c2=len(height)-1,algo=(1,1)):
    for i in range(len(height)):
        no = numbersFont.render(str(height[i]),False,(0,0,0))
        screen.blit(no,(x+23*i,900))
        if not(i == c1 or c2 == i):
            pygame.draw.rect(screen,(0,0,0),(x+spacing_btw_height*i,y,width,-1*height[i]))
        elif c2 == i:
            pygame.draw.rect(screen,(0,255,0),(x+spacing_btw_height*i,y,width,-1*height[i]))
        else:
            pygame.draw.rect(screen,(0,0,255),(x+spacing_btw_height*i,y,width,-1*height[i]))
        if algo[0] == "selection" and i <= algo[1]:
            pygame.draw.rect(screen,(255,255,0),(x+spacing_btw_height*i,y,width,-1*height[i]))


# positive negative separation (Rect is used intead of line)
def line():
    a = pygame.Rect(0,500,1000,4)
    pygame.draw.rect(screen,(255,0,0),a)


# Working Algo name (Not Completed)
def show_name():
    name = NameFont.render(f"Sorting Visualizer",False,(0,100,255))
    screen.blit(name,(370,10))


# Alogrithem List (Not Completed)
def show_options():
    option1 = optionsFont.render(f"1 : Bubble Sort",False,(0,0,0)) 
    option2 = optionsFont.render(f"1 : Bubble Sort",False,(0,0,0)) 
    screen.blit(option1,(700,20))
    screen.blit(option2,(700,40))


# updating screen (for reduce redentency)
def re_Draw(c1=0,c2=1,algo=(1,1)):
        screen.fill((255,255,255))
        show(height,c1,c2,algo)
       # show_options()
        display_side()
        show_name()
        line()
        pygame.display.update()
        ite.play()
        pygame.time.delay(20)


#Displaying positive and negative Sides
def display_side():
    positive = font.render("+",False,(10,255,0))
    negative = font.render("-",False,(255,0,0)) 
    screen.blit(negative,(20,0))
    screen.blit(positive,(950,0))



#Sorting Algorithems

def BubbleSort():
    global height
    count = 0
    for i in range(len(height)-2):
        for j in range(len(height)-1-i):
            count += 1
            if height[j] > height[j+1]:
                height[j+1],height[j] = height[j],height[j+1]
                re_Draw(j,j+1)


def SelectionSort():
    global height
    for i in range(len(height)-1):
        minValue = i
        for j in range(i,len(height)):
            if height[minValue] > height[j]:
                minValue = j 
            re_Draw(minValue,j)
        height[minValue],height[i] = height[i],height[minValue]
        re_Draw(minValue,j,algo=("selection",i))


def InsertionSort():                                                          
    global height
    for i in range(1,len(height)):  
        j = i-1
        while j >= 0 and height[j] > height[j+1]:
                height[j],height[j+1] = height[j+1],height[j]
                j -= 1
                re_Draw(i,j+1)
            

def quickSort(arr,left,right):
    if right - left <= 0: #Terminating Condition 
        return 
    
    i , j = left,right
    pivot = arr[int((left+right)/2)]
    
    while i <= j:
        while arr[i] < pivot:
            i += 1
            re_Draw(i,j)
    
        while arr[j] > pivot:
            j -= 1
            re_Draw(i,j)

        if i <= j :
            arr[i] , arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
            re_Draw(i,j)

        
    quickSort(arr,left,i - 1)
    quickSort(arr,i,right)


a = 2
options = ["bubble","selection","insertion","quick"]

while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if inputActivate:
                if event.key == pygame.K_RETURN:
                    inputActivate = False
                    inputRectColor = (0,0,0)
                elif event.key == pygame.K_BACKSPACE :
                    userText = userText[:-1]
                else:
                    userText += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if inputRect.collidepoint(event.pos):
                inputActivate = True
                inputRectColor = (0,150,255)
        if event.type == pygame.KEYDOWN:
            if not inputActivate:
                if event.key == pygame.K_SPACE:
                    execute = True
                if event.key == pygame.K_r:
                    execute = False
                    height = [random.randint(-240,430) for x in range(43)] 
            
    

    screen.fill((255,255,255))
    pygame.draw.rect(screen,inputRectColor,inputRect,2)
    input_field = inputFont.render(userText,False,(0,0,0))
    screen.blit(input_field,(inputRect.x + 5,inputRect.y + 5))
    inputRect.w = max(100,input_field.get_width() + 10)
    show(height)
    display_side()
    show_name()
    line()

    if not inputActivate:
        if userText.lower() in options:
            a = options.index(userText.lower()) 
        else:
            execute = False

    if execute:
        if a == 0:
            BubbleSort()
        elif a == 1:
            SelectionSort()
        elif a == 2:
            InsertionSort()
        elif a == 3:
            quickSort(height,0,len(height)-1)
        execute = False

    pygame.display.update()



