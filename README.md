# Nucleus

This is the repository of team Hooli, composed of Yiming Sun (ys3031), Minghao Li (ml4025), Yihan Lin (yl3820) and Yihao Li (yl3744).

Nucleus is a question-answering AI. Tell Nucleus a passage and some related questions, and you will get an answer shortly.

So far, an MVP is implemented. We trained a neural network, and it is able to be called through terminal. In the future, we are planning to do more things - deploying Nucleus onto RESTful APIs of AWS is one of them.

## Get Started

Before you start, remember to create a python 3.6 virtual environment. we recommend `virtualenv`. Then install all the packages inside `requirements.txt`.

## Usage
Run the following command at root directory, and you will see the result of Nucleus on some testcases stored in `testcases` folder.

```angular2html
python models/r_net/inference.py
```

You can also customize the questions and passage, of course. You may provide a text file like this:

```angular2html
Columbia University is established in 1754. Columbia University belongs to the Ivy League and is in the New York City. Lots of famous scientists and politicians graduated from Culumbia University.
```

and several questions like this:

```angular2html
Where is Columbia University?
Where does scientists and politicians come from?
When is Columbia University established?
```

put the context to `<root>/context.txt` and the question to `<root>/questions.txt`, then run the following command:

```angular2html
python models/r_net/inference.py --inference_mode customized --context_path <root>/context.txt --questions_path <root>/questions.txt
```



