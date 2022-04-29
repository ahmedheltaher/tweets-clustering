# tweets-clustering

A Simple clustering application created for FCIS-ASU Artificial Intelligence course in Spring of 2022

### The Flow of the Application

is explained here [Flow](./FLOW.md)

## Getting Started

Clone the project

```bash
 git clone https://github.com/ahmedheltaher/tweets-clustering.git
```

Go to the project directory

```bash
 cd tweets-clustering
```

Now You Have To setup the virtual env (You need Python to be installed)

```bash
 pip install virtualenv
```

Initialize the virtual env (you can call `tweets-clustering-env` what ever you want)

```bash
 virtualenv tweets-clustering-env
```

Run the virtual env

```bash
 source tweets-clustering-env/venv/bin/activate
```

Now Install the requirements for the project

```bash
 pip -r requirements.txt
```

## Before You Commit

Before everting make sure you are in the virtual env so the requirements file will be formed from only the truly need libs

then update requirements file if updated using this command:

``` bash
 pip freeze > requirements.txt
```

Then commit as you do usually

```bash
 git add.
 git commit -m "Your Commit Message"
 git push origin master
```
