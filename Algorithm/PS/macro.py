# macro.py
import pyautogui as pag
import time

n = 5
while True:
    n = -n
    pag.moveRel(n, 0)
    time.sleep(1)
    
    
    