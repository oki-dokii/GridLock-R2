"use strict";

function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
function ownKeys(e, r) { var t = Object.keys(e); if (Object.getOwnPropertySymbols) { var o = Object.getOwnPropertySymbols(e); r && (o = o.filter(function (r) { return Object.getOwnPropertyDescriptor(e, r).enumerable; })), t.push.apply(t, o); } return t; }
function _objectSpread(e) { for (var r = 1; r < arguments.length; r++) { var t = null != arguments[r] ? arguments[r] : {}; r % 2 ? ownKeys(Object(t), !0).forEach(function (r) { _defineProperty(e, r, t[r]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(t)) : ownKeys(Object(t)).forEach(function (r) { Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(t, r)); }); } return e; }
function _defineProperty(e, r, t) { return (r = _toPropertyKey(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: !0, configurable: !0, writable: !0 }) : e[r] = t, e; }
function _toPropertyKey(t) { var i = _toPrimitive(t, "string"); return "symbol" == _typeof(i) ? i : i + ""; }
function _toPrimitive(t, r) { if ("object" != _typeof(t) || !t) return t; var e = t[Symbol.toPrimitive]; if (void 0 !== e) { var i = e.call(t, r || "default"); if ("object" != _typeof(i)) return i; throw new TypeError("@@toPrimitive must return a primitive value."); } return ("string" === r ? String : Number)(t); }
function _slicedToArray(r, e) { return _arrayWithHoles(r) || _iterableToArrayLimit(r, e) || _unsupportedIterableToArray(r, e) || _nonIterableRest(); }
function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _unsupportedIterableToArray(r, a) { if (r) { if ("string" == typeof r) return _arrayLikeToArray(r, a); var t = {}.toString.call(r).slice(8, -1); return "Object" === t && r.constructor && (t = r.constructor.name), "Map" === t || "Set" === t ? Array.from(r) : "Arguments" === t || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _arrayLikeToArray(r, a) : void 0; } }
function _arrayLikeToArray(r, a) { (null == a || a > r.length) && (a = r.length); for (var e = 0, n = Array(a); e < a; e++) n[e] = r[e]; return n; }
function _iterableToArrayLimit(r, l) { var t = null == r ? null : "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (null != t) { var e, n, i, u, a = [], f = !0, o = !1; try { if (i = (t = t.call(r)).next, 0 === l) { if (Object(t) !== t) return; f = !1; } else for (; !(f = (e = i.call(t)).done) && (a.push(e.value), a.length !== l); f = !0); } catch (r) { o = !0, n = r; } finally { try { if (!f && null != t["return"] && (u = t["return"](), Object(u) !== u)) return; } finally { if (o) throw n; } } return a; } }
function _arrayWithHoles(r) { if (Array.isArray(r)) return r; }
var _React = React,
  useState = _React.useState,
  useMemo = _React.useMemo;

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// AREA NAMES â€” sourced from:
//   GRIDLOCK_IMPLEMENTATION_GUIDE.md Appendix A (confirmed coords + names)
//   MASTER_RESEARCH_COMBINED.md Â§1.6 (chronic hotspot name list)
//   Â§1.4 station coverage areas for the remaining top cells
// Keys are "lat.toFixed(3),lon.toFixed(3)"
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
var AREA_LOOKUP = {
  // Appendix A â€” confirmed name + coord pairs
  "12.981,77.610": {
    name: "Kamaraj Road, Sri Nagamma Devi Circle",
    station: "Shivajinagar"
  },
  "13.184,77.680": {
    name: "Sahakar Nagar Road, Fortune Acacia",
    station: "Kodigehalli"
  },
  "12.940,77.696": {
    name: "HAL Old Airport Corridor",
    station: "HAL Old Airport"
  },
  "12.996,77.669": {
    name: "New Horizon Rd, Embassy Tech Village",
    station: "HAL Old Airport"
  },
  // Â§1.6 chronic list â€” station-matched by proximity
  "12.964,77.577": {
    name: "Mysore Road, SKR Market",
    station: "City Market"
  },
  "12.977,77.576": {
    name: "6th Main Road, RK Puram (Gandhi Nagar)",
    station: "Upparpet"
  },
  "13.071,77.588": {
    name: "Chord Road, Manuvana",
    station: "Vijayanagara"
  },
  "12.934,77.691": {
    name: "MBT Road, Devasandra Junction",
    station: "K.R. Pura"
  },
  "12.984,77.603": {
    name: "Main Guard Cross Road, Tasker Town",
    station: "Shivajinagar"
  },
  "12.977,77.577": {
    name: "3rd Cross Road, Kempegowda Extension",
    station: "Upparpet"
  },
  "12.973,77.579": {
    name: "5th Main Road, KG Circle",
    station: "Upparpet"
  },
  "13.035,77.589": {
    name: "Meenakshi Koil Street",
    station: "Shivajinagar"
  },
  "12.984,77.604": {
    name: "Subedar Chatram Road, KG Circle",
    station: "Upparpet"
  },
  "12.982,77.608": {
    name: "Dispensary Road, Shivaji Nagar",
    station: "Shivajinagar"
  },
  "12.983,77.611": {
    name: "AS Char Main Road, Chickpet Circle",
    station: "City Market"
  },
  "12.980,77.607": {
    name: "Bellary Road, Vinayaka Nagar",
    station: "Hebbala"
  },
  "12.982,77.610": {
    name: "Commercial Street Junction",
    station: "Shivajinagar"
  }
};
function areaInfo(lat, lon) {
  var _AREA_LOOKUP$key;
  var key = "".concat(lat.toFixed(3), ",").concat(lon.toFixed(3));
  return (_AREA_LOOKUP$key = AREA_LOOKUP[key]) !== null && _AREA_LOOKUP$key !== void 0 ? _AREA_LOOKUP$key : {
    name: "Grid cell ".concat(lat.toFixed(3), ", ").concat(lon.toFixed(3)),
    station: "â€”"
  };
}

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// MONTHLY DATA â€” from DATA_ANALYSIS_RESULTS.md Â§P2.3
// Vehicle-type split scaled from 5-month totals (46.2% two-wheeler,
// 43.7% car/auto, 10.1% heavy) â€” no per-month vehicle breakdown in dataset.
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
var TOTAL_VIOLATIONS = 298450;
var TW_TOTAL = 137866;
var CA_TOTAL = 130530;
var HV_TOTAL = 30054;
var PHAT_TOTAL = 20349; // officers with pÌ‚ < 0.50 â€” from P1.6

function crore(n) {
  if (n >= 1e7) return "\u20B9".concat((n / 1e7).toFixed(2), " Cr");
  if (n >= 1e5) return "\u20B9".concat((n / 1e5).toFixed(1), " L");
  return "\u20B9".concat(n.toLocaleString("en-IN"));
}
function buildMonth(key, label, violations) {
  var f = violations / TOTAL_VIOLATIONS;
  var tw = Math.round(TW_TOTAL * f);
  var ca = Math.round(CA_TOTAL * f);
  var hv = Math.round(HV_TOTAL * f);
  return {
    key: key,
    label: label,
    violations: violations,
    phatFilterCount: Math.round(PHAT_TOTAL * f),
    twoWheelerCount: tw,
    twoWheelerRevenue: crore(tw * 1000),
    carAutoCount: ca,
    carAutoRevenue: crore(ca * 1500),
    heavyCount: hv,
    heavyRevenue: crore(hv * 1500),
    grossRevenue: crore(tw * 1000 + ca * 1500 + hv * 1500)
  };
}

// â”€â”€ PER-MONTH HOTSPOT DATA (computed from real dataset CSV) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
var MONTHLY_HOTSPOT_DATA = {
  nov2023: {
    "12.981,77.61":  { tickets:559,  rawScore:659.5,  avgSev:1.180 },
    "13.184,77.68":  { tickets:138,  rawScore:238.5,  avgSev:1.729 },
    "12.964,77.577": { tickets:365,  rawScore:374.6,  avgSev:1.026 },
    "12.977,77.576": { tickets:497,  rawScore:408.2,  avgSev:0.821 },
    "13.071,77.588": { tickets:111,  rawScore:86.0,   avgSev:0.775 },
    "12.934,77.691": { tickets:268,  rawScore:210.6,  avgSev:0.786 },
    "12.984,77.603": { tickets:309,  rawScore:326.6,  avgSev:1.057 },
    "12.977,77.577": { tickets:394,  rawScore:402.0,  avgSev:1.020 },
    "12.973,77.579": { tickets:354,  rawScore:239.2,  avgSev:0.676 },
    "13.035,77.589": { tickets:325,  rawScore:265.4,  avgSev:0.817 }
  },
  dec2023: {
    "12.981,77.61":  { tickets:731,  rawScore:877.6,  avgSev:1.201 },
    "13.184,77.68":  { tickets:451,  rawScore:795.7,  avgSev:1.764 },
    "12.964,77.577": { tickets:530,  rawScore:578.5,  avgSev:1.091 },
    "12.977,77.576": { tickets:728,  rawScore:585.2,  avgSev:0.804 },
    "13.071,77.588": { tickets:442,  rawScore:377.3,  avgSev:0.854 },
    "12.934,77.691": { tickets:365,  rawScore:294.8,  avgSev:0.808 },
    "12.984,77.603": { tickets:298,  rawScore:317.2,  avgSev:1.064 },
    "12.977,77.577": { tickets:351,  rawScore:374.7,  avgSev:1.068 },
    "12.973,77.579": { tickets:377,  rawScore:261.4,  avgSev:0.693 },
    "13.035,77.589": { tickets:605,  rawScore:507.6,  avgSev:0.839 }
  },
  jan2024: {
    "12.981,77.61":  { tickets:951,  rawScore:1159.1, avgSev:1.219 },
    "13.184,77.68":  { tickets:387,  rawScore:697.5,  avgSev:1.802 },
    "12.964,77.577": { tickets:730,  rawScore:762.2,  avgSev:1.044 },
    "12.977,77.576": { tickets:625,  rawScore:481.4,  avgSev:0.770 },
    "13.071,77.588": { tickets:868,  rawScore:773.8,  avgSev:0.891 },
    "12.934,77.691": { tickets:981,  rawScore:685.5,  avgSev:0.699 },
    "12.984,77.603": { tickets:437,  rawScore:527.4,  avgSev:1.207 },
    "12.977,77.577": { tickets:392,  rawScore:415.9,  avgSev:1.061 },
    "12.973,77.579": { tickets:648,  rawScore:497.0,  avgSev:0.767 },
    "13.035,77.589": { tickets:519,  rawScore:445.7,  avgSev:0.859 }
  },
  feb2024: {
    "12.981,77.61":  { tickets:904,  rawScore:1181.3, avgSev:1.307 },
    "13.184,77.68":  { tickets:394,  rawScore:594.9,  avgSev:1.510 },
    "12.964,77.577": { tickets:836,  rawScore:1020.9, avgSev:1.221 },
    "12.977,77.576": { tickets:455,  rawScore:523.4,  avgSev:1.150 },
    "13.071,77.588": { tickets:945,  rawScore:1065.3, avgSev:1.127 },
    "12.934,77.691": { tickets:951,  rawScore:1178.9, avgSev:1.240 },
    "12.984,77.603": { tickets:176,  rawScore:202.1,  avgSev:1.148 },
    "12.977,77.577": { tickets:233,  rawScore:282.0,  avgSev:1.210 },
    "12.973,77.579": { tickets:409,  rawScore:480.3,  avgSev:1.174 },
    "13.035,77.589": { tickets:390,  rawScore:399.8,  avgSev:1.025 }
  },
  mar2024: {
    "12.981,77.61":  { tickets:977,  rawScore:1307.4, avgSev:1.338 },
    "13.184,77.68":  { tickets:481,  rawScore:673.7,  avgSev:1.401 },
    "12.964,77.577": { tickets:1072, rawScore:1353.7, avgSev:1.263 },
    "12.977,77.576": { tickets:633,  rawScore:694.5,  avgSev:1.097 },
    "13.071,77.588": { tickets:721,  rawScore:838.2,  avgSev:1.162 },
    "12.934,77.691": { tickets:752,  rawScore:757.3,  avgSev:1.007 },
    "12.984,77.603": { tickets:385,  rawScore:428.9,  avgSev:1.114 },
    "12.977,77.577": { tickets:384,  rawScore:446.8,  avgSev:1.164 },
    "12.973,77.579": { tickets:462,  rawScore:447.6,  avgSev:0.969 },
    "13.035,77.589": { tickets:417,  rawScore:448.3,  avgSev:1.075 }
  },
  apr2024: {
    "12.981,77.61":  { tickets:283,  rawScore:359.9,  avgSev:1.272 },
    "13.184,77.68":  { tickets:75,   rawScore:102.3,  avgSev:1.365 },
    "12.964,77.577": { tickets:210,  rawScore:268.3,  avgSev:1.278 },
    "12.977,77.576": { tickets:244,  rawScore:278.0,  avgSev:1.139 },
    "13.071,77.588": { tickets:193,  rawScore:232.6,  avgSev:1.205 },
    "12.934,77.691": { tickets:26,   rawScore:25.2,   avgSev:0.969 },
    "12.984,77.603": { tickets:46,   rawScore:47.2,   avgSev:1.026 },
    "12.977,77.577": { tickets:153,  rawScore:182.4,  avgSev:1.192 },
    "12.973,77.579": { tickets:117,  rawScore:137.4,  avgSev:1.175 },
    "13.035,77.589": { tickets:28,   rawScore:28.0,   avgSev:1.000 }
  }
};

var CHRONIC_CELL_DEFS = [
  { rank:1,  lat:12.981, lon:77.610, coordKey:"12.981,77.61",  priorityScore:100 },
  { rank:2,  lat:13.184, lon:77.680, coordKey:"13.184,77.68",  priorityScore:84  },
  { rank:3,  lat:12.964, lon:77.577, coordKey:"12.964,77.577", priorityScore:76  },
  { rank:4,  lat:12.977, lon:77.576, coordKey:"12.977,77.576", priorityScore:64  },
  { rank:5,  lat:13.071, lon:77.588, coordKey:"13.071,77.588", priorityScore:60  },
  { rank:6,  lat:12.934, lon:77.691, coordKey:"12.934,77.691", priorityScore:57  },
  { rank:7,  lat:12.984, lon:77.603, coordKey:"12.984,77.603", priorityScore:50  },
  { rank:8,  lat:12.977, lon:77.577, coordKey:"12.977,77.577", priorityScore:49  },
  { rank:9,  lat:12.973, lon:77.579, coordKey:"12.973,77.579", priorityScore:46  },
  { rank:10, lat:13.035, lon:77.589, coordKey:"13.035,77.589", priorityScore:43  }
];

function getChronicCellsForMonth(monthKey) {
  var monthData = MONTHLY_HOTSPOT_DATA[monthKey] || {};
  return CHRONIC_CELL_DEFS.map(function(cell) {
    var m = monthData[cell.coordKey] || { tickets:0, rawScore:0, avgSev:0 };
    return _objectSpread(_objectSpread({}, cell), {}, {
      totalTickets: m.tickets,
      congestionScore: m.rawScore,
      avgSeverity: m.avgSev
    });
  });
}

var MODEL_EVAL_IMAGES = {
  nov2023: "predicted_vs_actual_nov2023.png",
  dec2023: "predicted_vs_actual_dec2023.png",
  jan2024: "predicted_vs_actual_jan2024.png",
  feb2024: "predicted_vs_actual_feb2024.png",
  mar2024: "predicted_vs_actual_mar2024.png",
  apr2024: "predicted_vs_actual.png"
};


var MONTHS = [buildMonth("nov2023", "November 2023", 43504), buildMonth("dec2023", "December 2023", 63917), buildMonth("jan2024", "January 2024", 65479), buildMonth("feb2024", "February 2024", 54660), buildMonth("mar2024", "March 2024", 55453), buildMonth("apr2024", "April 2024", 15432)];

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// SAMPLE RECORD GENERATOR
// Deterministic pseudo-random so records are stable per month/type.
// Replace with real API fetch when backend is connected.
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function lcg(seed) {
  var s = Math.abs(seed) % 0x7fffffff || 1;
  return function () {
    s = s * 1664525 + 1013904223 & 0x7fffffff;
    return s / 0x7fffffff;
  };
}
function pick(arr, rng) {
  return arr[Math.floor(rng() * arr.length)];
}
var STATION_AREAS = {
  Shivajinagar: ["Kamaraj Road", "Commercial Street", "Dispensary Road", "Main Guard Cross Rd", "Meenakshi Koil St"],
  Upparpet: ["Gandhi Nagar 6th Main", "KG Circle", "3rd Cross Kempegowda Ext.", "Subedar Chatram Rd", "Chickpet Circle"],
  Malleshwaram: ["Sampige Road", "8th Cross Malleshwaram", "Margosa Rd", "3rd Main"],
  "HAL Old Airport": ["Old Airport Road", "Domlur Layout", "Inner Ring Road", "New Horizon College Rd"],
  "City Market": ["Mysore Road SKR Market", "KR Market", "Old Tharagupet", "Avenue Road"],
  Vijayanagara: ["Chord Road Manuvana", "Magadi Main Rd", "4th Main Vijayanagara"],
  Kodigehalli: ["Sahakar Nagar Rd", "Outer Ring Road Kodigehalli", "Kogilu Main Rd"],
  Rajajinagar: ["BEL Road", "1st Block Rajajinagar", "Chord Road Rajajinagar"],
  "Magadi Road": ["Magadi Road Main", "Agrahara Layout"],
  "K.R. Pura": ["MBT Road Devasandra", "KR Pura Main Rd"]
};
var ALL_STATIONS = Object.keys(STATION_AREAS);
var VIOL_DATA = ["Wrong Parking", "No Parking", "Main Road Parking", "Footpath Parking", "Near Bus Stop", "Double Parking"];
var VEH_DATA = ["Two-Wheeler", "Two-Wheeler", "Car/Auto", "Car/Auto", "Heavy Vehicle"];
var STAT_DATA = ["Approved", "Approved", "Pending", "Rejected"];
var GOOD_OFFS = ["FKUSR00722", "FKUSR00996", "FKUSR01073", "FKUSR00005", "FKUSR02188", "FKUSR00236", "FKUSR01186"];
var BAD_OFFS = ["FKUSR01810", "FKUSR02046", "FKUSR01593", "FKUSR00926", "FKUSR01903", "FKUSR00617"];
var PHAT_MAP = {
  FKUSR00722: 0.96,
  FKUSR00996: 0.95,
  FKUSR01073: 0.95,
  FKUSR00005: 0.94,
  FKUSR02188: 0.93,
  FKUSR00236: 0.94,
  FKUSR01186: 0.93,
  FKUSR01810: 0.13,
  FKUSR02046: 0.16,
  FKUSR01593: 0.17,
  FKUSR00926: 0.19,
  FKUSR01903: 0.21,
  FKUSR00617: 0.22
};
function generateRecords(monthKey, drawerType) {
  var seed = monthKey.split("").reduce(function (a, c) {
    return a + c.charCodeAt(0);
  }, 0) + (drawerType === "flagged" ? 7919 : 0);
  var rng = lcg(seed);
  var count = drawerType === "flagged" ? 64 : 100;
  var year = monthKey.includes("2023") ? 2023 : 2024;
  var monthNum = {
    nov: 11,
    dec: 12,
    jan: 1,
    feb: 2,
    mar: 3,
    apr: 4
  }[monthKey.slice(0, 3)];
  var days = new Date(year, monthNum, 0).getDate();
  return Array.from({
    length: count
  }, function (_, i) {
    var _PHAT_MAP$officer;
    var station = pick(ALL_STATIONS, rng);
    var area = pick(STATION_AREAS[station], rng);
    var day = Math.floor(rng() * days) + 1;
    var hour = Math.floor(rng() * 14) + 7;
    var min = Math.floor(rng() * 60);
    var vehicleType = pick(VEH_DATA, rng);
    var violationType = pick(VIOL_DATA, rng);
    var officer = drawerType === "flagged" ? pick(BAD_OFFS, rng) : pick(GOOD_OFFS, rng);
    var status = drawerType === "flagged" ? "Pending" : pick(STAT_DATA, rng);
    var phat = (_PHAT_MAP$officer = PHAT_MAP[officer]) !== null && _PHAT_MAP$officer !== void 0 ? _PHAT_MAP$officer : 0.85;
    var confBand = phat < 0.20 ? "Very Low (< 20%)" : phat < 0.35 ? "Low (20%â€“35%)" : "Below Threshold (35%â€“50%)";
    return {
      id: "VIO-".concat(monthKey.toUpperCase().slice(0, 6), "-").concat(String(i + 1).padStart(4, "0")),
      date: "".concat(String(day).padStart(2, "0"), "/").concat(String(monthNum).padStart(2, "0"), "/").concat(year),
      time: "".concat(String(hour).padStart(2, "0"), ":").concat(String(min).padStart(2, "0")),
      area: area,
      station: station,
      vehicleType: vehicleType,
      violationType: violationType,
      officer: officer,
      status: status,
      phat: phat.toFixed(2),
      confBand: confBand
    };
  });
}

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// FILTER OPTIONS
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
var F_STATIONS = ["All Areas"].concat(ALL_STATIONS);
var F_VEHICLES = ["All Vehicles", "Two-Wheeler", "Car/Auto", "Heavy Vehicle"];
var F_VIOLS = ["All Violation Types"].concat(VIOL_DATA);
var F_STATUSES = ["All Statuses", "Approved", "Pending", "Rejected"];
var F_CONF = ["All Confidence Levels", "Very Low (< 20%)", "Low (20%â€“35%)", "Below Threshold (35%â€“50%)"];
var BLANK_FILT = {
  station: "All Areas",
  vehicle: "All Vehicles",
  viol: "All Violation Types",
  status: "All Statuses",
  conf: "All Confidence Levels"
};

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// TINY SHARED STYLES
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
var TH = {
  padding: "10px 14px",
  textAlign: "left",
  fontWeight: 600,
  fontSize: 11,
  color: "#475569",
  letterSpacing: "0.06em",
  textTransform: "uppercase",
  whiteSpace: "nowrap",
  background: "#111827",
  borderBottom: "1px solid rgba(255,255,255,0.08)"
};
var TD = {
  padding: "11px 14px",
  color: "#cbd5e1",
  verticalAlign: "top",
  borderBottom: "1px solid rgba(255,255,255,0.05)"
};
var SEL = {
  border: "1px solid rgba(255,255,255,0.12)",
  borderRadius: 8,
  padding: "7px 12px",
  fontSize: 13,
  color: "#e2e8f0",
  background: "rgba(30,41,59,0.8)",
  cursor: "pointer",
  outline: "none"
};

function downloadPDF(d) {
  var doc = new window.jspdf.jsPDF();
  
  var now = new Date();
  var dd = String(now.getDate()).padStart(2, '0');
  var mm = String(now.getMonth() + 1).padStart(2, '0');
  var yyyy = now.getFullYear();
  var dateStr = dd + '-' + mm + '-' + yyyy;

  // LaTeX article style title page elements
  var pageWidth = doc.internal.pageSize.getWidth();
  
  doc.setFont("times", "bold");
  doc.setFontSize(20);
  doc.text("GridLock Monthly Parking Enforcement Report", pageWidth / 2, 30, { align: 'center' });
  
  doc.setFontSize(14);
  doc.setFont("times", "normal");
  doc.text("Bengaluru Traffic Police", pageWidth / 2, 42, { align: 'center' });
  
  doc.setFontSize(12);
  doc.text(dateStr, pageWidth / 2, 50, { align: 'center' });

  // Abstract / Header Info
  doc.setFontSize(11);
  doc.text("Reporting Month: " + d.label, 14, 65);

  // Section 1
  doc.setFontSize(14);
  doc.setFont("times", "bold");
  doc.text("1   Summary Statistics", 14, 78);

  doc.autoTable({
    startY: 82,
    theme: 'plain',
    styles: { font: 'times', fontSize: 11, textColor: [0, 0, 0], halign: 'center' },
    headStyles: { fontStyle: 'bold', fontSize: 11, lineWidth: { top: 1.0, bottom: 0.5 }, halign: 'center' },
    footStyles: { lineWidth: { bottom: 1.0 } },
    head: [['Metric', 'Value']],
    body: [
      ['Total Violations Logged', d.violations.toLocaleString("en-IN")],
      ['Incomplete Records Removed', d.phatFilterCount.toLocaleString("en-IN")]
    ],
    foot: [['','']],
    margin: { left: 40, right: 40 }
  });

  // Section 2
  var startY2 = doc.lastAutoTable.finalY + 15;
  doc.setFontSize(14);
  doc.setFont("times", "bold");
  doc.text("2   Revenue Breakdown", 14, startY2);

  doc.autoTable({
    startY: startY2 + 5,
    theme: 'plain',
    styles: { font: 'times', fontSize: 11, textColor: [0, 0, 0] },
    headStyles: { fontStyle: 'bold', fontSize: 11, lineWidth: { top: 1.0, bottom: 0.5 } },
    footStyles: { lineWidth: { bottom: 1.0 } },
    head: [['Vehicle Type', 'Ticket Count', 'Fine Rate', 'Estimated Revenue']],
    body: [
      ['Two-Wheelers', d.twoWheelerCount.toLocaleString("en-IN"), '\u20B91,000', d.twoWheelerRevenue],
      ['Cars & Autos', d.carAutoCount.toLocaleString("en-IN"), '\u20B91,500', d.carAutoRevenue],
      ['Heavy Vehicles', d.heavyCount.toLocaleString("en-IN"), '\u20B91,500', d.heavyRevenue]
    ],
    foot: [
      ['Total Collection Estimate', '', '', d.grossRevenue]
    ],
    margin: { left: 20, right: 20 }
  });

  var hotspotRows = getChronicCellsForMonth(d.key).map(function(cell) {
    var info = areaInfo(cell.lat, cell.lon);
    return [
      cell.rank,
      info.name,
      info.station,
      cell.lat.toFixed(3) + ", " + cell.lon.toFixed(3),
      cell.congestionScore > 0 ? cell.congestionScore.toLocaleString("en-IN", {maximumFractionDigits:1}) : "â€”",
      cell.totalTickets > 0 ? cell.totalTickets.toLocaleString("en-IN") : "â€”",
      cell.avgSeverity > 0 ? cell.avgSeverity.toFixed(3) : "â€”",
      cell.priorityScore
    ];
  });

  // Section 3
  doc.addPage();
  doc.setFontSize(14);
  doc.setFont("times", "bold");
  doc.text("3   Appendix: Top 10 Chronic Hotspots", 14, 25);

  doc.autoTable({
    startY: 30,
    theme: 'plain',
    styles: { font: 'times', fontSize: 9.5, textColor: [0, 0, 0], cellPadding: 2.5 },
    headStyles: { fontStyle: 'bold', fontSize: 10, lineWidth: { top: 1.0, bottom: 0.5 } },
    footStyles: { lineWidth: { bottom: 1.0 } },
    head: [['Rank', 'Location', 'Station', 'Coordinates', 'Cong. Score', 'Tickets', 'Severity', 'Priority']],
    body: hotspotRows,
    foot: [['','','','','','','','']]
  });

  doc.save("gridlock-report-" + d.key + ".pdf");
}

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// STATUS / CONFIDENCE BADGES
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function Badge(_ref) {
  var label = _ref.label,
    color = _ref.color,
    bg = _ref.bg;
  return /*#__PURE__*/React.createElement("span", {
    style: {
      background: bg,
      color: color,
      borderRadius: 12,
      padding: "2px 10px",
      fontSize: 11,
      fontWeight: 600
    }
  }, label);
}
function StatusBadge(_ref2) {
  var _map$s;
  var s = _ref2.s;
  var map = {
    Approved: ["#166534", "#dcfce7"],
    Pending: ["#854d0e", "#fef9c3"],
    Rejected: ["#991b1b", "#fee2e2"]
  };
  var _ref3 = (_map$s = map[s]) !== null && _map$s !== void 0 ? _map$s : ["#475569", "#f1f5f9"],
    _ref4 = _slicedToArray(_ref3, 2),
    color = _ref4[0],
    bg = _ref4[1];
  return /*#__PURE__*/React.createElement(Badge, {
    label: s,
    color: color,
    bg: bg
  });
}
function ConfBadge(_ref5) {
  var phat = _ref5.phat;
  var v = parseFloat(phat);
  var _ref6 = v < 0.20 ? ["#991b1b", "#fee2e2"] : v < 0.35 ? ["#92400e", "#fef3c7"] : ["#854d0e", "#fef9c3"],
    _ref7 = _slicedToArray(_ref6, 2),
    color = _ref7[0],
    bg = _ref7[1];
  return /*#__PURE__*/React.createElement(Badge, {
    label: "p\u0302 = ".concat(phat),
    color: color,
    bg: bg
  });
}

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// RECORDS DRAWER
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
var PAGE_SIZE = 12;
function RecordsDrawer(_ref8) {
  var drawerType = _ref8.drawerType,
    monthKey = _ref8.monthKey,
    monthLabel = _ref8.monthLabel,
    onClose = _ref8.onClose;
  var _useState = useState(BLANK_FILT),
    _useState2 = _slicedToArray(_useState, 2),
    filt = _useState2[0],
    setFilt = _useState2[1];
  var _useState3 = useState(0),
    _useState4 = _slicedToArray(_useState3, 2),
    page = _useState4[0],
    setPage = _useState4[1];
  var upFilt = function upFilt(patch) {
    setFilt(function (f) {
      return _objectSpread(_objectSpread({}, f), patch);
    });
    setPage(0);
  };
  var all = useMemo(function () {
    return generateRecords(monthKey, drawerType);
  }, [monthKey, drawerType]);
  var filtered = useMemo(function () {
    return all.filter(function (r) {
      if (filt.station !== "All Areas" && r.station !== filt.station) return false;
      if (filt.vehicle !== "All Vehicles" && r.vehicleType !== filt.vehicle) return false;
      if (filt.viol !== "All Violation Types" && r.violationType !== filt.viol) return false;
      if (drawerType === "all" && filt.status !== "All Statuses" && r.status !== filt.status) return false;
      if (drawerType === "flagged" && filt.conf !== "All Confidence Levels" && r.confBand !== filt.conf) return false;
      return true;
    });
  }, [all, filt, drawerType]);
  var totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  var rows = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);
  var title = drawerType === "all" ? "All Ticket Records" : "Incomplete & Flagged Records";
  var subtitle = drawerType === "flagged" ? "Cases the system removed from the dispatch map. Officer confidence score (pÌ‚) was below 0.50." : "Every ticket logged this month. Use the filters below to narrow down by area, vehicle, or status.";
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    onClick: onClose,
    style: {
      position: "fixed",
      inset: 0,
      background: "rgba(0,0,0,0.65)",
      zIndex: 200,
      backdropFilter: "blur(4px)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "fixed",
      top: 0,
      right: 0,
      bottom: 0,
      width: "min(860px, 100vw)",
      background: "#0f172a",
      border: "1px solid rgba(255,255,255,0.1)",
      zIndex: 201,
      display: "flex",
      flexDirection: "column",
      boxShadow: "-8px 0 48px rgba(0,0,0,0.6)",
      fontFamily: "'Inter','Segoe UI',system-ui,sans-serif"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "20px 24px 16px",
      borderBottom: "1px solid rgba(255,255,255,0.08)",
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "flex-start",
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h2", {
    style: {
      margin: "0 0 4px",
      fontSize: 18,
      fontWeight: 700,
      color: "#f1f5f9"
    }
  }, title), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 13,
      color: "#94a3b8",
      lineHeight: 1.5
    }
  }, subtitle), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "6px 0 0",
      fontSize: 11,
      color: "#475569"
    }
  }, monthLabel, " \xB7 Showing ", filtered.length, " of ", all.length, " records", " ", "\xB7", " ", /*#__PURE__*/React.createElement("em", null, "Sample data \u2014 replace with live API response when backend is connected"))), /*#__PURE__*/React.createElement("button", {
    onClick: onClose,
    style: _objectSpread(_objectSpread({}, SEL), {}, {
      flexShrink: 0,
      color: "#e2e8f0",
      fontWeight: 600
    })
  }, "\u2715  Close"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 8,
      flexWrap: "wrap",
      padding: "12px 20px",
      background: "rgba(0,0,0,0.3)",
      borderBottom: "1px solid rgba(255,255,255,0.06)",
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("select", {
    style: SEL,
    value: filt.station,
    onChange: function onChange(e) {
      return upFilt({
        station: e.target.value
      });
    }
  }, F_STATIONS.map(function (s) {
    return /*#__PURE__*/React.createElement("option", {
      key: s
    }, s);
  })), /*#__PURE__*/React.createElement("select", {
    style: SEL,
    value: filt.vehicle,
    onChange: function onChange(e) {
      return upFilt({
        vehicle: e.target.value
      });
    }
  }, F_VEHICLES.map(function (v) {
    return /*#__PURE__*/React.createElement("option", {
      key: v
    }, v);
  })), /*#__PURE__*/React.createElement("select", {
    style: SEL,
    value: filt.viol,
    onChange: function onChange(e) {
      return upFilt({
        viol: e.target.value
      });
    }
  }, F_VIOLS.map(function (v) {
    return /*#__PURE__*/React.createElement("option", {
      key: v
    }, v);
  })), drawerType === "all" ? /*#__PURE__*/React.createElement("select", {
    style: SEL,
    value: filt.status,
    onChange: function onChange(e) {
      return upFilt({
        status: e.target.value
      });
    }
  }, F_STATUSES.map(function (s) {
    return /*#__PURE__*/React.createElement("option", {
      key: s
    }, s);
  })) : /*#__PURE__*/React.createElement("select", {
    style: SEL,
    value: filt.conf,
    onChange: function onChange(e) {
      return upFilt({
        conf: e.target.value
      });
    }
  }, F_CONF.map(function (c) {
    return /*#__PURE__*/React.createElement("option", {
      key: c
    }, c);
  })), /*#__PURE__*/React.createElement("button", {
    onClick: function onClick() {
      setFilt(BLANK_FILT);
      setPage(0);
    },
    style: _objectSpread(_objectSpread({}, SEL), {}, {
      marginLeft: "auto",
      color: "#94a3b8"
    })
  }, "Reset")), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      overflowY: "auto"
    }
  }, rows.length === 0 ? /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 60,
      textAlign: "center",
      color: "#475569",
      fontSize: 14
    }
  }, "No records match the selected filters.") : /*#__PURE__*/React.createElement("table", {
    style: {
      width: "100%",
      borderCollapse: "collapse",
      fontSize: 13
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
    style: {
      background: "#111827",
      borderBottom: "1px solid rgba(255,255,255,0.08)",
      position: "sticky",
      top: 0
    }
  }, /*#__PURE__*/React.createElement("th", {
    style: TH
  }, "Record ID"), /*#__PURE__*/React.createElement("th", {
    style: TH
  }, "Date & Time"), /*#__PURE__*/React.createElement("th", {
    style: TH
  }, "Area"), /*#__PURE__*/React.createElement("th", {
    style: TH
  }, "Station"), /*#__PURE__*/React.createElement("th", {
    style: TH
  }, "Vehicle"), /*#__PURE__*/React.createElement("th", {
    style: TH
  }, "Violation"), /*#__PURE__*/React.createElement("th", {
    style: TH
  }, "Officer"), /*#__PURE__*/React.createElement("th", {
    style: TH
  }, drawerType === "all" ? "Status" : "Confidence"))), /*#__PURE__*/React.createElement("tbody", null, rows.map(function (r, i) {
    return /*#__PURE__*/React.createElement("tr", {
      key: r.id,
      style: {
        background: i % 2 === 0 ? "transparent" : "rgba(255,255,255,0.02)"
      }
    }, /*#__PURE__*/React.createElement("td", {
      style: TD
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: "monospace",
        fontSize: 11,
        color: "#94a3b8"
      }
    }, r.id)), /*#__PURE__*/React.createElement("td", {
      style: TD
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontWeight: 500,
        color: "#f1f5f9"
      }
    }, r.date), /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 11,
        color: "#94a3b8",
        marginTop: 2
      }
    }, r.time)), /*#__PURE__*/React.createElement("td", {
      style: _objectSpread(_objectSpread({}, TD), {}, {
        maxWidth: 200
      })
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        color: "#e2e8f0",
        fontWeight: 500,
        lineHeight: 1.3
      }
    }, r.area)), /*#__PURE__*/React.createElement("td", {
      style: TD
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 12,
        color: "#64748b"
      }
    }, r.station)), /*#__PURE__*/React.createElement("td", {
      style: TD
    }, r.vehicleType), /*#__PURE__*/React.createElement("td", {
      style: TD
    }, r.violationType), /*#__PURE__*/React.createElement("td", {
      style: TD
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: "monospace",
        fontSize: 11
      }
    }, r.officer)), /*#__PURE__*/React.createElement("td", {
      style: TD
    }, drawerType === "all" ? /*#__PURE__*/React.createElement(StatusBadge, {
      s: r.status
    }) : /*#__PURE__*/React.createElement(ConfBadge, {
      phat: r.phat
    })));
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      padding: "12px 24px",
      borderTop: "1px solid rgba(255,255,255,0.08)",
      flexShrink: 0,
      background: "rgba(0,0,0,0.3)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      color: "#475569"
    }
  }, "Page ", page + 1, " of ", totalPages), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("button", {
    disabled: page === 0,
    onClick: function onClick() {
      return setPage(function (p) {
        return p - 1;
      });
    },
    style: _objectSpread(_objectSpread({}, SEL), {}, {
      color: page === 0 ? "#334155" : "#e2e8f0",
      cursor: page === 0 ? "not-allowed" : "pointer",
      opacity: page === 0 ? 0.5 : 1
    })
  }, "\u2190 Prev"), /*#__PURE__*/React.createElement("button", {
    disabled: page >= totalPages - 1,
    onClick: function onClick() {
      return setPage(function (p) {
        return p + 1;
      });
    },
    style: _objectSpread(_objectSpread({}, SEL), {}, {
      color: page >= totalPages - 1 ? "#334155" : "#e2e8f0",
      cursor: page >= totalPages - 1 ? "not-allowed" : "pointer",
      opacity: page >= totalPages - 1 ? 0.5 : 1
    })
  }, "Next \u2192")))));
}

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// STAT CARD
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function StatCard(_ref9) {
  var label = _ref9.label,
    value = _ref9.value,
    subtitle = _ref9.subtitle,
    muted = _ref9.muted,
    onClick = _ref9.onClick;
  var _useState5 = useState(false),
    _useState6 = _slicedToArray(_useState5, 2),
    hov = _useState6[0],
    setHov = _useState6[1];
  return /*#__PURE__*/React.createElement("div", {
    onClick: !muted ? onClick : undefined,
    onMouseEnter: function onMouseEnter() {
      return !muted && setHov(true);
    },
    onMouseLeave: function onMouseLeave() {
      return setHov(false);
    },
    style: {
      background: muted ? "rgba(30,41,59,0.4)" : "rgba(15,23,42,0.7)",
      backdropFilter: "blur(12px)",
      border: "1px solid ".concat(hov ? "rgba(59,130,246,0.6)" : "rgba(255,255,255,0.08)"),
      borderRadius: 12,
      padding: "20px 24px",
      flex: 1,
      minWidth: 0,
      cursor: muted ? "default" : "pointer",
      boxShadow: hov ? "0 0 0 2px rgba(59,130,246,0.3), 0 8px 32px rgba(0,0,0,0.4)" : "0 4px 20px rgba(0,0,0,0.3)",
      transition: "border-color 0.15s, box-shadow 0.15s"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "flex-start",
      marginBottom: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 10,
      fontWeight: 700,
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      color: muted ? "#334155" : "#3b82f6"
    }
  }, label), !muted && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 11,
      color: "#2563eb",
      fontWeight: 500
    }
  }, "View records \u2192")), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: muted ? 28 : 36,
      fontWeight: 700,
      color: muted ? "#334155" : "#f1f5f9",
      lineHeight: 1.1,
      marginBottom: 8,
      wordBreak: "break-word"
    }
  }, value), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      color: "#64748b",
      lineHeight: 1.5
    }
  }, subtitle));
}

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// PRIORITY BAR
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function PriorityBar(_ref0) {
  var score = _ref0.score;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 72,
      height: 6,
      background: "#1e293b",
      borderRadius: 3,
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: "".concat(score, "%"),
      height: "100%",
      borderRadius: 3,
      background: score >= 80 ? "#dc2626" : score >= 50 ? "#d97706" : "#2563eb"
    }
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      fontWeight: 700,
      color: "#e2e8f0",
      minWidth: 28
    }
  }, score));
}

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// REVENUE ROW
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function RevenueRow(_ref1) {
  var label = _ref1.label,
    sublabel = _ref1.sublabel,
    value = _ref1.value,
    isTotal = _ref1.isTotal;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      padding: isTotal ? "16px 20px" : "14px 20px",
      background: isTotal ? "rgba(59,130,246,0.08)" : "transparent",
      borderTop: isTotal ? "1px solid rgba(59,130,246,0.2)" : "1px solid rgba(255,255,255,0.05)"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: isTotal ? 15 : 14,
      fontWeight: isTotal ? 700 : 400,
      color: "#e2e8f0"
    }
  }, label), sublabel && /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      color: "#64748b",
      marginTop: 2
    }
  }, sublabel)), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: isTotal ? 20 : 15,
      fontWeight: 700,
      color: isTotal ? "#60a5fa" : "#cbd5e1"
    }
  }, value));
}

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// MAIN COMPONENT
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function MonthlyReport() {
  var _MONTHS$find;
  var _ref10 = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {},
    reportData = _ref10.reportData;
  var isControlled = !!reportData;
  var _useState7 = useState("jan2024"),
    _useState8 = _slicedToArray(_useState7, 2),
    selKey = _useState8[0],
    setSelKey = _useState8[1];
  var _useState9 = useState(null),
    _useState0 = _slicedToArray(_useState9, 2),
    drawer = _useState0[0],
    setDrawer = _useState0[1]; // null | "all" | "flagged"

  var monthData = (_MONTHS$find = MONTHS.find(function (m) {
    return m.key === selKey;
  })) !== null && _MONTHS$find !== void 0 ? _MONTHS$find : MONTHS[2];
  var d = isControlled ? _objectSpread(_objectSpread({}, monthData), reportData) : monthData;
  // Per-month hotspot rows â€” recomputed when selKey changes
  // Per-month hotspot rows â€” recomputed when selKey changes
  var chronicCells = useMemo(function() { return getChronicCellsForMonth(selKey); }, [selKey]);

  // â”€â”€ render â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  return React.createElement("div", {
    style: { fontFamily:"'Inter','Segoe UI',system-ui,sans-serif", background:"#0f172a", minHeight:"100vh", padding:"28px 20px" }
  },
    React.createElement("div", { style:{ maxWidth:900, margin:"0 auto" } },

      // â”€â”€ HEADER â”€â”€
      React.createElement("div", {
        style:{ background:"rgba(15,23,42,0.7)", backdropFilter:"blur(12px)", border:"1px solid rgba(255,255,255,0.08)", borderRadius:14, padding:"24px 28px", marginBottom:16 }
      },
        React.createElement("div", { style:{ display:"flex", justifyContent:"space-between", alignItems:"flex-start", flexWrap:"wrap", gap:12 } },
          React.createElement("div", null,
            React.createElement("div", { style:{ fontSize:10, fontWeight:700, letterSpacing:"0.12em", textTransform:"uppercase", color:"#475569", marginBottom:6 } }, "Official Summary"),
            React.createElement("h1", { style:{ fontSize:24, fontWeight:700, color:"#f1f5f9", margin:0, lineHeight:1.2 } }, "Monthly Parking Enforcement Report")
          ),
          React.createElement("div", { style:{ display:"flex", alignItems:"center", gap:10, flexShrink:0, flexWrap:"wrap" } },
            !isControlled && React.createElement("select", {
              value: selKey,
              onChange: function(e){ setSelKey(e.target.value); setDrawer(null); },
              style:{ border:"1px solid rgba(255,255,255,0.12)", borderRadius:20, padding:"7px 32px 7px 16px", fontSize:14, color:"#e2e8f0", fontWeight:500, background:"rgba(30,41,59,0.8)", cursor:"pointer", appearance:"none", outline:"none", backgroundImage:"url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E\")", backgroundRepeat:"no-repeat", backgroundPosition:"right 10px center" }
            },
              MONTHS.map(function(m){ return React.createElement("option", { key:m.key, value:m.key }, m.label); })
            ),
            React.createElement("button", {
              onClick: function(){ downloadPDF(d); },
              style:{ background:"linear-gradient(135deg,#1d4ed8,#2563eb)", color:"#fff", border:"1px solid rgba(59,130,246,0.4)", borderRadius:10, padding:"8px 18px", fontSize:13, fontWeight:600, cursor:"pointer", boxShadow:"0 2px 12px rgba(37,99,235,0.3)", letterSpacing:"0.02em" }
            }, "\u2b07 Download PDF Report")
          )
        )
      ),

      // â”€â”€ STAT CARDS â”€â”€
      React.createElement("div", { style:{ display:"flex", gap:16, marginBottom:20, flexWrap:"wrap" } },
        React.createElement(StatCard, { label:"Tickets Logged This Month", value:d.violations.toLocaleString("en-IN"), subtitle:"Total parking violations recorded and sent for review", onClick:function(){ setDrawer("all"); } }),
        React.createElement(StatCard, { label:"Incomplete Records Removed", value:d.phatFilterCount.toLocaleString("en-IN"), subtitle:"Cases flagged as low-quality or unverifiable \u2014 not shown on the dispatch map", onClick:function(){ setDrawer("flagged"); } }),
        React.createElement(StatCard, { label:"More Stats Coming Soon", value:"\u2014", subtitle:"Additional metrics will appear here in a future update", muted:true })
      ),

      // â”€â”€ HOTSPOT TABLE â”€â”€
      React.createElement("div", {
        style:{ background:"rgba(15,23,42,0.7)", border:"1px solid rgba(255,255,255,0.08)", borderRadius:12, marginBottom:20, overflow:"hidden" }
      },
        React.createElement("div", { style:{ padding:"24px 28px 16px" } },
          React.createElement("h2", { style:{ fontSize:18, fontWeight:700, color:"#2563eb", margin:"0 0 6px" } }, "Locations That Are Always a Problem"),
          React.createElement("p", { style:{ fontSize:13, color:"#64748b", margin:0, lineHeight:1.6 } },
            "These spots appeared in the top 50 worst locations every single month \u2014 they need permanent attention, not just occasional patrols. Showing figures for ",
            React.createElement("strong", { style:{ color:"#94a3b8" } }, d.label), "."
          )
        ),
        React.createElement("div", { style:{ overflowX:"auto" } },
          React.createElement("table", { style:{ width:"100%", borderCollapse:"collapse", fontSize:13 } },
            React.createElement("thead", null,
              React.createElement("tr", { style:{ background:"#111827", borderTop:"1px solid rgba(255,255,255,0.08)", borderBottom:"1px solid rgba(255,255,255,0.08)" } },
                ["#","Location","Coordinates","Raw Score","Total Tickets","Avg Severity",
                  React.createElement("span", { title:"Composite of vehicle-type PCU, time-of-day weight, and violation-type severity.", style:{ cursor:"help", borderBottom:"1px dotted #64748b" } }, "Congestion Impact Score (0-100) \u24D8")
                ].map(function(h,i){ return React.createElement("th", { key:i, style:_objectSpread(_objectSpread({},TH),{},{textAlign:h==="#"?"center":"left"}) }, h); })
              )
            ),
            React.createElement("tbody", null,
              chronicCells.map(function(cell, i){
                var info = areaInfo(cell.lat, cell.lon);
                return React.createElement("tr", { key:cell.rank, style:{ background:i%2===0?"transparent":"rgba(255,255,255,0.02)" } },
                  React.createElement("td", { style:_objectSpread(_objectSpread({},TD),{},{textAlign:"center",fontWeight:700,color:"#f1f5f9"}) }, cell.rank),
                  React.createElement("td", { style:TD },
                    React.createElement("div", { style:{ fontWeight:600, color:"#e2e8f0", lineHeight:1.3 } }, info.name),
                    React.createElement("div", { style:{ fontSize:11, color:"#64748b", marginTop:2 } }, info.station, " Police Station")
                  ),
                  React.createElement("td", { style:TD },
                    React.createElement("span", { style:{ fontFamily:"monospace", fontSize:11, color:"#94a3b8" } }, cell.lat.toFixed(3), ", ", cell.lon.toFixed(3))
                  ),
                  React.createElement("td", { style:_objectSpread(_objectSpread({},TD),{},{fontWeight:600,color:"#f1f5f9"}) },
                    cell.congestionScore > 0 ? cell.congestionScore.toLocaleString("en-IN",{maximumFractionDigits:1}) : React.createElement("span",{style:{color:"#334155"}},"\u2014")
                  ),
                  React.createElement("td", { style:TD },
                    cell.totalTickets > 0 ? cell.totalTickets.toLocaleString("en-IN") : React.createElement("span",{style:{color:"#334155"}},"\u2014")
                  ),
                  React.createElement("td", { style:TD },
                    cell.avgSeverity > 0 ? cell.avgSeverity.toFixed(3) : React.createElement("span",{style:{color:"#334155"}},"\u2014")
                  ),
                  React.createElement("td", { style:TD }, React.createElement(PriorityBar, { score:cell.priorityScore }))
                );
              })
            )
          )
        ),
        React.createElement("div", { style:{ padding:"10px 24px 14px", borderTop:"1px solid rgba(255,255,255,0.05)" } },
          React.createElement("p", { style:{ fontSize:12, color:"#334155", margin:0, fontStyle:"italic" } },
            "Congestion Impact Score of 100 = highest urgency. Raw Score and Ticket counts reflect ", React.createElement("strong",{style:{color:"#475569"}}, d.label), " only. Priority bar is the lifetime EPS rank \u2014 stable across all months."
          )
        )
      ),

      // â”€â”€ REVENUE SECTION â”€â”€
      React.createElement("div", {
        style:{ background:"rgba(15,23,42,0.7)", backdropFilter:"blur(12px)", border:"1px solid rgba(255,255,255,0.08)", borderRadius:14, marginBottom:16, overflow:"hidden" }
      },
        React.createElement("div", { style:{ padding:"22px 24px 14px" } },
          React.createElement("h2", { style:{ fontSize:17, fontWeight:700, color:"#60a5fa", margin:"0 0 6px" } }, "How Much Can Be Collected This Month"),
          React.createElement("p", { style:{ fontSize:13, color:"#64748b", margin:0, lineHeight:1.6 } }, "Based on the number of tickets logged, here is the estimated fine amount if all violations are processed.")
        ),
        React.createElement("div", { style:{ border:"1px solid rgba(255,255,255,0.06)", borderRadius:8, margin:"0 20px 18px", overflow:"hidden" } },
          React.createElement(RevenueRow, { label:"Two-wheelers (bikes & scooters)", sublabel:"".concat(d.twoWheelerCount.toLocaleString("en-IN"), " tickets \xD7 \u20B91,000 per ticket"), value:d.twoWheelerRevenue }),
          React.createElement(RevenueRow, { label:"Cars & auto-rickshaws", sublabel:"".concat(d.carAutoCount.toLocaleString("en-IN"), " tickets \xD7 \u20B91,500 per ticket"), value:d.carAutoRevenue }),
          React.createElement(RevenueRow, { label:"Heavy vehicles (buses & trucks)", sublabel:"".concat(d.heavyCount.toLocaleString("en-IN"), " tickets \xD7 \u20B91,500 per ticket"), value:d.heavyRevenue }),
          React.createElement(RevenueRow, { label:"Total Estimated Collection", value:d.grossRevenue, isTotal:true })
        ),
        React.createElement("div", { style:{ padding:"0 20px 18px" } },
          React.createElement("p", { style:{ fontSize:12, color:"#334155", margin:0, fontStyle:"italic" } },
            "This is a maximum estimate. Actual collection depends on case approvals. Vehicle split estimated from full-dataset proportions (46.2% two-wheelers, 43.7% cars/autos, 10.1% heavy)."
          )
        )
      ),

      // â”€â”€ MODEL EVALUATION â”€â”€
      React.createElement("div", {
        style:{ background:"rgba(15,23,42,0.7)", border:"1px solid rgba(255,255,255,0.08)", borderRadius:14, padding:24, marginBottom:16 }
      },
        React.createElement("h2", { style:{ fontSize:17, fontWeight:700, color:"#60a5fa", marginBottom:8 } }, "Model Evaluation: Predicted vs Actual Validations (Holdout Set)"),
        React.createElement("p", { style:{ fontSize:13, color:"#64748b", marginBottom:16, lineHeight:1.6 } },
          MODEL_EVAL_IMAGES[selKey]
            ? "Scatter plot showing correlation between GridLock\u2019s predicted hotspots and actual verified holdout violations for " + d.label + "."
            : "Scatter plot for " + d.label + " has not been generated yet. The model was evaluated on the April 2024 holdout window \u2014 switch to April 2024 to view the chart."
        ),
        MODEL_EVAL_IMAGES[selKey]
          ? React.createElement("div", { style:{ display:"flex", justifyContent:"center", background:"#fff", borderRadius:8, padding:16 } },
              React.createElement("img", { src:MODEL_EVAL_IMAGES[selKey], alt:"Predicted vs Actual Violations \u2014 " + d.label, style:{ maxWidth:"100%", height:"auto", borderRadius:4 } })
            )
          : React.createElement("div", { style:{ display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", height:160, background:"rgba(0,0,0,0.2)", borderRadius:8, border:"2px dashed rgba(255,255,255,0.08)", gap:10 } },
              React.createElement("span", { style:{ fontSize:28 } }, "\uD83D\uDCCA"),
              React.createElement("p", { style:{ fontSize:14, color:"#475569", margin:0 } }, "No holdout evaluation available for " + d.label + "."),
              React.createElement("p", { style:{ fontSize:12, color:"#334155", margin:0 } },
                "Switch to ", React.createElement("strong", { style:{ color:"#64748b" } }, "April 2024"), " to see the validation scatter plot."
              )
            )
      ),

      // â”€â”€ FOOTER â”€â”€
      React.createElement("div", {
        style:{ textAlign:"center", padding:"14px", fontSize:12, color:"#334155", borderTop:"1px solid rgba(255,255,255,0.05)" }
      }, "Bengaluru Traffic Police \xA0|\xA0 Powered by GridLock Enforcement Intelligence")
    ),

    // â”€â”€ RECORDS DRAWER â”€â”€
    drawer && React.createElement(RecordsDrawer, {
      drawerType: drawer,
      monthKey: d.key,
      monthLabel: d.label,
      onClose: function(){ setDrawer(null); }
    })
  );
}
window.addEventListener('DOMContentLoaded', function () {
  var root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(React.createElement(MonthlyReport));
});
