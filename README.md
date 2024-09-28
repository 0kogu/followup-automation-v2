# Follow up automation

This follow up generator extracts the account managers stats in the week of a inserted date directly from the API, paste it over a template, save it as image and store in a folder for that given date.

This is the second version of [this project](https://github.com/0kogu/followup-automation)

Here's a [video of the project working](https://youtu.be/1mE8IK77khM)


## Features

- **User Interface**: This version contains a interface where all the user needs to do is insert its bearer, select a folder and a date.
- - **API**: It retrieves data directly from the API
- **Smart Storing**: If the user inserts a date which only some managers work. saturday for example, a folder for that date will be created and it will store follow ups only for those who worked from tuesday to saturday, because the follow ups for manager who from monday to friday has been fully filled the day before and it was stored in the folder of the previous date.
- **Color indicator**: It displays a color indicator for each stat, green if the goal was achieved, red if it was not.
- **Dates**: It displays the worked dates in the week.


## Technologies

- **Python**
- **Tkinter** for GUI creation
- **Datetime** for hours and dates manipulation
- **Pillow** for image editing
- **Requests** to make requests to the API

  
## Future enhancements

- Create a request to list all managers' ID's
- Scheduling the script in the cloud
- Use Telegram API to automate the sending of follow ups


## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/0kogu/followup-automation-v2.git
   cd followup-automation-v2
