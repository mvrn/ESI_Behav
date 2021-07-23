#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.1.4),
    on Tue Jul 20 15:56:36 2021
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
expName = 'Test1'  # from the Builder filename that created this script
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
    originPath='/Users/mriveran/Documents/psychopy_exps/esi_study_run1.py',
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

# Initialize components for Routine "Study"
StudyClock = core.Clock()
study_stim = visual.ImageStim(
    win=win,
    name='study_stim', 
    image='sin', mask=None,
    ori=0.0, pos=(0, 0), size=(0.8, 0.6),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
study_key_resp = keyboard.Keyboard()

# Initialize components for Routine "Study_ISI"
Study_ISIClock = core.Clock()
study_cross = visual.ImageStim(
    win=win,
    name='study_cross', 
    image='sin', mask=None,
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
study_trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('esi_study_run1_stim.xlsx'),
    seed=None, name='study_trials')
thisExp.addLoop(study_trials)  # add the loop to the experiment
thisStudy_trial = study_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisStudy_trial.rgb)
if thisStudy_trial != None:
    for paramName in thisStudy_trial:
        exec('{} = thisStudy_trial[paramName]'.format(paramName))

for thisStudy_trial in study_trials:
    currentLoop = study_trials
    # abbreviate parameter names if possible (e.g. rgb = thisStudy_trial.rgb)
    if thisStudy_trial != None:
        for paramName in thisStudy_trial:
            exec('{} = thisStudy_trial[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "Study"-------
    continueRoutine = True
    routineTimer.add(2.000000)
    # update component parameters for each repeat
    study_stim.setImage(Stim)
    study_key_resp.keys = []
    study_key_resp.rt = []
    _study_key_resp_allKeys = []
    # keep track of which components have finished
    StudyComponents = [study_stim, study_key_resp]
    for thisComponent in StudyComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    StudyClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Study"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = StudyClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=StudyClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *study_stim* updates
        if study_stim.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            study_stim.frameNStart = frameN  # exact frame index
            study_stim.tStart = t  # local t and not account for scr refresh
            study_stim.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(study_stim, 'tStartRefresh')  # time at next scr refresh
            study_stim.setAutoDraw(True)
        if study_stim.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > study_stim.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                study_stim.tStop = t  # not accounting for scr refresh
                study_stim.frameNStop = frameN  # exact frame index
                win.timeOnFlip(study_stim, 'tStopRefresh')  # time at next scr refresh
                study_stim.setAutoDraw(False)
        
        # *study_key_resp* updates
        waitOnFlip = False
        if study_key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            study_key_resp.frameNStart = frameN  # exact frame index
            study_key_resp.tStart = t  # local t and not account for scr refresh
            study_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(study_key_resp, 'tStartRefresh')  # time at next scr refresh
            study_key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(study_key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(study_key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if study_key_resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > study_key_resp.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                study_key_resp.tStop = t  # not accounting for scr refresh
                study_key_resp.frameNStop = frameN  # exact frame index
                win.timeOnFlip(study_key_resp, 'tStopRefresh')  # time at next scr refresh
                study_key_resp.status = FINISHED
        if study_key_resp.status == STARTED and not waitOnFlip:
            theseKeys = study_key_resp.getKeys(keyList=['a', 'l'], waitRelease=False)
            _study_key_resp_allKeys.extend(theseKeys)
            if len(_study_key_resp_allKeys):
                study_key_resp.keys = _study_key_resp_allKeys[-1].name  # just the last key pressed
                study_key_resp.rt = _study_key_resp_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in StudyComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Study"-------
    for thisComponent in StudyComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    study_trials.addData('study_stim.started', study_stim.tStartRefresh)
    study_trials.addData('study_stim.stopped', study_stim.tStopRefresh)
    # check responses
    if study_key_resp.keys in ['', [], None]:  # No response was made
        study_key_resp.keys = None
    study_trials.addData('study_key_resp.keys',study_key_resp.keys)
    if study_key_resp.keys != None:  # we had a response
        study_trials.addData('study_key_resp.rt', study_key_resp.rt)
    study_trials.addData('study_key_resp.started', study_key_resp.tStartRefresh)
    study_trials.addData('study_key_resp.stopped', study_key_resp.tStopRefresh)
    
    # ------Prepare to start Routine "Study_ISI"-------
    continueRoutine = True
    routineTimer.add(4.000000)
    # update component parameters for each repeat
    study_cross.setImage('ISI_Stim.png')
    # keep track of which components have finished
    Study_ISIComponents = [study_cross]
    for thisComponent in Study_ISIComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Study_ISIClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Study_ISI"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Study_ISIClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Study_ISIClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *study_cross* updates
        if study_cross.status == NOT_STARTED and tThisFlip >= 2.0-frameTolerance:
            # keep track of start time/frame for later
            study_cross.frameNStart = frameN  # exact frame index
            study_cross.tStart = t  # local t and not account for scr refresh
            study_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(study_cross, 'tStartRefresh')  # time at next scr refresh
            study_cross.setAutoDraw(True)
        if study_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > study_cross.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                study_cross.tStop = t  # not accounting for scr refresh
                study_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(study_cross, 'tStopRefresh')  # time at next scr refresh
                study_cross.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Study_ISIComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Study_ISI"-------
    for thisComponent in Study_ISIComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    study_trials.addData('study_cross.started', study_cross.tStartRefresh)
    study_trials.addData('study_cross.stopped', study_cross.tStopRefresh)
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'study_trials'


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
