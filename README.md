
# Weather Data Analytics Documentation

This project provides a RESTful API for retrieving weather data and weather statistics for different weather stations. It includes functionality for querying weather data by station ID and date, as well as weather statistics for a specific station and year. The data is ingested from external weather files and stored in a database for easy querying.

## Features

- **Weather Data Retrieval**: Retrieve weather data for a given station and date.
- **Weather Statistics**: Retrieve weather statistics such as average maximum temperature, average minimum temperature, and total precipitation for a given station and year.
- **Pagination**: Supports pagination for large datasets.
- **Data Ingestion**: Ingest weather data files (e.g., `.txt` files) into the database, ensuring no duplicate records are inserted.

## Requirements

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- Flask-RESTX
- Pandas
- SQLAlchemy
- dotenv
- PostgreSQL (For the database)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repository/weather-data-analytics.git
cd weather-data-analytics
```

### 2. Install Dependencies

Create a virtual environment and install the required dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file at the root of the project and add the following environment variables:

```env
DATABASE_URL=your_database_connection_url
```

Replace `your_database_connection_url` with the actual database URL for your project (e.g., PostgreSQL).

### 4. Running the Application

To start the Flask application, run:

```bash
python3 run.py
```

This will start the API server, and you can access the documentation via `http://127.0.0.1:5000/swagger/`.

### 6. Data Ingestion

To ingest weather data from files, you can use the `WeatherDataIngestor` class. This can be done by running the `weather_data_ingestion.py` script, passing the database URL and table name as arguments.

Example:

```python
from weather_data_ingestion import WeatherDataIngestor

db_url = 'your_database_connection_url'
table_name = 'weather'

ingestor = WeatherDataIngestor(db_url, table_name)
ingestor.read_weather_file('path_to_file.txt')
```

### 7. API Endpoints

The API provides the following endpoints:

#### **Weather Data**

- **GET /api/weather**
  
  Retrieves weather data for a specific station and date with pagination.
  
  **Query Parameters**:
  - `station_id`: The ID of the weather station (required).
  - `date`: The date in `YYYY-MM-DD` format (optional).
  - `page`: The page number for pagination (optional, default is 1).

#### **Weather Statistics**

- **GET /api/weather/stats**
  
  Retrieves weather statistics for a specific station and year with pagination.
  
  **Query Parameters**:
  - `station_id`: The ID of the weather station (required).
  - `year`: The year for which to retrieve statistics (required).
  - `page`: The page number for pagination (optional, default is 1).

### 8. Running the Application with Swagger

    Swagger UI: The API documentation is automatically generated and can be accessed via http://localhost:5000/swagger.
    This UI allows you to interact with the API and test the available endpoints directly.

## Database Models

- **Weather**: Represents daily weather data for a station (temperature, precipitation, etc.).
- **WeatherStats**: Represents weather statistics (average temperature, total precipitation) for a specific station and year.

## Data File Ingestion

Weather data files (e.g., `.txt` files) are processed and ingested into the database using the `WeatherDataIngestor` class. This ensures that duplicate records are not added to the database based on `station_id` and `date`.

## Deployment Considerations

For production deployment, consider using the following:

- **Database**: Amazon RDS for PostgreSQL for scalability and reliability.
- **API Hosting**: AWS Elastic Beanstalk, AWS Lambda, or Heroku for hosting the Flask application.
- **Containerization**: Use Docker for containerizing the application for portability with AWS EKS (Elastic Kubernetes Service),AWS Fargate (serverless container management) or AWS ECS (Elastic Container Service) might be the best option..
- **Continuous Integration/Continuous Deployment (CI/CD)**: Implement CI/CD pipelines using tools like GitHub Actions, CircleCI, or Jenkins.
- **Monitoring & Logging**: Use AWS CloudWatch for centralized logging and monitoring of your application’s health and performance.

## Extra Features and Enhancements

- **Data Ingestion Scheduling**: You can schedule the data ingestion process using AWS Lambda and CloudWatch for periodic execution.
- **API Rate Limiting**: Implement rate limiting in the API to prevent abuse using Flask-Limiter or similar packages.
- **Authentication**: Add authentication (e.g., API key or JWT) to secure the API.
