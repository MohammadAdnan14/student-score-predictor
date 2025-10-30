document.getElementById("predictBtn").addEventListener("click", async () => {
  const hours = parseFloat(document.getElementById("hours").value);
  const prev = parseFloat(document.getElementById("prev").value);
  const sleep = parseFloat(document.getElementById("sleep").value);
  const papers = parseFloat(document.getElementById("papers").value);
  const extraValue = document.getElementById("extra").value;

  const payload = {
    hours_studied: hours,
    previous_scores: prev,
    sleep_hours: sleep,
    papers_practiced: papers,
    extracurricular: extraValue,
  };

  const resBox = document.getElementById("result");
  const scoreEl = document.getElementById("score");
  const remarkEl = document.getElementById("remark");
  const sourceEl = document.getElementById("source");

  try {
    const resp = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await resp.json();

    if (resp.ok) {
      scoreEl.textContent = data.predicted_score + " / 100";
      remarkEl.textContent = data.remark;
      sourceEl.textContent = "Source: " + data.source;
      resBox.hidden = false;
    } else {
      scoreEl.textContent = "Error";
      remarkEl.textContent = data.error || "Unknown error";
      sourceEl.textContent = JSON.stringify(data);
      resBox.hidden = false;
    }
  } catch (err) {
    scoreEl.textContent = "Network Error";
    remarkEl.textContent = err.message;
    sourceEl.textContent = "";
    resBox.hidden = false;
  }
});
