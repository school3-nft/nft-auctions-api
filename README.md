# NFT Auctions API

Part of PZSP2 project - **'NFT Platform for School Auctions'**


## Getting started with Docker Compose

To start the application whith Docker Compose, you need to have Docker installed on your system. With Docker installed, you need to run:

```
docker compose up
```


## Getting started with Python

To start the application with Python, you need to first install packages from `requirements.txt':

```
python3 -m pip install -r requirements.txt
```

The, run the uvicorn server:

```
uvicorn app.main:app --reload
```
