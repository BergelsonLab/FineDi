#!/usr/bin/env python
#
# all the imports
import os
import sqlite3
from flask import (Flask, request, session, g, redirect, url_for, abort,
                   render_template, flash)
from collections import defaultdict
import subprocess
from tempfile import mkstemp
from os import remove
from shutil import move

from utils import *
# create app
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py
# Load default config and override config from an environment variable
app.config.update(dict(
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default',
        MEDIA_ROOT='static/media'
        ))

@app.route('/')
def index():
    """ TODO DEFINE
        Let the user choose what routine (s)he wants to use
        to refine the diarization. 
        Suggested routines: - treat all wavs
                                - which transcription to use ? gold ? Diartk ?
                            - treat one wav
                                - give name
                                - which transcription to use ? gold ? Diartk ?
                            - upload one wav + transcription
    """
    wav_list = get_wav_list(os.path.join(app.root_path, 'static', 'audio'))
    output = create_segments()

    return render_template('index.html', wav=output)

#@app.route('/creating')
def create_segments():
    """ Take each wav, retrieve all the annotated segments,
        cut the wav into the segments corresponding to 'CHI'
        and check the labels.
        The names of the outputed wavs are :
            in_wav_on_off_spkr_lab.wav
        where in_wav is the input wav that is segmented, on is
        the time when the segment starts, off the time when the
        segment ends, spkr is the name of the speaker and label
        is the annotation associated with this speaker

    """
    # first get all the wavs
    wav_list = get_wav_list(os.path.join(app.root_path, 'static', 'audio'))
    
    # for each wav, retrieve the labels
    for wav_name in wav_list[0:1]:
        wav_rttm_dict = read_rttm(wav_name)
        for on, dur, lab in wav_rttm_dict['CHI']:
            wav_path = os.path.join(app.root_path, 'static',
                                    'audio', wav_name)
            # skip empty segments
            if dur <= 0:
                continue
            # define output wav path
            output_wav = wav_name.split('.')[0] + '_{}_{}_{}.wav'.format(on,
                                                                         dur,
                                                                         lab)
            output_path = os.path.join(app.root_path,
                                       app.config['MEDIA_ROOT'],
                                       output_wav)
        
            # create output wave name
            cmd=['sox', wav_path, output_path, 'trim', str(on), str(dur)]
            subprocess.call(cmd)

    # return first wav of the list to start manual annotation
    temp_wav_list = get_wav_list(os.path.join(app.root_path,
                                 app.config['MEDIA_ROOT']))
 
    return temp_wav_list[0] 


@app.route('/all_wavs/<wav_name>', methods=['GET', 'POST'])
def treat_all_wavs(wav_name='test1.wav'):
    """ This function creates the app
        when the user is treating all the wavs. 
        It gets the current wav but also the previous and the next.
        This page can be accessed in the browser by going directly 
        to localhost/all_wavs/<wav_name> , where wav_name is
        the name of the wav you want to treat. 

        TODO: add what kind of transcription you want to treat.
    """
 
    # if no wav is given as input, take the first one that's not locked
    # in the media folder.
    print wav_name
    wav_list = get_wav_list(os.path.join(app.root_path,
                                         app.config['MEDIA_ROOT']))
    # try to get the position of current wav in list
    #try:
    wav_index = wav_list.index(wav_name)
    
    
    # get previous wav
    if wav_index > 0:
        prev_wav = wav_list[wav_index - 1]
    else:
        prev_wav = None
    
    # get next wav
    if wav_index < len(wav_list) - 1:
        next_wav = wav_list[wav_index + 1]
    else:
        next_wav = None

    # get percentage of treated files for progress bar
    progress = round(( (float(wav_index) + 1) / len(wav_list) ) * 100)
    #except:
    #    print "except!" 
    #    # if the current wav is not in list, throw error page
    #    pass # TODO create error page

    # labels that can be put to the segment
    entries=["laugh", "cry", "speech", "do not change annotation"]
     
    # apply changes to RTTM and put lock to notify the use this file has been
    # treated
    correction = request.form.getlist('trs_label')
    if "Do Not Change Annotation" in correction:
        correction = []

    # extract description from wav name
    original_wav = "_".join(wav_name.split('_')[0:-3]) 
    wav_len = float(wav_name.split('_')[-2]) 
    #label = wav_name.split('_')[-1].split('.')[0]
    on_off = wav_name.split('_')[-3]
    label = get_label(original_wav, on_off, 'CHI')

    descriptors = [original_wav, wav_len, label, on_off]

    # if some corrections have been made,  change the rttm
    if len(correction) > 0:
        rttm_name = original_wav + '.rttm'
        rttm_in = os.path.join(app.root_path, 'static', 'audio', rttm_name)

        modify_rttm(rttm_in, descriptors, correction)
        lock_file(wav_name)

    return render_template('show_entries.html', entries=entries, 
                           wav=wav_name, next_wav=next_wav, prev_wav=prev_wav,
                           progress=progress, descriptors=descriptors)



