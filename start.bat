docker build -t curr .
docker run -p 8001:80 --name currency curr

pytest -s -v app/tests/*
