/*function previewImage(event) {
    const uploadedImage = document.getElementById('uploaded-image');
    uploadedImage.src = URL.createObjectURL(event.target.files[0]);
}


document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const predictButton = document.getElementById('predict-button');
    const predictionResult = document.getElementById('prediction-result');

    predictButton.addEventListener('click', function() {
        const formData = new FormData(uploadForm);

        fetch('http://127.0.0.1:8080/classify_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            predictionResult.innerHTML = `Prediction: ${result.prediction}`;
        })
        .catch(error => {
            predictionResult.innerHTML = 'Error predicting image.';
            console.error(error);
        });
    });
});*/

function previewImage(event) {
    const uploadedImage = document.getElementById('uploaded-image');
    uploadedImage.src = URL.createObjectURL(event.target.files[0]);
}

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const predictButton = document.getElementById('predict-button');
    const predictionResult = document.getElementById('prediction-result');

    predictButton.addEventListener('click', function() {
        const formData = new FormData(uploadForm);

        fetch('http://127.0.0.1:5000/classify_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            if (result.prediction !== undefined) {
                predictionResult.innerHTML = `Prediction: ${result.prediction}`;
            } else {
                predictionResult.innerHTML = 'Prediction not available.';
            }
        })
        .catch(error => {
            predictionResult.innerHTML = 'Error predicting image.';
            console.error(error);
        });
    });
});