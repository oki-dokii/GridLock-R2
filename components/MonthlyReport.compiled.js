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

// ─────────────────────────────────────────────────────────────────────────────
// AREA NAMES — sourced from:
//   GRIDLOCK_IMPLEMENTATION_GUIDE.md Appendix A (confirmed coords + names)
//   MASTER_RESEARCH_COMBINED.md §1.6 (chronic hotspot name list)
//   §1.4 station coverage areas for the remaining top cells
// Keys are "lat.toFixed(3),lon.toFixed(3)"
// ─────────────────────────────────────────────────────────────────────────────
var AREA_LOOKUP = {
  // Appendix A — confirmed name + coord pairs
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
  // §1.6 chronic list — station-matched by proximity
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
    station: "—"
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// MONTHLY DATA — from DATA_ANALYSIS_RESULTS.md §P2.3
// Vehicle-type split scaled from 5-month totals (46.2% two-wheeler,
// 43.7% car/auto, 10.1% heavy) — no per-month vehicle breakdown in dataset.
// ─────────────────────────────────────────────────────────────────────────────
var TOTAL_VIOLATIONS = 298450;
var TW_TOTAL = 137866;
var CA_TOTAL = 130530;
var HV_TOTAL = 30054;
var PHAT_TOTAL = 20349; // officers with p̂ < 0.50 — from P1.6

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

// PI=1.0 chronic cells — same every month by definition
// Source: DATA_ANALYSIS_RESULTS.md P1.2 + P1.7 + GRIDLOCK_IMPLEMENTATION_GUIDE.md Appendix A
var CHRONIC_CELLS = [{
  rank: 1,
  lat: 12.981,
  lon: 77.610,
  congestionScore: 5918.7,
  totalTickets: 4411,
  avgSeverity: 1.342,
  priorityScore: 100
}, {
  rank: 2,
  lat: 13.184,
  lon: 77.680,
  congestionScore: 3009.5,
  totalTickets: 1926,
  avgSeverity: 1.563,
  priorityScore: 84
}, {
  rank: 3,
  lat: 12.964,
  lon: 77.577,
  congestionScore: 2896.5,
  totalTickets: 3745,
  avgSeverity: 0.773,
  priorityScore: 76
}, {
  rank: 4,
  lat: 12.977,
  lon: 77.576,
  congestionScore: 2450.8,
  totalTickets: 3181,
  avgSeverity: 0.770,
  priorityScore: 64
}, {
  rank: 5,
  lat: 13.071,
  lon: 77.588,
  congestionScore: 2307.6,
  totalTickets: 3280,
  avgSeverity: 0.704,
  priorityScore: 60
}, {
  rank: 6,
  lat: 12.934,
  lon: 77.691,
  congestionScore: 2196.8,
  totalTickets: 3343,
  avgSeverity: 0.657,
  priorityScore: 57
}, {
  rank: 7,
  lat: 12.984,
  lon: 77.603,
  congestionScore: 1935.7,
  totalTickets: 1649,
  avgSeverity: 1.174,
  priorityScore: 50
}, {
  rank: 8,
  lat: 12.977,
  lon: 77.577,
  congestionScore: 1898.6,
  totalTickets: 1907,
  avgSeverity: 0.996,
  priorityScore: 49
}, {
  rank: 9,
  lat: 12.973,
  lon: 77.579,
  congestionScore: 1769.3,
  totalTickets: 2366,
  avgSeverity: 0.748,
  priorityScore: 46
}, {
  rank: 10,
  lat: 13.035,
  lon: 77.589,
  congestionScore: 1678.7,
  totalTickets: 2284,
  avgSeverity: 0.735,
  priorityScore: 43
}];
var MONTHS = [buildMonth("nov2023", "November 2023", 43504), buildMonth("dec2023", "December 2023", 63917), buildMonth("jan2024", "January 2024", 65479), buildMonth("feb2024", "February 2024", 54660), buildMonth("mar2024", "March 2024", 55453), buildMonth("apr2024", "April 2024", 15432)];

// ─────────────────────────────────────────────────────────────────────────────
// SAMPLE RECORD GENERATOR
// Deterministic pseudo-random so records are stable per month/type.
// Replace with real API fetch when backend is connected.
// ─────────────────────────────────────────────────────────────────────────────
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
    var confBand = phat < 0.20 ? "Very Low (< 20%)" : phat < 0.35 ? "Low (20%–35%)" : "Below Threshold (35%–50%)";
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

// ─────────────────────────────────────────────────────────────────────────────
// FILTER OPTIONS
// ─────────────────────────────────────────────────────────────────────────────
var F_STATIONS = ["All Areas"].concat(ALL_STATIONS);
var F_VEHICLES = ["All Vehicles", "Two-Wheeler", "Car/Auto", "Heavy Vehicle"];
var F_VIOLS = ["All Violation Types"].concat(VIOL_DATA);
var F_STATUSES = ["All Statuses", "Approved", "Pending", "Rejected"];
var F_CONF = ["All Confidence Levels", "Very Low (< 20%)", "Low (20%–35%)", "Below Threshold (35%–50%)"];
var BLANK_FILT = {
  station: "All Areas",
  vehicle: "All Vehicles",
  viol: "All Violation Types",
  status: "All Statuses",
  conf: "All Confidence Levels"
};

// ─────────────────────────────────────────────────────────────────────────────
// TINY SHARED STYLES
// ─────────────────────────────────────────────────────────────────────────────
var TH = {
  padding: "10px 14px",
  textAlign: "left",
  fontWeight: 600,
  fontSize: 11,
  color: "#64748b",
  letterSpacing: "0.05em",
  whiteSpace: "nowrap"
};
var TD = {
  padding: "11px 14px",
  color: "#374151",
  verticalAlign: "top"
};
var SEL = {
  border: "1px solid #e2e8f0",
  borderRadius: 8,
  padding: "7px 12px",
  fontSize: 13,
  color: "#374151",
  background: "#fff",
  cursor: "pointer"
};

// ─────────────────────────────────────────────────────────────────────────────
// STATUS / CONFIDENCE BADGES
// ─────────────────────────────────────────────────────────────────────────────
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

// ─────────────────────────────────────────────────────────────────────────────
// RECORDS DRAWER
// ─────────────────────────────────────────────────────────────────────────────
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
  var subtitle = drawerType === "flagged" ? "Cases the system removed from the dispatch map. Officer confidence score (p̂) was below 0.50." : "Every ticket logged this month. Use the filters below to narrow down by area, vehicle, or status.";
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    onClick: onClose,
    style: {
      position: "fixed",
      inset: 0,
      background: "rgba(0,0,0,0.4)",
      zIndex: 200
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "fixed",
      top: 0,
      right: 0,
      bottom: 0,
      width: "min(860px, 100vw)",
      background: "#fff",
      zIndex: 201,
      display: "flex",
      flexDirection: "column",
      boxShadow: "-6px 0 40px rgba(0,0,0,0.15)",
      fontFamily: "'Inter','Segoe UI',system-ui,sans-serif"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "20px 24px 16px",
      borderBottom: "1px solid #e2e8f0",
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
      color: "#0f172a"
    }
  }, title), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 13,
      color: "#64748b",
      lineHeight: 1.5
    }
  }, subtitle), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "6px 0 0",
      fontSize: 11,
      color: "#94a3b8"
    }
  }, monthLabel, " \xB7 Showing ", filtered.length, " of ", all.length, " records", " ", "\xB7", " ", /*#__PURE__*/React.createElement("em", null, "Sample data \u2014 replace with live API response when backend is connected"))), /*#__PURE__*/React.createElement("button", {
    onClick: onClose,
    style: _objectSpread(_objectSpread({}, SEL), {}, {
      flexShrink: 0,
      color: "#374151"
    })
  }, "\u2715  Close"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 8,
      flexWrap: "wrap",
      padding: "12px 20px",
      background: "#f8fafc",
      borderBottom: "1px solid #e2e8f0",
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
      color: "#64748b"
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
      color: "#94a3b8",
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
      background: "#f8fafc",
      borderBottom: "2px solid #e2e8f0",
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
        background: i % 2 === 0 ? "#fff" : "#fafbfc",
        borderBottom: "1px solid #f1f5f9"
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
        color: "#0f172a"
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
        color: "#0f172a",
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
      borderTop: "1px solid #e2e8f0",
      flexShrink: 0,
      background: "#fafbfc"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      color: "#64748b"
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
      color: page === 0 ? "#cbd5e1" : "#374151",
      cursor: page === 0 ? "not-allowed" : "pointer"
    })
  }, "\u2190 Prev"), /*#__PURE__*/React.createElement("button", {
    disabled: page >= totalPages - 1,
    onClick: function onClick() {
      return setPage(function (p) {
        return p + 1;
      });
    },
    style: _objectSpread(_objectSpread({}, SEL), {}, {
      color: page >= totalPages - 1 ? "#cbd5e1" : "#374151",
      cursor: page >= totalPages - 1 ? "not-allowed" : "pointer"
    })
  }, "Next \u2192")))));
}

// ─────────────────────────────────────────────────────────────────────────────
// STAT CARD
// ─────────────────────────────────────────────────────────────────────────────
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
      background: muted ? "#f8f9fa" : "#fff",
      border: "1px solid ".concat(hov ? "#2563eb" : "#e2e8f0"),
      borderRadius: 10,
      padding: "20px 24px",
      flex: 1,
      minWidth: 0,
      cursor: muted ? "default" : "pointer",
      boxShadow: hov ? "0 0 0 2px #bfdbfe" : "none",
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
      fontSize: 11,
      fontWeight: 600,
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      color: muted ? "#94a3b8" : "#2563eb"
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
      color: muted ? "#94a3b8" : "#0f172a",
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

// ─────────────────────────────────────────────────────────────────────────────
// PRIORITY BAR
// ─────────────────────────────────────────────────────────────────────────────
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
      background: "#e2e8f0",
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
      fontWeight: 600,
      color: "#0f172a",
      minWidth: 28
    }
  }, score));
}

// ─────────────────────────────────────────────────────────────────────────────
// REVENUE ROW
// ─────────────────────────────────────────────────────────────────────────────
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
      background: isTotal ? "#f8faff" : "#fff",
      borderTop: isTotal ? "2px solid #e2e8f0" : "1px solid #f1f5f9"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: isTotal ? 15 : 14,
      fontWeight: isTotal ? 700 : 400,
      color: "#0f172a"
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
      color: isTotal ? "#0f172a" : "#374151"
    }
  }, value));
}

// ─────────────────────────────────────────────────────────────────────────────
// MAIN COMPONENT
// ─────────────────────────────────────────────────────────────────────────────
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
  return /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Inter','Segoe UI',system-ui,sans-serif",
      background: "#f1f5f9",
      minHeight: "100vh",
      padding: "32px 24px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 900,
      margin: "0 auto"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: "#fff",
      border: "1px solid #e2e8f0",
      borderRadius: 12,
      padding: "24px 32px",
      marginBottom: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "flex-start",
      flexWrap: "wrap",
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      fontWeight: 600,
      letterSpacing: "0.1em",
      textTransform: "uppercase",
      color: "#64748b",
      marginBottom: 6
    }
  }, "Official Summary"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 26,
      fontWeight: 700,
      color: "#0f172a",
      margin: 0,
      lineHeight: 1.2
    }
  }, "Monthly Parking Enforcement Report")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 10,
      flexShrink: 0,
      flexWrap: "wrap"
    }
  }, !isControlled && /*#__PURE__*/React.createElement("select", {
    value: selKey,
    onChange: function onChange(e) {
      setSelKey(e.target.value);
      setDrawer(null);
    },
    style: {
      border: "1px solid #e2e8f0",
      borderRadius: 20,
      padding: "6px 32px 6px 16px",
      fontSize: 14,
      color: "#374151",
      fontWeight: 500,
      background: "#fff",
      cursor: "pointer",
      appearance: "none",
      backgroundImage: "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E\")",
      backgroundRepeat: "no-repeat",
      backgroundPosition: "right 10px center"
    }
  }, MONTHS.map(function (m) {
    return /*#__PURE__*/React.createElement("option", {
      key: m.key,
      value: m.key
    }, m.label);
  })), /*#__PURE__*/React.createElement("button", {
    style: {
      background: "#0f172a",
      color: "#fff",
      border: "none",
      borderRadius: 8,
      padding: "8px 16px",
      fontSize: 14,
      fontWeight: 500,
      cursor: "pointer"
    }
  }, "Download Report")))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 16,
      marginBottom: 20,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement(StatCard, {
    label: "Tickets Logged This Month",
    value: d.violations.toLocaleString("en-IN"),
    subtitle: "Total parking violations recorded and sent for review",
    onClick: function onClick() {
      return setDrawer("all");
    }
  }), /*#__PURE__*/React.createElement(StatCard, {
    label: "Incomplete Records Removed",
    value: d.phatFilterCount.toLocaleString("en-IN"),
    subtitle: "Cases flagged as low-quality or unverifiable \u2014 not shown on the dispatch map",
    onClick: function onClick() {
      return setDrawer("flagged");
    }
  }), /*#__PURE__*/React.createElement(StatCard, {
    label: "More Stats Coming Soon",
    value: "\u2014",
    subtitle: "Additional metrics will appear here in a future update",
    muted: true
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      background: "#fff",
      border: "1px solid #e2e8f0",
      borderRadius: 12,
      marginBottom: 20,
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "24px 28px 16px"
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 18,
      fontWeight: 700,
      color: "#2563eb",
      margin: "0 0 6px"
    }
  }, "Locations That Are Always a Problem"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      color: "#475569",
      margin: 0,
      lineHeight: 1.6
    }
  }, "These spots appeared in the top 50 worst locations every single month \u2014 they need permanent attention, not just occasional patrols.")), /*#__PURE__*/React.createElement("div", {
    style: {
      overflowX: "auto"
    }
  }, /*#__PURE__*/React.createElement("table", {
    style: {
      width: "100%",
      borderCollapse: "collapse",
      fontSize: 13
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
    style: {
      background: "#f8fafc",
      borderTop: "1px solid #e2e8f0",
      borderBottom: "1px solid #e2e8f0"
    }
  }, ["#", "Location", "Coordinates", "Congestion Score", "Total Tickets", "Avg Severity", "Priority Score"].map(function (h) {
    return /*#__PURE__*/React.createElement("th", {
      key: h,
      style: _objectSpread(_objectSpread({}, TH), {}, {
        textAlign: h === "#" ? "center" : "left"
      })
    }, h);
  }))), /*#__PURE__*/React.createElement("tbody", null, CHRONIC_CELLS.map(function (cell, i) {
    var info = areaInfo(cell.lat, cell.lon);
    return /*#__PURE__*/React.createElement("tr", {
      key: cell.rank,
      style: {
        background: i % 2 === 0 ? "#fff" : "#fafbfc",
        borderBottom: "1px solid #f1f5f9"
      }
    }, /*#__PURE__*/React.createElement("td", {
      style: _objectSpread(_objectSpread({}, TD), {}, {
        textAlign: "center",
        fontWeight: 700,
        color: "#0f172a"
      })
    }, cell.rank), /*#__PURE__*/React.createElement("td", {
      style: TD
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontWeight: 600,
        color: "#0f172a",
        lineHeight: 1.3
      }
    }, info.name), /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 11,
        color: "#64748b",
        marginTop: 2
      }
    }, info.station, " Police Station")), /*#__PURE__*/React.createElement("td", {
      style: TD
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: "monospace",
        fontSize: 11,
        color: "#94a3b8"
      }
    }, cell.lat.toFixed(3), ", ", cell.lon.toFixed(3))), /*#__PURE__*/React.createElement("td", {
      style: _objectSpread(_objectSpread({}, TD), {}, {
        fontWeight: 600,
        color: "#0f172a"
      })
    }, cell.congestionScore.toLocaleString("en-IN", {
      maximumFractionDigits: 1
    })), /*#__PURE__*/React.createElement("td", {
      style: TD
    }, cell.totalTickets.toLocaleString("en-IN")), /*#__PURE__*/React.createElement("td", {
      style: TD
    }, cell.avgSeverity.toFixed(3)), /*#__PURE__*/React.createElement("td", {
      style: TD
    }, /*#__PURE__*/React.createElement(PriorityBar, {
      score: cell.priorityScore
    })));
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "12px 28px",
      borderTop: "1px solid #f1f5f9"
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 12,
      color: "#64748b",
      margin: 0,
      fontStyle: "italic"
    }
  }, "Priority Score of 100 = highest urgency. Deploy here first. Congestion scores and ticket counts are cumulative over the full dataset \u2014 these locations are chronic across all months."))), /*#__PURE__*/React.createElement("div", {
    style: {
      background: "#fff",
      border: "1px solid #e2e8f0",
      borderRadius: 12,
      marginBottom: 20,
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "24px 28px 16px"
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 18,
      fontWeight: 700,
      color: "#2563eb",
      margin: "0 0 6px"
    }
  }, "How Much Can Be Collected This Month"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      color: "#475569",
      margin: 0,
      lineHeight: 1.6
    }
  }, "Based on the number of tickets logged, here is the estimated fine amount if all violations are processed.")), /*#__PURE__*/React.createElement("div", {
    style: {
      border: "1px solid #e2e8f0",
      borderRadius: 8,
      margin: "0 24px 20px",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement(RevenueRow, {
    label: "Two-wheelers (bikes & scooters)",
    sublabel: "".concat(d.twoWheelerCount.toLocaleString("en-IN"), " tickets \xD7 \u20B91,000 per ticket"),
    value: d.twoWheelerRevenue
  }), /*#__PURE__*/React.createElement(RevenueRow, {
    label: "Cars & auto-rickshaws",
    sublabel: "".concat(d.carAutoCount.toLocaleString("en-IN"), " tickets \xD7 \u20B91,500 per ticket"),
    value: d.carAutoRevenue
  }), /*#__PURE__*/React.createElement(RevenueRow, {
    label: "Heavy vehicles (buses & trucks)",
    sublabel: "".concat(d.heavyCount.toLocaleString("en-IN"), " tickets \xD7 \u20B91,500 per ticket"),
    value: d.heavyRevenue
  }), /*#__PURE__*/React.createElement(RevenueRow, {
    label: "Total Estimated Collection",
    value: d.grossRevenue,
    isTotal: true
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "0 28px 20px"
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 12,
      color: "#64748b",
      margin: 0,
      fontStyle: "italic"
    }
  }, "This is a maximum estimate. Actual collection depends on case approvals. Vehicle split estimated from full-dataset proportions (46.2% two-wheelers, 43.7% cars/autos, 10.1% heavy)."))), /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "center",
      padding: "16px",
      fontSize: 13,
      color: "#94a3b8",
      borderTop: "1px solid #e2e8f0"
    }
  }, "Bengaluru Traffic Police \xA0|\xA0 Powered by GridLock Enforcement Intelligence")), drawer && /*#__PURE__*/React.createElement(RecordsDrawer, {
    drawerType: drawer,
    monthKey: d.key,
    monthLabel: d.label,
    onClose: function onClose() {
      return setDrawer(null);
    }
  }));
}
window.addEventListener('DOMContentLoaded', function () {
  var root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(React.createElement(MonthlyReport));
});