# vibraniumdome-streamlit-app demo

## Run locally
```
pip3 install streamlit openai==0.28.1 vibraniumdome-sdk 
streamlit run streamlit_app.py
```

## Run with docker
```
docker build -t vibraniumdome-streamlit-app .
docker run -it -p 8501:8501 vibraniumdome-streamlit-app
open http://localhost:8501
```