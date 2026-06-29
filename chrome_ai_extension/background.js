chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "SUMMARIZE") {
    // We must run async work in an IIFE and return true to keep the message channel open
    (async () => {
      try {
        // In a real extension, we would send the extracted text from the tab to an AI endpoint here.
        // For the simulation, we'll wait a bit and return a mock summary.
        
        // Wait 2 seconds to simulate AI processing
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const summary = `This is a generated summary of the webpage at ${request.url}. \n\nIn a production environment, this text would be the output of an LLM API call (like OpenAI or Gemini) parsing the text scraped by the content script.`;
        
        sendResponse({ summary: summary });
      } catch (err) {
        sendResponse({ error: err.message });
      }
    })();
    return true; // Keeps the message channel open for the async response
  }
});
