import os
import openai
from dotenv import load_dotenv
from git import Repo
from pathlib import Path
import json 
from sort_csv import process_csv_data

# Load environment variables and set OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the path to the blog repository and its content directory
PATH_TO_BLOG_REPO = Path('/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/.git')
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
PATH_TO_CONTENT = PATH_TO_BLOG/"content"
PATH_TO_SUMMARY = PATH_TO_CONTENT/"test.html"

# Ensure the content directory exists
PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)

course_name = 'Dexgreen Catalogue Summary'

def update_summary(commit_message='Updates summary'):
    """
    Update and push changes to the repository.
    """
    update_index()
    repo = Repo(PATH_TO_BLOG_REPO)
    repo.git.add(all=True)
    repo.index.commit(commit_message)
    origin = repo.remote(name='origin')
    origin.push()


def write_summary_to_html(summary_json):
    """
    Writes the provided structured summary JSON to summary.html in the specified directory.
    Dynamically handles sections, including lists and paragraphs, displaying them with appropriate styling and heading levels.
    """
    try:
        summary_data = json.loads(summary_json)
    except json.JSONDecodeError:
        print("Failed to decode summary JSON. Please check the format.")
        return

    # HTML content initialization
    html_content = [
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{course_name}</title>
            <link rel="stylesheet" href="../static/styles.css">
        </head>
        <body>
            <div class="container">
        """,
        f'<h1><img  class="img-heading" src="../images/skillsbase.png" alt="skillsbase logo"></h1>'

    ]

    def handle_value(key, value, heading_level=2, is_nested=False):
        """
        Recursively handles values in the summary, adjusting heading levels for nested content and aligning paragraphs.
        Uses 'inner-section' class for nested sections.
        """
        html = []
        heading_tag = f"h{min(heading_level, 6)}"  # Limit heading level to h6
        section_class = "inner-section" if is_nested else "content-section"

        # Wrap each section in a div with the appropriate class
        html.append(f"<div class='{section_class}'>")
        html.append(f"<h1>Dexgreen Catalogue Summary</h1>")
        if isinstance(value, list):
            html.append(f"<{heading_tag}>{key}</{heading_tag}><div class='list-container'><ul>")
            for item in value:
                if isinstance(item, (dict, list)):
                    # Increment heading level for nested lists/dicts, mark as nested
                    html.extend(handle_value(key, item, heading_level+1, True))
                else:
                    html.append(f"<li>{item}</li>")
            html.append("</ul></div>")
        elif isinstance(value, dict):
            html.append(f"<{heading_tag}>{key}</{heading_tag}>")
            for sub_key, sub_value in value.items():
                # Increment heading level for nested dicts, mark as nested
                html.extend(handle_value(sub_key, sub_value, heading_level+1, True))
        else:
            html.append(f"<p><strong>{key}:</strong> {value}</p>")
        
        html.append("</div>")
        
        return html

    for section_title, section_content in summary_data.items():
        html_content.extend(handle_value(section_title, section_content, 2))  # Start with h2 for the top level

    html_content.append("</div></body></html>")
    
    with open(PATH_TO_SUMMARY, 'w') as file:
        file.write('\n'.join(html_content))

# example test files

with open('/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/example_courses/test_contents.txt', 'r') as file:
    train_contents = file.read()

with open('/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/example_courses/product_cata.txt', 'r') as file:
    dexgreen_cata = file.read()

with open('/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/example_courses/skillsbase_operator.txt', 'r') as file:
    skillsbase_contents = file.read()

with open('/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/example_courses/general_cata.txt', 'r') as file:
    general_cata = file.read()

filename = '/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/example_courses/csp.csv'
csp_course = process_csv_data(filename)

# prompt engineeing

# system roles
    
general_role = "Given a large amount of information, provide a summary 'overview' that will be shown at the end of the course, format it in json dict, for example: \"Overview\" (list of all main topics), \"(name of topic 1)\" (key and value information),\"(name of topic 2)\" (key and value information) and so on."

skillsbase_role_1 ="Given a training course from Skillsbase Ltd, provide a summary by picking an 'overview' of the course and then the information, format the summary in json dict, for example: \"Overview\" (list of all main topics), \"(name of topic 1)\" (key and value information),\"(name of topic 2)\" (key and value information) and so on. This summary is meant for someone that has just finished the course and wants to review the main learning points."

skillsbase_role_2 = "Given a training course from Skillsbase Ltd, provide a summary by picking an 'overview' of the course and then the information, format the summary in json dict, for example: \"Overview\" (list of all main topics), \"(name of topic 1)\" (key and value information),\"(name of topic 2)\" (key and value information) and so on."

# user prompts

skillsbase_course_prompt1 = f"""
The below content is taken from mobile app based training courses. These training courses are composed of various interactive modules like videos, images with text, quizzes, checklists and more. 

{skillsbase_contents}
 
Based on the content provide a summary of the entire course. This summary is meant for someone that has just finished the course and wants to review the main learning points."""

csp_course_prompt1 = f"""
The below content is taken from mobile app based training courses. These training courses are composed of various interactive modules like videos, images with text, quizzes, checklists and more. 

{csp_course}
 
Based on the content provide a summary of the entire course. This summary is meant for someone that has just finished the course and wants to review the main learning points."""

dexgreen_course_prompt1 = f"""
The below content is taken from mobile app based training courses. These training courses are composed of various interactive modules like videos, images with text, quizzes, checklists and more. 

{dexgreen_cata}
 
Based on the content provide a summary of the entire course."""

dexgreen_course_prompt2 = f"""
The below content is taken from mobile app based training courses. These training courses are composed of various interactive modules like videos, images with text, quizzes, checklists and more. 

{general_cata}
 
Based on the content provide a summary of the entire course."""

def get_summary_from_openai(file_path):
    """
    Fetches the course summary using the OpenAI API and writes it to summary.html.
    """
    # prompt = create_prompt()  # Assuming create_prompt returns the desired text
    response = openai.chat.completions.create(model="gpt-4-turbo-preview",
                                              response_format={ "type": "json_object" }, 
                                              messages=[
                                                  {"role":"system","content":skillsbase_role_2},
                                                  {"role":"user","content":dexgreen_course_prompt2}
                                              ],
                                              temperature=1,
                                              max_tokens=4096                                           
                                              )
    
    summary = response.choices[0].message.content

    write_summary_to_html(summary)  # Save the summary to summary.html
    return summary


# Example usage:
summary = get_summary_from_openai("/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/skillsbase_operator.txt")
print(summary)



def update_index():
    # Folder containing the HTML files
    contents_folder = 'content'
    # Output file name
    output_file = 'index.html'

    # HTML template for the index page
    html_template = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contents Index</title>
    </head>
    <body>
        <h1>Contents Index</h1>
        <ul>
            {links}
        </ul>
    </body>
    </html>"""

    # Generate the list items as links for the HTML files
    links = []
    for filename in os.listdir(contents_folder):
        if filename.endswith('.html'):
            filepath = os.path.join(contents_folder, filename)
            links.append(f'<li><a href="{filepath}">{filename}</a></li>')

    # Join the links into a single string
    links_html = '\n        '.join(links)

    # Write the index.html file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template.format(links=links_html))

    print(f'{output_file} has been generated with links to all HTML files in the {contents_folder} folder.')


update_summary('Updates course summary on website')
