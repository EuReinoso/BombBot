import cv2, os
import pyautogui as atg
from time import sleep
from random import uniform


#images
CLOSE_IMG       = cv2.imread("imgs/x.png")
ERROR_OK_IMG    = cv2.imread("imgs/ok.png")
WORK_ALL_IMG    = cv2.imread("imgs/all.png")
PLAY_IMG        = cv2.imread("imgs/play.png")
HEROES_IMG      = cv2.imread("imgs/heroes.png")
ASSINAR_IMG     = cv2.imread("imgs/assinar.png")
UP_ARROW_IMG    = cv2.imread("imgs/up_arrow.png")
CONECTAR_IMG    = cv2.imread("imgs/conectar.png")
METAMASK_IMG    = cv2.imread("imgs/metamask.png")
DOWN_ARROW_IMG  = cv2.imread("imgs/down_arrow.png")

#game_window
ULTRAWIDE_SIZE = {
    'game' : (790, 170, 960, 600),
    'full' : (0, 0, 2560, 1080)}

actual_size = ULTRAWIDE_SIZE

#method
METHOD = cv2.TM_CCOEFF_NORMED

#THRESHOLD
TH = 0.8

#pyautogui  pause
atg.PAUSE = 0.1



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

def click_img(img_loc, fullscreen = False):
    if fullscreen:
        atg.moveTo(img_loc['max_loc'][0] + actual_size['full'][0], img_loc['max_loc'][1] + actual_size['full'][1], uniform(0.3, 0.8))
    else:
        atg.moveTo(img_loc['max_loc'][0] + actual_size['game'][0], img_loc['max_loc'][1] + actual_size['game'][1], uniform(0.3, 0.8))
    atg.click()

def th_test(img_loc):
    if img_loc['max_val'] >= TH:
        return True
    return False

def update_screen(fullscreen = False):
    if fullscreen:
        screen_img = atg.screenshot("imgs/screen.png")
    else:
        screen_img = atg.screenshot("imgs/screen.png", actual_size['game'])

    screen_img = cv2.imread("imgs/screen.png")

    return screen_img 

def seach_click(img, fullscreen= False, sleep_time= 1):
    screen_img = update_screen(fullscreen=fullscreen)
    img_loc = seach_img(screen_img, img)
    if th_test(img_loc):
        click_img(img_loc, fullscreen=fullscreen)
        sleep(sleep_time)
        return True
    return False

def all_work():
        success = False
        if seach_click(UP_ARROW_IMG):
            if seach_click(HEROES_IMG, sleep_time=5):
                if seach_click(WORK_ALL_IMG, sleep_time=3):
                    if seach_click(CLOSE_IMG):
                        if seach_click(DOWN_ARROW_IMG):
                            success = True
        if not success:
            close_heroes()

def close_heroes():
    seach_click(CLOSE_IMG)
    seach_click(DOWN_ARROW_IMG)


def login_play():
    success = False
    if seach_click(CONECTAR_IMG, sleep_time=10):
        if seach_click(ASSINAR_IMG, fullscreen=True, sleep_time=20):
                success = True
        else:
            if seach_click(METAMASK_IMG,fullscreen=True, sleep_time=10):
                if seach_click(ASSINAR_IMG, fullscreen=True, sleep_time=20):
                    success = True
    if success:
        if not seach_click(PLAY_IMG):
            login_play()
    else:
        atg.press('f5')
        sleep(10)
        login_play()

def main():
    print("BOMBBOT\n")
    work_time = int(input("Digite o tempo de trabalho (em minutos): "))
    work_time *= 60

    login_play()
    error_count = 0
    work_count = 0
    runtime_count = 0
    timer = work_time
    while True:
        sleep(10)
        os.system("cls")
        timer += 10
        if seach_click(ERROR_OK_IMG, sleep_time=15):
            login_play()
            timer  = work_time
            error_count += 1

        if timer >= work_time:
            all_work()
            work_count += 1
            timer = 0

        runtime_count += 10

        print("BOMBBOT\n")
        print("Tempo de Execução: {:.2f} min".format(runtime_count / 60))
        print("Timer: {:.2f} min".format(work_time - (timer / 60)))
        print("Total de Erros:", error_count)
        print("Contador de Trabalho:", work_count)

main()
    


