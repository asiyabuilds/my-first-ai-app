from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

API_KEY = "your-groq-api-key-here"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Ask AI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }

        body {
            background-color: #f9f0f7;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            background: #fff5fe;
            border-radius: 24px;
            padding: 40px;
            width: 90%;
            max-width: 600px;
            box-shadow: 0 8px 32px rgba(200,150,200,0.15);
        }

        h1 {
            text-align: center;
            color: #c084b0;
            font-size: 28px;
            margin-bottom: 8px;
        }

        p.subtitle {
            text-align: center;
            color: #d4a8cc;
            font-size: 14px;
            margin-bottom: 32px;
        }

        input {
            width: 100%;
            padding: 16px 20px;
            border: 2px solid #e8c8e0;
            border-radius: 50px;
            font-size: 15px;
            color: #7a5a75;
            background: #fff0fb;
            outline: none;
            margin-bottom: 16px;
            transition: border 0.3s;
        }

        input:focus {
            border-color: #c084b0;
        }

        button {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #d4a0c8, #c084b0);
            color: white;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            cursor: pointer;
            transition: opacity 0.3s;
        }

        button:hover {
            opacity: 0.9;
        }

        .reply-box {
            margin-top: 24px;
            background: #fce8f8;
            border-radius: 16px;
            padding: 20px;
            color: #7a5a75;
            font-size: 15px;
            line-height: 1.7;
            display: none;
        }

        .loading {
            text-align: center;
            color: #c084b0;
            margin-top: 20px;
            display: none;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌸 Ask Anything</h1>
        <p class="subtitle">Your calm AI companion</p>

        <input type="text" id="msg" placeholder="Type your question gently...">
        <button onclick="ask()">Ask 🌷</button>

        <div class="loading" id="loading">✨ Thinking...</div>
        <div class="reply-box" id="reply"></div>
    </div>

    <script>
        async function ask() {
            let msg = document.getElementById("msg").value;
            if (!msg) return;

            document.getElementById("loading").style.display = "block";
            document.getElementById("reply").style.display = "none";

            let res = await fetch("/ask", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({message: msg})
            });

            let data = await res.json();
            document.getElementById("loading").style.display = "none";
            document.getElementById("reply").style.display = "block";
            document.getElementById("reply").innerText = data.reply;
        }

        document.getElementById("msg").addEventListener("keypress", function(e) {
            if (e.key === "Enter") ask();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data["message"]

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a calm, warm, helpful assistant. Today's date is May 19, 2026."},
                {"role": "user", "content": user_message}
            ]
        }
    )

    reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
