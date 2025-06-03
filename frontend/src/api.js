// src/api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/ask'; // FastAPI backend endpoint

// Function to ask a legal question
export const askQuestion = async (question) => {
  try {
    const response = await axios.post(
      API_URL,
      { question },
      {
        timeout: 15000, // 15 seconds timeout in case the API hangs
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    return response.data;
  } catch (error) {
    // Log the error in dev tools for debugging
    console.error('❌ API call failed:', error);

    // Return a friendly error message
    return {
      question,
      answer: '❌ Sorry, the server is not responding. Please check your backend or internet connection.',
      context: []
    };
  }
};
