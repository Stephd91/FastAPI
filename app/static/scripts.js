// scripts.js 
// https://getbootstrap.com/docs/4.0/getting-started/javascript/

// FLASH SESSION
function launchFlashSession() {
    // Get the selected themes from the checkboxes
    const selectedThemes = [];
    const checkboxes = document.querySelectorAll(".form-check-input");
    checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
            selectedThemes.push(checkbox.value);
        }
    });

    // Send the selected themes to the /launch-flash-session/ route using a POST request
    fetch("/launch-flash-session/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(selectedThemes),
    })
    .then((response) => response.json())
    .then((data) => {
        // Handle the response from the server if needed
        console.log(data);
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}

// FLIP CARDS 
function flipCard(card) {
    card.classList.toggle('flipped');
}
