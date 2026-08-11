async function runVeritasVerification() {
    const textInput = document.getElementById("newsContent").value;
    const scopeInput = document.getElementById("scopeTier").value;
    const cityInput = document.getElementById("targetCity").value;
    const executeBtn = document.getElementById("executeBtn");

    // UI Feedback State Matrix
    executeBtn.innerText = "Analyzing Live Data Channels...";
    executeBtn.disabled = true;

    try {
        // Constructing URL parameters dynamically to prevent pipeline data blocks
        const queryUrl = `http://127.0.0{encodeURIComponent(textInput)}&scope=${scopeInput}&city=${encodeURIComponent(cityInput)}`;
        
        const response = await fetch(queryUrl);
        const data = await response.json();

        // 1. Update the live scoring index metrics
        document.getElementById("scoreValue").innerText = `${data.score} / 100`;
        document.getElementById("progressBar").style.width = `${data.score}%`;
        document.getElementById("statusFooter").innerText = `Status Critical: ${data.status}`;

        // 2. Adjust styling depending on anomaly levels
        const alertBox = document.getElementById("alertBox");
        const alertTitle = document.getElementById("alertTitle");
        const alertBody = document.getElementById("alertBody");

        if (data.score >= 75) {
            alertBox.className = "alert-box success";
            alertTitle.innerText = "Multi-Channel Verification Found:";
            alertBody.innerText = `Confirmed across: ${data.sources.join(", ")}`;
            document.getElementById("progressBar").style.backgroundColor = "#0056b3"; // Solid Blue Anchor
        } else {
            alertBox.className = "alert-box danger";
            alertTitle.innerText = "Zero Network Verification Found:";
            alertBody.innerText = `Warning: No reliable reports matching these details were located in the ${scopeInput.toUpperCase()} data grid registers.`;
            document.getElementById("progressBar").style.backgroundColor = "#dc3545"; // Red Alert Status
        }

    } catch (error) {
        console.error("Veritas AI Connection Interrupted:", error);
        document.getElementById("statusFooter").innerText = "Network Error: Failed to link to the live backend server node.";
    } finally {
        executeBtn.innerText = "Execute Direct Fact Verification";
        executeBtn.disabled = false;
    }
}

