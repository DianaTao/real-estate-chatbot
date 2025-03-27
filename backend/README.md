# Real Estate Chatbot Backend

This backend is a simple Flask application that uses the OpenAI API to provide real estate recommendations based on user prompts.
## Example Usage
Once the server is running, you can interact with the backend using tools like curl, Postman, or Axios in a frontend application.

Below is a curl example:

bash
Copy
Edit
curl -X POST http://127.0.0.1:5001/chat \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Find me a 2-bedroom apartment under $3000."
}'