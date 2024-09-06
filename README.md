
# AI-Powered Comedy Show Generator


https://github.com/user-attachments/assets/98587006-db8f-4a6c-9176-2d2ee4c6f633


This project combines a React frontend with a Python backend to create an AI-powered comedy show generator. It uses OpenAI's GPT and DALL-E models to generate jokes, images, and videos based on user input.

## Project Structure

- `frontend/`: React application
- `backend/`: Python backend server

## Features

- Generate jokes using AI
- Create images and videos based on generated content
- User-friendly chat interface
- Video generation with text-to-speech and image synthesis

## Prerequisites

- Node.js and npm
- Python 3.7+
- OpenAI API key

## Setup

### Frontend

1. Navigate to the `frontend` directory
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```

The React app will be available at `http://localhost:3000`.

### Backend

1. Navigate to the `backend` directory
2. Create a virtual environment:
   ```
   python -m venv env
   ```
3. Activate the virtual environment:
   - On Windows: `env\Scripts\activate`
   - On macOS and Linux: `source env/bin/activate`
4. Install dependencies (requirements.txt file needed)
5. Set up your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
6. Start the backend server (command needed)

## Usage

1. Open the frontend application in your web browser
2. Enter a prompt or select a joke type
3. The AI will generate jokes and optionally create images and videos
4. You can view the generated content and interact with the chat interface

## Technologies Used

- Frontend:
  - React
  - Tailwind CSS
- Backend:
  - Python
  - OpenAI API (GPT and DALL-E)
  - MoviePy for video generation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
