import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';

const app = express();
app.use(cors());
app.use(express.json());

app.post('/api/generate', async (req, res) => {
    // In production, verify Stripe subscription status here
    // const hasSubscription = await checkStripeSubscription(req.headers.authorization);
    // if (!hasSubscription) return res.status(403).json({error: "Payment required"});

    const { jobDescription, resumeText } = req.body;
    // We would use an environment variable for the API key in production
    const OPENAI_API_KEY = process.env.OPENAI_API_KEY; 

    if (!OPENAI_API_KEY) {
        return res.status(500).json({error: "Missing OpenAI API Key on server"});
    }

    try {
        const aiResponse = await fetch("https://api.openai.com/v1/chat/completions", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${OPENAI_API_KEY}`
            },
            body: JSON.stringify({
                model: "gpt-4o-mini",
                messages: [
                    {role: "system", content: "You are an expert resume writer. Return a JSON object with two fields: 'coverLetter' (a string containing a tailored cover letter) and 'improvements' (an array of 3 string tips for the resume)."},
                    {role: "user", content: `Job Description:\n${jobDescription}\n\nResume:\n${resumeText}`}
                ],
                response_format: { type: "json_object" }
            })
        });

        const data = await aiResponse.json();
        if (data.error) {
            return res.status(500).json({error: data.error.message});
        }

        const result = JSON.parse(data.choices[0].message.content);
        res.json(result);
    } catch (e) {
        res.status(500).json({error: e.message});
    }
});

const PORT = 3001;
app.listen(PORT, () => console.log(`Resume backend running on port ${PORT}`));
