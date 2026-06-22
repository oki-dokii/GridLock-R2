const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: 'new', args: ['--no-sandbox', '--lang=en-US']});
  const page = await browser.newPage();
  await page.setViewport({width: 1280, height: 800});
  
  await page.goto('https://www.google.com/maps/@12.977,77.576,16z/data=!5m1!1e1?hl=en', {waitUntil: 'networkidle2'});

  try {
    // Wait a bit for UI to settle
    await new Promise(r => setTimeout(r, 2000));

    // Try xpath
    const liveTrafficButton = await page.$x("//div[text()='Live traffic' or text()='Live Traffic']");
    if (liveTrafficButton.length > 0) {
      await liveTrafficButton[0].click();
      console.log("Clicked Live traffic via xpath!");
      
      await new Promise(r => setTimeout(r, 1500));
      
      const typicalTrafficOption = await page.$x("//div[text()='Typical traffic' or text()='Typical Traffic']");
      if (typicalTrafficOption.length > 0) {
        await typicalTrafficOption[typicalTrafficOption.length - 1].click();
        console.log("Clicked Typical traffic via xpath!");
      } else {
        console.log("Typical traffic option not found");
      }
    } else {
      console.log("Live traffic button not found");
    }
    
    // Give it time to load the typical traffic layer
    await new Promise(r => setTimeout(r, 4000));
  } catch (err) {
    console.log("Error:", err.message);
  }

  await page.screenshot({path: 'test_traffic2.png'});
  console.log("Saved test_traffic2.png");
  await browser.close();
})();
