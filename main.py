#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

try:
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import selenium.common.exceptions as seleniumexcept
except ImportError:
    print("Missing selenium module. Please install it with 'pip install selenium'.")
    sys.exit(1)

try:
    import pynput
except ImportError:
    print("Missing pynput module. Please install it with 'pip install pynput'.")
    sys.exit(1)


def printHelp(isLaunchArgument=False):
    if isLaunchArgument:
        print("> Usage example: python %s typing" % sys.argv[0])
        print("> Set an optional limit: %s verbal_memory -limit 100" % sys.argv[0])
        print("> Start stable mode: %s visual_memory -limit 40 stable" % sys.argv[0])
        print("> Print help: python %s -help" % sys.argv[0])
        print("> Available tests:\n\t- number_memory\n\t- reaction_time\n\t- verbal_memory\n\t- visual_memory\n\t- typing\n\t- aim_trainer\n\t- chimp")
    else:
        print("> Available commands:")
        print("\t- 'quit' : Terminates the program")
        print("\t- 'close' : Terminates the program and closes the browser")
        print("\t- 'help' : Prints this help")
        print("\t- '-limit x': Sets the limit to x")
        print("\t- 'fast' / 'stable' : Switch between fast and stable execution of the next tests")
        print("\t- 'testname' : Starts the test \"testname\"")
        print("> Available tests:\n\t- number_memory\n\t- reaction_time (stable only on Linux)\n\t- verbal_memory\n\t- visual_memory\n\t- typing\n\t- aim_trainer\n\t- chimp")

def handleNumberMemory(limit):
    wait = 3
    startButton = driver.find_element(By.XPATH,"//button[text()='Start']")
    try:
        startButton.click()
    except:
        pass

    for i in range(limit):
        print("> Executing test: %d / %d" % (i + 1, limit), end='\r')
        sys.stdout.flush()
        number = driver.find_element(By.CLASS_NAME, "big-number").text

        inputFieldPresent = EC.presence_of_element_located(
            (By.XPATH, "//input[@type='text' and @pattern='[0-9]*']"))
        try:
            inputField = WebDriverWait(driver, wait).until(inputFieldPresent)
        except TimeoutException:
            print("> Timed out while waiting for input field.")
            sys.exit(-1)
        inputField.send_keys(number)
        inputField.send_keys(Keys.RETURN)
        nextButton = driver.find_element(By.XPATH,"//button[text()='NEXT']")
        nextButton.click()
        wait += 1
    print("")

def handleReactionTimeFast():
    print("> Fast mode not supported on Linux. Using stable mode instead.")
    handleReactionTimeStable()

def handleReactionTimeStable():
    startScreenPresent = EC.presence_of_element_located(
        (By.XPATH, "//div[@class='css-42wpoy e19owgy79']"))
    try:
        WebDriverWait(driver, 3).until(startScreenPresent).click()
    except TimeoutException:
        print("> Timed out waiting for start screen.")
        sys.exit(-1)

    limit = 5
    for i in range(limit):
        greenPanelPresent = EC.presence_of_element_located(
            (By.XPATH, "//div[text()='Wait for green']"))
        try:
            WebDriverWait(driver, 15).until(greenPanelPresent).click()
        except TimeoutException:
            print("> Green panel took too long to appear.")
            return
        time.sleep(0.1)
        try:
            timeDisplay = driver.find_element(By.XPATH, "//div[@class='css-1qvtbrk e19owgy78']/h1/div")
            print("> Took", timeDisplay.text)
        except seleniumexcept.NoSuchElementException:
            print("> Couldn't find time display.")
        try:
            if (i != limit - 1):
                driver.find_element(By.XPATH, "//h2[text()='Click to keep going']").click()
        except seleniumexcept.NoSuchElementException:
            print("> Couldn't continue with the test")

def handleVerbalMemory(limit):
    startButtonPresent = EC.element_to_be_clickable((By.XPATH, "//button[text()='Start']"))
    try:
        startButton = WebDriverWait(driver, 6).until(startButtonPresent)
    except TimeoutException:
        print("> Timed out waiting for site to load.")
        sys.exit(-1)
    startButton.click()

    alreadySeen = []
    for i in range(limit):
        print("> Executing test: %d / %d" % (i + 1, limit), end='\r')
        sys.stdout.flush()
        currentWord = driver.find_element(By.CLASS_NAME, "word").text
        if currentWord in alreadySeen:
            driver.find_element(By.XPATH, "//button[text()='SEEN']").click()
        else:
            alreadySeen.append(currentWord)
            driver.find_element(By.XPATH, "//button[text()='NEW']").click()
    print("")

def handleVisualMemory(limit, fast):
    startButtonPresent = EC.element_to_be_clickable((By.XPATH, "//button[text()='Start']"))
    try:
        startButton = WebDriverWait(driver, 6).until(startButtonPresent)
    except TimeoutException:
        print("> Timed out waiting for site to load.")
        sys.exit(-1)
    startButton.click()

    myMouse = pynput.mouse.Controller()
    verticalOffset = 80

    for i in range(limit):
        print("> Executing test: %d / %d" % (i + 1, limit), end='\r')
        sys.stdout.flush()
        whiteSquaresPresent = EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".square.active"))
        try:
            whiteSquares = WebDriverWait(driver, 3).until(whiteSquaresPresent)
        except TimeoutException:
            print("> Timed out waiting for white squares.")
            sys.exit(-1)
        time.sleep(1.5)
        for square in whiteSquares:
            coordinates = (square.rect["x"] + square.rect["width"]/2,
                           square.rect["y"] + square.rect["height"]/2 + verticalOffset)
            myMouse.position = coordinates
            myMouse.click(pynput.mouse.Button.left, 1)
        time.sleep(1)
    print("")

def handleTyping(fast):
    time.sleep(0.5)
    textbox = driver.find_element(By.CLASS_NAME, "letters")
    myKeyboard = pynput.keyboard.Controller()
    myMouse = pynput.mouse.Controller()
    coordinates = (textbox.rect["x"] + textbox.rect["width"]/2,
                   textbox.rect["y"] + textbox.rect["height"]/2 + 80)

    textElements = driver.find_elements(By.CLASS_NAME, "incomplete")
    text = "".join([el.text if el.text else " " for el in textElements])

    if fast:
        myMouse.position = coordinates
        myMouse.click(pynput.mouse.Button.left, 1)
        myKeyboard.type(text)
    else:
        textbox.send_keys(text)

    try:
        wpm = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//h1[@class='css-0']"))
        ).text
        print("> Finished with:", wpm)
    except:
        print("> Problem getting typing results.")

def handleAimTest():
    targetPresent = EC.element_to_be_clickable(
        (By.XPATH, "//div[@data-aim-target='true']/div[@style='width: 100px; height: 2px;']"))
    try:
        target = WebDriverWait(driver, 6).until(targetPresent)
        target.click()
    except TimeoutException:
        print("> Timed out waiting for site to load.")
        sys.exit(-1)
    for _ in range(30):
        try:
            WebDriverWait(driver, 6).until(targetPresent).click()
        except:
            print("Failed to aim at target")

def handleChimpTest(limit):
    startButton = driver.find_element(By.XPATH, "//button[text()='Start Test']")
    startButton.click()


def handleUserInput(userInput, limit, fast):
    url = "https://www.humanbenchmark.com"

    if userInput is None:
        driver.get(url)
    elif userInput == "help":
        printHelp(False)
    elif userInput.startswith("-limit"):
        parts = userInput.split()
        if len(parts) == 2 and parts[1].isdigit():
            limit = int(parts[1])
            print("> Changed limit to:", limit)
        else:
            print("> Invalid -limit argument")
    elif userInput == "fast":
        fast = True
        print("> Changed to fast (typing/visual only on Linux)")
    elif userInput == "stable":
        fast = False
        print("> Changed to stable")
    elif userInput == "quit":
        print("> Goodbye.")
        sys.exit(0)
    elif userInput == "close":
        print("> Goodbye.")
        try:
            driver.close()
        except seleniumexcept.WebDriverException:
            pass
        sys.exit(0)
    elif userInput == "number_memory":
        driver.get(url + "/tests/number-memory")
        handleNumberMemory(limit)
    elif userInput == "reaction_time":
        driver.get(url + "/tests/reactiontime")
        if fast:
            handleReactionTimeFast()
        else:
            handleReactionTimeStable()
    elif userInput == "verbal_memory":
        driver.get(url + "/tests/verbal-memory")
        handleVerbalMemory(limit)
    elif userInput == "visual_memory":
        driver.get(url + "/tests/memory")
        handleVisualMemory(limit, fast)
    elif userInput == "typing":
        driver.get(url + "/tests/typing")
        handleTyping(fast)
    elif userInput == "aim_trainer":
        driver.get(url + "/tests/aim")
        handleAimTest()
    elif userInput == "chimp":
        driver.get(url + "/tests/chimp")
        handleChimpTest(limit)
    else:
        print("> Unknown test:", userInput)

    return limit, fast

# ---------------------------
# Main
# ---------------------------

if __name__ == "__main__":
    limit = 10
    fast = True

    if len(sys.argv) >= 2 and sys.argv[1] in ["-help", "help"]:
        printHelp(True)
        sys.exit(0)

    if len(sys.argv) >= 4 and sys.argv[2] == "-limit" and sys.argv[3].isdigit():
        limit = int(sys.argv[3])

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])

    try:
        driver = webdriver.Chrome(options=options)
    except seleniumexcept.WebDriverException:
        print("Failed to start Chrome. Make sure chromedriver is installed and in PATH.")
        sys.exit(1)

    if len(sys.argv) > 1:
        testName = sys.argv[1]
        if (len(sys.argv) >= 3 and sys.argv[2] == "stable") or (len(sys.argv) == 5 and sys.argv[4] == "stable"):
            fast = False
        handleUserInput(testName, limit, fast)

    # Loop for continuous input
    while True:
        userInput = input("\n> What next? (Type help for help)\n# ")
        limit, fast = handleUserInput(userInput, limit, fast)
