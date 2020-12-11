# Regelhulpify

## What is Regelhulpify
The word 'Regelhulpify' is derived from the Dutch word 'rule aid', a tool that helps personalise laws, rules and guidelines. The Regelhulpify app allows anyone to make an account and start creating such a tool. In practice, a Regelhulp is a bit like a quiz, but without wrong or right answers: the logic one attaches to the answers makes sure the end user gets personalized information. Regelhulpify allows registered users to create a Regelhulp with a main image and a shorturl, a set of questions (of which the order can be manipulated) each with a set of answers (that point to another question or result.) Non-registered visitors can use all the tools made with regelhulpify.

## For CS50: distinctiveness and complexity
This project has been decidedly more complex to build than previous project, owing partly to the fact that this app has started from an actual use case and had to be translated back to a UX design and the theory covered in the course. The app is distinct from previous projects in that it allows the end user to manipulate the underlying databases in many more ways, requiring very careful project design to avoid invalid relationships. The complexity of the app has further increased after implementing actual user feedback, many in the field of usability. This means I have gotten to delve deeper into both Django's and JS's capabilities than in any prior project. 

## How Regelhulpify was built
As per the requirements, I've built the app in a combination of Django and JavaScript, trying to explore as many functionalities as possible from both within the scope of the project. I started with creating the models, and the views that allow the Question model to have a user-modifiable order. I then wrote the JavaScript to generate the pages displaying tools and questions, using fetch requests to get the necessary data from Django. 

### Views.py
I used three distinct categories of views: 
* Front views, used to display the user-created tools;
* Builder views, creating the pages on which users build those tools;
* API functions, to execute tasks initiated by JS fetch requests.

### Util.py
Some helper functions that avoid unecessary repetitive or long view functions. 'question_load_helper' ties the Question and Answers models together into one dictionary; 'reset_tool' helps keeping the positioning of a Tool's Questions tidy by making sure position numbers are consecutive, even after deleting a question.  

### Models.py
The data structure is built around three strictly related models: Tools, Questions and Answers. In addition, I've used Django's built-in User model for user management. These models allow users to build quiz-like structures. 
* The Tool model encompasses, among other things, an owner field that decides who gets to edit a tool, and a shorturl field that (together with the url.py file) makes sharing a tool a lot easier.
* The Question model has a 'position' integer field that allows users to modify order without touching the primary key, and a 'result' boolean field that marks a question as an end result in a tool, meaning it doesn't take answers and gets a different layout in the front-end. 
* The Answer field has a 'nextquestion' integer field, that allows users to add logic to their tool. 

### Forms.py 
As database manipulation is central to this app, so are the forms. I've used the forms in Forms.py for single-item entry and editing (e.g., a single question); I use JS for a more complex multi-answer form. I have customized the forms in a few ways: mainly to include important, non-modifialble info (such as foreignkey pk's) in hidden fields.  

### Templates
Most templates are quite sparse, as much of the rendering takes place using Javascript and Django forms (with the form_snippet included to keep things DRY). 

### Context_processor.py
I used a context processor to allow users to log in in from the navbar. 

### Styling & responsiveness
I used customized Bootstrap SCSS file to style the app and make it responsive. I have tested the app successfully on desktop, tablet and mobile.

### Extra module: Django_-_registration
I have used Django_registration for the user registration part of the website. Although it now uses one-step verification only, I like the fact that I can change it to automated two-step (email) verification in the future. I have already prepared the relevant files for such a modification (in django_registration/two-step) and tested it (sending the authentication code to the console instead of using an email server).

## Future development
Although I'm handing in this project now as I think it complies with all requirements, I will continue developing this project – or even redo it entirely leveraging the Django REST framework and React. This will allow me to improve functionality and usability even more. Thank you for your time and for an excellent course!

