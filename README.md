Change the current working directory to the location where you want the cloned repository.
1. Open Terminal
2. Type mkdir my_fastapi_project
3. Type cd my_fastapi_project
To clone the repository:
4. Type git clone git@github.com:ramona-2020/addressesFastAPI.git
5. Press Enter to create your local clone.
6. Type cd addressesFastAPI
7. Create the virtual environment, run the command below (based on Ubuntu)
python3 -m venv venv
source venv/bin/activate
8. Install all the modules required for the project by running:
pip install -r requirements.txt
9. Run this command to start the FastAPI HTTP server with Uvicorn.
uvicorn main:app --host localhost --port 8000 --reload

![terminal](https://i.ibb.co/mJb90Hm/terminal.png)

Actions:
Once the FastAPI server is listening on port 8000, open a new tab in your browser and visit http://localhost:8000/ to see the JSON object sent by the server.
Open http://localhost:8000/docs to see and use all provided Addresses API routes.
(or use Postman to execute the requests)


![docs](https://i.ibb.co/yFqxcxy/docs.png)
