const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(endpoint, options = {}) {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    options
  );

  if (!response.ok) {
    let message = "Something went wrong.";

    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {
      // Ignore invalid JSON responses.
    }

    throw new Error(message);
  }

  return response.json();
}

export function getCompanyProfile(companyId) {
  return request(`/companies/${companyId}/profile`);
}

export function getCompanyTrends(companyId) {
  return request(`/companies/${companyId}/trends`);
}

export function getCompanyReport(companyId) {
  return request(`/companies/${companyId}/report`);
}

export function getTransactions(companyId) {
  return request(
    `/transactions?company_id=${encodeURIComponent(companyId)}`
  );
}

export function uploadTransactions(file) {
  const formData = new FormData();
  formData.append("file", file);

  return request("/transactions/upload-csv", {
    method: "POST",
    body: formData,
  });
}

export function askCompanyAssistant(companyId, question) {
  return request(`/companies/${companyId}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
      n_results: 12,
    }),
  });
}