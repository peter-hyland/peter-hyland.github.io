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
    Writes the provided structured summary JSON to summary.html in the specified directory.
    Dynamically handles sections, including lists, displaying them as bullet points, and includes specified head elements.
    """
    try:
        summary_data = json.loads(summary_json)
    except json.JSONDecodeError:
        print("Failed to decode summary JSON. Please check the format.")
        return

    # Updated HTML content initialization to include the specified head elements
    html_content = [
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Information Summary</title>
            <link rel="stylesheet" href="../static/styles.css">
            <script src="script.js" defer></script>
        </head>
        <body>
            <h1>Information Summary</h1>
        """
    ]

    def handle_value(key, value, indent_level=0):
        html = []
        if isinstance(value, list):
            html.append(f"{'  '*indent_level}")
            for item in value:
                if isinstance(item, (dict, list)):
                    html.extend(handle_value(key, item, indent_level+1))
                else:
                    html.append(f"{'  '*(indent_level+1)}<li>{item}</li>")
            html.append(f"{'  '*indent_level}</ul>")
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                html.extend(handle_value(sub_key, sub_value, indent_level))
        else:
            html.append(f"{'  '*indent_level}<p><strong>{key}:</strong> {value}</p>")
        return html

    for section_title, section_content in summary_data.items():
        html_content.append(f"<h2>{section_title}</h2>")
        html_content.extend(handle_value(section_title, section_content))

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

    """
    Fetches the course summary using the OpenAI API and writes it to summary.html.
    """
    # prompt = create_prompt()  # Assuming create_prompt returns the desired text
    response = openai.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role":"system","content":"Given a large amount of information, provide a summary 'overview' that will be shown at the end of the course, format it in json dict, for example: \"Overview\" (list of all main topics), \"(name of topic 1)\" (key and value information),\"(name of topic 2)\" (key and value information) and so on"},
                                                  {"role":"user","content":product_catalogue},
                                    
                                    
                                              ])
    summary = response.choices[0].message.content
    write_summary_to_html(summary)  # Save the summary to summary.html
    return summary

# prompts
# {"role":"system","content":"Given a training course from Skillsbase Ltd, provide a summary by picking out the main goals of the course"}

# Example usage:
summary = get_summary_from_openai("/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/skillsbase_operator.txt")
print(summary)
# update_summary('Updates course summary on website')


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