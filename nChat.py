###############################################################
# nChat - Simple chat app with multiple lines and a detached
# input box.  Background of the chat window and around the
# input become transparent as well as the chat text eventually
#
# I basically just ripped off the way XyChat works because it
# was crashing my game when I used my countdown app lol and I
# also wanted a detached input box and some other things.
###############################################################

import ac
import acsys
import math
import random

appWindow = 0
inputWindow = 0
textInput = 0
messages = []
lines = []
updateTrans = 1001
currentTrans = 0
textTrans = 3001
currentText = 0
maxLines = 6
title = None
driver = ac.getDriverName(0).strip()

def acMain(ac_version):
    global textInput, appWindow, inputWindow, messages, lines, maxLines
    appWindow = ac.newApp('nChat')
    inputWindow = ac.newApp('nInput')

    ac.setSize(appWindow, 500, 100)
    ac.drawBorder(appWindow, 0)
    ac.setTitle(appWindow, '')
    ac.setIconPosition(appWindow, -9000, 0)
    ac.setBackgroundOpacity(appWindow, 0)

    ac.setSize(inputWindow, 435, 62)
    ac.drawBorder(inputWindow, 0)
    ac.setTitle(inputWindow, '')
    ac.setIconPosition(inputWindow, -9000, 0)
    ac.setBackgroundOpacity(inputWindow, 0)

    textInput = ac.addTextInput(inputWindow, 'TEXT_INPUT')
    ac.setPosition(textInput, 1, 32)
    ac.setSize(textInput, 435, 30)

    ac.addOnChatMessageListener(appWindow, onChatMessage)
    ac.addOnClickedListener(appWindow, onWindowClick)

    ac.addOnValidateListener(textInput, onValidateListener)
    ac.addOnClickedListener(inputWindow, onWindowClick)

    for i in range(0, maxLines):
        lines.append([ac.addLabel(appWindow, ''), ac.addLabel(appWindow, '')])
        for x in range(0, 2):
            ac.setSize(lines[i][x], 14*60, 14)
            ac.setPosition(lines[i][x], 0, i*14+5)
            ac.setFontSize(lines[i][x], 14)

    # Maybe add back in later
    #lines.reverse()

    onChatMessage('Loaded...', 'nChat')
    return "nChat"

def onChatMessage(message, author) :
    global messages, lines, maxLines, currentText

    currentText = 1
    messages.append([author, message])
    if len(messages) > maxLines:
        messages = messages[len(messages)-maxLines:]

    for i in range(0, maxLines):
        if i < len(messages):
            msg = messages[len(messages)-1-i]
            scale = abs(float(-2))
            n_width = 14*len(msg[0])/scale
            m_width = 14*len(msg[1])/scale

            ac.setText(lines[maxLines-1-i][1], msg[1])
            ac.setSize(lines[maxLines-1-i][0], n_width, 14*1.4)
            ac.setSize(lines[maxLines-1-i][1], m_width, 14*1.4)
            if msg[0].strip().find(driver) > -1:
                ac.setFontColor(lines[maxLines-1-i][0], 0, 1, 0, 1)
            else:
                ac.setFontColor(lines[maxLines-1-i][0], random.random(), random.random(), random.random(), 1)
            ac.setFontColor(lines[maxLines-1-i][1], 1, 1, 1, 1)
            ac.setVisible(lines[maxLines-1-i][0], 1)
            ac.setVisible(lines[maxLines-1-i][1], 1)
            ac.setPosition(lines[maxLines-1-i][0], 0, ac.getPosition(lines[maxLines-1-i][0])[1])
            ac.setFontAlignment(lines[maxLines-1-i][0], "left")
            ac.setPosition(lines[maxLines-1-i][1], n_width+5, ac.getPosition(lines[maxLines-1-i][1])[1])
            ac.setFontAlignment(lines[maxLines-1-i][1], "left")
            ac.setText(lines[maxLines-1-i][0], msg[0]+":")

def onValidateListener(string):
    global textInput
    text = ac.getText(textInput)
    ac.setText(textInput, '')
    ac.setFocus(textInput, 1)
    ac.sendChatMessage(text)

def onWindowClick(x, y):
    global currentTrans, currentText, lines, maxLines
    currentTrans = 1
    currentText = 1
    for i in range(0, maxLines):
        for x in range(0, 2):
            ac.setVisible(lines[i][x], 1)

def acUpdate(deltaT):
    global appWindow, inputWindow, currentTrans, updateTrans, currentText, textTrans, lines, maxLines

    if currentTrans != 0:
        if currentTrans < updateTrans:
            currentTrans += 1
        else:
            ac.setBackgroundOpacity(appWindow, 0)
            ac.setBackgroundOpacity(inputWindow, 0)
            currentTrans = 0

    if currentText != 0:
        if currentText < textTrans:
            currentText += 1
        else:
            for i in range(0, maxLines):
                for x in range(0, 2):
                    ac.setVisible(lines[i][x], 0)
    