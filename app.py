from flask import Flask, jsonify
from scraper import run_harvester
import threading

# Initialize the Flask web application
app = Flask(__name__)

@app.route('/')
def home():
    """
    The default health-check route.
    Render uses this to verify the web service is alive and running.
    """
    return (
        "<h1>ALX Harvester Engine is Online 🟢</h1>"
        "<p>This service manages the background web scrapers for the Creative Economy Terminal.</p>"
        "<p>To manually trigger a data scrape, visit the <code>/run</code> endpoint.</p>"
    )

@app.route('/run')
def trigger_scrape():
    """
    The endpoint used to trigger the scraping logic.
    We use threading so the web server responds immediately while the scraper runs in the background.
    """
    # Initialize the background thread pointing to the run_harvester function
    thread = threading.Thread(target=run_harvester)
    
    # Start the background thread
    thread.start()
    
    # Return an immediate success message to the browser or Cron Job bot
    return jsonify({
        "status": "success", 
        "message": "Scraping protocol initiated in the background. Check your Render server logs for live updates."
    })

# Required for local testing. Render uses Gunicorn instead.
if __name__ == '__main__':
    # Runs the server locally on port 10000
    app.run(host='0.0.0.0', port=10000)