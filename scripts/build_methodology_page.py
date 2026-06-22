import os

with open('math_foundation.html', 'r') as f:
    content = f.read()

# Extract everything up to </style>
head_end = content.find('</head>')
head = content[:head_end]

body = """</head>
<body>
  <header class="hero">
    <div class="hero-badge">Methodology & Assumptions</div>
    <h1>System Parameters & Assumptions</h1>
    <p>A centralized log of parameters, heuristic assumptions, and confidence tiering rules utilized across the GridLock-R2 platform. Documented to ensure transparency and accurately track uncertainty.</p>
  </header>

  <main>
    <div class="module">
      <div class="module-header">
        <div class="module-num m1">1</div>
        <div>
          <div class="module-title">Traffic Flow & PCU Constraints</div>
          <div class="module-subtitle">Road capacity scaling and threshold limits</div>
        </div>
      </div>
      <p>GridLock uses an established heuristic for estimating road network capacity under constraint.</p>
      
      <div class="formula-block boxed">
        $$V/C = 0.85$$
      </div>
      <div class="note">
        <strong>V/C Threshold:</strong> We define the maximum acceptable volume-to-capacity (V/C) ratio before cascading gridlock as <strong>0.85</strong>. This is a standard traffic engineering assumption acknowledging that at 85% capacity, any minor disruption (such as illegal parking) forces traffic to a standstill.
      </div>

      <div class="formula-block boxed">
        $$\text{Capacity} \approx 150 \text{ veh/hr/PCU}$$
      </div>
      <div class="note">
        <strong>Lane Capacity:</strong> We assume an operational flow limit of <strong>150 vehicles per hour per Passenger Car Unit (PCU)</strong> in urban Indian contexts, heavily influenced by mixed-traffic dynamics and friction.
      </div>
    </div>

    <div class="module">
      <div class="module-header">
        <div class="module-num m2">2</div>
        <div>
          <div class="module-title">Operational Capacity (BTP)</div>
          <div class="module-subtitle">Resource constraints for enforcement units</div>
        </div>
      </div>
      <p>To produce realistic dispatch routing and avoid overwhelming local police stations, the model binds optimization targets to assumed hardware availability.</p>
      
      <div class="metrics-grid">
        <div class="formula-block">
          <h3>Patrol Vehicles</h3>
          <p style="font-size: 2rem; color: var(--accent3); font-weight: 700; margin-bottom: 0;">2</p>
          <p style="color: var(--muted); font-size: 13px;">per station</p>
        </div>
        <div class="formula-block">
          <h3>Tow Trucks</h3>
          <p style="font-size: 2rem; color: var(--accent3); font-weight: 700; margin-bottom: 0;">3.5</p>
          <p style="color: var(--muted); font-size: 13px;">per station (avg)</p>
        </div>
      </div>
      <div class="warn">
        <strong>Assumption Risk:</strong> These are flat heuristic averages. Real capacity fluctuates daily based on maintenance, staffing, and VIP movement. Future iterations should integrate live BTP fleet availability.
      </div>
    </div>

    <div class="module">
      <div class="module-header">
        <div class="module-num m3">3</div>
        <div>
          <div class="module-title">OpenStreetMap (OSM) Infrastructure</div>
          <div class="module-subtitle">Road type and junction proximity metadata</div>
        </div>
      </div>
      <p>The model maps raw violation coordinates to the actual road network to derive structural vulnerability (e.g., proximity to arterial roads or major intersections).</p>
      
      <div class="example">
        <strong>Current Coverage:</strong> ~60% mapped via Overpass API.<br>
        <strong>Target Coverage:</strong> >90% (Background batch fetching is active to respect Overpass rate limits and exponentially back off on HTTP 429s).
      </div>
      <p>For the remaining uncovered points, the model temporarily falls back to a spatial heuristic, estimating road type based on aggregate traffic density in the immediate grid cell.</p>
    </div>

    <div class="module">
      <div class="module-header">
        <div class="module-num m4">4</div>
        <div>
          <div class="module-title">Confidence Tiering (Low-n Filtering)</div>
          <div class="module-subtitle">Visual tracking of statistical uncertainty</div>
        </div>
      </div>
      <p>When reporting stratified evaluation metrics (Precision/Recall across specific vehicle types or police stations), sample size (n) dramatically impacts reliability. Instead of presenting unstable metrics as facts, GridLock uses a 3-tier reporting system.</p>
      
      <table>
        <thead>
          <tr>
            <th>Sample Size (n)</th>
            <th>Display Logic</th>
            <th>Rationale</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>n < 30</td>
            <td><span style="color:#f85149">Hidden</span> (Replaced with "low_conf")</td>
            <td>Distribution is untrustworthy. Discarded to prevent misinterpretation of volatile percentages.</td>
          </tr>
          <tr>
            <td>30 ≤ n < 100</td>
            <td><span style="color:#ffa657">Visible but Flagged (⚠️)</span></td>
            <td>Reported, but the margin of error is wide. Treat as directional rather than definitive.</td>
          </tr>
          <tr>
            <td>n ≥ 100</td>
            <td><span style="color:#7ee787">Normal Display</span></td>
            <td>Statistically stable subgroup suitable for hard operational decisions.</td>
          </tr>
        </tbody>
      </table>
    </div>

  </main>
</body>
</html>
"""

with open('methodology_and_assumptions.html', 'w') as f:
    f.write(head + body)
print("Created methodology_and_assumptions.html")
