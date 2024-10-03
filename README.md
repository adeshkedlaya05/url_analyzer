# Safe Url Analyzer
## Malicious URL Detection with Machine Learning

## Objective:
This project aims to create a user-friendly web application that leverages a machine-learning model to detect malicious URLs. 
The application will allow users to input URLs, view the AI-generated probability of the URL being malicious or Safe. 

Phishing attacks pose a significant cybersecurity threat, often employing deceptive URLs to trick users. 
While machine learning models can effectively identify url patterns. 
This project addresses the challenge of creating an interactive application that combines AI-driven analysis with user input to improve malicious url detection rates.

## 1.Dataset Utilization:
○ Utilized the   https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset  Dataset, which contains various URL features.

○ Cleaned and preprocessed the dataset to handle missing values, outliers, and feature encoding.

## 2.Feature Engineering:
○ Enhanced the dataset by engineering additional features that could improve the model’s accuracy. 

## 3.Model Development:
○ implemented XGBoost Model to train and implement the machine learning model.

## 4.Web Application:
○ A user-friendly and visually appealing web application with a clear input field for URLs.
Real-time display of the AI-generated probability. A database to store all the userdata,urls and its result and also the display the urls,and its results

## 5.Results of the Model:
The model's performance on the test dataset is summarized below:

- **Accuracy**: 94.81%
- **Precision**: 95.21%
- **Recall**: 88.86%
- **F1-Score**: 91.92%

## Graph for comparing actual and predicted values

<img src=https://github.com/user-attachments/assets/679bb067-4f9e-4455-b7fc-2a8d2ae79b28 width="500"/>


 ## Technologies Used

| Technology         | Description                                   |
|--------------------|-----------------------------------------------|
| HTML               | Markup language for creating web pages       |
| CSS                | Stylesheet language for styling web pages     |
| JavaScript         | Programming language for client-side scripting|
| Django             | High-level web framework for Python           |
| Python             | Programming language used for backend logic   |
| XGBoost            | Machine learning library for model training   |
| Pandas             | Data manipulation and analysis library        |
| scikit-learn       | Machine learning library for evaluation       |

## Clone the Repository

You can clone this repository using the following command:

```bash
git clone https://github.com/adeshkedlaya05/url_analyzer
```


### Key Points

- **Clear Steps**: Provide step-by-step instructions so that users can easily follow along.
- **Clone Command**: Make sure to include the correct clone command for your repository.
- **Virtual Environment**: It’s a good practice to encourage the use of virtual environments to avoid conflicts with other projects.
- **Installation Command**: Use `pip install -r requirements.txt` command to install dependencies required for this project .
- **Perform Migrations**: Run this command to create new migration files based on the changes made to your models.`python manage.py makemigrations` and run this command to apply the created migrations to the database.`python manage.py migrate`
- **Run the application**: Run the application using `python manage.py runserver` command .



# Sample Images of the Project
## 1.Login Page
![Screenshot 2024-10-02 221140](https://github.com/user-attachments/assets/073f4dd4-f20f-41de-b281-6dd92c71ed87)

## 2.Signup Page
![Screenshot 2024-10-02 221150](https://github.com/user-attachments/assets/b87378fa-9913-4728-b99b-24b9656333f2)

## 3.forgot password
![Screenshot 2024-10-02 221200](https://github.com/user-attachments/assets/056159d7-365a-4e90-887f-b35f963638f8)

## 4.Dashboard
![Screenshot 2024-10-02 221214](https://github.com/user-attachments/assets/f213fdde-9ddb-4439-a656-094064b69d46)

## 5.Results
![Screenshot 2024-10-02 221227](https://github.com/user-attachments/assets/c5050378-c2cb-41e2-b007-386ac363758b) 


![Screenshot 2024-10-02 221236](https://github.com/user-attachments/assets/a5a39895-b307-4893-8bc3-f6cf2ebeec4f)


![Screenshot 2024-10-02 221249](https://github.com/user-attachments/assets/08397702-614a-4634-989c-0de944694634)









