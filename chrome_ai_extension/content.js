// This script is injected into the active tab to read its contents.
// For now, it just signals that it successfully ran.
// A full implementation would use document.body.innerText or Readability.js.
(function() {
  // Scrape logic would go here
  const pageText = document.body.innerText.substring(0, 5000); // Grab first 5000 chars
  
  // We can return data directly if we executed this script dynamically,
  // but in our setup, the background worker handles the logic.
  return pageText;
})();
