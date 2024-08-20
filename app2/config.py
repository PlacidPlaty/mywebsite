from pydantic_settings import BaseSettings
'''
Provide a list of all the environment variables you need set
This is useful if you want your application to not crash when variables like database username/password change.
This performs validation to ensure that everything has been set during application start up.
Variables are not case sensitive. 
If variables are not provided with default value and value is not provided in Environment variables, ERROR WILL BE THROWN

'''
class Settings(BaseSettings):
    # Environment variables are read as strings
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    # tell pydantic to import from the .env file
    class Config:
        env_file = ".env"
# Store the class Settings in variable called settings
settings = Settings()