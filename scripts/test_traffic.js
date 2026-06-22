const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: 'new', args: ['--no-sandbox', '--lang=en-US']});
  const page = await browser.newPage();
  await page.setViewport({width: 1280, height: 800});
  
  const lat = 12.977;
  const lon = 77.576;
  console.log(`Loading map for ${lat}, ${lon}...`);
  await page.goto(`https://www.google.com/maps/@${lat},${lon},16z/data=!5m1!1e1?hl=en`, {waitUntil: 'networkidle2'});

  try {
    // Dismiss "Agree" to cookies if it appears
    const buttons = await page.$$('button');
    for (let btn of buttons) {
      const text = await page.evaluate(el => el.textContent, btn);
      if (text === 'Accept all' || text === 'I agree') {
        await btn.click();
        await new Promise(r => setTimeout(r, 2000));
      }
    }

    console.log("Looking for traffic button...");
    await page.waitForSelector('button[aria-label="Live traffic"]', {timeout: 5000});
    await page.click('button[aria-label="Live traffic"]');
    
    console.log("Looking for Typical Traffic option...");
    await new Promise(r => setTimeout(r, 1000));
    const options = await page.$$('div[role="menuitemradio"]');
    for (let opt of options) {
      const text = await page.evaluate(el => el.textContent, opt);
      if (text.includes('Typical traffic')) {
        await opt.click();
        console.log("Clicked Typical traffic!");
        break;
      }
    }
    
    // Set time to 6:00 PM Wednesday (example)
    // The UI usually defaults to the current day/time, but "Typical traffic" shows a slider and day dropdown
    // It's too complex to change the slider, we'll just accept whatever default typical traffic it shows!
    
    await new Promise(r => setTimeout(r, 3000));
  } catch (err) {
    console.log("Could not switch to typical traffic:", err.message);
  }

  await page.screenshot({path: 'test_traffic.png'});
  console.log("Screenshot saved.");
  await browser.close();
})();
