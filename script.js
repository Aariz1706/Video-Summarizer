const form = document.getElementById("uploadForm");
const input = document.getElementById("videoInput");
const output = document.getElementById("output");
const fileNameDisplay = document.getElementById("fileName");

// Show selected filename
input.addEventListener("change", () => {
  const file = input.files[0];
  if (file) {
    fileNameDisplay.textContent = `Selected: ${file.name}`;
    fileNameDisplay.classList.remove("hidden");
  } else {
    fileNameDisplay.textContent = "";
    fileNameDisplay.classList.add("hidden");
  }
});

// Handle form submission
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = input.files[0];
  if (!file) {
    alert("Please select a video first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  output.innerHTML = `<p class="text-gray-500">Uploading and summarizing your video...</p>`;

  try {
    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();  // Try reading the JSON no matter what
    console.log("Server response", response)

    if (!response.ok) {
      throw new Error(result.error || "Failed to summarize video.");
    }

    if (!result.summary) {
      throw new Error("No summary returned.");
    }

    output.innerHTML = `
      <div class="bg-gray-100 p-4 rounded mt-4">
        <h2 class="text-xl font-semibold text-primary mb-2">Summary:</h2>
        <p class="text-gray-700">${result.summary}</p>
      </div>
    `;

  } catch (error) {
    console.error("Frontend Error:", error);
    output.innerHTML = `<p class="text-red-500">Error: ${error.message}</p>`;
  }
});