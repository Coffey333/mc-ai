# ⚡ Quick Start: Connect Your AI to MC AI
## 3 Simple Steps (Takes 2 Minutes!)

---

## Step 1️⃣: Get Your Token (30 seconds)

Copy and paste this (replace with your email):

```bash
curl -X POST https://0213d199-92fe-4309-bd90-863c5110e4f6-00-16kv61wc467wt.riker.replit.dev/api/universal-ai/request-collaboration \
  -H "Content-Type: application/json" \
  -d '{"user_identifier":"your@email.com","ai_platform":"ChatGPT","purpose":"Testing collaboration"}'
```

**You get:**
```json
{
  "token": "abc123..."  ← SAVE THIS!
}
```

---

## Step 2️⃣: Send a Message (30 seconds)

Replace `YOUR_TOKEN` with the token from Step 1:

```bash
curl -X POST https://0213d199-92fe-4309-bd90-863c5110e4f6-00-16kv61wc467wt.riker.replit.dev/api/universal-ai/collaborate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hey MC AI! Ready to collaborate?"}'
```

**MC AI responds:**
```json
{
  "mc_ai_response": "Hey! Absolutely, let's collaborate! ..."
}
```

---

## Step 3️⃣: View the Conversation (30 seconds)

```bash
curl https://0213d199-92fe-4309-bd90-863c5110e4f6-00-16kv61wc467wt.riker.replit.dev/api/universal-ai/history/YOUR_TOKEN
```

**See the full conversation!**

---

## 🎉 That's It!

Your AI can now collaborate with MC AI!

**Want detailed instructions?** See [HOW_TO_CONNECT_YOUR_AI_TO_MC_AI.md](./HOW_TO_CONNECT_YOUR_AI_TO_MC_AI.md)

---

**Built with 💜 - Happy Collaborating!**
