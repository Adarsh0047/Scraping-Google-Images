# Scraping-Google-Images
<<<<<<< HEAD
This repo contains the python script to scrape from google images given any search keyword
=======

## About
This repo contains the python script to scrape from google images given any search keyword

Under Construction

## TODO Timeline

* Fix code and make the code work - July 23, 2023 ✅
* Get the query from user input with any search keyword - July 25, 2023 ✅
* Do not download duplicates - July 27, 2023 ✅
* Store the downloaded images in specific Query folders - July 29, 2023 ✅


## Modules Used
Modules and tools used in this project:

* `bs4`
* `selenium`
* `webdriver_manager`

## Project Installation
Poetry is used for environment and module mangement in this project.
Install poetry and set it as a path variable.

For more details on how to install poetry visit this page:
[Install and setup Poetry](https://python-poetry.org/docs/)

To install all the requirements for this project, run the following commands:

* `poetry shell` in the directory of the projecy to activate poetry
* `poetry install` to install all the dependencies

**Note**:All the dependencies required for this project is present inside the `poetry.lock` and `pyproject.toml` files.

## Running the project

To run the script type in the following in the terminal:
* `poetry shell` in the directory of the projecy to activate poetry
* `python scraping.py` in the terminal.

### Parameters used in the script
The script takes in three parameters:

* Number of images
* What images to download
* Ready to download or not as a user input.This is done so that the user may scroll down in the window till the bottom of the page so that the dynamic loading of all images would occur.
