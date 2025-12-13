const API_BASE_URL = "";

const form = document.getElementById("roi-form");
const resultsDiv = document.getElementById("results");
const messageDiv = document.getElementById("message");
const emptyStateDiv = document.getElementById("empty-state");

const elPredictedRent = document.getElementById("predicted_rent");
const elPredictedPrice = document.getElementById("predicted_price");
const elAnnualRent = document.getElementById("annual_rent");
const elGrossYield = document.getElementById("gross_yield");
const elGrossYieldPercent = document.getElementById("gross_yield_percent");

let barChartInstance = null;
let pieChartInstance = null;

function readNumber(id) {
  const value = document.getElementById(id).value;
  return value === "" ? null : Number(value);
}

function readText(id) {
  return document.getElementById(id).value || "";
}

function readApiKey() {
  return (document.getElementById("api_key")?.value || "").trim();
}

function updateCharts(data) {
  const { predicted_rent, predicted_price, annual_rent, gross_yield_percent } = data;

  const barCtx = document.getElementById("barChart").getContext("2d");
  const pieCtx = document.getElementById("pieChart").getContext("2d");

  const rentValue = predicted_rent || 0;
  const priceValue = predicted_price || 0;
  const annualValue = annual_rent || 0;
  const yieldPercent = gross_yield_percent || 0;

  if (barChartInstance) {
    barChartInstance.data.datasets[0].data = [rentValue, annualValue, priceValue];
    barChartInstance.update();
  } else {
    barChartInstance = new Chart(barCtx, {
      type: "bar",
      data: {
        labels: ["Monthly Rent", "Annual Rent", "Sale Price"],
        datasets: [
          {
            label: "Amount",
            data: [rentValue, annualValue, priceValue],
            backgroundColor: [
              "rgba(251, 191, 36, 0.9)",
              "rgba(96, 165, 250, 0.9)",
              "rgba(52, 211, 153, 0.9)",
            ],
            borderRadius: 8,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.parsed.y.toLocaleString()}`,
            },
          },
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#e5e7eb" },
          },
          y: {
            grid: { color: "rgba(55, 65, 81, 0.6)" },
            ticks: {
              color: "#9ca3af",
              callback: (value) => value.toLocaleString(),
            },
          },
        },
      },
    });
  }

  const yieldPortion = Math.max(0, Math.min(100, yieldPercent));
  const nonYieldPortion = 100 - yieldPortion;

  if (pieChartInstance) {
    pieChartInstance.data.datasets[0].data = [yieldPortion, nonYieldPortion];
    pieChartInstance.update();
  } else {
    pieChartInstance = new Chart(pieCtx, {
      type: "doughnut",
      data: {
        labels: ["Gross Yield", "Capital Portion"],
        datasets: [
          {
            data: [yieldPortion, nonYieldPortion],
            backgroundColor: [
              "rgba(249, 115, 22, 0.95)",
              "rgba(31, 41, 55, 0.9)",
            ],
            borderWidth: 0,
          },
        ],
      },
      options: {
        cutout: "65%",
        plugins: {
          legend: {
            display: true,
            labels: { color: "#e5e7eb" },
          },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.label}: ${ctx.parsed.toFixed(2)}%`,
            },
          },
        },
      },
    });
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  messageDiv.textContent = "";
  resultsDiv.classList.add("hidden");

  const payload = {
    size_sq_ft: readNumber("size_sq_ft"),
    propertyType: readText("propertyType"),
    bedrooms: readNumber("bedrooms"),
    localityName: readText("localityName"),
    suburbName: readText("suburbName"),
    cityName: readText("cityName"),
    closest_metro_station_km: readNumber("closest_metro_station_km"),
    Aiims_dist_km: readNumber("Aiims_dist_km"),
    NDRLW_dist_km: readNumber("NDRLW_dist_km"),
  };

  // Add latitude and longitude only if they have values
  const latitude = readNumber("latitude");
  const longitude = readNumber("longitude");
  if (latitude !== null) payload.latitude = latitude;
  if (longitude !== null) payload.longitude = longitude;

  // API key is optional - proceed without validation
  const apiKey = readApiKey();

  try {
    const headers = {
      "Content-Type": "application/json",
    };
    
    // Only add API key header if it exists
    if (apiKey) {
      headers["X-API-Key"] = apiKey;
    }

    const response = await fetch(`${API_BASE_URL}/calculate_roi`, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error (${response.status}): ${errorText}`);
    }

    const data = await response.json();

    elPredictedRent.textContent = data.predicted_rent.toFixed(2);
    elPredictedPrice.textContent = data.predicted_price.toFixed(2);
    elAnnualRent.textContent = data.annual_rent.toFixed(2);
    elGrossYield.textContent = data.gross_yield.toFixed(4);
    elGrossYieldPercent.textContent = data.gross_yield_percent.toFixed(2) + "%";

    updateCharts(data);

    resultsDiv.classList.remove("hidden");
    if (emptyStateDiv) {
      emptyStateDiv.classList.add("hidden");
    }
  } catch (err) {
    console.error("API call failed:", err);
    messageDiv.textContent = `API Error: ${err.message}`;
  }
});
