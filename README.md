# NewsGate
# API Gateway with JWT Authentication

This project implements an API Gateway that uses JSON Web Tokens (JWT) for secure authentication and role-based access control. The gateway acts as a centralized entry point for multiple APIs, ensuring that only authenticated and authorized users can access specific resources.

Key Features:
JWT-based Authentication: Users log in with a username and password to obtain a JWT, which is then used to access protected endpoints.
Role-based Access Control (RBAC): Depending on the user's role (Admin, Premium User, or Regular User), the API Gateway routes requests to different endpoints: /news/admin, /news/premium, and /news/user.

Frontend: Built using Streamlit, the frontend provides a login page where users authenticate, and based on their role, they can access and view relevant news content retrieved via API calls.

Secure API Access: Ensures that only valid tokens can access the API, adding an extra layer of security to prevent unauthorized access.

This project demonstrates how to integrate JWT authentication in a microservice architecture, providing a secure way to manage and control API access. It also features a dashboard for Admin users to perform sentiment analysis and filter news based on categories such as crime, violence, and disaster, providing a clear and user-friendly interface.
