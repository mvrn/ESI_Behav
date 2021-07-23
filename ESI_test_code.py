#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.1.4),
    on Fri Jul 23 15:32:57 2021
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.1.4'
expName = 'esi_test'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/mriveran/Documents/psychopy_exps/esi_test.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1440, 900], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "Test"
TestClock = core.Clock()
test_stim = visual.ImageStim(
    win=win,
    name='test_stim', 
    image='sin', mask=None,
    ori=0.0, pos=(0, 0), size=(0.8, 0.6),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
test_key_resp = keyboard.Keyboard()

# Initialize components for Routine "Test_ISI"
Test_ISIClock = core.Clock()
test_cross = visual.ImageStim(
    win=win,
    name='test_cross', 
    image='/Users/mriveran/Documents/psychopy_exps/ISI_Stim.png', mask=None,
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
test_trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('esi_test_stim.xlsx'),
    seed=None, name='test_trials')
thisExp.addLoop(test_trials)  # add the loop to the experiment
thisTest_trial = test_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTest_trial.rgb)
if thisTest_trial != None:
    for paramName in thisTest_trial:
        exec('{} = thisTest_trial[paramName]'.format(paramName))

for thisTest_trial in test_trials:
    currentLoop = test_trials
    # abbreviate parameter names if possible (e.g. rgb = thisTest_trial.rgb)
    if thisTest_trial != None:
        for paramName in thisTest_trial:
            exec('{} = thisTest_trial[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "Test"-------
    continueRoutine = True
    routineTimer.add(2.000000)
    # update component parameters for each repeat
    test_stim.setImage(Stim)
    test_key_resp.keys = []
    test_key_resp.rt = []
    _test_key_resp_allKeys = []
    # keep track of which components have finished
    TestComponents = [test_stim, test_key_resp]
    for thisComponent in TestComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    TestClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Test"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = TestClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=TestClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *test_stim* updates
        if test_stim.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            test_stim.frameNStart = frameN  # exact frame index
            test_stim.tStart = t  # local t and not account for scr refresh
            test_stim.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_stim, 'tStartRefresh')  # time at next scr refresh
            test_stim.setAutoDraw(True)
        if test_stim.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > test_stim.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                test_stim.tStop = t  # not accounting for scr refresh
                test_stim.frameNStop = frameN  # exact frame index
                win.timeOnFlip(test_stim, 'tStopRefresh')  # time at next scr refresh
                test_stim.setAutoDraw(False)
        
        # *test_key_resp* updates
        waitOnFlip = False
        if test_key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            test_key_resp.frameNStart = frameN  # exact frame index
            test_key_resp.tStart = t  # local t and not account for scr refresh
            test_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_key_resp, 'tStartRefresh')  # time at next scr refresh
            test_key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(test_key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(test_key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if test_key_resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > test_key_resp.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                test_key_resp.tStop = t  # not accounting for scr refresh
                test_key_resp.frameNStop = frameN  # exact frame index
                win.timeOnFlip(test_key_resp, 'tStopRefresh')  # time at next scr refresh
                test_key_resp.status = FINISHED
        if test_key_resp.status == STARTED and not waitOnFlip:
            theseKeys = test_key_resp.getKeys(keyList=['a', 'l'], waitRelease=False)
            _test_key_resp_allKeys.extend(theseKeys)
            if len(_test_key_resp_allKeys):
                test_key_resp.keys = _test_key_resp_allKeys[-1].name  # just the last key pressed
                test_key_resp.rt = _test_key_resp_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in TestComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Test"-------
    for thisComponent in TestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    test_trials.addData('test_stim.started', test_stim.tStartRefresh)
    test_trials.addData('test_stim.stopped', test_stim.tStopRefresh)
    # check responses
    if test_key_resp.keys in ['', [], None]:  # No response was made
        test_key_resp.keys = None
    test_trials.addData('test_key_resp.keys',test_key_resp.keys)
    if test_key_resp.keys != None:  # we had a response
        test_trials.addData('test_key_resp.rt', test_key_resp.rt)
    test_trials.addData('test_key_resp.started', test_key_resp.tStartRefresh)
    test_trials.addData('test_key_resp.stopped', test_key_resp.tStopRefresh)
    
    # ------Prepare to start Routine "Test_ISI"-------
    continueRoutine = True
    routineTimer.add(4.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    Test_ISIComponents = [test_cross]
    for thisComponent in Test_ISIComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Test_ISIClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Test_ISI"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Test_ISIClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Test_ISIClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *test_cross* updates
        if test_cross.status == NOT_STARTED and tThisFlip >= 2.0-frameTolerance:
            # keep track of start time/frame for later
            test_cross.frameNStart = frameN  # exact frame index
            test_cross.tStart = t  # local t and not account for scr refresh
            test_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_cross, 'tStartRefresh')  # time at next scr refresh
            test_cross.setAutoDraw(True)
        if test_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > test_cross.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                test_cross.tStop = t  # not accounting for scr refresh
                test_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(test_cross, 'tStopRefresh')  # time at next scr refresh
                test_cross.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Test_ISIComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Test_ISI"-------
    for thisComponent in Test_ISIComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    test_trials.addData('test_cross.started', test_cross.tStartRefresh)
    test_trials.addData('test_cross.stopped', test_cross.tStopRefresh)
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'test_trials'


# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
