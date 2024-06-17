# Dev Assessment - Webhook Receiver

### README Paragraph

This project is designed to test and demonstrate the webhook feature of GitHub. It listens to push, pull request, and merge events from a repository named `action-rope`, processes the incoming webhook data, and stores it in a remotely hosted MongoDB database. The entire workflow is managed and displayed using a Flask web application, which provides a user-friendly interface to view and analyze the recorded events in real-time. This setup offers a practical example of integrating GitHub webhooks with a backend service for efficient event tracking and management.
UI Implemented
![Screenshot from 2024-06-17 16-38-10](https://github.com/haleelsada/web-hook/assets/75977159/70a637e9-bda4-4cc5-8a8b-f47868f9f1a9)

*******************

## Setup

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at `app/extensions.py`)

*******************
