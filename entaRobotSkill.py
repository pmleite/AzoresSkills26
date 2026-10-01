"""
Azores Skills 2026 - programa principal do robot.

Apresenta um menu no LCD:
  PB1 - passa para a opcao seguinte
  PB2 - executa a opcao selecionada
Para acrescentar opcoes basta adicionar entradas a MENU_OPTIONS.
"""

import sys
import time
import signal
from onepi.one import BnrOneAPlus

import lineCalibration
import motorCalibration
import lineFollowerPID

one = BnrOneAPlus(0, 0)  # object to control Bot'n Roll ONE A+



def wait_button_release():
    while one.read_button() != 0:
        time.sleep(0.050)


def calibrate_line():
    print("Line calibration selected")
    lineCalibration.run(one)


def calibrate_motors():
    print("Motor calibration selected")
    motorCalibration.run(one)
    
def follow_line_pid():
    print("Line follower PID selected")
    lineFollowerPID.run(one)
    


def exit_program():
    print("Exiting")
    one.stop()
    one.lcd1("   A terminar   ")
    one.lcd2("    Adeus!      ")
    time.sleep(1)
    sys.exit(0)


# (text shown on the LCD, max 14 chars; function to execute)
MENU_OPTIONS = [
    ("Cal. linha", calibrate_line),
    ("Cal. motores", calibrate_motors),
    ("Seg. linha PID", follow_line_pid),
    ("Sair", exit_program),
]


def show_menu_option(index):
    text, _ = MENU_OPTIONS[index]
    one.lcd1(f"Menu {index + 1}/{len(MENU_OPTIONS)}".ljust(9) + "PB1>PB2")
    one.lcd2(("> " + text).ljust(16))


def select_menu_option():
    """
    PB1 cycles through the options, PB2 confirms.
    Returns the index of the selected option.
    """
    index = 0
    show_menu_option(index)
    wait_button_release()
    while True:
        button = one.read_button()
        if button == 1:
            index = (index + 1) % len(MENU_OPTIONS)
            show_menu_option(index)
            wait_button_release()
        elif button == 2:
            wait_button_release()
            return index
        time.sleep(0.050)


def setup():
    print("Starting Azores Skills 2026 Robot")
    one.stop()


def loop():
    index = select_menu_option()
    _, action = MENU_OPTIONS[index]
    action()
    one.stop()


def main():
    """
    Calls setup and then loops forever
    """

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
