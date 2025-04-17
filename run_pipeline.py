import schedule
import time
from clear_and_load import main as process_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def job():
    try:
        logger.info("Starting data processing job...")
        process_data()
        logger.info("Data processing completed successfully")
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")

def main():
    # Schedule job to run daily at midnight
    schedule.every().day.at("00:00").do(job)
    
    # Run job immediately on start
    logger.info("Running initial job...")
    job()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
