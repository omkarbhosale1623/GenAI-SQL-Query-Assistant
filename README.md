# GenAI SQL Query Assistant

🧠 **GenAI SQL Query Assistant** is a Streamlit-based web application that enables natural language (NL) queries to be converted into SQL statements using a Generative AI model. It then executes these queries on your database and presents the results in an interactive dashboard.

## 🚀 Features

- **Natural Language Input**: Input queries in plain English (or other supported languages).
- **SQL Generation**: Utilizes a Generative AI model to convert NL queries into SQL.
- **Interactive Dashboard**: Displays query results with key metrics and visualizations.
- **Custom Visualizations**: Allows users to create personalized charts.
- **Speech Recognition**: Supports voice input for queries.

## 🔧 Technologies Used

- **Streamlit**: For building the web application.
- **SQLAlchemy**: For database interaction.
- **Plotly**: For data visualizations.
- **SpeechRecognition**: For voice input.
- **Pandas**: For data manipulation.

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.8+
- A database (e.g., PostgreSQL, MySQL)
- `DATABASE_URI` configured in a `config.py` file

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/omkarbhosale1623/genai-sql-query-assistant.git
   cd genai-sql-query-assistant
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configure your database URI in config.py:

python
Copy code
DATABASE_URI = 'your_database_uri_here'
Run the application:

bash
Copy code
streamlit run app.py
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request.

📞 Contact
For questions or feedback, please open an issue on the GitHub repository.
