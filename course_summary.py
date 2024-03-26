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
    "Module 1": "Schedule and Gym Session Plans",
    "Module 2": "Pitch Setting Exercises"
  },
  "Module 1": {
    "Title": "Schedule and Gym Session Plans",
    "Description": "This module focuses on the weekly schedule and gym session plans for a summer pre-season training program.",
    "Submodules": {
      "Weekley Schedule": {
        "Info": "Outlined a detailed daily schedule including recovery, training, skills session, team meetings, and game day preparations.",
      },
      "Monday full body gym": {
        "Info": "Focused on compound movements like squats, bench press, deadlifts, and pull-ups for a full-body workout."
      },
      "Tuesday upper body gym": {
        "Info": "Included exercises like bench press, bent-over rows, overhead press, and pull-ups to target upper body muscle groups."
      },
      "Thursday lower body gym": {
        "Info": "Consisted of exercises such as squats, deadlifts, lunges, and leg press to strengthen and tone the lower body muscles."
      }
    }
  },
  "Module 2": {
    "Title": "Pitch Setting Exercises",
    "Description": "This module demonstrates various exercises to enhance running form, speed, agility, and acceleration to deceleration skills.",
    "Submodules": {
      "A-Skip": {
        "Info": "A drill designed to enhance knee lift, rhythm, and coordination crucial for sprinting and agility."
      },
      "A-March": {
        "Info": "Focuses on high knee lift and proper foot mechanics to improve running form and promote better movement."
      },
      "Acceleration to Deceleration": {
        "Info": "Drill aimed at improving the ability to gain speed rapidly and slow down efficiently, essential for sports with quick speed changes."
      }
    }
  }
}
"""
    """
    Fetches the course summary using the OpenAI API and writes it to summary.html.
    """
    # prompt = create_prompt()  # Assuming create_prompt returns the desired text
    response = openai.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role":"system","content":"Given a large amount of information, provide a summary 'overview' that will be shown at the end of the course, format it in json dict, for example: \"Overview\" (all main topics), \"(name of topic 1)\" (summary of topic 1),\"(name of topic 2)\" (summary of topic 2) and so on"},
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
