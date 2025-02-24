

const form = document.getElementById('uploadForm');
const responseDiv = document.getElementById('response');

form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(form);

    try {
        responseDiv.innerHTML = "<p style='color: white;'>Uploading and processing...</p>";
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();

        // Check if the recognized person is "Unknown"
        if (result.name === "Unknown") {
            responseDiv.innerHTML = `
                <p style="color: white;"><strong>Recognized Person:</strong> ${result.name}</p>
            `;
        } else {
            responseDiv.innerHTML = `
                <p style="color: white;"><strong>Recognized Person:</strong> ${result.name}</p>
                <p style="color: white;"><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(2)}%</p>
            `;
        }
    } catch (error) {
        responseDiv.innerHTML = `<p style="color: white;">Error: ${error.message}</p>`;
    }
});
