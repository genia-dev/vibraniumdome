# vibraniumdome-streamlit-app demo

## Run locally
```
pip3 install virtualenv
python3 -m venv ~/.venv
source ~/.venv/bin/activate
pip3 install vibraniumdome-sdk openai==0.28.1 streamlit termcolor bs4
streamlit run streamlit_app.py
```

## Run with docker
```
docker build -t vibraniumdome-streamlit-app .
docker run -it -p 8501:8501 vibraniumdome-streamlit-app
open http://localhost:8501
```
