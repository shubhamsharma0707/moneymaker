document.addEventListener('DOMContentLoaded', () => {
  const summarizeBtn = document.getElementById('summarize-btn');
  const upgradeBtn = document.getElementById('upgrade-btn');
  const copyBtn = document.getElementById('copy-btn');
  
  const loadingDiv = document.getElementById('loading');
  const resultDiv = document.getElementById('result');
  const errorDiv = document.getElementById('error');
  const summaryText = document.getElementById('summary-text');

  summarizeBtn.addEventListener('click', async () => {
    // Hide previous states
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    summarizeBtn.disabled = true;
    
    // Show loading
    loadingDiv.classList.remove('hidden');

    try {
      // 1. Get active tab
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tab) throw new Error("No active tab found");

      // 2. Inject content script if needed and extract text
      const injectionResults = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
      });

      // 3. Send message to background script to summarize
      const response = await chrome.runtime.sendMessage({
        action: "SUMMARIZE",
        url: tab.url
      });

      if (response.error) {
        throw new Error(response.error);
      }

      // 4. Show summary
      summaryText.innerText = response.summary;
      loadingDiv.classList.add('hidden');
      resultDiv.classList.remove('hidden');

    } catch (err) {
      loadingDiv.classList.add('hidden');
      errorDiv.innerText = "Error: " + err.message;
      errorDiv.classList.remove('hidden');
    } finally {
      summarizeBtn.disabled = false;
    }
  });

  copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(summaryText.innerText);
    copyBtn.innerText = "Copied!";
    setTimeout(() => copyBtn.innerText = "Copy to Clipboard", 2000);
  });

  upgradeBtn.addEventListener('click', () => {
    chrome.tabs.create({ url: "https://buy.stripe.com/mock-link-for-extension" });
  });
});
