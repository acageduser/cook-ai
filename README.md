# Cook-AI

Create a recipe based on ONLY the ingredients inside your fridge! Skip the store and simply cook with this HTML Website + Flask Server Host + OpenAI API Integration.









#
# DEMO

## Sign in
<img width="2556" height="1369" alt="login1" src="https://github.com/user-attachments/assets/4737e319-6631-4e0a-b991-b8747fcf03da" />
To keep track of users and respect the safety of login information, we opted to use a fully Google-sided logon integration. Google handles the entire login process and only touches our database using an API call to create a user hash. This hash is stored in our database securely and is used to connect the user to their fridge. No emails or passwords are ever stored on our server.

Workflow: Sign on page -> connect to Google API sign in pop up -> user signs in -> user hash is generated and stored in our database to connect the user to their virtual fridge

## Upload Image to Populate Fridge
<img width="1278" height="685" alt="1111111111ezgif com-optimize" src="https://github.com/user-attachments/assets/de20c442-c061-4add-b0fc-48b2f4ca884c" />
Based on feedback we got, we knew many users had setup time issues the first time populating their virtual fridge with items. This process could take up to 5 minutes to complete and would often deter new users from using CookAI. To avoid users having to manually input all their ingredients, we added an AI vision option. Duplicate items are automatically filtered out as 1 item.

Simply upload an image of the inside of your real life refrigerator and let our service populate your entire fridge in mere seconds!

Workflow: Click on Choose File -> select your image -> wait ~3s to have your image processed -> OpenAI's API is called to process the image, and a .json is returned with the list of foods -> the .json is saved to our database and output to the Fridge webpage

## Edit Fridge
<img width="2556" height="1369" alt="fridge-management" src="https://github.com/user-attachments/assets/492e6c30-d022-4dce-a9a0-28b6c59053ec" />
Users might want to edit their virutal fridge list in certain cases, so we added 4 functions: ADD, EDIT, CLEAR, and DELETE. Each item in the fridge can be individually set to any food.

Workflow: <user \action> -> database updated according to action

## Generate Recipe (Recommended)

Generates a recipe based ONLY on the foods included in the user's virtual fridge. Make sure to populate the fridge first.
<img width="1278" height="685" alt="gen-recipe-recommended-mini" src="https://github.com/user-attachments/assets/b72fb9c6-6c82-4435-9247-d9254a38b5dc" />

Workflow: user's virtual fridge list sent via API call to OpenAI -> recipe recieved in a .json format -> recipe output

## Generate Recipe (Beta)
<img width="2556" height="1369" alt="gen-recipe-beta" src="https://github.com/user-attachments/assets/0604f0d0-2479-415e-9474-8ffee5379fbb" />
Generates a recipe based on the food inputted into the box. It will generate any recipe regardless of what the user has in their virtual fridge. This was used as a test feature in a v0 of CookAI and we decided to leave it in as a feature.

Workflow: user's input sent via API call to OpenAI -> recipe recieved in a .json format -> recipe output










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

# Installation

1. Download the latest 'cookai.exe' file and double click. Find the .exe file in the '[Releases](https://github.com/acageduser/cook-ai/releases)' section on the right.

## CookAI Flask Application

This Flask application generates recipes in JSON format using OpenAI's GPT-4o-turbo.

#### Prerequisites

- None. Everything is within the website version and executable version (.exe)

## Running the Application
- Run ```cookai.exe``` within a folder of your choice. Note: It is a good idea to download the ```.exe``` in its own folder because it will create sub folders located where the app is run from.

