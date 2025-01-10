### MOVIE SEARCH TELEGRAM BOT
#### Creat by Volodymyr Mutaf --> https://www.linkedin.com/in/volodymyr-mutaf-6566a431a/

**Local launch:**:
1. Make a local copy of the repository. In the console, select the directory where the project repository will be cloned.\
Enter the command in the console -> `git clone git@github.com:Mutaf-Volodymyr/movie_tgb.git`
2. You must have Python 3.12
3. Create environment `python3 -m venv .venv` and `source .venv/bin/activate`

4. You must have next moduls  
   * `SQLAlchemy==2.0.36`
   * `python-dotenv==1.0.1`
   * `telebot==0.0.5`
   For it enter the command in the console -> `pip install -r requirements.txt`
5. Create a `.env` file in the root of your project, for example:
   ```
    host=***********************
    user=***********************
    password=*******************
    database=*******************
    token=**********************
   ```

> Attention. Before using SHOW POPULAR, go through all other scenarios, because the application complains, on an empty base.