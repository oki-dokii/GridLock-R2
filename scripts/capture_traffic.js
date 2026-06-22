const puppeteer = require('puppeteer');
const fs = require('fs');

const data = JSON.parse(fs.readFileSync('hotspot_data.json'));
const getScore = hs => hs.priorityScore || hs.totalPCS || 0;
const sorted = data.sort((a,b) => getScore(b) - getScore(a));

const top10 = sorted.slice(0, 10);
const bottom10 = sorted.slice(-10);

(async () => {
  const browser = await puppeteer.launch({headless: 'new', args: ['--no-sandbox', '--lang=en-US']});
  const page = await browser.newPage();
  await page.setViewport({width: 1200, height: 800});
  
  if (!fs.existsSync('screenshots')) {
    fs.mkdirSync('screenshots');
  }

  const processList = async (list, prefix) => {
    for (let i = 0; i < list.length; i++) {
      const hs = list[i];
      const lat = hs.lat;
      const lon = hs.lon;
      console.log(`Processing ${prefix} ${i+1}: ${lat}, ${lon}`);
      
      await page.goto(`https://www.google.com/maps/@${lat},${lon},16z/data=!5m1!1e1?hl=en`, {waitUntil: 'networkidle2'});
      
      try {
        await new Promise(r => setTimeout(r, 2000));
        
        // Find and click "Live traffic"
        const liveTrafficElements = await page.$$('::-p-xpath(//div[text()="Live traffic" or text()="Live Traffic"])');
        if (liveTrafficElements.length > 0) {
          await liveTrafficElements[0].click();
          await new Promise(r => setTimeout(r, 1000));
          
          // Find and click "Typical traffic"
          const typicalTrafficElements = await page.$$('::-p-xpath(//div[text()="Typical traffic" or text()="Typical Traffic"])');
          if (typicalTrafficElements.length > 0) {
            await typicalTrafficElements[typicalTrafficElements.length - 1].click();
            await new Promise(r => setTimeout(r, 1000)); // wait for typical traffic to render
          }
        }
      } catch (e) {
        console.log("Failed to toggle typical traffic:", e.message);
      }
      
      await page.screenshot({path: `screenshots/${prefix}_${i+1}.png`});
    }
  };

  await processList(top10, 'top');
  await processList(bottom10, 'bottom');

  await browser.close();
})();
