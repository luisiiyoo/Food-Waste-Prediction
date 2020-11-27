Food Waste Prediction
===================
> TODO: Add a description about the project

![Pipeline](pipeline.png)

Project layout
--------------
This directory contains all backend related artifacts. The directory structure is intended to separate concerns as follows:

    .
    ├── App                         # All the source code goes here
        ├── Controllers             # All the endpoints defined goes here
        ├── Database    `           # Data layer access is handled by this module
        ├── Models                  # Models for the database
        ├── Server                  # All the services used to make predictions (see the above image)
            ├── DatasetCreation     # Dataset logic module
            ├── Preprocessing       # Preprocessing data logic module
        ├── Util                    # Auxiliary functions and constants goes here
    ├── config                      # Configuration files for mongo, uploading files, etc. goes here
    ├── sample_data                 # Temporary folder containing raw sample data
        ├── menus                   # Raw menus data
        ├── registers               # Raw registers data
    ├── temp                        # Temporary uploaded files goes here (like sample-data)
 
Installation
--------------

Install [pipenv] and clone the repository on your local computer
```bash
git clone <git_url_project>
cd FoodWastePrediction
```

Run the next command to install all the project dependencies:
```bash
pipenv install
```

Finally, use the next command to run the service:
```bash
python3 main_app.py
```

Uploading data (optional)
--------------
In order to feed the dataset (if it is empty) is required to run the next script to upload all the sample data
```bash
python3 upload_sample_data.py
```
 
<!-- References -->

[pipenv]:        https://pypi.org/project/pipenv/
