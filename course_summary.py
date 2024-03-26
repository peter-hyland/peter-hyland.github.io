import os
import openai
from dotenv import load_dotenv
from git import Repo
from pathlib import Path
import json 

# Load environment variables and set OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the path to the blog repository and its content directory
PATH_TO_BLOG_REPO = Path('/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/.git')
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
PATH_TO_CONTENT = PATH_TO_BLOG/"content"
PATH_TO_SUMMARY = PATH_TO_CONTENT/"summary.html"

# Ensure the content directory exists
PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)

def update_summary(commit_message='Updates summary'):
    """
    Update and push changes to the repository.
    """
    repo = Repo(PATH_TO_BLOG_REPO)
    repo.git.add(all=True)
    repo.index.commit(commit_message)
    origin = repo.remote(name='origin')
    origin.push()


def write_summary_to_html(summary_json):
    """
    Writes the provided summary JSON to summary.html in the content directory.
    The summary is expected to have an "Overview" followed by topics and their summaries.
    """
    try:
        summary_data = json.loads(summary_json)
    except json.JSONDecodeError:
        print("Failed to decode summary JSON. Please check the format.")
        return

    html_content = ["<html><head><title>Course Summary</title></head><body><h1>Course Summary</h1>"]

    # Handling the Overview separately
    if "Overview" in summary_data:
        html_content.append(f"<h2>Overview</h2><p>{summary_data['Overview']}</p>")
    
    # Handling other topics
    for key, value in summary_data.items():
        if key != "Overview":  # Skip the Overview since it's already handled
            html_content.append(f"<h2>{key}</h2><p>{value}</p>")
    
    html_content.append("</body></html>")
    
    with open(PATH_TO_SUMMARY, 'w') as file:
        file.write('\n'.join(html_content))

def get_summary_from_openai(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()

    with open('/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/test_contents.txt', 'r') as file:
        train_contents = file.read()

    with open('/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/product_cata.txt', 'r') as file:
        product_catalogue = file.read()

    assistant_prompt = """{
  "Overview": [
    "How to Create an Account",
    "How to Sign In",
    "Changing your Password",
    "Using the Dashboard",
    "User Management",
    "Course Management",
    "Submodule Templates",
    "Troubleshooting"
  ],
  "How to Create an Account": "To sign into the Operator Dashboard, it is necessary to have an account created by contacting info@skillsbase.io.",
  "How to Sign In": "Navigate to https://operator.skillsbase.io/ and enter login details received via email.",
  "Changing your Password": "Change password by accessing 'My Account' and selecting 'Change Password'.",
  "Using the Dashboard": "Dashboard provides quick view options for Users, Groups, Courses, Modules, Products, and Resources.",
  "User Management": "View, create, and manage user accounts including assigning courses and viewing training progress.",
  "Course Management": "Overview of courses, modules, creation, editing, and filtering options.",
  "Submodule Templates": "Various submodule templates available like Title Slide, Web Viewer, Video Player, Image Gallery, Mini Quiz, etc., for creating content.",
  "Troubleshooting": "Guide for common issues like sign-in problems, password reset, user login trouble, push notification errors, team member addition, email correction, and contact information for unlisted issues."
}
    """
    course_overview = """{
    "Overview": [
        "Summer Pre-season Course",
        "Schedule and Gym Session Plans",
        "Pitch Setting Exercises"
    ],
    "Summer Pre-season Course": "Provides a detailed weekly schedule for summer pre-season training activities.",
    "Schedule and Gym Session Plans": "Includes submodules for Monday full body gym, Tuesday upper body gym, and Thursday lower body gym.",
    "Pitch Setting Exercises": "Focuses on exercises like A-Skip, A-March, and Acceleration to Deceleration for improving running form and speed.",
    }
    """
    """
    Fetches the course summary using the OpenAI API and writes it to summary.html.
    """
    # prompt = create_prompt()  # Assuming create_prompt returns the desired text
    response = openai.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role":"system","content":"Given a large amount of information, provide a summary 'overview' that will be shown at the end of the course, format it in json dict, for example: \"Overview\" (list of all main topics), \"(name of topic 1)\" (summary of topic 1),\"(name of topic 2)\" (summary of topic 2) and so on"},
                                                  {"role":"user","content":file_contents},
                                    
                                    
                                              ])
    summary = response.choices[0].message.content
    write_summary_to_html(summary)  # Save the summary to summary.html
    return summary

# prompts
# {"role":"system","content":"Given a training course from Skillsbase Ltd, provide a summary by picking out the main goals of the course"}

# Example usage:
summary = get_summary_from_openai("/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/skillsbase_operator.txt")
print(summary)
update_summary('Updates course summary on website')
