import datetime
import os

def add_submissions_to_database():
    # Get the current date for the submission
    while True:
        submission_date = input("Enter the submission date (DD/MM): ")
        try:
            submission_datetime = datetime.datetime.strptime(submission_date, "%d/%m")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in the format 'DD/MM'.")

    # Prompt the user for the projects until they say stop
    projects = []
    while True:
        project = input("Enter a project (or 'stop' to finish): ")
        if project == 'stop':
            break
        projects.append(project)

    # Sort the projects in alphabetical order
    projects.sort()

    # Create the separator and the text to add to the file
    separator = "------------------"
    submission_text = f"{separator}\nSubmission date: {submission_datetime.strftime('%d/%m')}\n\n"
    submission_text += "\n".join(projects)

    # Calculate the due date for the submissions
    submission_due_date = calculate_submission_due_date(submission_datetime)

    # Add the due date to the submission text
    submission_text += f"\n\nTakedown date: {submission_due_date.strftime('%d/%m')}\n"

    # Write the submission text to the database file
    try:
        with open("back_catalogue_submissions.txt", "a") as file:
            file.write(submission_text)
    except IOError:
        print("Error writing to file.")
        return

    # Open the file
    try:
        file_path = "back_catalogue_submissions.txt"
        os.startfile(file_path)
    except OSError:
        print("Error opening file.")
        return


def calculate_submission_due_date(submission_datetime):
    # Calculate the number of business days to add
    business_days_to_add = 5

    # Loop through the days to add, skipping weekends (Saturday and Sunday)
    while business_days_to_add > 0:
        submission_datetime += datetime.timedelta(days=1)
        if submission_datetime.weekday() < 5:
            business_days_to_add -= 1

    return submission_datetime


# Call the function to add new submissions to the database
add_submissions_to_database()
