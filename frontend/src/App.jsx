import { useState, useEffect } from "react";
import { postFile, postJson, getJson } from "./api.js";

const PAGES = [
  ["home", "Home"], ["dashboard", "Dashboard"], ["analyze", "Food Analysis"], ["nutrition", "Nutrition"],
  ["freshness", "Freshness"], ["hygiene", "Hygiene"], ["cooking", "Cooking Assistant"], ["planner", "Meal Planner"],
];

/* ---------- small reusable pieces ---------- */
function Bar({ value, max = 100, color }) {
  return (
    <div className="bar"><div style={{ width: Math.min(100, (value / max) * 100) + "%", background: color || "var(--forest)" }} /></div>
  );
}
const scoreColor = (s) => (s >= 75 ? "var(--forest)" : s >= 55 ? "var(--turmeric)" : "var(--chili)");

function Note({ children }) { return <p className="note">{children}</p>; }
function ErrorMsg({ msg }) { return msg ? <p className="error">{msg}</p> : null; }

function Upload({ accept, onFile, label, isVideo }) {
  const [url, setUrl] = useState(null);
  const pick = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    setUrl(URL.createObjectURL(f));
    onFile(f);
  };
  return (
    <div className="upload">
      <label className="dropzone">
        <input type="file" accept={accept} onChange={pick} />
        <span>{label}</span>
      </label>
      {url && (isVideo ? <video src={url} controls className="preview" /> : <img src={url} className="preview" alt="uploaded" />)}
    </div>
  );
}

function NutritionCard({ n }) {
  const rows = [["Protein", n.protein, 50], ["Carbohydrates", n.carbs, 100], ["Fat", n.fat, 40]];
  return (
    <div className="card">
      <h3>{n.food_name}</h3>
      <div className="big">{n.calories}<small> kcal (estimated)</small></div>
      {rows.map(([k, v, mx]) => (
        <div key={k} className="row"><span>{k}</span><Bar value={v} max={mx} color="var(--turmeric)" /><b>{v} g</b></div>
      ))}
      <div className="row"><span>Health score</span><Bar value={n.health_score} color={scoreColor(n.health_score)} /><b>{n.health_score}/100</b></div>
      <Note>{n.label}. Values are approximate and not exact measurements.</Note>
    </div>
  );
}

/* ---------- pages ---------- */
function Home({ go }) {
  return (
    <div className="hero">
      <h1>FoodVerse</h1>
      <p className="sub">Multimodal Food Intelligence Platform</p>
      <p className="desc">Analyze food, understand nutrition, assess freshness, evaluate kitchen hygiene, and get personalized meal recommendations.</p>
      <div className="btns">
        <button onClick={() => go("analyze")}>Analyze Food</button>
        <button onClick={() => go("freshness")}>Check Freshness</button>
        <button onClick={() => go("hygiene")}>Kitchen Hygiene</button>
        <button onClick={() => go("cooking")}>Cooking Assistant</button>
        <button onClick={() => go("planner")}>Meal Planner</button>
      </div>
    </div>
  );
}

function Analyze() {
  const [res, setRes] = useState(null), [busy, setBusy] = useState(false), [err, setErr] = useState("");
  const run = async (f) => {
    setBusy(true); setErr(""); setRes(null);
    try { setRes(await postFile("/analyze-image", f)); } catch (e) { setErr(e.message); }
    setBusy(false);
  };
  return (
    <>
      <h2>Food Analysis</h2>
      <p className="lead">Upload a food photo to identify the dish and see its estimated nutrition.</p>
      <Upload accept="image/*" onFile={run} label="Choose a food image" />
      {busy && <p>Analyzing…</p>}
      <ErrorMsg msg={err} />
      {res && (
        <div className="grid2">
          <div className="card">
            <h3>Recognized food</h3>
            <div className="big">{res.food_name}</div>
            <div className="row"><span>Confidence</span><Bar value={res.confidence * 100} /><b>{Math.round(res.confidence * 100)}%</b></div>
            <Note>AI-generated recognition (demo model). Results may be inaccurate.</Note>
          </div>
          <NutritionCard n={res.nutrition} />
        </div>
      )}
    </>
  );
}

function Nutrition() {
  const [name, setName] = useState("Pizza"), [res, setRes] = useState(null), [err, setErr] = useState("");
  const run = async (e) => {
    e.preventDefault(); setErr("");
    try { setRes(await postJson("/nutrition", { food_name: name })); } catch (x) { setErr(x.message); }
  };
  return (
    <>
      <h2>Nutrition</h2>
      <p className="lead">Look up estimated nutrition by food name (try Pizza, Burger, Salad, Biryani, Dosa).</p>
      <form className="inline" onSubmit={run}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Food name" />
        <button>Get nutrition</button>
      </form>
      <ErrorMsg msg={err} />
      {res && <NutritionCard n={res} />}
    </>
  );
}

function Freshness() {
  const [res, setRes] = useState(null), [err, setErr] = useState("");
  const run = async (f) => {
    setErr(""); setRes(null);
    try { setRes(await postFile("/freshness", f)); } catch (e) { setErr(e.message); }
  };
  const color = res && (res.status === "Fresh" ? "var(--forest)" : res.status === "Moderately Fresh" ? "var(--turmeric)" : "var(--chili)");
  return (
    <>
      <h2>Freshness</h2>
      <p className="lead">Upload a photo of food for a visual freshness classification.</p>
      <Upload accept="image/*" onFile={run} label="Choose a food image" />
      <ErrorMsg msg={err} />
      {res && (
        <div className="card" style={{ borderLeft: "6px solid " + color }}>
          <h3>{res.status}</h3>
          <div className="row"><span>Confidence</span><Bar value={res.confidence * 100} color={color} /><b>{Math.round(res.confidence * 100)}%</b></div>
          <p>{res.explanation}</p>
          <p><b>Recommendation:</b> {res.recommendation}</p>
          <Note>{res.disclaimer}</Note>
        </div>
      )}
    </>
  );
}

function Hygiene() {
  const [res, setRes] = useState(null), [busy, setBusy] = useState(false), [err, setErr] = useState("");
  const run = async (f) => {
    setBusy(true); setErr(""); setRes(null);
    try { setRes(await postFile("/hygiene", f)); } catch (e) { setErr(e.message); }
    setBusy(false);
  };
  return (
    <>
      <h2>Restaurant Hygiene</h2>
      <p className="lead">Upload a short kitchen video to get a simulated hygiene assessment.</p>
      <Upload accept="video/*" isVideo onFile={run} label="Choose a kitchen video" />
      {busy && <p>Analyzing video…</p>}
      <ErrorMsg msg={err} />
      {res && (
        <div className="card">
          <h3>Kitchen Hygiene Score</h3>
          <div className="big" style={{ color: scoreColor(res.score) }}>{res.score}<small>/100</small></div>
          {res.observations.map((o) => (
            <div key={o.indicator} className="row">
              <span>{o.status === "ok" ? "✓" : "⚠"} {o.indicator}</span>
              <Bar value={o.score} color={scoreColor(o.score)} /><b>{o.note}</b>
            </div>
          ))}
          <Note>{res.disclaimer}</Note>
        </div>
      )}
    </>
  );
}

function Cooking() {
  const [q, setQ] = useState("Paneer, tomato, onion"), [res, setRes] = useState(null), [err, setErr] = useState("");
  const run = async (e) => {
    e.preventDefault(); setErr("");
    try { setRes(await postJson("/recipe", { query: q })); } catch (x) { setErr(x.message); }
  };
  return (
    <>
      <h2>Cooking Assistant</h2>
      <p className="lead">Enter a dish name or the ingredients you have.</p>
      <form className="inline" onSubmit={run}>
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="e.g. Aloo Gobi or egg, tomato" />
        <button>Get recipe</button>
      </form>
      <ErrorMsg msg={err} />
      {res && (
        <div className="card">
          <h3>{res.dish}</h3>
          <p><b>Cooking time:</b> {res.cooking_time}</p>
          <h4>Ingredients</h4>
          <p>{res.ingredients.join(", ")}</p>
          {res.missing.length > 0 && <p className="warn">You may still need: {res.missing.join(", ")}</p>}
          <h4>Steps</h4>
          <ol>{res.steps.map((s, i) => <li key={i}>{s}</li>)}</ol>
          <h4>Tips</h4>
          <ul>{res.tips.map((t, i) => <li key={i}>{t}</li>)}</ul>
          <Note>{res.note}</Note>
        </div>
      )}
    </>
  );
}

function Planner() {
  const [f, setF] = useState({ age: 21, goal: "Healthy eating", diet: "Vegetarian", preferences: "", meals_per_day: 3, days: 1 });
  const [res, setRes] = useState(null), [err, setErr] = useState("");
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });
  const run = async (e) => {
    e.preventDefault(); setErr("");
    try { setRes(await postJson("/meal-plan", { ...f, age: +f.age, meals_per_day: +f.meals_per_day, days: +f.days })); } catch (x) { setErr(x.message); }
  };
  return (
    <>
      <h2>Meal Planner</h2>
      <p className="lead">Tell us about your goal and get a simple meal plan.</p>
      <form className="card form" onSubmit={run}>
        <label>Age<input type="number" min="10" max="90" value={f.age} onChange={set("age")} /></label>
        <label>Goal
          <select value={f.goal} onChange={set("goal")}>
            <option>Weight loss</option><option>Weight gain</option><option>Maintenance</option><option>Healthy eating</option>
          </select></label>
        <label>Dietary preference
          <select value={f.diet} onChange={set("diet")}><option>Vegetarian</option><option>Non-vegetarian</option></select></label>
        <label>Food preferences<input value={f.preferences} onChange={set("preferences")} placeholder="e.g. paneer, oats" /></label>
        <label>Meals per day
          <select value={f.meals_per_day} onChange={set("meals_per_day")}><option>2</option><option>3</option><option>4</option><option>5</option></select></label>
        <label>Plan length
          <select value={f.days} onChange={set("days")}><option value="1">1 day</option><option value="7">7 days</option></select></label>
        <button>Generate plan</button>
      </form>
      <ErrorMsg msg={err} />
      {res && (
        <>
          <p className="lead">Daily target: about <b>{res.target_calories} kcal</b> ({res.goal}, {res.diet})</p>
          <div className="grid3">
            {res.plan.map((d) => (
              <div className="card" key={d.day}>
                <h3>Day {d.day}</h3>
                {d.meals.map((m, i) => <div className="meal" key={i}><b>{m.meal}</b><span>{m.item}</span><small>~{m.calories} kcal</small></div>)}
              </div>
            ))}
          </div>
          <Note>{res.disclaimer}</Note>
        </>
      )}
    </>
  );
}

function Dashboard() {
  const [d, setD] = useState(null), [err, setErr] = useState("");
  useEffect(() => { getJson("/dashboard").then(setD).catch((e) => setErr(e.message)); }, []);
  if (err) return <ErrorMsg msg={err} />;
  if (!d) return <p>Loading…</p>;
  const maxCal = Math.max(100, ...d.recent_nutrition.map((n) => n.calories));
  const T = d.totals;
  return (
    <>
      <h2>Dashboard</h2>
      <div className="stats">
        {[["Food analyses", T.food_analyses], ["Freshness checks", T.freshness_checks], ["Hygiene reports", T.hygiene_reports], ["Meal plans", T.meal_plans]]
          .map(([k, v]) => <div className="stat" key={k}><b>{v}</b><span>{k}</span></div>)}
      </div>
      <div className="grid2">
        <div className="card">
          <h3>Recent analyses: calories and health score</h3>
          {d.recent_nutrition.length === 0 && <p>No analyses yet. Try Food Analysis first.</p>}
          {d.recent_nutrition.map((n, i) => (
            <div key={i} className="row"><span>{n.food_name}</span><Bar value={n.calories} max={maxCal} color="var(--turmeric)" /><b>{n.calories} kcal · {n.health_score}</b></div>
          ))}
        </div>
        <div className="card">
          <h3>Latest results</h3>
          <p><b>Freshness:</b> {d.latest_freshness ? d.latest_freshness.status + " (" + Math.round(d.latest_freshness.confidence * 100) + "%)" : "none yet"}</p>
          <p><b>Kitchen hygiene:</b> {d.latest_hygiene ? d.latest_hygiene.score + "/100" : "none yet"}</p>
          <p><b>Meal plan:</b> {d.latest_meal_plan ? d.latest_meal_plan.goal + ", " + d.latest_meal_plan.target_calories + " kcal/day" : "none yet"}</p>
          {d.latest_meal_plan && d.latest_meal_plan.first_day.meals.map((m, i) => <div className="meal" key={i}><b>{m.meal}</b><span>{m.item}</span></div>)}
        </div>
      </div>
    </>
  );
}

/* ---------- app shell ---------- */
export default function App() {
  const [page, setPage] = useState("home");
  const views = { home: <Home go={setPage} />, dashboard: <Dashboard />, analyze: <Analyze />, nutrition: <Nutrition />,
    freshness: <Freshness />, hygiene: <Hygiene />, cooking: <Cooking />, planner: <Planner /> };
  return (
    <div className="shell">
      <aside>
        <div className="brand" onClick={() => setPage("home")}>FoodVerse</div>
        <nav>{PAGES.map(([k, l]) => <button key={k} className={page === k ? "active" : ""} onClick={() => setPage(k)}>{l}</button>)}</nav>
      </aside>
      <main key={page}>{views[page]}</main>
    </div>
  );
}
