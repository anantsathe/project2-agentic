1) fastAPI app file : main.py
2) use following command to run fastAPI app on azure server:
   docker run --env-file .env -d -p 8000:8000 --name fastapi_container_6 anantsathe/tdsproject-2
3) .env is to export environment variables of github and openai_proxy key
4) url to interact from browser : http://4.240.110.230:8000/docs
