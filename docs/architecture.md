# Architecture

### Chosen Architecture and Technologies

As part of this project, I've decided on a development setup that emphasizes speed, simplicity, and efficiency, perfectly aligning with the project's scope and size. Here's an overview of my chosen architecture, technologies, and workflow:

- **Monolithic Architecture**: I've opted for a monolithic architecture because it suits the smaller scale of this project. This approach simplifies development, testing, and deployment processes, making it ideal for a single, unified codebase.
- **SQLite Database**: For database management, I'm using SQLite. It's a lightweight, file-based database that's easy to integrate with Python. This choice minimizes setup complexities and eliminates the need for a separate database server.
- **No Docker**: Given the project's focus on simplicity and quick setup, I have decided not to use Docker. This reduces the complexity and resource requirements, allowing me to concentrate on the core functionalities of the application.

### Development and Operation Workflow

1. **Environment Management**:
    - I am utilizing `pipenv` for creating a virtual environment and managing dependencies. The use of `Pipfile` and `Pipfile.lock` ensures that everyone working on the project has consistent dependency versions.
2. **FastAPI Webserver**:
    - My API is developed using FastAPI, a modern, high-performance web framework for Python. Its simplicity and speed make it an excellent choice for this project.
3. **Testing**:
    - I am writing both unit and integration tests for the application. These tests can be executed easily through commands defined in the `Pipfile` scripts section or via a separate script file.
4. **Database Integration**:
    - The integration of SQLite directly into the application allows for easy management of the database. The setup for database initialization and schema is managed through Python scripts.
5. **Version Control**:
    - I'm using Git for version control to effectively track and manage code changes throughout the development stages.
6. **Documentation**:
    - I have included a `README.md` file in the project, providing clear instructions for setting up the environment, running the server, and executing tests.

### Summary

My project setup is intentionally streamlined for ease of development and use, focusing on showcasing my software engineering skills without overcomplicating the solution. The combination of FastAPI and SQLite, managed within a Python environment using `pipenv`, strikes a balance between employing modern software practices and maintaining the simplicity needed for a project of this scale.

In making these decisions, I've demonstrated an ability to select appropriate tools and frameworks that align with the project's requirements, a crucial skill in software development. While Docker is not utilized in this project, my decision-making process and the reasons behind it are integral to demonstrating sound software engineering judgment.