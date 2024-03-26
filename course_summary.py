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
    Writes the provided summary JSON to summary.html in the content directory,
    with course names as headings and their content as paragraphs.
    """
    try:
        summary_data = json.loads(summary_json)
    except json.JSONDecodeError:
        print("Failed to decode summary JSON. Please check the format.")
        return

    html_content = ["<html><head><title>Course Summary</title></head><body><h1>Course Summary</h1>"]
    
    for key, value in summary_data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                html_content.append(f"<h2>{sub_key}</h2><p>{sub_value}</p>")
        else:
            html_content.append(f"<h2>{key}</h2><p>{value}</p>")
    
    html_content.append("</body></html>")
    
    with open(PATH_TO_SUMMARY, 'w') as file:
        file.write('\n'.join(html_content))

def get_summary_from_openai(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    """
    Fetches the course summary using the OpenAI API and writes it to summary.html.
    """
    # prompt = create_prompt()  # Assuming create_prompt returns the desired text
    response = openai.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role":"system","content":"Given a training course from Skillsbase Ltd, provide a summary by picking out the main attributes of the course"},
                                                  {"role":"user","content":file_contents}
                                              ])
    summary = response.choices[0].message.content
    write_summary_to_html(summary)  # Save the summary to summary.html
    return summary

def create_prompt():
    prompt = """Course Name: Summer Pre-season
 
Description: Summer pre-season

Module: 
Module Name: Schedule and Gym Session Plans 

Submodules:
Submodule Name: Weekley Schedule
Info:
Monday: Recovery and Light Training
Morning: Rest or active recovery (e.g., light jog, swimming, yoga), gym
Afternoon: Team meeting to review previous game footage and discuss the week's focus
Evening: Light skills session focusing on handling and passing drills
Tuesday: Intensive Training Day
Morning: Strength and conditioning session in the gym (focus on compound movements like squats, deadlifts, bench presses, and rugby-specific plyometrics)
Afternoon: On-field training session focusing on defensive structures and tackling technique
Wednesday: Skills and Team Plays
Morning: Rest or optional recovery session (e.g., massage therapy, physiotherapy)
Afternoon: High-intensity skills training, focusing on attack strategies, set plays, and lineouts/scrum practice
Thursday: Team Tactics and Light Training
Morning: Light gym session, focusing on mobility and core strength
Afternoon: On-field tactical session, running through game plans and set pieces specific to the upcoming opponent
Friday: Captain’s Run and Mental Preparation
Morning: Rest or team walk-through
Afternoon: Captain’s run - a light, fast-paced training session to fine-tune strategies and ensure clarity on team plays. This session is followed by team meetings focused on mental preparation and game visualization.
Saturday: Game Day
Morning: Team walkthrough or light stretching session, team breakfast, and mental preparation
Afternoon/Evening: Warm-up, game, cool down, and initial post-game recovery (ice baths, stretching)
Sunday: Rest and Recovery
All Day: Complete rest from physical activity. Emphasis on mental recovery, hydration, and nutrition to start repairing the body.

Submodule Name: Monday full body gym
Info:
Squats (Compound - Legs and Core)
3 sets of 8-12 reps
Use a barbell or dumbbells for added resistance.
Bench Press (Compound - Chest, Shoulders, Triceps)
3 sets of 8-12 reps
Can be performed with a barbell or dumbbells on a flat bench.
Deadlifts (Compound - Back, Legs, Core)
3 sets of 8-12 reps
Focus on form to prevent back injuries.
Pull-Ups or Lat Pull-Downs (Compound - Upper Back, Biceps)
3 sets of 8-12 reps
If you can't do pull-ups, lat pull-downs are a good alternative.

Submodule Name: Tuesday upper body gym
Info:
Bench Press (Chest, Shoulders, Triceps)
3 sets of 8-12 reps
Can be done with a barbell or dumbbells on a flat bench.
Bent-Over Rows (Back, Biceps)
3 sets of 8-12 reps
Perform with a barbell or dumbbells, maintaining a slight bend in your knees and a flat back.
Overhead Press (Shoulders, Triceps)
3 sets of 8-12 reps
Stand or sit with a barbell or dumbbells. Press the weight overhead without arching your back.
Pull-Ups or Lat Pull-Downs (Upper Back, Biceps)
3 sets of 8-12 reps
If pull-ups are too challenging, lat pull-downs are a great alternative.

Submodule Name: Thursday lower body gym:
Info:
Squats (Quads, Hamstrings, Glutes, Core)
3 sets of 8-12 reps
Can be performed with a barbell for added resistance, or bodyweight for beginners.
Deadlifts (Hamstrings, Glutes, Lower Back)
3 sets of 8-12 reps
Use a barbell or dumbbells, keeping your back straight and lifting with your legs.
Lunges (Quads, Hamstrings, Glutes)
3 sets of 10 reps per leg
Perform walking lunges or stationary lunges with dumbbells for added resistance.
Leg Press (Quads, Glutes, Hamstrings)
3 sets of 8-12 reps
Adjust the weight to challenge yourself while maintaining good form.

Module:
Module Name: Pitch Setting Exercises

Description: This is a module that shows how to complete different excercises.

Submodule Name: A-Skip
Info:
Objective: The A-Skip exercise aims to improve knee lift, rhythm, and coordination, essential for sprinting and agility.

How to Perform:

Starting Position: Stand tall with your feet hip-width apart.
Movement: Begin by driving one knee up towards your chest as high as possible, keeping the opposite arm forward in a running motion. The raised leg should maintain a 90-degree angle at the knee.
Skip: As you bring the raised leg back down, simultaneously lift the other knee and switch arms, mimicking a skipping motion.
Rhythm: Maintain a rhythmic pattern, focusing on height and quickness of the knee lift with each skip.
Continue: Perform the exercise for a set distance (e.g., 20-30 meters) or time (e.g., 30 seconds).

Submodule Name: A-March
Info:
Objective: The A-March is a drill that focuses on high knee lift and proper foot mechanics, promoting improved running form.

How to Perform:

Starting Position: Stand tall with your feet hip-width apart.
Movement: Lift one knee up towards your chest, aiming for a thigh parallel to the ground while keeping the opposite arm forward.
Foot Action: Ensure the lifted leg's foot is dorsiflexed (toes pointing upwards) as if stepping over a hurdle.
March: Place the lifted foot back on the ground and simultaneously lift the opposite knee, switching arms in a controlled marching motion.
Continue: Perform the exercise in a forward-moving march for a set distance or time, focusing on form and control.

Submodule Name: Acceleration to Deceleration
Info:
Objective: This drill aims to improve acceleration (the ability to gain speed rapidly) and deceleration (the ability to slow down efficiently), crucial for sports requiring quick changes in speed.

How to Perform:

Starting Position: Begin in a ready stance, with your feet shoulder-width apart and knees slightly bent.
Acceleration: From the starting position, explosively accelerate forward by pushing off strongly with your legs. Increase your speed rapidly over a short distance (e.g., 10-20 meters), focusing on quick, powerful strides.
Transition: After reaching your maximum acceleration, begin to decelerate by gradually reducing your stride length and speed. Use your arms for balance and control as you slow down.
Deceleration: Aim to come to a complete stop smoothly and safely, lowering your center of gravity and bending your knees as you decelerate to absorb the impact.
Practice: Repeat the drill several times, focusing on smooth transitions between acceleration and deceleration.

""".format()
    return prompt

# Example usage:
summary = get_summary_from_openai("/Users/peterhyland/Documents/GitHub/peter-hyland.github.io/test_contents.txt")
print(summary)
update_summary('Updates course summary on website')
