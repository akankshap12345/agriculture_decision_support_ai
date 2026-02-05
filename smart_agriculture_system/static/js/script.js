// Smart Agriculture Decision Support System - Main JavaScript

// Utility function to show/hide loading spinner
function showLoading(elementId) {
    document.getElementById(elementId).classList.add('show');
}

function hideLoading(elementId) {
    document.getElementById(elementId).classList.remove('show');
}

// Utility function to show/hide results
function showResults(elementId) {
    document.getElementById(elementId).classList.add('show');
}

function hideResults(elementId) {
    document.getElementById(elementId).classList.remove('show');
}

// Crop Recommendation Form Handler
function handleCropRecommendation(event) {
    event.preventDefault();
    
    // Get form data
    const formData = {
        nitrogen: document.getElementById('nitrogen').value,
        phosphorus: document.getElementById('phosphorus').value,
        potassium: document.getElementById('potassium').value,
        temperature: document.getElementById('temperature').value,
        humidity: document.getElementById('humidity').value,
        ph: document.getElementById('ph').value,
        rainfall: document.getElementById('rainfall').value
    };
    
    // Show loading, hide previous results
    showLoading('loading');
    hideResults('results');
    
    // Make API call
    fetch('/api/recommend-crop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        hideLoading('loading');
        
        if (data.success) {
            displayCropRecommendation(data);
            showResults('results');
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        hideLoading('loading');
        alert('An error occurred. Please try again.');
        console.error('Error:', error);
    });
}

// Display crop recommendation results
function displayCropRecommendation(data) {
    // Main recommendation
    document.getElementById('recommended-crop').textContent = data.recommended_crop.toUpperCase();
    
    // Top 3 recommendations
    const recommendationsHtml = data.top_recommendations.map(rec => `
        <div class="recommendation-item">
            <span class="recommendation-crop">${rec.crop.toUpperCase()}</span>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${rec.confidence}%"></div>
            </div>
            <span class="confidence-text">${rec.confidence}%</span>
        </div>
    `).join('');
    document.getElementById('recommendations').innerHTML = recommendationsHtml;
    
    // Input parameters
    const parametersHtml = Object.entries(data.input_parameters).map(([key, value]) => `
        <div class="result-item">
            <strong>${key}</strong>
            <span>${value}</span>
        </div>
    `).join('');
    document.getElementById('input-parameters').innerHTML = parametersHtml;
    
    // Advice
    const adviceHtml = data.advice.map(advice => `
        <li>${advice}</li>
    `).join('');
    document.getElementById('advice').innerHTML = adviceHtml;
}

// Yield Prediction Form Handler
function handleYieldPrediction(event) {
    event.preventDefault();
    
    // Get form data
    const formData = {
        state: document.getElementById('state').value,
        crop: document.getElementById('crop').value,
        area: document.getElementById('area').value,
        rainfall: document.getElementById('rainfall-yield').value,
        fertilizer: document.getElementById('fertilizer').value,
        pesticide: document.getElementById('pesticide').value
    };
    
    // Show loading, hide previous results
    showLoading('loading-yield');
    hideResults('results-yield');
    
    // Make API call
    fetch('/api/predict-yield', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        hideLoading('loading-yield');
        
        if (data.success) {
            displayYieldPrediction(data);
            showResults('results-yield');
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        hideLoading('loading-yield');
        alert('An error occurred. Please try again.');
        console.error('Error:', error);
    });
}

// Display yield prediction results
function displayYieldPrediction(data) {
    // Yield values
    document.getElementById('predicted-yield').textContent = data.predicted_yield + ' tons/ha';
    document.getElementById('total-production').textContent = data.total_production + ' tons';
    
    // Input parameters
    const parametersHtml = Object.entries(data.input_parameters).map(([key, value]) => `
        <div class="result-item">
            <strong>${key}</strong>
            <span>${value}</span>
        </div>
    `).join('');
    document.getElementById('input-parameters-yield').innerHTML = parametersHtml;
    
    // Advice
    const adviceHtml = data.advice.map(advice => `
        <li>${advice}</li>
    `).join('');
    document.getElementById('advice-yield').innerHTML = adviceHtml;
}

// Weather Advisory Form Handler
function handleWeatherAdvisory(event) {
    event.preventDefault();
    
    // Get city name
    const city = document.getElementById('city').value;
    
    // Show loading, hide previous results
    showLoading('loading-weather');
    hideResults('results-weather');
    
    // Make API call
    fetch('/api/weather', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city: city })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading('loading-weather');
        
        if (data.success) {
            displayWeatherAdvisory(data);
            showResults('results-weather');
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        hideLoading('loading-weather');
        alert('An error occurred. Please try again.');
        console.error('Error:', error);
    });
}

// Display weather advisory results
function displayWeatherAdvisory(data) {
    const weather = data.weather;
    
    // Weather card
    document.getElementById('weather-city').textContent = weather.city;
    document.getElementById('weather-temp').textContent = weather.temperature + '°C';
    document.getElementById('weather-desc').textContent = weather.description;
    document.getElementById('weather-humidity').textContent = weather.humidity + '%';
    document.getElementById('weather-rainfall').textContent = weather.rainfall + ' mm';
    document.getElementById('weather-wind').textContent = weather.wind_speed + ' km/h';
    document.getElementById('weather-time').textContent = weather.timestamp;
    
    // Advisory
    const advisoryHtml = data.advisory.map(item => `
        <div class="advisory-item ${item.type}">
            <h4>${item.title}</h4>
            <p>${item.message}</p>
        </div>
    `).join('');
    document.getElementById('advisory').innerHTML = advisoryHtml;
}

// Input validation helpers
function validateNumber(input, min, max) {
    const value = parseFloat(input.value);
    if (isNaN(value) || value < min || value > max) {
        input.style.borderColor = 'red';
        return false;
    }
    input.style.borderColor = '';
    return true;
}

// Add real-time validation for numeric inputs
document.addEventListener('DOMContentLoaded', function() {
    // Crop recommendation form validation
    const nitrogenInput = document.getElementById('nitrogen');
    if (nitrogenInput) {
        nitrogenInput.addEventListener('input', function() {
            validateNumber(this, 0, 200);
        });
    }
    
    // Add smooth scroll for navigation
    const navLinks = document.querySelectorAll('.nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Update active state
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
});

// Utility function to reset form
function resetForm(formId) {
    document.getElementById(formId).reset();
}

// Export functions for global use
window.handleCropRecommendation = handleCropRecommendation;
window.handleYieldPrediction = handleYieldPrediction;
window.handleWeatherAdvisory = handleWeatherAdvisory;
window.resetForm = resetForm;
