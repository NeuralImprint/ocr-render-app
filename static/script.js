// static/script.js
document.getElementById("ocrForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const imageName = document.getElementById("imageSelect").value;

    fetch("/process", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ image: imageName })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("resultBox").innerHTML =
            `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    })
    .catch(error => {
        document.getElementById("resultBox").innerText = "Error: " + error;
    });
});
// Show selected file name
document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("imageUpload");
  const fileNameDisplay = document.getElementById("file-name");

  fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
      fileNameDisplay.textContent = `Selected file: ${fileInput.files[0].name}`;
    } else {
      fileNameDisplay.textContent = "";
    }
  });
});
