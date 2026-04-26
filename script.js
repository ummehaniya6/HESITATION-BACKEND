let lastActionTime = null;

document.getElementById("actionBtn").addEventListener("click", function() {

    let currentTime = new Date().getTime();

    // First click
    if (lastActionTime === null) {
        lastActionTime = currentTime;
        document.getElementById("result").innerText = "First action recorded";
        return;
    }

    // Calculate delay
    let delay = currentTime - lastActionTime;
    lastActionTime = currentTime;

    // Rule-based threshold (2 seconds)
    let hesitation = delay > 2000 ? "Hesitation Detected" : "No Hesitation";

    // Store data in local storage
    let data = {
        delay: delay,
        result: hesitation,
        time: new Date().toLocaleTimeString()
    };

    let records = JSON.parse(localStorage.getItem("data")) || [];
    records.push(data);
    localStorage.setItem("data", JSON.stringify(records));

    // Show result
    document.getElementById("result").innerText =
        "Delay: " + delay + " ms → " + hesitation;

});