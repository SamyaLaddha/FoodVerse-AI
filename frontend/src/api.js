// Backend address. Change here if your backend runs elsewhere.
export const API = "http://localhost:8000";

async function handle(res) {
  if (!res.ok) throw new Error("Request failed (" + res.status + "). Is the backend running on " + API + "?");
  return res.json();
}

export const postFile = (path, file) => {
  const fd = new FormData();
  fd.append("file", file);
  return fetch(API + path, { method: "POST", body: fd }).then(handle);
};

export const postJson = (path, body) =>
  fetch(API + path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }).then(handle);

export const getJson = (path) => fetch(API + path).then(handle);
