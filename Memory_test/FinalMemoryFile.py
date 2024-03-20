import time
import random
import requests
from bs4 import BeautifulSoup
import json
import time
import csv
from IPython.display import HTML, clear_output, display

def run_memory_test():
    # Initial user_data dictionary
    user_data = {}

    #Function to display images
    def display_image(image_name):
        img_html = HTML(f"<img src='{image_name}' alt='Image' style='width: 400px;'>")
        display(img_html)

    # Data consent
    data_consent_info = """DATA CONSENT INFORMATION:

    Please read:

    We wish to record your response data
    to an anonymised public data repository. 
    Your data will be used for educational teaching purposes
    practising data analysis and visualisation.

    Please type   yes   in the box below if you consent to the upload."""

    print(data_consent_info)
    result = input("> ") 

    if result == "yes": # Code continues only if the input is "yes"
        print("Thanks for your participation.")
        print("Please contact a.fedorec@ucl.ac.uk")
        print("If you have any questions or concerns")
        print("regarding the stored results.")
        time.sleep(4)
        clear_output(wait=True)
    else: 
        # End code execution by raising an exception if the answer is "no"
        raise(Exception("User did not consent to continue test."))
        time.sleep(3)
        clear_output(wait=True)

    # Name and age inputs
    welcome_code = "Welcome to the Memory Test"
    style = "color: black; font-size: 28px;"
    html_out = HTML(f"""<span style='{style}'>{welcome_code}</span>""")
    display(html_out)
    id_instructions = """

    Enter your anonymised ID

    To generate an anonymous 4-letter unique user identifier please enter:
    - two letters based on the initials (first and last name) of a childhood friend
    - two letters based on the initials (first and last name) of a favourite actor / actress

    e.g. if your friend was called Charlie Brown and film star was Tom Cruise
         then your unique identifier would be CBTC
    """

    print(id_instructions)
    user_id = input("> ")
    user_data['user_id'] = user_id # Store user_id in the dictionary user_data 
    print("User entered id:", user_id)

    ans2 = input("Please enter your age: ")
    clear_output(wait=True)
    user_data['age'] = ans2 # Store age in the dictionary user_data 
    gender = input("Please enter your gender (m/f/o): ")
    clear_output(wait=True)
    user_data['gender'] = gender # Store gender in the dictionary user_data 
    instructions = "Here are your test instructions"
    time.sleep(1)

    print("An image will appear for 10 seconds and you need to do your best to remember it")
    time.sleep(2)
    print("Then three sets of questions will be asked about the image")
    time.sleep(2)
    print("This will repeat for 6 images") 
    time.sleep(2)
    print("Good luck!")
    time.sleep(2)
    clear_output(wait=True)

    # Function to run the memory test for a set of questions and answers
    def run_memory_test(image_name, questions_answers):
        display_image(image_name)
        time.sleep(10)  
        clear_output()  

        total_correct_answers = 0 # Correct answer counter

        start_time = time.time()

        for question, answer in questions_answers.items():
            ans = input(f"Question: {question}\nAnswer: ")
            if ans.lower() == answer.lower():
                total_correct_answers += 1 # Add to the counter if the answer matches the question in dictionary 

            print("Next question!")
            time.sleep(1)
            clear_output()  

        end_time = time.time()
        time_taken = end_time - start_time # Time taken for question

        return total_correct_answers, time_taken

    # Function for the full test with the different images
    def run_full_memory_test(images_questions_answers):
        total_correct_answers = 0
        time_measurements = []

        for image_name, questions_answers in images_questions_answers.items():
            correct_answers, time_taken = run_memory_test(image_name, questions_answers)
            total_correct_answers += correct_answers
            time_measurements.append((image_name, time_taken))

        return total_correct_answers, time_measurements

    # Dictionary of the images w/ questions and answers
    images_questions_answers = {
        'img1.png': {
            'What shape was in the top right corner?': 'sun',
            'What colour was the heart?': 'green',
            'What way as the arrow pointing?': 'right'
        },
        'img2.png': {
            'What shape was inside the circle': 'star',
            'What colour was the sun?': 'black',
            'What colour was the triangle': 'purple'
        }, 
        'img3.png': {
            'What shape was in the top left corner?':'rectangle',
            'What colour was the arrow?':'blue',
            'Which way was the triangle pointing?':'down'
        },
        'img4.png': {
            'What shape was inside the circle?':'heart',
            'What colour was the shape inside the star?':'light blue',
            'What shape was the equals sign inside of?':'square'
        },
        'img5.png': {
            'What shape was brown?':'sun',
            'What shape was between the moon and star?':'square',
            'What shape was in the bottom right corner':'arrow'
        },
        'img6.png': {
            'What shape was pink?':'triangle',
            'Which way was the arrow inside the circle pointing?':'up',
            'What shape was between the divide and multiply signs?:':'diamond'
        },
    }

    # Running the full test
    score, time_measurements = run_full_memory_test(images_questions_answers)

    # Results
    print("Time measurements for each image:")
    for image_name, time_taken in time_measurements:
        print(f"{image_name}: {time_taken:.2f} seconds")
    print("Total correct answers:", score, "out of 18")
    print("Congrats!")

    # Score added to dictionary 
    user_data['total_correct_answers'] = score

    # Time measurements added to dictionary 
    for i, (image_name, time_taken) in enumerate(time_measurements, start=1):
        user_data[f"image_{i}_time_taken"] = round(time_taken, 2)

    # Functions to send user_data to google form
    def send_to_google_form(user_data, form_url):
        ''' Helper function to upload information to a corresponding google form 
            You are not expected to follow the code within this function!
        '''
        form_id = form_url[34:90]
        view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
        post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

        page = requests.get(view_form_url)
        content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
        content = content.text[27:-1]
        result = json.loads(content)[1][1]
        form_dict = {}

        loaded_all = True
        for item in result:
            if item[1] not in user_data:
                print(f"Form item {item[1]} not found. Data not uploaded.")
                loaded_all = False
                return False
            form_dict[f'entry.{item[4][0][0]}'] = user_data[item[1]]

        post_result = requests.post(post_form_url, data=form_dict)
        return post_result.ok

    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeawuzxWQdrz0DxmpXa6BINMfXzqWKyCYVPMY2gFJ3vSSzXJA/viewform"
    send_to_google_form(user_data, form_url) 

# Run the memory test
run_memory_test()
