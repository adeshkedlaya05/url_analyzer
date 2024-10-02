// Select the binary flow container
const binaryFlow = document.getElementById('binary-flow');
// Function to generate random binary digits (0 or 1)
function getRandomBinary() {
    return Math.random() > 0.5 ? '1' : '0';
}
// Function to generate a random integer between min and max
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
// Function to create a single binary digit
function createBinaryDigit() {
    const binaryDigit = document.createElement('div');
    binaryDigit.classList.add('binary-digit');
    // Set random binary digit
    binaryDigit.innerText = getRandomBinary();
    // Randomize starting left position
    binaryDigit.style.left = `${getRandomInt(0, 100)}vw`;
    // Randomize the speed of the digit
    const animationDuration = getRandomInt(5, 10);
    binaryDigit.style.animationDuration = `${animationDuration}s`;
    // Append the digit to the binary flow container
    binaryFlow.appendChild(binaryDigit);
    // Remove digit after animation ends to prevent overflow
    setTimeout(() => {
        binaryDigit.remove();
    }, animationDuration * 1000);
}
// Function to create multiple binary digits at once
function createBinaryFlow() {
    const numberOfDigitsToCreate = 5; // Number of digits to create each time
    for (let i = 0; i < numberOfDigitsToCreate; i++) {
        createBinaryDigit();
    }
}
// Call the function to create the binary flow initially
createBinaryFlow();
// Use setInterval to keep adding new binary digits for a continuous effect
setInterval(createBinaryFlow, 500); // Adds new digits every 0.5 seconds
const wrapper=document.querySelector('.wrapper');
const signuplink=document.querySelector('.signup-link');
const signinlink=document.querySelector('.signin-link');
//for toggling the signup and login page
signuplink.addEventListener('click',() =>{
    wrapper.classList.add('animate-signin');
    wrapper.classList.remove('animate-signup');
});
signinlink.addEventListener('click',() =>{
    wrapper.classList.add('animate-signup');
    wrapper.classList.remove('animate-signin');
});
function clearInput() {
    document.getElementById('urlInput').value = ''; // Clear the input field
    document.getElementById('outputArea').style.display = "none"; // Hide the output area if visible
}
const forgotPassLink = document.getElementById('forgotPassLink');
const forgotPassModal = document.getElementById('forgotPassModal');
const closeModalBtn = document.querySelector('.close-btn');
// Show the modal when the link is clicked
forgotPassLink.addEventListener('click', function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    forgotPassModal.style.display = 'flex'; // Show the modal
});
// Close the modal when the close button is clicked
closeModalBtn.addEventListener('click', function () {
    forgotPassModal.style.display = 'none'; // Hide the modal
});
// Close the modal when clicking outside the modal content
window.addEventListener('click', function (event) {
    if (event.target === forgotPassModal) {
        forgotPassModal.style.display = 'none'; // Hide the modal
    }
});
function addHistoryEntry(url, result) {
    const csrftoken = getCookie('csrftoken');

    // Send request to add history
    fetch('/add-history/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ url: url, result: result })
    })
    .then(response => response.json())
    .then(data => {
        if (data.timestamp) {
            // Entry added successfully
            console.log('Entry added successfully:', data);
            // Immediately update the table without refreshing
            addRowToTable(data.timestamp, data.url, data.result);
        } else if (data.error) {
            console.error('Error:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}
// Function to dynamically add a new row to the table without refreshing
function addRowToTable(timestamp, url, result) {
    const tableBody = document.querySelector('#historyTable tbody');

    const newRow = document.createElement('tr');
    
    // Create a new row with the data returned from the backend
    newRow.innerHTML = `
        <td>${timestamp}</td>
        <td>${url}</td>
        <td>${result}</td>
    `;
    // Add the new row to the top of the table
    tableBody.prepend(newRow);
}
// Function to get the CSRF token (if using Django's CSRF protection)
function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}
function clearHistory() {
    const csrftoken = getCookie('csrftoken');

    fetch('/clear-history/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        // Clear the table from the frontend immediately
        const tableBody = document.querySelector('#historyTable tbody');
        tableBody.innerHTML = '';  // Clear all rows
    })
    .catch(error => console.error('Error:', error));
}
// Example of adding a history entry based on a URL analysis result
document.getElementById('urlForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const urlInput = document.getElementById('urlInput').value;
    const result = 'Safe'; // Replace this with the actual analysis result
    addHistoryEntry(urlInput, result);
});

// Add event listener for the clear history button
document.getElementById('clearHistoryButton').addEventListener('click', clearHistory);
// Example function to analyze URL and add to history
function analyzeURL() {
    const url = document.getElementById('urlInput').value;
    const outputArea = document.getElementById('outputArea');
    const outputText = document.getElementById('output');
    // Check if the URL is empty
    if (!url.trim()) {
        outputText.innerHTML = "No URL provided. Please enter a URL.";
        outputText.className = "output-malicious"; // You can style this differently if needed
        outputArea.style.display = 'block';
        return; // Stop execution if no URL is provided
    }
    // Send AJAX request to Django backend
    fetch('/api/analyze-url/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken') // CSRF token
        },
        body: new URLSearchParams({
            'url': url // The URL to analyze
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            outputText.innerHTML = "An error occurred: " + data.error;
            outputText.className = "output-malicious";
        } else {
            //Displaying the appropriate results
            console.log(`The URL is ${data.result}`);
            if (data.result === 'malicious') {
                outputText.innerHTML = "The URL is malicious.";
                outputText.className = "output-malicious";
            } else {
                outputText.innerHTML = "The URL is safe.";
                outputText.className = "output-safe";
            }
        }
        outputArea.style.display = 'block';
    })
    .catch(error => {
        console.error('Fetch Error:', error);
        outputText.innerHTML = "An error occurred while analyzing the URL.";
        outputText.className = "output-malicious";
        outputArea.style.display = 'block';
    });
}
// Function to clear input and output area
function clearInput() {
    document.getElementById('urlInput').value = ''; // Clear the input field
    document.getElementById('outputArea').style.display = 'none'; // Hide the output area
    document.getElementById('output').innerHTML = ''; // Clear any output message
}
// Function to get CSRF token for secure POST requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Function to show the forgot password modal
document.getElementById('forgotPassLink').onclick = function() {
    document.getElementById('forgotPassModal').style.display = 'block';
};
// Close the modal when the close button is clicked
document.querySelector('.close-btn').onclick = function() {
    document.getElementById('forgotPassModal').style.display = 'none';
};
// Close the modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('forgotPassModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};
// Function to submit the new password
function submitResetPassword() {
    const username = document.getElementById('usernameInput').value;
    const newPassword = document.getElementById('newPasswordInput').value;
    // Make an AJAX request to update the password
    fetch('/reset-password/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Use your method to get CSRF token
        },
        body: JSON.stringify({ username: username, new_password: newPassword }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || 'Password reset successfully!'); // Show success message
        document.getElementById('forgotPassModal').style.display = 'none'; // Close the modal
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.'); // Show error message
    });
}
