const form = document.getElementById('predictionForm');
const result = document.getElementById('predictionResult');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const payload = {
        Rainfall: Number(document.getElementById('rainfall').value),
        Temperature: Number(document.getElementById('temperature').value),
        Humidity: Number(document.getElementById('humidity').value),
        Water_Usage: Number(document.getElementById('waterUsage').value),
    };

    result.textContent = 'Predicting...';

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const data = await response.json();
        if (!response.ok) {
            result.textContent = `Error: ${data.error || 'Unable to predict'}`;
            return;
        }

        result.textContent = `Predicted groundwater level: ${data.prediction}`;
    } catch (error) {
        result.textContent = 'Unable to connect to the API. Start backend/api.py first.';
    }
});
