import cv2, os
import pyautogui as atg
from time import sleep
from datetime import timedelta, time
from random import uniform


#images
CLOSE_IMG       = cv2.imread("imgs/x.png")
ERROR_OK_IMG    = cv2.imread("imgs/ok.png")
WORK_ALL_IMG    = cv2.imread("imgs/all.png")
PLAY_IMG        = cv2.imread("imgs/play.png")
HEROES_IMG      = cv2.imread("imgs/heroes.png")
FULLBAR_IMG     = cv2.imread("imgs/fullbar.png") 
ASSINAR_IMG     = cv2.imread("imgs/assinar.png")
UP_ARROW_IMG    = cv2.imread("imgs/up_arrow.png")
CONECTAR_IMG    = cv2.imread("imgs/conectar.png")
METAMASK_IMG    = cv2.imread("imgs/metamask.png")
DOWN_ARROW_IMG  = cv2.imread("imgs/down_arrow.png")

#game_window
ULTRAWIDE_SIZE = {
    'game' : (790, 170, 960, 600),
    'full' : (0, 0, 2560, 1080)
}
FELIPE_SIZE = {
    'game' : (230, 153, 965, 606),
    'full' : (0, 0, 1440, 900)
}

actual_size = None

#method
METHOD = cv2.TM_CCOEFF_NORMED


#pyautogui  pause
atg.PAUSE = 0.1
ST = 15



def seach_img(background_img, img):
    result = cv2.matchTemplate(background_img, img, METHOD)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    img_loc = {
        'min_val' : min_val,
        'max_val' : max_val,
        'min_loc' : min_loc,
        'max_loc' : max_loc
    }

    return  img_loc

def click_img(img_loc, fullscreen = False, ax=0, ay=0):
    if fullscreen:
        atg.moveTo(img_loc['max_loc'][0] + actual_size['full'][0] + ax, img_loc['max_loc'][1] + actual_size['full'][1] + ay, uniform(0.3, 0.8))
    else:
        atg.moveTo(img_loc['max_loc'][0] + actual_size['game'][0] + ax, img_loc['max_loc'][1] + actual_size['game'][1] + ay, uniform(0.3, 0.8))
    atg.click()

def th_test(img_loc, th=0.8):
    if img_loc['max_val'] >= th:
        return True
    return False

def update_screen(fullscreen = False):
    if fullscreen:
        screen_img = atg.screenshot("imgs/screen.png")
    else:
        screen_img = atg.screenshot("imgs/screen.png", actual_size['game'])

    screen_img = cv2.imread("imgs/screen.png")

    return screen_img 

def seach_click(img, fullscreen= False, sleep_time= 1, ax=0, ay=0, th=0.8):
    screen_img = update_screen(fullscreen=fullscreen)
    img_loc = seach_img(screen_img, img)
    if th_test(img_loc, th=th):
        click_img(img_loc, fullscreen=fullscreen, ax=ax, ay=ay)
        sleep(sleep_time)
        return True
    return False

def close_heroes():
    seach_click(CLOSE_IMG)
    seach_click(DOWN_ARROW_IMG)

def open_heroes():
    seach_click(UP_ARROW_IMG)
    seach_click(HEROES_IMG, sleep_time=5)

def seach_full_heroes(ax=0, ay=0):
    if seach_click(FULLBAR_IMG, ax= ax, ay=ay, th=0.95):
        count = seach_full_heroes(ax=ax, ay=ay)
        return count + 1
    else:
        return 0

def login():
    if seach_click(CONECTAR_IMG, sleep_time=10):
        if seach_click(ASSINAR_IMG, fullscreen=True, sleep_time=20):
                return True
        else:
            if seach_click(METAMASK_IMG,fullscreen=True, sleep_time=10):
                if seach_click(ASSINAR_IMG, fullscreen=True, sleep_time=20):
                    return True
    else:
        atg.press('f5')
        sleep(10)
        login()

def play():
    seach_click(PLAY_IMG)

def main():
    global actual_size
    runtime = timedelta()
    error_count = 0
    
    print("BOMBBOT\n")
    
    print("1 - ULTRAWIDE")
    print("2 - FELIPE")
    size = input("Digite sua resolução: ")
    if size == "1":
        actual_size = ULTRAWIDE_SIZE
    elif size == "2":
        actual_size = FELIPE_SIZE

    work_time = int(input("De quanto em quanto tempo devo verificar? (em minutos): "))
    work_time = timedelta(minutes=work_time)
    timer = work_time
    work_count = 0

    login()
    play()
    while True:
        sleep(ST)
        
        if seach_click(ERROR_OK_IMG, sleep_time=15):
            login()
            play()
            timer = work_time
            error_count += 1

        if timer >= work_time:
            open_heroes()
            work_count += seach_full_heroes(ax=90, ay=15)
            close_heroes()
            timer = timedelta()

        timer += timedelta(seconds=ST)
        runtime += timedelta(seconds=ST)
        verification_time = work_time - timer

        os.system("cls")
        print("BOMBBOT\n")
        print("Execução:____________________{} h".format(str(runtime)))
        print("Proxima Verificação:_________{} min".format((verification_time.total_seconds() % 3600) // 60))
        print("Contator Trabalho:___________" + str(work_count))
        print("Total de Erros:______________" + str(error_count))

main()
    


