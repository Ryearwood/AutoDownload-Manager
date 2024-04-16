## Python AutoDownload Manager

A Python application to automate sorting of your downloaded files on MacOS. 

## Why?

Having recently made the switch from Windows to MacOS, I've found it mildly frustrating the number of things that I took for granted in a Windows system environment. Things like automatic file sorting on download, or individual application volume control are simply not available on Mac without:
1) High background memory usage (Looking at you Automator)
2) Paying USD $40 for volume control options (The trend being to pay for things that should be included as default functionality)

Therefore, I decided to simply build myself a working solution using Python and have it run as a low-memory, background process that starts up each time my laptop wakes.

## How Does it Work?

The Python script runs in the background passively and uses system logs to monitor whenever a file is downloaded into the default download folder. Once a download log has been detected, the script simply moves the file, according to filetype, to the desired location.

___
All you have to do is designate which folders you want which files to be sorted into!
<br>
<br>
<img width="700" alt="Screenshot 4" src="https://github.com/Ryearwood/AutoDownload-Manager/assets/75701990/d5add73a-f06c-471c-bb2f-1f1c5fa0ab16">

## Want to run this file automatically on Startup on your MacBook?

  1. Create a ```.zh``` file and input the following (I use conda but if you don't, just exclude the conda lines from the ```.zh``` file.)

    #!/bin/zsh
    
    Set current directory to project folder containing script (ex. cd <path_to_project_folder>)
    Path to Python env manager (ex. source /opt/anaconda3/etc/profile.d/conda.sh) }
    Environment activation (ex. conda_activate <name_of_your_environment>)
    python auto_file_management.py
    
  
  2. Now that the shell script has been created (Step 1), follow these steps in order.
       * Create a shell script named as ```login.sh``` in your ```$HOME``` folder.
       * Paste the following one-line command into ```Script Editor```: 
         ```
         do shell script "$HOME/login.sh"
         ```
    
  4. Then save it as an Application.
  5. Finally add the newly created Application to your login items via the General Settings on your Macbook
     <img width="585" alt="Screenshot 3" src="https://github.com/Ryearwood/AutoDownload-Manager/assets/75701990/2ce4eb81-973a-472c-9018-b2284c1d6f6f">
  7. (Optional) If you want to make the script output visual, you can swap step 2 for this:
        ```
        tell application "Terminal"
          activate
          do script "$HOME/login.sh"
        end tell
        ```

  8. (Optional) If multiple commands are needed something like this can be used:
       ```
       tell application "Terminal"
         activate
         do script "cd $HOME"
         do script "./login.sh" in window 1
       end tell
       ```
<br>

## Considerations and Future Changelog

I started and built this relatively quickly just to get the functionality up and running without much thought to ease of use or distribution.

As such, in the future, I will be cleaning this up and creating a packaged version with pre-set defaults and better folder structure integrity(for example for verification and creation if a download location does not exist).

## Contributions

- If you do come across this, like it or think it's useful - please give a ⭐
- if you'd like to contribute, feel free to fork and submit a PR for merge attached to a related issue log.
