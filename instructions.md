# Instructions

Note: the symbol `$` will be at the beginning of each terminal command. It is used to signify the prompt, so simply enter the command that follows the dollar sign.

## 1. Setting up the environment

## 1.1. Setting up the environment for the first time

### 1.1.1. Set git

__NB: you need to have a GitHub account!__

- Open Terminal and clone the repository

  `$ git clone git@github.com:aclew/FineDi.git ~/Desktop/FineDi`

- Go into this directory

  `$ cd ~/Desktop/FineDi/`

- Check that you are on the right branch

  `$ git branch -a`

  - If the output has `*master` in green (or anything other than `whole_vs_500` in green), change branch using

    `$ git checkout whole_vs_500`
    
  - Repeat instruction `$ git branch -a` to check that `* whole_vs_500` is now in green in the top row


### 1.1.2. Put dataset at the right place

- On your desktop, go to _FineDi -> fineDi -> static_

  - Check that the files _info_dict.txt_ and _summary.txt_ exist (if not, don't go any further, and ask Gladys)

  - In _FineDi -> fineDi -> static_, create a folder named _media_

  - Login to PN-Opus and Copy the folder _Seedlings -> classif_comparison -> cut_dir_ into the  _media_ folder you just created in the static_ folder (it may take up to 5 minutes)

## 1.2. Retrieving changes (if not first time)

- Open Terminal and get the latest modifications to the files _info_dict.txt_ and _summary.txt_

  `$ cd ~/Desktop/Finedi`

  `$ git pull`

  - If there is a merging issue... should not happen...but go bug Gladys if it does:)
  
## 2. Check volume

- Listen to one of the clips in _media->cutdir->full_ and adjust the volume. Please do not change the volume during the task.
  
## 3. Running the app

### 3.1. Launching the app

- Once the environment is set up, open `Terminal`

- Write `cd ` then drag and drop the FineDi folder in the terminal (the command should look like `$ cd /Users/gb146/Desktop/FineDi`)

- Check that you are at the right place by writing the following command in the terminal:

  `$ ls`

You should then see the name `launch_app.sh` appear in the list

- Launch the app from the Terminal

  `$ sh launch_app.sh`

- Open the corresponding address in Firefox

  - Open Firefox

  - Enter the address `localhost:5000` in the address bar, enter

### 3.2. Options to choose

- Choose __Start session__

- Click on the task that you want to do (__500, first pass, second pass__)

### 3.3. Steps to follow

- For __500__ or __second pass__

  - Listen to the clip by clicking the play button

  - Choose a label, then click __Submit query__; this will automatically go to the next wav

- For __first pass__

  - Listen to the clip by clicking the play button

  - Say whether you hear a child or not by clicking __Exclude__ or __Keep__, then click __Submit query__; this will automatically go to the next wav

## 4. Finishing a session

- A progress bar indicates the proportion of files that you heard and the proportion that is left to hear. You will hear a maximum of 100 clips by session. Once the progress bar is full, a success page appears: your task is complete!

  - Quit Firefox

  - In the terminal, press _ctrl+C_ to quit the app

- __!!! Save your progress on the git repository - this MUST be done before you leave !!!__

  - In the terminal, write the commands:

    `$ git add findeDi/static/summary.txt`

    `$ git add findeDi/static/info_dict.txt`

    `$ git commit -m "processed [n] files for task [i]"` (with n the number of files that you listened to and i the name of the task). For example, if you have done 2 series of 100 segments for the 'whole, first pass' task, your commit command will be `$ git commit -m "processed 200 files for task whole, first pass"`

    `$ git push`


## You did your part, thank you!
