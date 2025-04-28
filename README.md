# mini-twitter
You are tasked with implementing a scalable REST API for a simple social media platform ("Mini-Twitter")

[TC.1] API Development:

        Use Python 3 and a Python web framework of your choice (Django REST Framework preferred).

        Implement the API following RESTful design principles.

🔐 [TC.2] Authentication:

        Use JWT (JSON Web Tokens) for user authentication and session management.

💽 [TC.3.1] Database:

        Use a relational database (preferably PostgreSQL).

        Ensure the database design follows best practices, with attention to normalization and performance optimization.

📄 [TC.4.] Pagination

        Implement pagination for the posts list

📂 [TC.8] Git

        Your project must be stored in a public git repository

        Failing this criteria will eliminate you immediately


ENDPOINTS

👨🏼‍🏫 USE CASES
CASE 1: User Registration

    Users should be able to sign up via the API by providing an email, username, and password.

    Use JWT to handle authentication for login and session management.

CASE 2: Post Creation

    Authenticated users can create a post with text and one image as content

    Posts can be liked by other users.

CASE 3: Follow/Unfollow User

    Users should be able to follow or unfollow others.

    The feed should only show posts from users the authenticated user follows.

CASE 4: Viewing Feed

    The user can view a paginated list of posts from the users they follow.

    Posts should be ordered by creation time, from most recent to oldest.