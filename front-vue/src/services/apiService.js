import axios from 'axios';

// Utiliser le proxy local au lieu de l'URL directe
const API_URL = import.meta.env.VITE_API_URL ?? '/api';

const analyzeECG = (formData) => {
    return axios.post(`${API_URL}/analyze`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
        .then(response => response.data)  // Traiter la réponse
        .catch(error => {
            console.error("Erreur lors de la requête à l'API :", error);
            throw error;
        });
};

const getRandomPlot = () => {
    return axios.get(`${API_URL}/get-random-plot`)
        .then(response => response.data)  // Traiter la réponse
        .catch(error => {
            console.error("Erreur lors de la requête à l'API :", error);
            throw error;
        });
};

const saveScore = (score) => {
    return axios.post(`${API_URL}/score?value=${score}`)
        .then(response => response.data)  // Traiter la réponse
        .catch(error => {
            console.error("Erreur lors de la requête à l'API :", error);
            throw error;
        });
};

const getAverageScore = () => {
    return axios.get(`${API_URL}/score/stats`)
        .then(response => response.data)  // Traiter la réponse
        .catch(error => {
            console.error("Erreur lors de la requête à l'API :", error);
            throw error;
        });
};

export { analyzeECG, getRandomPlot, saveScore, getAverageScore };
