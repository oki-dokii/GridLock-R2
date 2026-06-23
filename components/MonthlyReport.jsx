import { useState, useMemo } from "react";

// ─────────────────────────────────────────────────────────────────────────────
// AREA NAMES — sourced from:
//   GRIDLOCK_IMPLEMENTATION_GUIDE.md Appendix A (confirmed coords + names)
//   MASTER_RESEARCH_COMBINED.md §1.6 (chronic hotspot name list)
//   §1.4 station coverage areas for the remaining top cells
// Keys are "lat.toFixed(3),lon.toFixed(3)"
// ─────────────────────────────────────────────────────────────────────────────
const AREA_LOOKUP = {
  // Appendix A — confirmed name + coord pairs
  "12.981,77.610": { name: "Kamaraj Road, Sri Nagamma Devi Circle", station: "Shivajinagar" },
  "13.184,77.680": { name: "Sahakar Nagar Road, Fortune Acacia",    station: "Kodigehalli" },
  "12.940,77.696": { name: "HAL Old Airport Corridor",              station: "HAL Old Airport" },
  "12.996,77.669": { name: "New Horizon Rd, Embassy Tech Village",  station: "HAL Old Airport" },

  // §1.6 chronic list — station-matched by proximity
  "12.964,77.577": { name: "Mysore Road, SKR Market",               station: "City Market" },
  "12.977,77.576": { name: "6th Main Road, RK Puram (Gandhi Nagar)", station: "Upparpet" },
  "13.071,77.588": { name: "Chord Road, Manuvana",                  station: "Vijayanagara" },
  "12.934,77.691": { name: "MBT Road, Devasandra Junction",         station: "K.R. Pura" },
  "12.984,77.603": { name: "Main Guard Cross Road, Tasker Town",    station: "Shivajinagar" },
  "12.977,77.577": { name: "3rd Cross Road, Kempegowda Extension",  station: "Upparpet" },
  "12.973,77.579": { name: "5th Main Road, KG Circle",              station: "Upparpet" },
  "13.035,77.589": { name: "Meenakshi Koil Street",                 station: "Shivajinagar" },
  "12.984,77.604": { name: "Subedar Chatram Road, KG Circle",       station: "Upparpet" },
  "12.982,77.608": { name: "Dispensary Road, Shivaji Nagar",        station: "Shivajinagar" },
  "12.983,77.611": { name: "AS Char Main Road, Chickpet Circle",    station: "City Market" },
  "12.980,77.607": { name: "Bellary Road, Vinayaka Nagar",          station: "Hebbala" },
  "12.982,77.610": { name: "Commercial Street Junction",            station: "Shivajinagar" },
};

function areaInfo(lat, lon) {
  const key = `${lat.toFixed(3)},${lon.toFixed(3)}`;
  return AREA_LOOKUP[key] ?? { name: `Grid cell ${lat.toFixed(3)}, ${lon.toFixed(3)}`, station: "—" };
}

// ─────────────────────────────────────────────────────────────────────────────
// MONTHLY DATA — from DATA_ANALYSIS_RESULTS.md §P2.3
// Vehicle-type split scaled from 5-month totals (46.2% two-wheeler,
// 43.7% car/auto, 10.1% heavy) — no per-month vehicle breakdown in dataset.
// ─────────────────────────────────────────────────────────────────────────────
const TOTAL_VIOLATIONS = 298450;
const TW_TOTAL = 137866;
const CA_TOTAL = 130530;
const HV_TOTAL = 30054;
const PHAT_TOTAL = 20349; // officers with p̂ < 0.50 — from P1.6

function crore(n) {
  if (n >= 1e7)  return `₹${(n / 1e7).toFixed(2)} Cr`;
  if (n >= 1e5)  return `₹${(n / 1e5).toFixed(1)} L`;
  return `₹${n.toLocaleString("en-IN")}`;
}

function buildMonth(key, label, violations) {
  const f = violations / TOTAL_VIOLATIONS;
  const tw = Math.round(TW_TOTAL * f);
  const ca = Math.round(CA_TOTAL * f);
  const hv = Math.round(HV_TOTAL * f);
  return {
    key, label, violations,
    phatFilterCount:    Math.round(PHAT_TOTAL * f),
    twoWheelerCount:    tw,   twoWheelerRevenue: crore(tw * 1000),
    carAutoCount:       ca,   carAutoRevenue:    crore(ca * 1500),
    heavyCount:         hv,   heavyRevenue:      crore(hv * 1500),
    grossRevenue:       crore(tw * 1000 + ca * 1500 + hv * 1500),
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// PER-MONTH HOTSPOT DATA — computed from the real dataset CSV.
// Each key is "lat,lon" matching the chronic cell coords below.
// tickets    = actual violation count that month
// rawScore   = Σ PCS (PCU × temporal × severity) that month
// avgSev     = rawScore / tickets
// priorityScore (0–100) is stable — it is the lifetime EPS rank, not monthly.
// ─────────────────────────────────────────────────────────────────────────────
const MONTHLY_HOTSPOT_DATA = {
  nov2023: {
    "12.981,77.61":  { tickets: 559,  rawScore: 659.5,  avgSev: 1.180 },
    "13.184,77.68":  { tickets: 138,  rawScore: 238.5,  avgSev: 1.729 },
    "12.964,77.577": { tickets: 365,  rawScore: 374.6,  avgSev: 1.026 },
    "12.977,77.576": { tickets: 497,  rawScore: 408.2,  avgSev: 0.821 },
    "13.071,77.588": { tickets: 111,  rawScore: 86.0,   avgSev: 0.775 },
    "12.934,77.691": { tickets: 268,  rawScore: 210.6,  avgSev: 0.786 },
    "12.984,77.603": { tickets: 309,  rawScore: 326.6,  avgSev: 1.057 },
    "12.977,77.577": { tickets: 394,  rawScore: 402.0,  avgSev: 1.020 },
    "12.973,77.579": { tickets: 354,  rawScore: 239.2,  avgSev: 0.676 },
    "13.035,77.589": { tickets: 325,  rawScore: 265.4,  avgSev: 0.817 },
  },
  dec2023: {
    "12.981,77.61":  { tickets: 731,  rawScore: 877.6,  avgSev: 1.201 },
    "13.184,77.68":  { tickets: 451,  rawScore: 795.7,  avgSev: 1.764 },
    "12.964,77.577": { tickets: 530,  rawScore: 578.5,  avgSev: 1.091 },
    "12.977,77.576": { tickets: 728,  rawScore: 585.2,  avgSev: 0.804 },
    "13.071,77.588": { tickets: 442,  rawScore: 377.3,  avgSev: 0.854 },
    "12.934,77.691": { tickets: 365,  rawScore: 294.8,  avgSev: 0.808 },
    "12.984,77.603": { tickets: 298,  rawScore: 317.2,  avgSev: 1.064 },
    "12.977,77.577": { tickets: 351,  rawScore: 374.7,  avgSev: 1.068 },
    "12.973,77.579": { tickets: 377,  rawScore: 261.4,  avgSev: 0.693 },
    "13.035,77.589": { tickets: 605,  rawScore: 507.6,  avgSev: 0.839 },
  },
  jan2024: {
    "12.981,77.61":  { tickets: 951,  rawScore: 1159.1, avgSev: 1.219 },
    "13.184,77.68":  { tickets: 387,  rawScore: 697.5,  avgSev: 1.802 },
    "12.964,77.577": { tickets: 730,  rawScore: 762.2,  avgSev: 1.044 },
    "12.977,77.576": { tickets: 625,  rawScore: 481.4,  avgSev: 0.770 },
    "13.071,77.588": { tickets: 868,  rawScore: 773.8,  avgSev: 0.891 },
    "12.934,77.691": { tickets: 981,  rawScore: 685.5,  avgSev: 0.699 },
    "12.984,77.603": { tickets: 437,  rawScore: 527.4,  avgSev: 1.207 },
    "12.977,77.577": { tickets: 392,  rawScore: 415.9,  avgSev: 1.061 },
    "12.973,77.579": { tickets: 648,  rawScore: 497.0,  avgSev: 0.767 },
    "13.035,77.589": { tickets: 519,  rawScore: 445.7,  avgSev: 0.859 },
  },
  feb2024: {
    "12.981,77.61":  { tickets: 904,  rawScore: 1181.3, avgSev: 1.307 },
    "13.184,77.68":  { tickets: 394,  rawScore: 594.9,  avgSev: 1.510 },
    "12.964,77.577": { tickets: 836,  rawScore: 1020.9, avgSev: 1.221 },
    "12.977,77.576": { tickets: 455,  rawScore: 523.4,  avgSev: 1.150 },
    "13.071,77.588": { tickets: 945,  rawScore: 1065.3, avgSev: 1.127 },
    "12.934,77.691": { tickets: 951,  rawScore: 1178.9, avgSev: 1.240 },
    "12.984,77.603": { tickets: 176,  rawScore: 202.1,  avgSev: 1.148 },
    "12.977,77.577": { tickets: 233,  rawScore: 282.0,  avgSev: 1.210 },
    "12.973,77.579": { tickets: 409,  rawScore: 480.3,  avgSev: 1.174 },
    "13.035,77.589": { tickets: 390,  rawScore: 399.8,  avgSev: 1.025 },
  },
  mar2024: {
    "12.981,77.61":  { tickets: 977,  rawScore: 1307.4, avgSev: 1.338 },
    "13.184,77.68":  { tickets: 481,  rawScore: 673.7,  avgSev: 1.401 },
    "12.964,77.577": { tickets: 1072, rawScore: 1353.7, avgSev: 1.263 },
    "12.977,77.576": { tickets: 633,  rawScore: 694.5,  avgSev: 1.097 },
    "13.071,77.588": { tickets: 721,  rawScore: 838.2,  avgSev: 1.162 },
    "12.934,77.691": { tickets: 752,  rawScore: 757.3,  avgSev: 1.007 },
    "12.984,77.603": { tickets: 385,  rawScore: 428.9,  avgSev: 1.114 },
    "12.977,77.577": { tickets: 384,  rawScore: 446.8,  avgSev: 1.164 },
    "12.973,77.579": { tickets: 462,  rawScore: 447.6,  avgSev: 0.969 },
    "13.035,77.589": { tickets: 417,  rawScore: 448.3,  avgSev: 1.075 },
  },
  apr2024: {
    "12.981,77.61":  { tickets: 283,  rawScore: 359.9,  avgSev: 1.272 },
    "13.184,77.68":  { tickets: 75,   rawScore: 102.3,  avgSev: 1.365 },
    "12.964,77.577": { tickets: 210,  rawScore: 268.3,  avgSev: 1.278 },
    "12.977,77.576": { tickets: 244,  rawScore: 278.0,  avgSev: 1.139 },
    "13.071,77.588": { tickets: 193,  rawScore: 232.6,  avgSev: 1.205 },
    "12.934,77.691": { tickets: 26,   rawScore: 25.2,   avgSev: 0.969 },
    "12.984,77.603": { tickets: 46,   rawScore: 47.2,   avgSev: 1.026 },
    "12.977,77.577": { tickets: 153,  rawScore: 182.4,  avgSev: 1.192 },
    "12.973,77.579": { tickets: 117,  rawScore: 137.4,  avgSev: 1.175 },
    "13.035,77.589": { tickets: 28,   rawScore: 28.0,   avgSev: 1.000 },
  },
};

// ─────────────────────────────────────────────────────────────────────────────
// CHRONIC CELL DEFINITIONS — coords + lifetime priority score (stable).
// totalTickets / congestionScore / avgSeverity are filled per-month from
// MONTHLY_HOTSPOT_DATA above. The coord key must match that lookup.
// ─────────────────────────────────────────────────────────────────────────────
const CHRONIC_CELL_DEFS = [
  { rank:1,  lat:12.981, lon:77.610, coordKey:"12.981,77.61",  lifetimeCongestion:5918.7, priorityScore:100 },
  { rank:2,  lat:13.184, lon:77.680, coordKey:"13.184,77.68",  lifetimeCongestion:3009.5, priorityScore:84  },
  { rank:3,  lat:12.964, lon:77.577, coordKey:"12.964,77.577", lifetimeCongestion:2896.5, priorityScore:76  },
  { rank:4,  lat:12.977, lon:77.576, coordKey:"12.977,77.576", lifetimeCongestion:2450.8, priorityScore:64  },
  { rank:5,  lat:13.071, lon:77.588, coordKey:"13.071,77.588", lifetimeCongestion:2307.6, priorityScore:60  },
  { rank:6,  lat:12.934, lon:77.691, coordKey:"12.934,77.691", lifetimeCongestion:2196.8, priorityScore:57  },
  { rank:7,  lat:12.984, lon:77.603, coordKey:"12.984,77.603", lifetimeCongestion:1935.7, priorityScore:50  },
  { rank:8,  lat:12.977, lon:77.577, coordKey:"12.977,77.577", lifetimeCongestion:1898.6, priorityScore:49  },
  { rank:9,  lat:12.973, lon:77.579, coordKey:"12.973,77.579", lifetimeCongestion:1769.3, priorityScore:46  },
  { rank:10, lat:13.035, lon:77.589, coordKey:"13.035,77.589", lifetimeCongestion:1678.7, priorityScore:43  },
];

// Returns the chronic cells enriched with per-month actuals for the given month key
function getChronicCellsForMonth(monthKey) {
  const monthData = MONTHLY_HOTSPOT_DATA[monthKey] ?? {};
  return CHRONIC_CELL_DEFS.map(cell => {
    const m = monthData[cell.coordKey] ?? { tickets: 0, rawScore: 0, avgSev: 0 };
    return {
      ...cell,
      totalTickets:   m.tickets,
      congestionScore: m.rawScore,
      avgSeverity:    m.avgSev,
    };
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// MODEL EVALUATION IMAGE — one scatter plot image per month.
// April is the only one computed; other months show a placeholder message.
// ─────────────────────────────────────────────────────────────────────────────
const MODEL_EVAL_IMAGES = {
  apr2024: "predicted_vs_actual.png",
};

const MONTHS = [
  buildMonth("nov2023", "November 2023", 43504),
  buildMonth("dec2023", "December 2023", 63917),
  buildMonth("jan2024", "January 2024",  65479),
  buildMonth("feb2024", "February 2024", 54660),
  buildMonth("mar2024", "March 2024",    55453),
  buildMonth("apr2024", "April 2024",    15432),
];

// ─────────────────────────────────────────────────────────────────────────────
// SAMPLE RECORD GENERATOR
// Deterministic pseudo-random so records are stable per month/type.
// Replace with real API fetch when backend is connected.
// ─────────────────────────────────────────────────────────────────────────────
function lcg(seed) {
  let s = Math.abs(seed) % 0x7fffffff || 1;
  return () => { s = (s * 1664525 + 1013904223) & 0x7fffffff; return s / 0x7fffffff; };
}
function pick(arr, rng) { return arr[Math.floor(rng() * arr.length)]; }

const STATION_AREAS = {
  Shivajinagar:    ["Kamaraj Road", "Commercial Street", "Dispensary Road", "Main Guard Cross Rd", "Meenakshi Koil St"],
  Upparpet:        ["Gandhi Nagar 6th Main", "KG Circle", "3rd Cross Kempegowda Ext.", "Subedar Chatram Rd", "Chickpet Circle"],
  Malleshwaram:    ["Sampige Road", "8th Cross Malleshwaram", "Margosa Rd", "3rd Main"],
  "HAL Old Airport": ["Old Airport Road", "Domlur Layout", "Inner Ring Road", "New Horizon College Rd"],
  "City Market":   ["Mysore Road SKR Market", "KR Market", "Old Tharagupet", "Avenue Road"],
  Vijayanagara:    ["Chord Road Manuvana", "Magadi Main Rd", "4th Main Vijayanagara"],
  Kodigehalli:     ["Sahakar Nagar Rd", "Outer Ring Road Kodigehalli", "Kogilu Main Rd"],
  Rajajinagar:     ["BEL Road", "1st Block Rajajinagar", "Chord Road Rajajinagar"],
  "Magadi Road":   ["Magadi Road Main", "Agrahara Layout"],
  "K.R. Pura":     ["MBT Road Devasandra", "KR Pura Main Rd"],
};
const ALL_STATIONS = Object.keys(STATION_AREAS);

const VIOL_DATA  = ["Wrong Parking","No Parking","Main Road Parking","Footpath Parking","Near Bus Stop","Double Parking"];
const VEH_DATA   = ["Two-Wheeler","Two-Wheeler","Car/Auto","Car/Auto","Heavy Vehicle"];
const STAT_DATA  = ["Approved","Approved","Pending","Rejected"];
const GOOD_OFFS  = ["FKUSR00722","FKUSR00996","FKUSR01073","FKUSR00005","FKUSR02188","FKUSR00236","FKUSR01186"];
const BAD_OFFS   = ["FKUSR01810","FKUSR02046","FKUSR01593","FKUSR00926","FKUSR01903","FKUSR00617"];
const PHAT_MAP   = {
  FKUSR00722:0.96,FKUSR00996:0.95,FKUSR01073:0.95,FKUSR00005:0.94,FKUSR02188:0.93,FKUSR00236:0.94,FKUSR01186:0.93,
  FKUSR01810:0.13,FKUSR02046:0.16,FKUSR01593:0.17,FKUSR00926:0.19,FKUSR01903:0.21,FKUSR00617:0.22,
};

function generateRecords(monthKey, drawerType) {
  const seed = monthKey.split("").reduce((a, c) => a + c.charCodeAt(0), 0)
    + (drawerType === "flagged" ? 7919 : 0);
  const rng  = lcg(seed);
  const count = drawerType === "flagged" ? 64 : 100;
  const year  = monthKey.includes("2023") ? 2023 : 2024;
  const monthNum = { nov:11, dec:12, jan:1, feb:2, mar:3, apr:4 }[monthKey.slice(0,3)];
  const days = new Date(year, monthNum, 0).getDate();

  return Array.from({ length: count }, (_, i) => {
    const station    = pick(ALL_STATIONS, rng);
    const area       = pick(STATION_AREAS[station], rng);
    const day        = Math.floor(rng() * days) + 1;
    const hour       = Math.floor(rng() * 14) + 7;
    const min        = Math.floor(rng() * 60);
    const vehicleType   = pick(VEH_DATA, rng);
    const violationType = pick(VIOL_DATA, rng);
    const officer    = drawerType === "flagged" ? pick(BAD_OFFS, rng) : pick(GOOD_OFFS, rng);
    const status     = drawerType === "flagged" ? "Pending" : pick(STAT_DATA, rng);
    const phat       = PHAT_MAP[officer] ?? 0.85;
    const confBand   = phat < 0.20 ? "Very Low (< 20%)"
                     : phat < 0.35 ? "Low (20%–35%)"
                     :               "Below Threshold (35%–50%)";
    return {
      id: `VIO-${monthKey.toUpperCase().slice(0,6)}-${String(i+1).padStart(4,"0")}`,
      date: `${String(day).padStart(2,"0")}/${String(monthNum).padStart(2,"0")}/${year}`,
      time: `${String(hour).padStart(2,"0")}:${String(min).padStart(2,"0")}`,
      area, station, vehicleType, violationType, officer, status,
      phat: phat.toFixed(2), confBand,
    };
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// FILTER OPTIONS
// ─────────────────────────────────────────────────────────────────────────────
const F_STATIONS  = ["All Areas", ...ALL_STATIONS];
const F_VEHICLES  = ["All Vehicles", "Two-Wheeler", "Car/Auto", "Heavy Vehicle"];
const F_VIOLS     = ["All Violation Types", ...VIOL_DATA];
const F_STATUSES  = ["All Statuses", "Approved", "Pending", "Rejected"];
const F_CONF      = ["All Confidence Levels", "Very Low (< 20%)", "Low (20%–35%)", "Below Threshold (35%–50%)"];
const BLANK_FILT  = { station:"All Areas", vehicle:"All Vehicles", viol:"All Violation Types", status:"All Statuses", conf:"All Confidence Levels" };

// ─────────────────────────────────────────────────────────────────────────────
// TINY SHARED STYLES
// ─────────────────────────────────────────────────────────────────────────────
const TH = { padding:"10px 14px", textAlign:"left", fontWeight:600, fontSize:11, color:"#64748b", letterSpacing:"0.05em", whiteSpace:"nowrap" };
const TD = { padding:"11px 14px", color:"#374151", verticalAlign:"top" };
const SEL = {
  border:"1px solid #e2e8f0", borderRadius:8, padding:"7px 12px",
  fontSize:13, color:"#374151", background:"#fff", cursor:"pointer",
};

// ─────────────────────────────────────────────────────────────────────────────
// STATUS / CONFIDENCE BADGES
// ─────────────────────────────────────────────────────────────────────────────
function Badge({ label, color, bg }) {
  return <span style={{ background:bg, color, borderRadius:12, padding:"2px 10px", fontSize:11, fontWeight:600 }}>{label}</span>;
}
function StatusBadge({ s }) {
  const map = { Approved:["#166534","#dcfce7"], Pending:["#854d0e","#fef9c3"], Rejected:["#991b1b","#fee2e2"] };
  const [color, bg] = map[s] ?? ["#475569","#f1f5f9"];
  return <Badge label={s} color={color} bg={bg} />;
}
function ConfBadge({ phat }) {
  const v = parseFloat(phat);
  const [color,bg] = v<0.20 ? ["#991b1b","#fee2e2"] : v<0.35 ? ["#92400e","#fef3c7"] : ["#854d0e","#fef9c3"];
  return <Badge label={`p̂ = ${phat}`} color={color} bg={bg} />;
}

// ─────────────────────────────────────────────────────────────────────────────
// RECORDS DRAWER
// ─────────────────────────────────────────────────────────────────────────────
const PAGE_SIZE = 12;

function RecordsDrawer({ drawerType, monthKey, monthLabel, onClose }) {
  const [filt, setFilt]   = useState(BLANK_FILT);
  const [page, setPage]   = useState(0);

  const upFilt = (patch) => { setFilt(f => ({...f, ...patch})); setPage(0); };

  const all = useMemo(() => generateRecords(monthKey, drawerType), [monthKey, drawerType]);

  const filtered = useMemo(() => all.filter(r => {
    if (filt.station !== "All Areas"           && r.station     !== filt.station)  return false;
    if (filt.vehicle !== "All Vehicles"        && r.vehicleType !== filt.vehicle)  return false;
    if (filt.viol    !== "All Violation Types" && r.violationType !== filt.viol)   return false;
    if (drawerType === "all"    && filt.status !== "All Statuses"          && r.status    !== filt.status)   return false;
    if (drawerType === "flagged"&& filt.conf   !== "All Confidence Levels" && r.confBand  !== filt.conf)     return false;
    return true;
  }), [all, filt, drawerType]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const rows = filtered.slice(page * PAGE_SIZE, (page+1) * PAGE_SIZE);

  const title    = drawerType === "all" ? "All Ticket Records" : "Incomplete & Flagged Records";
  const subtitle = drawerType === "flagged"
    ? "Cases the system removed from the dispatch map. Officer confidence score (p̂) was below 0.50."
    : "Every ticket logged this month. Use the filters below to narrow down by area, vehicle, or status.";

  return (
    <>
      {/* Backdrop */}
      <div onClick={onClose} style={{ position:"fixed", inset:0, background:"rgba(0,0,0,0.4)", zIndex:200 }} />

      {/* Drawer */}
      <div style={{
        position:"fixed", top:0, right:0, bottom:0,
        width:"min(860px, 100vw)",
        background:"#fff", zIndex:201,
        display:"flex", flexDirection:"column",
        boxShadow:"-6px 0 40px rgba(0,0,0,0.15)",
        fontFamily:"'Inter','Segoe UI',system-ui,sans-serif",
      }}>

        {/* Header */}
        <div style={{ padding:"20px 24px 16px", borderBottom:"1px solid #e2e8f0", flexShrink:0 }}>
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"flex-start", gap:12 }}>
            <div>
              <h2 style={{ margin:"0 0 4px", fontSize:18, fontWeight:700, color:"#0f172a" }}>{title}</h2>
              <p style={{ margin:0, fontSize:13, color:"#64748b", lineHeight:1.5 }}>{subtitle}</p>
              <p style={{ margin:"6px 0 0", fontSize:11, color:"#94a3b8" }}>
                {monthLabel} · Showing {filtered.length} of {all.length} records
                {" "}·{" "}
                <em>Sample data — replace with live API response when backend is connected</em>
              </p>
            </div>
            <button onClick={onClose} style={{ ...SEL, flexShrink:0, color:"#374151" }}>
              ✕  Close
            </button>
          </div>
        </div>

        {/* Filter bar */}
        <div style={{ display:"flex", gap:8, flexWrap:"wrap", padding:"12px 20px", background:"#f8fafc", borderBottom:"1px solid #e2e8f0", flexShrink:0 }}>
          <select style={SEL} value={filt.station} onChange={e => upFilt({station:e.target.value})}>
            {F_STATIONS.map(s => <option key={s}>{s}</option>)}
          </select>
          <select style={SEL} value={filt.vehicle} onChange={e => upFilt({vehicle:e.target.value})}>
            {F_VEHICLES.map(v => <option key={v}>{v}</option>)}
          </select>
          <select style={SEL} value={filt.viol} onChange={e => upFilt({viol:e.target.value})}>
            {F_VIOLS.map(v => <option key={v}>{v}</option>)}
          </select>
          {drawerType === "all" ? (
            <select style={SEL} value={filt.status} onChange={e => upFilt({status:e.target.value})}>
              {F_STATUSES.map(s => <option key={s}>{s}</option>)}
            </select>
          ) : (
            <select style={SEL} value={filt.conf} onChange={e => upFilt({conf:e.target.value})}>
              {F_CONF.map(c => <option key={c}>{c}</option>)}
            </select>
          )}
          <button
            onClick={() => { setFilt(BLANK_FILT); setPage(0); }}
            style={{ ...SEL, marginLeft:"auto", color:"#64748b" }}
          >
            Reset
          </button>
        </div>

        {/* Table */}
        <div style={{ flex:1, overflowY:"auto" }}>
          {rows.length === 0 ? (
            <div style={{ padding:60, textAlign:"center", color:"#94a3b8", fontSize:14 }}>
              No records match the selected filters.
            </div>
          ) : (
            <table style={{ width:"100%", borderCollapse:"collapse", fontSize:13 }}>
              <thead>
                <tr style={{ background:"#f8fafc", borderBottom:"2px solid #e2e8f0", position:"sticky", top:0 }}>
                  <th style={TH}>Record ID</th>
                  <th style={TH}>Date & Time</th>
                  <th style={TH}>Area</th>
                  <th style={TH}>Station</th>
                  <th style={TH}>Vehicle</th>
                  <th style={TH}>Violation</th>
                  <th style={TH}>Officer</th>
                  <th style={TH}>{drawerType === "all" ? "Status" : "Confidence"}</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r, i) => (
                  <tr key={r.id} style={{ background: i%2===0 ? "#fff" : "#fafbfc", borderBottom:"1px solid #f1f5f9" }}>
                    <td style={TD}><span style={{ fontFamily:"monospace", fontSize:11, color:"#94a3b8" }}>{r.id}</span></td>
                    <td style={TD}>
                      <div style={{ fontWeight:500, color:"#0f172a" }}>{r.date}</div>
                      <div style={{ fontSize:11, color:"#94a3b8", marginTop:2 }}>{r.time}</div>
                    </td>
                    <td style={{ ...TD, maxWidth:200 }}>
                      <div style={{ color:"#0f172a", fontWeight:500, lineHeight:1.3 }}>{r.area}</div>
                    </td>
                    <td style={TD}><span style={{ fontSize:12, color:"#64748b" }}>{r.station}</span></td>
                    <td style={TD}>{r.vehicleType}</td>
                    <td style={TD}>{r.violationType}</td>
                    <td style={TD}><span style={{ fontFamily:"monospace", fontSize:11 }}>{r.officer}</span></td>
                    <td style={TD}>
                      {drawerType === "all"
                        ? <StatusBadge s={r.status} />
                        : <ConfBadge phat={r.phat} />
                      }
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Pagination */}
        <div style={{
          display:"flex", justifyContent:"space-between", alignItems:"center",
          padding:"12px 24px", borderTop:"1px solid #e2e8f0", flexShrink:0,
          background:"#fafbfc",
        }}>
          <span style={{ fontSize:13, color:"#64748b" }}>
            Page {page+1} of {totalPages}
          </span>
          <div style={{ display:"flex", gap:8 }}>
            <button
              disabled={page === 0}
              onClick={() => setPage(p => p-1)}
              style={{ ...SEL, color: page===0 ? "#cbd5e1" : "#374151", cursor: page===0 ? "not-allowed" : "pointer" }}
            >← Prev</button>
            <button
              disabled={page >= totalPages-1}
              onClick={() => setPage(p => p+1)}
              style={{ ...SEL, color: page>=totalPages-1 ? "#cbd5e1" : "#374151", cursor: page>=totalPages-1 ? "not-allowed" : "pointer" }}
            >Next →</button>
          </div>
        </div>
      </div>
    </>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// STAT CARD
// ─────────────────────────────────────────────────────────────────────────────
function StatCard({ label, value, subtitle, muted, onClick }) {
  const [hov, setHov] = useState(false);
  return (
    <div
      onClick={!muted ? onClick : undefined}
      onMouseEnter={() => !muted && setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        background: muted ? "#f8f9fa" : "#fff",
        border: `1px solid ${hov ? "#2563eb" : "#e2e8f0"}`,
        borderRadius:10, padding:"20px 24px", flex:1, minWidth:0,
        cursor: muted ? "default" : "pointer",
        boxShadow: hov ? "0 0 0 2px #bfdbfe" : "none",
        transition:"border-color 0.15s, box-shadow 0.15s",
      }}
    >
      <div style={{ display:"flex", justifyContent:"space-between", alignItems:"flex-start", marginBottom:8 }}>
        <span style={{ fontSize:11, fontWeight:600, letterSpacing:"0.08em", textTransform:"uppercase", color: muted ? "#94a3b8" : "#2563eb" }}>
          {label}
        </span>
        {!muted && <span style={{ fontSize:11, color:"#2563eb", fontWeight:500 }}>View records →</span>}
      </div>
      <div style={{ fontSize: muted ? 28 : 36, fontWeight:700, color: muted ? "#94a3b8" : "#0f172a", lineHeight:1.1, marginBottom:8, wordBreak:"break-word" }}>
        {value}
      </div>
      <div style={{ fontSize:13, color:"#64748b", lineHeight:1.5 }}>{subtitle}</div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// PRIORITY BAR
// ─────────────────────────────────────────────────────────────────────────────
function PriorityBar({ score }) {
  return (
    <div style={{ display:"flex", alignItems:"center", gap:8 }}>
      <div style={{ width:72, height:6, background:"#e2e8f0", borderRadius:3, overflow:"hidden" }}>
        <div style={{
          width:`${score}%`, height:"100%", borderRadius:3,
          background: score>=80 ? "#dc2626" : score>=50 ? "#d97706" : "#2563eb",
        }} />
      </div>
      <span style={{ fontSize:13, fontWeight:600, color:"#0f172a", minWidth:28 }}>{score}</span>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// REVENUE ROW
// ─────────────────────────────────────────────────────────────────────────────
function RevenueRow({ label, sublabel, value, isTotal }) {
  return (
    <div style={{
      display:"flex", justifyContent:"space-between", alignItems:"center",
      padding: isTotal ? "16px 20px" : "14px 20px",
      background: isTotal ? "#f8faff" : "#fff",
      borderTop: isTotal ? "2px solid #e2e8f0" : "1px solid #f1f5f9",
    }}>
      <div>
        <div style={{ fontSize: isTotal?15:14, fontWeight: isTotal?700:400, color:"#0f172a" }}>{label}</div>
        {sublabel && <div style={{ fontSize:12, color:"#64748b", marginTop:2 }}>{sublabel}</div>}
      </div>
      <div style={{ fontSize: isTotal?20:15, fontWeight:700, color: isTotal?"#0f172a":"#374151" }}>{value}</div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// MODEL EVALUATION SECTION — responds to the selected month
// ─────────────────────────────────────────────────────────────────────────────
function ModelEvalSection({ monthKey, monthLabel }) {
  const imgSrc = MODEL_EVAL_IMAGES[monthKey];

  return (
    <div style={{
      background:"rgba(30,41,59,0.04)", border:"1px solid #e2e8f0",
      borderRadius:16, padding:24, marginBottom:20,
    }}>
      <h2 style={{ fontSize:18, fontWeight:700, color:"#0f172a", marginBottom:8 }}>
        Model Evaluation: Predicted vs Actual Validations (Holdout Set)
      </h2>
      <p style={{ fontSize:13, color:"#64748b", marginBottom:20, lineHeight:1.6 }}>
        {imgSrc
          ? `Scatter plot showing correlation between GridLock's predicted hotspots and actual verified holdout violations for ${monthLabel}.`
          : `Scatter plot for ${monthLabel} has not been generated yet. The model was evaluated on the April 2024 holdout window — switch to April 2024 to view the chart.`
        }
      </p>
      {imgSrc ? (
        <div style={{ display:"flex", justifyContent:"center", background:"#fff", borderRadius:8, padding:16 }}>
          <img
            src={imgSrc}
            alt={`Predicted vs Actual Violations — ${monthLabel}`}
            style={{ maxWidth:"100%", height:"auto", borderRadius:4 }}
          />
        </div>
      ) : (
        <div style={{
          display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center",
          height:180, background:"#f8fafc", borderRadius:8,
          border:"2px dashed #e2e8f0", gap:10,
        }}>
          <span style={{ fontSize:32 }}>📊</span>
          <p style={{ fontSize:14, color:"#94a3b8", margin:0, textAlign:"center" }}>
            No holdout evaluation available for {monthLabel}.
          </p>
          <p style={{ fontSize:12, color:"#cbd5e1", margin:0 }}>
            Switch to <strong style={{ color:"#64748b" }}>April 2024</strong> to see the validation scatter plot.
          </p>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// MAIN COMPONENT
// ─────────────────────────────────────────────────────────────────────────────
export default function MonthlyReport({ reportData } = {}) {
  const isControlled = !!reportData;
  const [selKey, setSelKey]       = useState("jan2024");
  const [drawer, setDrawer]       = useState(null); // null | "all" | "flagged"

  const monthData = MONTHS.find(m => m.key === selKey) ?? MONTHS[2];
  const d = isControlled ? { ...monthData, ...reportData } : monthData;

  // Per-month hotspot data — recomputed whenever selKey changes
  const chronicCells = useMemo(() => getChronicCellsForMonth(selKey), [selKey]);

  return (
    <div style={{ fontFamily:"'Inter','Segoe UI',system-ui,sans-serif", background:"#f1f5f9", minHeight:"100vh", padding:"32px 24px" }}>
      <div style={{ maxWidth:900, margin:"0 auto" }}>

        {/* ── PAGE HEADER ──────────────────────────────────────── */}
        <div style={{ background:"#fff", border:"1px solid #e2e8f0", borderRadius:12, padding:"24px 32px", marginBottom:20 }}>
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"flex-start", flexWrap:"wrap", gap:12 }}>
            <div>
              <div style={{ fontSize:11, fontWeight:600, letterSpacing:"0.1em", textTransform:"uppercase", color:"#64748b", marginBottom:6 }}>
                Official Summary
              </div>
              <h1 style={{ fontSize:26, fontWeight:700, color:"#0f172a", margin:0, lineHeight:1.2 }}>
                Monthly Parking Enforcement Report
              </h1>
            </div>
            <div style={{ display:"flex", alignItems:"center", gap:10, flexShrink:0, flexWrap:"wrap" }}>
              {!isControlled && (
                <select
                  value={selKey}
                  onChange={e => { setSelKey(e.target.value); setDrawer(null); }}
                  style={{
                    border:"1px solid #e2e8f0", borderRadius:20, padding:"6px 32px 6px 16px",
                    fontSize:14, color:"#374151", fontWeight:500, background:"#fff",
                    cursor:"pointer", appearance:"none",
                    backgroundImage:"url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E\")",
                    backgroundRepeat:"no-repeat", backgroundPosition:"right 10px center",
                  }}
                >
                  {MONTHS.map(m => <option key={m.key} value={m.key}>{m.label}</option>)}
                </select>
              )}
              <button style={{ background:"#0f172a", color:"#fff", border:"none", borderRadius:8, padding:"8px 16px", fontSize:14, fontWeight:500, cursor:"pointer" }}>
                Download Report
              </button>
            </div>
          </div>
        </div>

        {/* ── STAT CARDS ───────────────────────────────────────── */}
        <div style={{ display:"flex", gap:16, marginBottom:20, flexWrap:"wrap" }}>
          <StatCard
            label="Tickets Logged This Month"
            value={d.violations.toLocaleString("en-IN")}
            subtitle="Total parking violations recorded and sent for review"
            onClick={() => setDrawer("all")}
          />
          <StatCard
            label="Incomplete Records Removed"
            value={d.phatFilterCount.toLocaleString("en-IN")}
            subtitle="Cases flagged as low-quality or unverifiable — not shown on the dispatch map"
            onClick={() => setDrawer("flagged")}
          />
          <StatCard
            label="More Stats Coming Soon"
            value="—"
            subtitle="Additional metrics will appear here in a future update"
            muted
          />
        </div>

        {/* ── HOTSPOT TABLE ─────────────────────────────────────── */}
        <div style={{ background:"#fff", border:"1px solid #e2e8f0", borderRadius:12, marginBottom:20, overflow:"hidden" }}>
          <div style={{ padding:"24px 28px 16px" }}>
            <h2 style={{ fontSize:18, fontWeight:700, color:"#2563eb", margin:"0 0 6px" }}>
              Locations That Are Always a Problem
            </h2>
            <p style={{ fontSize:14, color:"#475569", margin:0, lineHeight:1.6 }}>
              These spots appeared in the top 50 worst locations every single month — they need permanent attention, not just occasional patrols.
              Showing figures for <strong>{d.label}</strong>.
            </p>
          </div>
          <div style={{ overflowX:"auto" }}>
            <table style={{ width:"100%", borderCollapse:"collapse", fontSize:13 }}>
              <thead>
                <tr style={{ background:"#f8fafc", borderTop:"1px solid #e2e8f0", borderBottom:"1px solid #e2e8f0" }}>
                  {["#", "Location", "Coordinates", "Raw Score", "Total Tickets", "Avg Severity", 
                    <span title="Composite of vehicle-type PCU, time-of-day weight, and violation-type severity. Literature-derived proxy, not a measured traffic metric." style={{ cursor: "help", borderBottom: "1px dotted #64748b" }}>Congestion Impact Score (0-100) ⓘ</span>
                  ].map((h, i) => (
                    <th key={i} style={{ ...TH, textAlign: h==="#" ? "center" : "left" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {chronicCells.map((cell, i) => {
                  const info = areaInfo(cell.lat, cell.lon);
                  return (
                    <tr key={cell.rank} style={{ background: i%2===0 ? "#fff" : "#fafbfc", borderBottom:"1px solid #f1f5f9" }}>
                      <td style={{ ...TD, textAlign:"center", fontWeight:700, color:"#0f172a" }}>{cell.rank}</td>
                      <td style={TD}>
                        <div style={{ fontWeight:600, color:"#0f172a", lineHeight:1.3 }}>{info.name}</div>
                        <div style={{ fontSize:11, color:"#64748b", marginTop:2 }}>{info.station} Police Station</div>
                      </td>
                      <td style={TD}>
                        <span style={{ fontFamily:"monospace", fontSize:11, color:"#94a3b8" }}>
                          {cell.lat.toFixed(3)}, {cell.lon.toFixed(3)}
                        </span>
                      </td>
                      <td style={{ ...TD, fontWeight:600, color:"#0f172a" }}>
                        {cell.congestionScore === 0
                          ? <span style={{ color:"#94a3b8" }}>—</span>
                          : cell.congestionScore.toLocaleString("en-IN", { maximumFractionDigits:1 })}
                      </td>
                      <td style={TD}>
                        {cell.totalTickets === 0
                          ? <span style={{ color:"#94a3b8" }}>—</span>
                          : cell.totalTickets.toLocaleString("en-IN")}
                      </td>
                      <td style={TD}>
                        {cell.avgSeverity === 0
                          ? <span style={{ color:"#94a3b8" }}>—</span>
                          : cell.avgSeverity.toFixed(3)}
                      </td>
                      <td style={TD}><PriorityBar score={cell.priorityScore} /></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          <div style={{ padding:"12px 28px", borderTop:"1px solid #f1f5f9" }}>
            <p style={{ fontSize:12, color:"#64748b", margin:0, fontStyle:"italic" }}>
              Congestion Impact Score of 100 = highest urgency. Deploy here first.
              Congestion scores and ticket counts are cumulative over the full dataset — these locations are chronic across all months.
            </p>
          </div>
        </div>

        {/* ── REVENUE SECTION ───────────────────────────────────── */}
        <div style={{ background:"#fff", border:"1px solid #e2e8f0", borderRadius:12, marginBottom:20, overflow:"hidden" }}>
          <div style={{ padding:"24px 28px 16px" }}>
            <h2 style={{ fontSize:18, fontWeight:700, color:"#2563eb", margin:"0 0 6px" }}>
              How Much Can Be Collected This Month
            </h2>
            <p style={{ fontSize:14, color:"#475569", margin:0, lineHeight:1.6 }}>
              Based on the number of tickets logged, here is the estimated fine amount if all violations are processed.
            </p>
          </div>
          <div style={{ border:"1px solid #e2e8f0", borderRadius:8, margin:"0 24px 20px", overflow:"hidden" }}>
            <RevenueRow label="Two-wheelers (bikes & scooters)" sublabel={`${d.twoWheelerCount.toLocaleString("en-IN")} tickets × ₹1,000 per ticket`} value={d.twoWheelerRevenue} />
            <RevenueRow label="Cars & auto-rickshaws"           sublabel={`${d.carAutoCount.toLocaleString("en-IN")} tickets × ₹1,500 per ticket`}  value={d.carAutoRevenue} />
            <RevenueRow label="Heavy vehicles (buses & trucks)" sublabel={`${d.heavyCount.toLocaleString("en-IN")} tickets × ₹1,500 per ticket`}    value={d.heavyRevenue} />
            <RevenueRow label="Total Estimated Collection" value={d.grossRevenue} isTotal />
          </div>
          <div style={{ padding:"0 28px 20px" }}>
            <p style={{ fontSize:12, color:"#64748b", margin:0, fontStyle:"italic" }}>
              This is a maximum estimate. Actual collection depends on case approvals.
              Vehicle split estimated from full-dataset proportions (46.2% two-wheelers, 43.7% cars/autos, 10.1% heavy).
            </p>
          </div>
        </div>

        {/* ── FOOTER ───────────────────────────────────────────── */}
        <div style={{ textAlign:"center", padding:"16px", fontSize:13, color:"#94a3b8", borderTop:"1px solid #e2e8f0" }}>
          Bengaluru Traffic Police &nbsp;|&nbsp; Powered by GridLock Enforcement Intelligence
        </div>
      </div>

      {/* ── RECORDS DRAWER (portal-style) ────────────────────── */}
      {drawer && (
        <RecordsDrawer
          drawerType={drawer}
          monthKey={d.key}
          monthLabel={d.label}
          onClose={() => setDrawer(null)}
        />
      )}
    </div>
  );
}
