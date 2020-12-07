# Regelhulpify

## What is Regelhulpify
The word 'Regelhulpify' is derived from the Dutch word 'rule aid', a tool that helps personalise laws, rules and guidelines. The Regelhulpify app allows anyone to make an account and start creating such a tool. In practice, a Regelhulp is a bit like a quiz, but without wrong or right answers: the logic one attaches to the answers makes sure the end user gets personalized information.

## How Regelhulpify was built
As per the requirements, I've built the app in a combination of Django and JavaScript, trying to explore as many functionalities as possible from both within the scope of the project.

### Models
The data structure is built around three strictly related models: Tools, Questions and Answers. In addition, I've used Django's built-in User model for user management. These models allow users to build quiz-like structures.

### Forms 
As database manipulation is central to this app, so are the forms. I've used the forms in Forms.py for single-item entry and editing (e.g., a single question); I use JS for a more complex multi-answer form.   

