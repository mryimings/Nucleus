# Nucleus

This is the repository of team Hooli, composed of Yiming Sun (ys3031), Minghao Li (ml4025), Yihan Lin (yl3820) and Yihao Li (yl3744).

Nucleus is a question-answering AI. Tell Nucleus a passage and some related questions, and you will get an answer shortly.

The key part of Nucleus is BERT, a fast and accurate deep neural network that could answer you question, if you simply provide a question and a related context.

Now, Nucleus has two different mode: context-related and context-free. In context-related mode, things go easier with the help of BERT. you provide a context to Nucleus and a question based on this context. Nucleus will tell you the answer of it.

In context-free mode, things become more interesting. At the very beginning we only planned the context-related mode. After we finished it, however, we decided to challenge ourselves, and here it comes the context-free mode.

In context-free mode, you don't need to provide a context, we do this for you - we use abundant wikipedia API to search the most possible page that may contain answer. Calling multiple APIs including Wikipedia API, rake_nltk, etc.


  
## Get Started

Before you start, remember to create a python 3.6 virtual environment. we recommend `virtualenv`. Then install all the packages inside `requirements.txt` by doing:

```angular2html
pip install -r requirements.txt
```

Before you fully launch Nucleus, you need two more things:

### Config AWS

you need to config six AWS credentials, and put them in a file named `config.py` at root directory

```angular2html
cognito_userpool_id = <your_userpool_id>
cognito_app_client_id = <your_config_id>
database_user_name = <your_database_username>
database_endpoint = <your_database_endpoint>
port = <your_endpoint_number>
database_pwd = <your_database_password>
```

### Find model

Download the model via `https://1drv.ms/f/s!AtfKeiTxgnoqjt0M3lrLoowcsjbKcA`, name the whole dir as `model_data`, and put it to `<root>/models/bert`

### Launch Nucleus

To launch Nucleus, simply run:

```angular2html
python application.py
```

then open your browser and visit `http://127.0.0.1:5000`. Please make sure you are not running any other web app on port 5000.

# Required packages:

```angular2html
pre-commit
spacy
tensorflow
tqdm
ujson
flask
warrant
wikipedia
nltk
rake-nltk
mysql-connector-python
```

## CI Configurations and Test Results 

All the results, and files required by the professor, including pre-commit and post-commit config, unit test reports, bug-finder reports, are in the `result` folder. **These files should be read only**

## Implementation Detail

The basic workflow of our context-free mode is:

1. a user submits a question at the frontend;
2. Nucleus' backend extract keywords from the question, with rake_nltk API;
3. these keywords are send to wikipedia API, which returns the pages of these keywords;
4. we split these pages into a list of paragraphs, each of which is about 700 characters long;
5. we put the list of paragraphs as contexts and the question into BERT model, and the model returns an answer and a confidence for each of question-context pair;
6. we select the answer with the best confidence, and return it to the user.
