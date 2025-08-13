const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class APIService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async askQuestion(question, language = 'en') {
    try {
      const response = await fetch(`${this.baseURL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          language
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  async getHealth() {
    try {
      const response = await fetch(`${this.baseURL}/health`);
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      return { status: 'error' };
    }
  }

  async getCategories() {
    try {
      const response = await fetch(`${this.baseURL}/categories`);
      return await response.json();
    } catch (error) {
      console.error('Categories fetch failed:', error);
      return { categories: [] };
    }
  }

  async getFreeServices() {
    try {
      const response = await fetch(`${this.baseURL}/free-services`);
      return await response.json();
    } catch (error) {
      console.error('Free services fetch failed:', error);
      return {};
    }
  }

  async sendSMS(phoneNumber, message) {
    try {
      const response = await fetch(`${this.baseURL}/sms/send?phone_number=${encodeURIComponent(phoneNumber)}&message=${encodeURIComponent(message)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      return await response.json();
    } catch (error) {
      console.error('SMS send failed:', error);
      throw error;
    }
  }
}

export const apiService = new APIService();