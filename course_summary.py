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

    assistant_prompt = """{
  "Overview": {
    "title": "SkillsBase App for Experts",
    "description": "A comprehensive guide on how to use the SkillsBase App for Experts Operator Dashboard, including creating an account, signing in, changing passwords, using the dashboard, user management, course management, submodule templates, and troubleshooting.",
    "prepared_by": "Mark Horgan",
    "email": "info@skillsbase.io",
    "version": "Version 4 – 14th March 2023"
  },
  "How to Create an Account": {
    "summary": "To sign into the Operator Dashboard, you need to have an account created manually by contacting info@skillsbase.io. Once created, login details will be sent to you.",
    "steps": [
      "Contact info@skillsbase.io to request an account",
      "Login details will be sent after the account is created"
    ]
  },
  "How to Sign In": {
    "summary": "After creating an account, access the dashboard at https://operator.skillsbase.io/ and log in using the provided credentials.",
    "steps": [
      "Visit https://operator.skillsbase.io/",
      "Use the provided login details to sign in"
    ]
  },
  "Changing your Password": {
    "summary": "Upon logging in, change your password by accessing 'My Account' and selecting 'Change Password' to set a new password.",
    "steps": [
      "Access 'My Account'",
      "Choose 'Change Password'",
      "Set a new password"
    ]
  },
  "Using the Dashboard": {
    "summary": "The Dashboard contains quick view options for users, groups, courses, modules, products, and resources. Navigate using the sidebar menu.",
    "features": [
      "View users, groups, courses, modules, products, and resources",
      "Use the sidebar menu for navigation"
    ]
  },
  "User Management": {
    "summary": "View, create, enable, disable, and manage users on the platform. Assign courses and monitor user progress.",
    "steps": [
      "View users list, create new users, and set user passwords",
      "Assign courses, track training progress"
    ]
  },
  "Course Management": {
    "summary": "Create, edit, and manage courses, modules, and submodules. Utilize different templates for varied content.",
    "features": [
      "Create courses, generate links, filter, and view course details",
      "Manage modules, add submodules, set progression settings"
    ]
  },
  "Submodule Templates": {
    "summary": "Includes various submodule types like Title Slide, Web Viewer, Video Player, Image Gallery, Mini Quiz, and more for interactive content creation.",
    "templates": [
      "Title Slide, Web Viewer, Video Player, Image Gallery, etc."
    ]
  },
  "Troubleshooting": {
    "summary": "Addresses common issues like login problems, forgotten passwords, user login errors, push notification failures, team member addition, email corrections, and provides a contact point for unlisted problems.",
    "issues": [
      "Login errors, password resets, user issues, notification problems",
      "Team member addition, email corrections, contact details"
    ]
  }
}"""
    """
    Fetches the course summary using the OpenAI API and writes it to summary.html.
    """
    # prompt = create_prompt()  # Assuming create_prompt returns the desired text
    response = openai.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role":"system","content":"Given a large amount of information, provide a summary 'overview' that will be shown at the end of the course, format it in json dict, for example: \"Overview\" (all main topics), \"Title of Topic 1\" (summary of topic 1),\"Title of Topic 2\" (summary of topic 2) and so on"},
                                                  {"role":"user","content":train_contents}
                                                #   {"role":"assistant","content":assistant_prompt},
                                                #   {"role":"user","content":file_contents}
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
