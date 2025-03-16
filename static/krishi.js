// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    // Select the Sign In and Sign Up buttons
    const signInButton = document.querySelector(".secondary-button");
    const signUpButton = document.querySelector(".primary-button");

    // Add click event listeners
    if (signInButton) {
        signInButton.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default link behavior
            // Redirect to the Sign In page
            window.location.href = "/login";//signin.html
        });
    }

    if (signUpButton) {
        signUpButton.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default link behavior
            // Redirect to the Sign Up page
            window.location.href = "/login";//signup.html
        });
    }
});
document.addEventListener("DOMContentLoaded", function () {
    // Handle Sign In Form Submission
    const signInForm = document.querySelector("#signin-form");
    if (signInForm) {
        signInForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent form from submitting normally
            // Perform validation or authentication here if needed
            console.log("Sign In Successful!");
            // Redirect to the homepage
            window.location.href = "/login";
        });
    }

    // Handle Sign Up Form Submission
    const signUpForm = document.querySelector("#signup-form");
    if (signUpForm) {
        signUpForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent form from submitting normally
            // Perform validation or save user details here if needed
            console.log("Sign Up Successful!");
            // Redirect to the homepage
            window.location.href = "/";
        });
    }
});
document.addEventListener("DOMContentLoaded", function () {
    const getStartedButton = document.getElementById("getStartedButton");

    // Add event listener for "Get Started" button
    getStartedButton.addEventListener("click", function (e) {
        e.preventDefault(); // Prevent default link behavior

        // Redirect to signin.html
        window.location.href = "/login";//
    });
});


// document.addEventListener('DOMContentLoaded', () => {
//     const getStartedButton = document.getElementById('getStartedButton');
//     const imageInput = document.getElementById('imageInput');

//     // Event listener for the Get Started button
//     getStartedButton.addEventListener('click', (e) => {
//         e.preventDefault();
//         imageInput.click(); // Trigger the hidden file input
//     });

//     // Event listener for image selection
//     imageInput.addEventListener('change', (event) => {
//         const file = event.target.files[0]; // Get the selected file

//         if (file) {
//             const reader = new FileReader();

//             reader.onload = (e) => {
//                 // Create an image element and display the uploaded image
//                 const imageDisplayArea = document.createElement('div');
//                 imageDisplayArea.innerHTML = `
//                     <div style="margin-top: 20px;">
//                         <h3>Uploaded Image:</h3>
//                         <img src="${e.target.result}" alt="Uploaded Image" style="max-width: 20%; height: auto; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
//                     </div>
//                 `;

//                 // Append the imageDisplayArea to the body or a specific container
//                 document.body.appendChild(imageDisplayArea);
//             };

//             reader.readAsDataURL(file); // Read the file as a data URL
//         }
//     });
// });
//  // Function to send the image to a machine learning model (ML)
//  function sendImageToML(file) {
//     const formData = new FormData();
//     formData.append("image", file);

//     fetch('ml_endpoint_url', { // Replace 'ml_endpoint_url' with your actual endpoint
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Image processed by ML:', data);
//         // Handle the ML response if needed
//     })
//     .catch(error => {
//         console.error('Error processing image with ML:', error);
//     });
// }


// BACKEND  =>>>  (PYTHON AND FLASK )

// from flask import Flask, request, jsonify
// from PIL import Image
// import io

// app = Flask(__name__)

// @app.route('/process', methods=['POST'])
// def process_image():
//     # Check if an image was sent in the request
//     if 'image' not in request.files:
//         return jsonify({'error': 'No image provided'}), 400
    
//     image_file = request.files['image']
//     image = Image.open(image_file.stream)  # Open the image

//     # Process the image with your ML model (e.g., prediction, analysis, etc.)
//     # result = model.predict(image)  # Example of using an ML model for inference
    
//     # For now, we'll return a dummy response
//     result = {'prediction': 'Healthy livestock'}

//     return jsonify(result)

// if __name__ == '__main__':
//     app.run(debug=True)

window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-links a');
    
    sections.forEach((section, index) => {
        if (window.scrollY >= section.offsetTop - 50) {
            navLinks.forEach(link => link.classList.remove('active'));
            navLinks[index].classList.add('active');
        }
    });
});





