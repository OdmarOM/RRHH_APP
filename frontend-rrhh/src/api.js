import axios from 'axios';

// Creamos una instancia configurada para apuntar siempre a tu backend en Python
export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});