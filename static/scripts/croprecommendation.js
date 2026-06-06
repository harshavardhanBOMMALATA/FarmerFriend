document.getElementById("cropForm").addEventListener("submit", async function(e){

    e.preventDefault();

    const data = {
        N: document.getElementById("n").value,
        P: document.getElementById("p").value,
        K: document.getElementById("k").value,
        temperature: document.getElementById("temperature").value,
        humidity: document.getElementById("humidity").value,
        ph: document.getElementById("ph").value,
        rainfall: document.getElementById("rainfall").value
    };

    try{

        const response = await fetch("/recommendation/predict/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();


        document.getElementById("cropResult").innerHTML = `
    <img
        class="crop-image"
        src="https://source.unsplash.com/600x400/?${result.recommended_crop},crop"
        alt="${result.recommended_crop}">

    <div class="crop-name">
        ${result.recommended_crop}
    </div>

    <p class="crop-desc">
        Best crop for current conditions.
    </p>

    <div class="reason-cards">

        <div class="reason-card">
            <h4>🌡️ Temperature</h4>
            <p>${result.temperature_reason}</p>
        </div>

        <div class="reason-card">
            <h4>💧 Humidity</h4>
            <p>${result.humidity_reason}</p>
        </div>

        <div class="reason-card">
            <h4>📈 Market Trend</h4>
            <p>${result.market_reason}</p>
        </div>

    </div>
`;


    }
    catch(error){

        console.error(error);

        document.getElementById("cropResult").innerHTML = `
            <div class="crop-name">
                Prediction Failed
            </div>
        `;
    }

});