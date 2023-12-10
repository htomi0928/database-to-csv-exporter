# Database-to-CSV Exporter

A graphical application for exporting the content of MySQL database tables to CSV files.

## Features

- Connects to a MySQL database using configurations from a specified configuration file.
- Displays database tables in a table/grid format.
- First column is checkbox-enabled.
- Second column displays the database table names.
- Provides a "Save" button at the bottom of the window to export selected tables' content to CSV in the working directory.

## Requirements

- Python 3.9
- wxPython 4.2.1a

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/htomi0928/database-to-csv-exporter.git
    cd database-to-csv-exporter
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    python src/main.py
    ```

## Configuration

Edit the `config/db_config.ini` file with your MySQL database connection details.

## Usage

1. Launch the application using the provided instructions.
2. Select tables to export by checking the corresponding checkboxes.
3. Click the "Save" button to export the selected tables to CSV files in the working directory.

## Contributors

- Tamás Hollósi (tomi.hollosi@gmail.com)