# Google Maps Typical Traffic Spot-Check

This is a **spot-check, not a validation**. The goal is to provide a real-world, directional correlation check between the model's Congestion Impact Score and actual road infrastructure as seen on Google Maps' typical traffic overlay.

I wrote a headless browser script to automatically visit the exact coordinates of our Top 10 (highest priority score) and Bottom 10 (lowest priority score) hotspots, toggle the traffic layer, and capture the typical conditions.

## Directional Match Findings

The directional match is solid. 

**Top 10 Hotspots** (High Congestion Impact Score): These are overwhelmingly located in dense, central, hyper-constrained junctions (e.g., Upparpet around Majestic, Shivajinagar). The screenshots show dense intersecting traffic flows, consistent with areas where even a single illegally parked vehicle or a minor accident causes cascading gridlock.

**Bottom 10 Hotspots** (Low Congestion Impact Score): These tend to be either on peripheral roads (Kodigehalli, Byatarayanapura) or locations where traffic volume exists but the road capacity is higher, meaning violations don't cause the same acute bottlenecks. 

---

## 🔴 Top 10 Hotspots (High Impact)

````carousel
![Top 1: Upparpet - Dhanvanthari Road (Score: 95)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/top_1.png)
<!-- slide -->
![Top 2: Shivajinagar - Dickenson Road (Score: 89)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/top_2.png)
<!-- slide -->
![Top 3: Upparpet - BGS Flyover (Score: 88)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/top_3.png)
<!-- slide -->
![Top 4: Jeevanbheemanagar - New Horizon College Road (Score: 87)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/top_4.png)
<!-- slide -->
![Top 5: Upparpet - Kempegowda Road (Score: 77)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/top_5.png)
<!-- slide -->
![Top 6: Upparpet - NR Road (Score: 74)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/top_6.png)
<!-- slide -->
![Top 7: Upparpet - Kempegowda Road (Score: 73)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/top_7.png)
<!-- slide -->
![Top 8: Jeevanbheemanagar - New Horizon College Road (Score: 73)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/top_8.png)
<!-- slide -->
![Top 9: Upparpet - Dhanvanthari Road (Score: 72)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/top_9.png)
<!-- slide -->
![Top 10: Upparpet - Kempegowda Road (Score: 72)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/top_10.png)
````

---

## 🟢 Bottom 10 Hotspots (Low Impact)

````carousel
![Bottom 1: Whitefield (Score: 16)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/bottom_1.png)
<!-- slide -->
![Bottom 2: Magadi Road (Score: 16)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/bottom_2.png)
<!-- slide -->
![Bottom 3: Byatarayanapura (Score: 16)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/bottom_3.png)
<!-- slide -->
![Bottom 4: Kodigehalli (Score: 16)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/bottom_4.png)
<!-- slide -->
![Bottom 5: Jeevanbheemanagar (Score: 15)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/bottom_5.png)
<!-- slide -->
![Bottom 6: Upparpet (Score: 15)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/bottom_6.png)
<!-- slide -->
![Bottom 7: Whitefield (Score: 15)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/bottom_7.png)
<!-- slide -->
![Bottom 8: KR Pura (Score: 15)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/bottom_8.png)
<!-- slide -->
![Bottom 9: Jeevanbheemanagar (Score: 15)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/bottom_9.png)
<!-- slide -->
![Bottom 10: Rajajinagar (Score: 15)](/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/bottom_10.png)
````
