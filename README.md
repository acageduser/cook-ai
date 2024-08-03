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
![image](https://github.com/user-attachments/assets/83203b34-a954-4010-9b11-0ab959d1b4f2)
