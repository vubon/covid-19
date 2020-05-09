import environ
# Read environment variables
env = environ.Env(
    MAIL_LIST=(list),
)
environ.Env.read_env()

MAIL_LIST = env("MAIL_LIST")
SENDGRID_API_KEY = env("SENDGRID_API_KEY")
TEMPLATE_ID = env("TEMPLATE_ID")
API_HOST = env("API_HOST")
