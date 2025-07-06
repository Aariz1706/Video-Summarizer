// Get references to HTML elements by their IDs
const form = document.getElementById("uploadForm");
const input = document.getElementById("videoInput");
const output = document.getElementById("output");
const file_name = document.getElementById("fileName");
const loading = document.getElementById("loading");

// When a video is selected, show its name
input.addEventListener("change", () => {
  const file = input.files[0]; // Get selected file
  if (file) {
    file_name.textContent = `📁 Selected: ${file.name}`; // Show filename
    file_name.classList.remove("hidden"); // Make filename visible
  } else {
    file_name.classList.add("hidden"); // Hide if no file
  }
});

// Handle form submission when user clicks "Summarize Video"
form.addEventListener("submit", async (e) => {
  e.preventDefault(); // Prevent page reload

  const file = input.files[0]; // Get selected video
  if (!file) {
    alert("Please select a video.");
    return;
  }

  // Prepare form data to send to the backend
  const formData = new FormData();
  formData.append("file", file);

  // Show loading animation
  output.innerHTML = "";
  loading.classList.remove("hidden");

  try {
    // Send video to Flask backend for processing
    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });

    // Convert response to JSON
    const result = await response.json();
    console.log("Received Summary:", result.summary);
    console.log("Received Transcription:", result.transcription);
    loading.classList.add("hidden");
    const summaryText = result.summary || "Summary not available.";
    const transcriptionText = result.transcription || "Transcription not available.";

    // Show the summary on the screen
    output.innerHTML = `
      <div class="bg-white p-6 rounded-xl shadow-md">
        <h2 class="text-xl font-bold text-primary mb-2">📝 Summary:</h2>
        <p class="text-gray-700 whitespace-pre-line mb-4" id="summaryText">${summaryText}</p>

        <!-- Buttons -->
        <div class="flex gap-3 flex-wrap">
          <button onclick="copyText()" class="bg-gray-100 hover:bg-gray-200 text-sm px-3 py-1 rounded">📋 Copy Summary</button>
          <button onclick="downloadText()" class="bg-gray-100 hover:bg-gray-200 text-sm px-3 py-1 rounded">💾 Download .txt</button>
        </div>

        <!-- Transcription Toggle -->
        <details class="mt-6">
          <summary class="cursor-pointer text-indigo-600 hover:underline text-sm">📄 Show Full Transcription</summary>
          <p class="mt-2 text-gray-600 whitespace-pre-line">${transcriptionText}</p>
        </details>
      </div>
    `;
  } catch (error) {
    console.error("Error:", error);
    loading.classList.add("hidden"); // Hide loader
    output.innerHTML = `<p class="text-red-500 mt-4">Something went wrong while summarizing the video.</p>`;
  }
});

// Function to copy summary text to clipboard
function copyText() {
  const summaryText = document.querySelector("#output p").innerText;
  navigator.clipboard.writeText(summaryText).then(() => {
    alert("Summary copied to clipboard!");
  });
}
// 💾 Download summary as .txt
function downloadText() {
  const text = document.getElementById("summaryText").innerText;
  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = "summary.txt";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
