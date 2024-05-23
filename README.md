# Data Testing Project for 'AdventureWorks' Database
The project goal is running great_expectations and perform basics profiling and verification of data from
"Adventureworks2012" database.

### Prerequisites
* Python 3.x
* MSSQL Server
* Required Python packages listed in requirements.txt

### Installation

1. Set up MSSQL "AdventureWorks2012" database locally
2. Create user in MSSQL to connect from Python
3. Install Microsoft ODBC driver for SQL
4. Clone the repository to your local machine

```
git clone
https://github.com/kate1503/GX_Test_Project.git
cd GX_Test_Project
```
5. Install necessary Python packages (listed in requirements.txt)
```
pip install -r requirements.txt
```

6. Create .env file in the root project directory with your MSSQL user credentials and server port
```
GX_Test_Project/
└── .env
...

USERID=your_user
PASSWORD=your_user_password
SERVER_PORT=your_server_port
```

### Running tests
To execute 
run gx_script.py