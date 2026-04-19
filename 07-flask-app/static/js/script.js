function fetchAPI() {
    fetch('/api/hello')
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('api-result');
            resultDiv.innerHTML = `<strong>API Response:</strong> ${data.message}`;
            resultDiv.classList.add('show');
        })
        .catch(error => console.error('Error:', error));
}

console.log('🚀 Flask App loaded!');
