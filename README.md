# Django Admin Panel for Task Automation

This repository contains a Django-based admin panel designed to streamline several key tasks, including importing and exporting table data, sending bulk emails, processing email metrics, and compressing images. It also includes user authentication and utilizes Celery with Redis for handling massive background tasks efficiently.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

1. **Table Management**
   - Import data into tables from Django models.
   - Export data from tables for external use.

2. **Email Management**
   - Send bulk emails efficiently.
   - Track email metrics, including open rates and click-through rates.

3. **Image Compression**
   - Compress images to reduce storage and bandwidth usage.

4. **Authentication**
   - Secure login and user management.

5. **Background Task Processing**
   - Uses Celery with Redis to manage and execute large-scale tasks in the background.

## Installation

### Prerequisites

- Python 3.x
- Django
- Redis
- Celery

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/MAQilH/Boring-Stuff.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Boring-Stuff
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: You will need to manually create a `requirements.txt` file with the dependencies used in your project.*

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the Redis server:
   ```bash
   redis-server
   ```

6. Start the Celery worker for background tasks:
   ```bash
   celery -A Boring-Stuff worker --loglevel=info
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Access the admin panel by navigating to `http://127.0.0.1:8000/admin/` in your web browser.
2. Use the features provided in the dashboard for managing data, emails, and images.

## Project Structure

```plaintext
Boring-Stuff/
├── .idea/
├── Datasets/
├── __MACOSX/Datasets/
├── awd_main/
├── dashboard/
├── dataentry/
├── emails/
├── image_compression/
├── static/
├── templates/
├── uploads/
├── .gitignore
├── README.md
├── dump.rdb
├── manage.py
├── test.py
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear and descriptive messages.
4. Push your changes to your fork.
5. Open a pull request to the main repository.

## License

This project is licensed under the [MIT License](./LICENSE).

---

Thank you for using the Django Admin Panel for Task Automation. Your feedback and suggestions are greatly appreciated!

