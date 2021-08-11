# JHAKAAS - A Python BaaS

## Run Instructions

#### A. MongoDB Database

1. Navigate to the root directory (where the three directories backend, database and frontend are present) or start your existing MongoDB server
2. Start MongoDB server

```bash
mongod --dbpath=database
```

3. The MongoDB server will be hosted at its default port 27017

#### B. Python/FastAPI Backend

1. Navigate into /backend directory (where main.py is present)
2. Activate the virtual environment

```bash
pipenv shell
```

3. Install dependencies, if not already done

```bash
pipenv install
```

4. Start FastAPI server

```bash
uvicorn main:app --reload
```

5. The FastAPI server will be hosted at its default port 8000
6. To access SwaggerUI for API testing and documentation, goto [http://localhost:8000/docs](http://localhost:8000/docs)

#### C. React Frontend

1. Navigate to /frontend directory (where package.json is present)
2. Install dependencies, if not already done

```bash
npm install
```

3. Start React Web Application

```bash
npm start
```

4. The React web application will be hosted at its default port 3000, goto [http://localhost:3000/](http://localhost:3000/)
