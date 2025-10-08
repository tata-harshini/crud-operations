## AWS Lambda CRUD Integration with DynamoDB & API Gateway

# Task Overview
A serverless employee management system built using AWS Lambda, API Gateway, and DynamoDB to perform full CRUD operations(Create, Read, Update, Delete). This setup allows you to manage employee records using a single API endpoint.

# Technologies Used
- AWS Lambda
- AWS DynamoDB
- AWS API Gateway
- Python (boto3)

# Features
- Add new employee records (POST)
- Retrieve all or specific employee records (GET)
- Update existing records (PUT)
- Delete specific employee records (DELETE)

# 💡 Key Learnings
- Building serverless backends on AWS  
- Integrating Lambda with DynamoDB  
- Using ExpressionAttributeNames for reserved keywords  
- Managing IAM permissions securely  
- Debugging and monitoring with CloudWatch  

## ▶️ How to Deploy
1. Create a DynamoDB table named **Employees** with `id` as the Partition key.
2. Create a Lambda function and upload this `lambda_function.py` file.
3. Attach an IAM role with full DynamoDB access.
4. Integrate the Lambda function with **API Gateway** and enable all methods (GET, POST, PUT, DELETE).
5. Test using **Postman** or API Gateway console.


