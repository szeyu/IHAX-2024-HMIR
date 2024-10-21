# Hackathon Project for IHAX2024

## Pitch Deck
[Canva | HMIR Scholar Pitch Deck](https://www.canva.com/design/DAGT_B_Hd90/CatUwwum7jXPZKmK2iylng/view?utm_content=DAGT_B_Hd90&utm_campaign=designshare&utm_medium=link&utm_source=editor)


# Project Setup

Follow these steps to set up the project.

## 1. Clone the Github Repo
Navigate to the directory you want to clone the repo into and execute:

```
git clone https://github.com/szeyu/IHAX-2024-HMIR

```

## 2. Create a New Conda Environment

Create a new Conda environment with Python 3.12 by running the following command:

```
conda create --name myenv python=3.12
```

## 3. Install Necessary Dependencies in requirements.txt
Activate your conda environment and install necessary dependencies:
```
conda activate myenv
pip install -r requirements.txt
```

## 4. Put your Open AI keys to your `.env` File
```
OPENAI_API_KEY=<KEY>
```

## 5. Run the Streamlit App
```
streamlit run app.py
```
