import Webcam from "webcam-easy";

const webcamElement = document.getElementById("webcam");
const canvasElement = document.getElementById("canvas");
const snapSoundElement = document.getElementById("snapSound");
const webcam = new Webcam(
  webcamElement,
  "user",
  canvasElement,
  snapSoundElement
);

webcam
  .start()
  .then((result) => {
    console.log("webcam started");
  })
  .catch((err) => {
    console.log(err);
  });

document.getElementById("capture").addEventListener("click", () => {
  let picture = webcam.snap();
  // Send the captured image to the backend
  const imageData = picture.replace(/^data:image\/(png|jpg);base64,/, ""); // Remove the prefix

  const csrfToken = document
    .querySelector("meta[name='csrf-token']")
    .getAttribute("content");

  fetch("/capture", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-csrf-token": csrfToken,
    },
    body: JSON.stringify({ image: imageData }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.json(); // assuming the response is in JSON format
    })
    .then((data) => {
      // Process and render the response data
      const statusMessage = data.message;
      const signal = data.result;

      // Update the DOM to show status and signal
      const statusContainer = document.getElementById("status");
      statusContainer.textContent = `Status: ${statusMessage}`;

      const signalContainer = document.getElementById("signal");
      signalContainer.textContent = `Signal: "${signal}"`;

      // Add an icon based on the signal (example: thumbs-up icon)
      const iconContainer = document.getElementById("icon");
      iconContainer.innerHTML = ""; // Clear previous icon
      if (signal === "thumbs-up") {
        const thumbsUpIcon = document.createElement("i");
        thumbsUpIcon.classList.add("fas", "fa-thumbs-up"); // Font Awesome thumbs-up icon
        iconContainer.appendChild(thumbsUpIcon);
      } else {
      }
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
      const resultContainer = document.getElementById("result");
      resultContainer.innerHTML = ""; // Clear any previous content
      const errorText = document.createElement("p");
      errorText.textContent = "Error: " + error.message;
      resultContainer.appendChild(errorText);
    });
});

//   const resultText = document.createElement('p');
//   statusContainer.appendChild(resultText);

// const resultContainer = document.getElementById('result');
// resultContainer.innerHTML = ''; // Clear any previous content
// const resultText = document.createElement('p');
// resultText.textContent = 'Response from server: ' + JSON.stringify(data);
// resultContainer.appendChild(resultText);
