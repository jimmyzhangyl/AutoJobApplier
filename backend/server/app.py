from flask import Flask
from routes.job_routes import job_scraper_blueprint

app = Flask(__name__)
app.register_blueprint(job_scraper_blueprint, url_prefix="/scraper")

if __name__ == "__main__":
    app.run(debug=True)
