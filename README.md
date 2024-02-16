# Chatbot

### Description:
An NLP project for learning purposes. The aim is to have a chatbot that can answer questions about me and my schooling or the subjects of my school essays in a comprehensive, understandable manner. For this purpose the final goal is to have a conversational model that draws from the essay database, a conversational database, and a database which it populates itself with its conversations.

### Status:
Currently, I've spent the last couple of weeks compiling a database of all of my school essays, with titles, years, (processed) content, full_text, summary, and keywords. Now the next step is to download and assess the usability of various conversational datasets on the internet.

However, the essay database is completely finished, and most of the supporting files are finished.

### Use and Usability:
The model itself isn't usable, however the web interface is in its alpha version and does also answer with predetermined answers when it detects certain keywords.

As for file_setup and database access, except for the 'maintain.py' file, all the files are up and running as are their corresponding tests.

#### Configurability:
Most of the database files were not designed with generalization to other databases in mind, so the only truly configurable part of this is the config.py, where you can change the various path variables to the proper directories.