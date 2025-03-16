// Elements
const imageInput = document.getElementById("imageInput");
const previewContainer = document.querySelector("#preview .images");
const uploadButton = document.getElementById("uploadButton");
const countDisplay = document.createElement("p");
countDisplay.classList.add("image-count");
previewContainer.parentElement.appendChild(countDisplay);

// Function to display image previews and count images
imageInput.addEventListener("change", () => {
    const files = Array.from(imageInput.files); // Get selected files
    previewContainer.innerHTML = ""; // Clear previous previews

    if (files.length !== 4) {
        countDisplay.textContent = `Please select exactly 4 images. You selected ${files.length}.`;
        return;
    }

    countDisplay.textContent = `Number of images selected: ${files.length}`;

    files.forEach(file => {
        if (file.type.startsWith("image/")) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement("img");
                img.src = e.target.result;
                img.alt = file.name;
                img.classList.add("preview-image");
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file); // Read image data
        } else {
            alert(`Unsupported file type: ${file.name}`);
        }
    });
});

// Function to send images to ML backend
uploadButton.addEventListener("click", () => {
    const files = Array.from(imageInput.files);

    if (files.length !== 4) {
        alert("Please select exactly 4 images before submitting.");
        return;
    }

    const formData = new FormData();

    files.forEach((file, index) => {
        formData.append(`image${index}`, file);
    });

    // Replace this URL with your backend endpoint
    const backendURL = "https://your-ml-api-endpoint.com/analyze";

    fetch(backendURL, {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            alert("Images uploaded successfully. ML response: " + JSON.stringify(data));
        })
        .catch(error => {
            console.error("Error uploading images:", error);
            alert("Failed to upload images. Please try again.");
        });
});
