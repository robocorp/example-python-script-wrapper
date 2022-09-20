# Python Wrapper Robot

This robot is an example of how you can wrap an existing Python script into a robot that is runnable on Robocorp's Control Room. It shows the following concepts:

1. How to configure a Python robot to accept [email triggers from Control Room](https://robocorp.com/docs/control-room/attended-or-unattended/email-trigger#configuration-options).
2. How to extract a file from a [work item](https://robocorp.com/docs/development-guide/control-room/work-items#what-is-a-work-item) (an Excel file).
3. Using secrets from the [Control Room Vault](https://robocorp.com/docs/development-guide/variables-and-secrets/vault).
4. How to send an output file via [IMAP/SMPT mail services](https://robocorp.com/docs/libraries/rpa-framework/rpa-email-imapsmtp).
5. Logging to the `artifactDir` as defined in `robot.yaml`.

## Additional Stretch Goals

1. Reproduce examples above using Robot Framework calling Python as keyword(s).
2. Allow robot to utilize [behavior-driven-style .feature files](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#behavior-driven-style) as if they were robot files.

# Usage as a template

This repository can be used as a template for building similar automations when you already have an existing Python script that you wish to automate via the Control Room. You will need to modify implementation of each keyword in `task.py` considering the use case of your Python script, but the basic concepts should be followed to facilitate scheduling and reporting of activity from the Python script. 

## Setting dependencies

You must determine what dependencies your script has and add them to the `conda.yaml`. You should use specific versions to lock the dependencies because floating versions or undefined versions result in environment rebuild every run with our tooling.

## Modifying the existing script

While you should not have to perform extensive modifications, you must consider if your script is interacting with the underlying system and modify it to change that behavior. Robots generally interact only within their own directory tree through the use of `output` and `temp` directories. 

Work items offer a method to get new input files to your script if that is necessary. You can modify your script to directly utilize work items following the example in `task.py` here or you can extract the file and provide it to the underlying script.

You can use the Robocorp Control Room vault to manage credentials securely, and again, you can modify your script to directly use the vault or you can set environment variables or pass them in via function calls as you prefer.