chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "SUMMARIZE") {
    // We must run async work in an IIFE and return true to keep the message channel open
    (async () => {
      try {
        // To implement this fully securely, query a backend server you own instead of directly hitting OpenAI from the client.
        // For demonstration, we assume the user provided their API key in the extension options.
        chrome.storage.sync.get(['OPENAI_API_KEY'], async (result) => {
          const apiKey = result.OPENAI_API_KEY;
          if (!apiKey) {
            sendResponse({ error: "No API key configured. Please set it in options." });
            return;
          }

          try {
            const apiResponse = await fetch("https://api.openai.com/v1/chat/completions", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${apiKey}`
              },
              body: JSON.stringify({
                model: "gpt-4o-mini",
                messages: [
                  {"role": "system", "content": "You are an expert summarizer. Summarize the provided webpage text."},
                  {"role": "user", "content": `Summarize this page (${request.url}):\n\n${request.text ? request.text.substring(0, 4000) : "No text found"}`}
                ]
              })
            });
            
            const data = await apiResponse.json();
            if (data.error) {
              sendResponse({ error: data.error.message });
              return;
            }
            
            const summary = data.choices[0].message.content;
            sendResponse({ summary: summary });
          } catch (e) {
            sendResponse({ error: e.message });
          }
        });
      } catch (err) {
        sendResponse({ error: err.message });
      }
    })();
    return true; // Keeps the message channel open for the async response
  }
});
