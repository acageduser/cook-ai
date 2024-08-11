# Cook-AI

Create a recipe based on ONLY the ingredients inside your fridge! Skip the store and simply cook with this HTML Website + Flask Server Host + OpenAI API Integration.

# Key Skills Demonstrated

- Web Development: Developed a full-stack web application using Flask, showcasing proficiency in creating dynamic web pages and handling HTTP requests. Designed and implemented user-friendly and responsive web pages using HTML and CSS, ensuring compatibility across different browsers and devices. Utilized JavaScript for enhanced interactivity and functionality on the client side.
- API Integration: Integrated OpenAI's GPT models to generate recipe content dynamically, demonstrating the ability to work with external APIs and manage API requests effectively. Utilized the Requests library for seamless API communication, ensuring efficient data retrieval and handling.
- Data Management: Managed data storage and retrieval using JSON, demonstrating skills in data serialization and deserialization. Implemented file handling operations to read, write, and update JSON files, showcasing proficiency in managing data persistence in a web application.
- Error Handling and Debugging: Implemented error handling mechanisms to ensure the application gracefully handles unexpected scenarios and provides meaningful error messages to users. Set up detailed logging to track application behavior and debug issues effectively, demonstrating the ability to maintain and troubleshoot a complex codebase.
- User Interface and Experience: Ensured that the application is fully responsive, providing an optimal viewing experience across a wide range of devices. Ensured maintaining a 'clean' user interface with minimal noise to keep the user experience tidy.
- Version Control and Collaboration: Used Git for version control, maintaining a clean commit history and leveraging branches for feature development and bug fixes. Utilized GitHub for project collaboration, managing issues, pull requests, and project documentation effectively.
- Project Management: Created comprehensive project documentation, including setup instructions, usage guidelines, and key features, ensuring the project is easily understandable and maintainable. Managed project tasks efficiently, prioritizing features and bug fixes to meet project milestones and deadlines.
- Deployment and Hosting: Configured a local development server using Flask, demonstrating the ability to set up and manage development environments. Conducted extensive testing and debugging to ensure the application runs smoothly and efficiently in a local environment.

This project is intended for educational purposes only.
#
#


## CookAI Flask Application

This Flask application generates recipes in JSON format using OpenAI's GPT-4o-turbo.

#### Prerequisites

- [Python 3.7](https://www.python.org/downloads/release/python-3120/) or higher (Make sure Python is [added to your system's PATH](https://www.youtube.com/watch?v=iNoQeRj52zo&ab_channel=ChartExplorers))

- [pip](https://www.youtube.com/watch?v=fJKdIf11GcI&ab_channel=TheCodeCity)

## Installation

First, clone the repository to your local machine:

```
git clone https://github.com/acageduser/cook-ai.git
cd cook-ai
```

## Running the Application

#### Windows
To start the application on Windows, run the provided batch file:

```
start_local-windows_setup_and_server.bat
```

#### macOS and Linux
To start the application on macOS or Linux, run the provided shell script:

```
./start_local-macos-linux.sh
```

## Accessing the Application
Open ```start_local-windows_setup_and_server.bat``` (Windows) or ```start_local-mac.sh``` (mac/Linux). This is the local server. Once the local server is running, open your web browser and navigate to:

[```http://127.0.0.1:5000```](http://127.0.0.1:5000)
This will bring up the CookAI interface where you can generate recipes based on the ingredients you have.

#
# TO DO:
Task List for CookAI Fall 2024  
---------------------------------

1. Project Hosting:
   - The project is currently hosted locally.
   - Migrate hosting to Firebase, including both the site and database.
     - Firebase Hosting Documentation: https://firebase.google.com/docs/hosting
     - Firebase Database Documentation: https://firebase.google.com/docs/database
   
   How to Get Started:
   - Step 1: Sign up for a Firebase account at https://firebase.google.com/ if you don’t already have one.
   - Step 2: Create a new project in Firebase and set up the hosting by following the  Firebase Hosting Guide (https://firebase.google.com/docs/hosting).
   - Step 3: Follow the steps in the  Firebase Database Guide (https://firebase.google.com/docs/database) to set up your database.
   - Step 4: Deploy your local project to Firebase Hosting by using Firebase CLI tools.

2. Login Page:
   - Implement user login using Firebase Authentication, supporting only Gmail sign-ins.
     - Documentation: https://firebase.google.com/docs/auth
   - Design and develop a dedicated sign-in page.
   - Create a special admin account with free access to the web app.
   
   How to Get Started:
   - Step 1: Set up Firebase Authentication in your Firebase project by following the Authentication Guide (https://firebase.google.com/docs/auth).
   - Step 2: In your web app, use Firebase Authentication methods to implement Gmail sign-in.
   - Step 3: Design a simple login page using HTML/CSS and integrate it with the Firebase Auth API.
   - Step 4: In the Firebase Console, create a new user account for the admin, and assign the necessary permissions.

3. Register Page:
   - Allow users to register using their Gmail accounts.
   - Design and develop a dedicated sign-up page.
   
   How to Get Started:
   - Step 1: Utilize the Firebase Authentication API to implement Gmail-based registration.
   - Step 2: Design the sign-up page using HTML/CSS, similar to the login page.
   - Step 3: Integrate the sign-up form with Firebase, ensuring it connects to your Firebase project and stores user data securely.

4. Global Sign-In/Out:
   - Include sign-in and logout buttons on every page.
   - Implement session tracking to ensure users can’t access the site unless they are logged in.
   - Users can still access the landing page and sign in/sign up pages even when they're not logged in.
      - Update the landing page to direct the user to a log/sign up page.
   
   How to Get Started:
   - Step 1: In your main HTML/CSS layout, add sign-in and logout buttons that are available across all pages.
   - Step 2: Use Firebase Authentication to manage user sessions. Ensure that upon login, a session is created, and users are redirected to the appropriate page.
   - Step 3: Implement a check in your JavaScript code that verifies if a user session exists before granting access to any page.

5. API Key Security:
   - Ensure the API key is encrypted and securely stored in Firebase. The key should never be exposed on the client side.
     - Consider using this guide for implementation: https://chatgpt.com/share/d4ffce3d-e8f1-4681-b7c6-b4cc12075559
   
   How to Get Started:
   - Step 1: Learn about environment variables and secrets management in Firebase Functions.
   - Step 2: Store your API key in Firebase using Firebase Functions or Cloud Secrets Manager.
   - Step 3: Modify your API calls in the front end to retrieve the key securely from your backend, without exposing it on the client side.

6. Subscription Model Implementation:
   - Implement a subscription model using PayPal’s API.
     - Documentation: https://developer.paypal.com/api/rest/
   - Create a dedicated payment page for handling subscriptions.
   
   How to Get Started:
   - Step 1: Sign up for a PayPal Developer account and create a REST API app to obtain your API credentials.
   - Step 2: Use the PayPal API documentation to integrate subscription payment functionality into your web app.
   - Step 3: Design a payment page where users can manage their subscriptions. Implement this page to interact with the PayPal API to handle transactions.

7. Profile Page:
   - Develop a profile page where users can manage their subscriptions and delete their account.
   
   How to Get Started:
   - Step 1: Design the profile page using HTML/CSS, ensuring it fits with the rest of your site’s design.
   - Step 2: Implement functionality that allows users to view and manage their subscription status, using data stored in Firebase or retrieved from PayPal.
   - Step 3: Provide an option for users to delete their account, which should be handled securely through Firebase Authentication.

8. Advanced Syntax Checker:
   - Improve the functionality and accuracy of the advanced syntax checker.
   
   How to Get Started:
   - Step 1: Research common algorithms for syntax checking, particularly for the type of input your app will handle.
   - Step 2: Enhance the existing syntax checker code, or implement a new solution if necessary, by refining the rules and logic used.
   - Step 3: Test the syntax checker thoroughly with various inputs to ensure accuracy and reliability.

9. API Key Management:
   - Remove the ‘Input API Key’ fields from all pages and ensure the API key is fetched directly from the database.
   
   How to Get Started:
   - Step 1: Identify all instances in your codebase where the API key is being input by the user.
   - Step 2: Modify these sections to automatically retrieve the API key from the database or a secure backend service.
   - Step 3: Ensure this process is seamless and that the API key is never exposed to the client side.

10. Fridge Page UI Enhancement:
    - Update the buttons on the Fridge page to match the orange color scheme used throughout the site.
   
    How to Get Started:
    - Step 1: Identify the current styles applied to buttons on the Fridge page.
    - Step 2: Update the CSS styles to ensure the buttons use the same orange color as the rest of the site.
    - Step 3: Test the page to ensure visual consistency across all buttons and elements.

11. Remove AppleOS Script:
    - Eliminate the `.sh` file related to AppleOS. There’s no need to manage MacOS scripts for testing.

12. Expand "Specific Recipe" Section:
    - After generating a recipe using OpenAI's API, cross-reference the recipe's ingredients with the user's fridge.
    - Display a "shopping list" of items that the user does not have in their fridge.

    How to Get Started:
    - Step 1: Review the existing "Specific Recipe" section to understand how recipes are generated using OpenAI's API. (they're in haul/haul.json)
    - Step 2: Implement a function that compares the ingredients list from the generated recipe with the user's fridge contents (stored in a JSON-formatted list).
    - Step 3: Create a shopping list that includes any items from the recipe that the user does not have in their fridge.
    - Step 4: Display this shopping list to the user alongside the generated recipe, clearly indicating which ingredients they need to purchase.
    - Step 5: Test the functionality by generating various recipes and verifying that the shopping list accurately reflects missing items based on the fridge contents.

#
#

#
![image](https://github.com/user-attachments/assets/83203b34-a954-4010-9b11-0ab959d1b4f2)
