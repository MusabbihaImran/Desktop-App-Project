# PixelAlchemy

A Python/Tkinter desktop art application designed for creating and experimenting with pixel-based artwork.

PixelAlchemy was developed as a university software engineering project and was built incrementally. The initial application focused on the core desktop experience, while additional functionality—including a Flask-based REST API for gallery data—was added later as an extension of the project.

## ✨ Features

* 🎨 Pixel-based drawing canvas
* 🖼️ Image filtering and processing
* 🎨 Color theory tools
* 🔷 Mathematical pattern generation
* 🗂️ Gallery for saved artwork
* 💾 SQLite database integration
* 🌐 Flask REST API for gallery data
* 🧪 Automated testing
* 📊 UML and software design documentation

## 🛠️ Technologies

* **Python**
* **Tkinter** — desktop graphical user interface
* **SQLite** — local data storage
* **Flask** — REST API microservice
* **unittest** — testing
* **PlantUML** — UML diagrams

## 📁 Project Structure

```text
Desktop-App-Project/
│
├── PixelAlchemy/
│   ├── modules/          # Application modules
│   ├── tests/            # Automated tests
│   └── ...               # Main desktop application
│
├── microservice/         # Flask REST API
├── saved_art/            # Saved artwork
├── UML diagrams/         # System design documentation
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## 🌐 REST API

The project was later extended with a Flask REST API to provide access to gallery data stored in the application's SQLite database.

The microservice provides functionality including:

* Gallery queries
* Filtering
* Statistics
* JSON export
* ZIP export
* Health checks
* Error handling and logging

Additional information about the microservice can be found in:

* `MICROSERVICE_BUILD_SUMMARY.md`
* `MICROSERVICE_QUICK_REFERENCE.md`

## 🧪 Testing

Testing was incorporated into the project to verify application functionality and individual components.

The repository includes automated tests and supporting testing utilities under the project's test directories.

## 📐 Software Design

UML diagrams and supporting documentation are included to describe the system's structure and behavior.

The repository contains:

* Use-case diagrams
* Class diagrams
* Activity diagrams
* Sequence diagrams

## 🚀 Running the Project

Clone the repository:

```bash
git clone https://github.com/MusabbihaImran/Desktop-App-Project.git
```

Navigate into the project:

```bash
cd Desktop-App-Project
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Then follow the project-specific deployment instructions in the `PixelAlchemy` directory.

## 🎓 Project Context

This project was developed as part of university coursework and evolved through multiple stages of development.

The initial focus was the desktop application, followed by additional work involving testing, software documentation, and a Flask-based microservice extension.

## 📌 Status

This is a completed university project maintained as part of my software development portfolio.

