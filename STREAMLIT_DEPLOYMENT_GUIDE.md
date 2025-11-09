# Streamlit Cloud Deployment Guide

Complete guide for deploying SCS Mediator SDK to Streamlit Cloud for public access.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (5 minutes)](#quick-start)
3. [Detailed Setup Steps](#detailed-setup-steps)
4. [Configuration](#configuration)
5. [Secrets Management](#secrets-management)
6. [Monitoring & Logs](#monitoring--logs)
7. [Troubleshooting](#troubleshooting)
8. [Custom Domain (Optional)](#custom-domain-optional)
9. [Updating Your Deployment](#updating-your-deployment)

---

## Prerequisites

Before deploying, ensure you have:

- [ ] GitHub account with this repository pushed
- [ ] Streamlit Cloud account (free at https://streamlit.io/cloud)
- [ ] Anthropic API key (get one at https://console.anthropic.com/)
- [ ] Git repository is public or Streamlit has access to private repos

**Time Required**: 5-10 minutes for first deployment

---

## Quick Start

**If you just want to deploy quickly:**

1. Push your code to GitHub
2. Go to https://share.streamlit.io/
3. Sign in with GitHub
4. Click "New app"
5. Select repository: `scs_mediator_sdk_v2`
6. Main file path: `src/scs_mediator_sdk/ui/multiplayer_app.py`
7. Add secret: `ANTHROPIC_API_KEY = "sk-ant-api03-..."`
8. Click "Deploy"

Done! Your app will be live in ~2 minutes at a URL like: `https://your-username-scs-mediator-sdk.streamlit.app`

**Continue reading for detailed instructions and best practices.**

---

## Detailed Setup Steps

### Step 1: Push Code to GitHub

If you haven't already pushed your code to GitHub:

```bash
cd /home/dk/scs_mediator_sdk_v2

# Initialize git (if not already done)
git init

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/scs_mediator_sdk_v2.git

# Add all files
git add .

# Commit
git commit -m "Prepare for Streamlit Cloud deployment"

# Push to main branch
git push -u origin main
```

**Important**: Ensure `.gitignore` excludes `.streamlit/secrets.toml` to protect your API keys (already configured).

### Step 2: Create Streamlit Cloud Account

1. Go to https://streamlit.io/cloud
2. Click **"Sign up"**
3. Sign up with your GitHub account
4. Authorize Streamlit to access your GitHub repositories

### Step 3: Deploy Your App

1. **From Streamlit Cloud Dashboard**:
   - Click **"New app"** button (top right)

2. **Configure Deployment**:
   ```
   Repository: your-username/scs_mediator_sdk_v2
   Branch: main
   Main file path: src/scs_mediator_sdk/ui/multiplayer_app.py
   ```

3. **Advanced Settings** (click to expand):
   - **Python version**: 3.10 or 3.11 (recommended)
   - **Custom subdomain**: Choose a memorable name (e.g., `scs-mediator`)
   - Your app URL will be: `https://scs-mediator.streamlit.app`

4. **Click "Deploy"**

Streamlit will now:
- Clone your repository
- Install dependencies from `requirements.txt`
- Start your application
- Assign a public URL

**Deployment time**: ~2-3 minutes for first deployment.

---

## Configuration

### App Configuration (.streamlit/config.toml)

Your app is already configured with optimal settings in `.streamlit/config.toml`:

```toml
[server]
headless = true          # Run without GUI (cloud environment)
port = 8501              # Standard Streamlit port
enableCORS = false       # CORS handled by Streamlit Cloud
enableXsrfProtection = true  # Security enabled

[browser]
gatherUsageStats = false  # Privacy-friendly
serverAddress = "0.0.0.0"  # Listen on all interfaces

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true   # Helpful for debugging
toolbarMode = "minimal"   # Clean UI
```

**No changes needed** - these settings are optimized for Streamlit Cloud.

### Requirements (requirements.txt)

Your dependencies are already configured. Streamlit Cloud will automatically install:

- Core: `streamlit>=1.36.0`, `fastapi>=0.115.0`
- Simulation: `mesa>=2.2.0`, `numpy>=1.26.0`, `pandas>=2.2.0`
- AI: `anthropic>=0.18.0`
- Visualization: `plotly>=5.18.0`, `matplotlib>=3.8.0`

**All dependencies are pinned for reproducible builds.**

---

## Secrets Management

### Why Secrets?

Your app requires an `ANTHROPIC_API_KEY` for AI Guide features. **Never commit API keys to git.**

### Adding Secrets to Streamlit Cloud

**Method 1: Web Interface (Recommended)**

1. Go to your app dashboard: https://share.streamlit.io/
2. Click on your app
3. Click ⚙️ **"Settings"** (top right)
4. Select **"Secrets"** tab
5. Paste the following (replace with your actual API key):

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-your-actual-key-here"
```

6. Click **"Save"**
7. Your app will automatically restart with the new secret

**Method 2: TOML File (Local Development)**

For local development, create `.streamlit/secrets.toml`:

```bash
# Copy template
cp .streamlit/secrets.toml.template .streamlit/secrets.toml

# Edit and add your API key
nano .streamlit/secrets.toml
```

Add:
```toml
ANTHROPIC_API_KEY = "sk-ant-api03-your-actual-key-here"
```

**Important**: This file is already excluded from git via `.gitignore`.

### Accessing Secrets in Code

Your app already uses this pattern:

```python
import streamlit as st

# Access secrets (works both locally and on Streamlit Cloud)
api_key = st.secrets.get("ANTHROPIC_API_KEY", "")

if not api_key:
    st.warning("⚠️ ANTHROPIC_API_KEY not configured. AI Guide features will be disabled.")
```

### Getting an Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **"Create Key"**
5. Copy the key (starts with `sk-ant-api03-`)
6. Store it securely

**Free Tier**: Anthropic offers $5 in free credits for new accounts.

---

## Monitoring & Logs

### Viewing Logs

**Real-time Logs**:
1. Go to your app dashboard
2. Click **"Manage app"** → **"Logs"**
3. View live logs and errors

**Log Levels**:
- ✅ **Info**: Normal operation (session created, simulation run)
- ⚠️ **Warning**: Non-critical issues (API key missing, player disconnected)
- ❌ **Error**: Critical failures (simulation crash, database error)

### Health Monitoring

Streamlit Cloud provides:
- **Uptime monitoring**: Automatic health checks every 60 seconds
- **Auto-restart**: Crashes trigger automatic restart
- **Resource usage**: CPU and memory metrics in dashboard

**App Hibernation**: Free tier apps sleep after 7 days of inactivity. They wake up automatically when accessed.

### Performance Metrics

Track in your app dashboard:
- **Viewers**: Current active sessions
- **Total views**: Historical traffic
- **Errors**: Error rate and types
- **Response time**: Average page load

---

## Troubleshooting

### Issue: App Won't Deploy

**Symptoms**: Deployment fails with error message

**Solutions**:
1. **Check requirements.txt**:
   ```bash
   # Verify all dependencies are pinned
   grep ">=" requirements.txt
   ```

2. **Check Python version**:
   - Streamlit Cloud supports Python 3.8-3.11
   - Recommended: 3.10 or 3.11

3. **Check main file path**:
   - Must be: `src/scs_mediator_sdk/ui/multiplayer_app.py`
   - Not: `multiplayer_app.py` (incorrect)

4. **View deployment logs**:
   - Click app → "Manage app" → "Logs"
   - Look for import errors or missing dependencies

### Issue: AI Guide Not Working

**Symptoms**: AI features show warning "API key not configured"

**Solution**:
1. Verify secret is set:
   - Go to app settings → Secrets
   - Ensure `ANTHROPIC_API_KEY = "sk-ant-..."` is present

2. **Restart app**:
   - Click "Reboot app" to reload secrets

3. **Test API key**:
   ```python
   # Test in Python
   import anthropic
   client = anthropic.Anthropic(api_key="your-key")
   message = client.messages.create(
       model="claude-sonnet-4-5-20250929",
       max_tokens=100,
       messages=[{"role": "user", "content": "Hello"}]
   )
   print(message.content)
   ```

### Issue: App is Slow

**Symptoms**: Long load times, timeout errors

**Solutions**:
1. **Check resource limits** (Free tier):
   - 1 GB RAM
   - 1 CPU core
   - If exceeded, consider upgrading to Team plan

2. **Optimize session state**:
   - Reduce cached data size
   - Clear old sessions

3. **Profile your code**:
   ```python
   import time
   start = time.time()
   # Your code here
   print(f"Took {time.time() - start:.2f}s")
   ```

### Issue: Session Codes Not Working

**Symptoms**: Players can't join sessions, "Session not found" errors

**Cause**: In-memory storage is reset on app restart (free tier)

**Solutions**:
1. **Short-term**: Players must join during same session
2. **Long-term**: Upgrade to persistent storage (PostgreSQL)

**Note**: This is expected behavior for MVP deployment. For production, see ENGINEERING_DOCUMENTATION.md for database setup.

### Issue: App Shows "Sleeping"

**Symptoms**: App shows "This app has gone to sleep" message

**Cause**: Free tier apps hibernate after 7 days of inactivity

**Solution**:
- Just access the URL - it wakes up automatically in ~30 seconds
- Or upgrade to Team plan for always-on deployment

---

## Custom Domain (Optional)

### Using Your Own Domain

**Free Tier**: Not available
**Team Plan ($20/month)**: Custom domains supported

**Steps** (Team plan only):
1. Go to app settings → **"Domains"**
2. Click **"Add custom domain"**
3. Enter your domain: `negotiations.your-domain.com`
4. Add DNS records (provided by Streamlit):
   ```
   CNAME: negotiations → your-app.streamlit.app
   ```
5. Wait for DNS propagation (5-60 minutes)
6. SSL certificate is auto-configured

### Free Alternative: Use Streamlit Subdomain

Choose a memorable subdomain during deployment:
- `scs-mediator.streamlit.app`
- `maritime-negotiations.streamlit.app`
- `crisis-simulation.streamlit.app`

**Tip**: Keep it short, descriptive, and professional.

---

## Updating Your Deployment

### Automatic Updates (Recommended)

Streamlit Cloud automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "feat: add new scenario"
git push

# Streamlit Cloud detects the push and redeploys automatically
```

**Redeployment time**: ~1-2 minutes

### Manual Reboot

Force a restart without code changes:
1. Go to app dashboard
2. Click **"Manage app"** → **"Reboot app"**
3. Confirm

**Use cases**:
- Update secrets
- Clear cached data
- Recover from stuck state

### Rollback to Previous Version

1. Go to app settings → **"Advanced"**
2. Click **"Rerun"** on a specific git commit
3. Or revert in git:
   ```bash
   git revert HEAD
   git push
   ```

---

## Best Practices

### Security

- ✅ **Never commit secrets**: Use `.streamlit/secrets.toml` (already in `.gitignore`)
- ✅ **Use environment-specific secrets**: Different keys for dev/prod
- ✅ **Rotate API keys**: Regenerate keys every 90 days
- ✅ **Monitor API usage**: Check Anthropic dashboard for unusual activity

### Performance

- ✅ **Use caching**: Streamlit's `@st.cache_data` for expensive computations
- ✅ **Minimize session state**: Only store essential data
- ✅ **Optimize imports**: Import libraries only when needed
- ✅ **Profile regularly**: Identify bottlenecks with timing decorators

### Reliability

- ✅ **Test locally first**: Always test changes locally before deploying
- ✅ **Use git tags**: Tag releases for easy rollback (`git tag v1.0.0`)
- ✅ **Monitor errors**: Check logs daily for new issues
- ✅ **Have a rollback plan**: Know how to revert to last working version

### User Experience

- ✅ **Show loading states**: Use `st.spinner()` for long operations
- ✅ **Handle errors gracefully**: Try/except with user-friendly messages
- ✅ **Provide feedback**: Success messages and error guidance
- ✅ **Test on mobile**: Streamlit apps work on mobile browsers

---

## Cost Considerations

### Free Tier (Recommended for Testing)

**Includes**:
- ✅ 1 public app
- ✅ 1 GB RAM, 1 CPU core
- ✅ Community support
- ✅ Streamlit subdomain
- ⚠️ App hibernates after 7 days inactivity
- ⚠️ Deployment queue during peak times

**Best for**:
- Academic demos
- Proof of concepts
- Class exercises (low concurrency)

### Team Plan ($20/month per user)

**Includes**:
- ✅ Unlimited apps
- ✅ 4 GB RAM, 2 CPU cores
- ✅ Always-on (no hibernation)
- ✅ Custom domains
- ✅ Priority support
- ✅ Private apps (password-protected)
- ✅ Team collaboration

**Best for**:
- Production deployments
- Professional training
- Research projects
- High-concurrency use

### Enterprise Plan (Contact Streamlit)

**Includes**: Everything in Team, plus:
- Custom resource limits
- SSO integration
- SLA guarantees
- Dedicated support
- On-premise deployment option

---

## Sharing Your App

### Public Link

After deployment, share your app URL:
```
https://your-app-name.streamlit.app
```

**Tips**:
- Include in research papers
- Add to course syllabi
- Share on social media
- Link from your GitHub README

### Embed in Website (Team Plan)

```html
<iframe
  src="https://your-app-name.streamlit.app/?embed=true"
  width="100%"
  height="600"
  frameborder="0">
</iframe>
```

### QR Code for Workshops

Generate a QR code pointing to your app:
- Use https://qr-code-generator.com/
- Print on handouts
- Display on slides

---

## Next Steps

After successful deployment:

1. **Test All Features**:
   - [ ] Create facilitator session
   - [ ] Join as multiple players
   - [ ] Submit proposals and responses
   - [ ] Run simulation
   - [ ] Test AI Guide
   - [ ] Execute strategic actions

2. **Share with Users**:
   - [ ] Send link to collaborators
   - [ ] Add to course materials
   - [ ] Update GitHub README with live demo link

3. **Monitor & Iterate**:
   - [ ] Check logs for errors
   - [ ] Collect user feedback
   - [ ] Plan improvements

4. **Consider Upgrades** (if needed):
   - [ ] Custom domain for professional branding
   - [ ] Team plan for always-on availability
   - [ ] Database for persistent sessions

---

## Support Resources

### Official Documentation

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-cloud
- **Streamlit API Reference**: https://docs.streamlit.io/library/api-reference
- **Anthropic API Docs**: https://docs.anthropic.com/

### Community Support

- **Streamlit Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: https://github.com/streamlit/streamlit/issues
- **Discord**: https://discord.gg/streamlit

### Project-Specific Help

For issues specific to this project:
- See **MULTIPLAYER_USER_GUIDE.md** for app usage
- See **MULTIPLAYER_TESTING_GUIDE.md** for testing
- See **ENGINEERING_DOCUMENTATION.md** for technical details

---

## Frequently Asked Questions

**Q: Can I deploy multiple apps from the same repo?**
A: Yes! Create multiple apps with different main file paths:
- `src/scs_mediator_sdk/ui/multiplayer_app.py` (multiplayer)
- `src/scs_mediator_sdk/ui/enhanced_multi_view.py` (single-player)

**Q: How long does deployment take?**
A: 2-3 minutes for first deployment, ~1 minute for updates.

**Q: Can students access the app for free?**
A: Yes! Free tier allows unlimited viewers/users. Only the deployer needs a Streamlit account.

**Q: What happens if I exceed resource limits?**
A: App may slow down or show "Out of memory" errors. Solution: Upgrade to Team plan.

**Q: Can I password-protect my app?**
A: Yes, with Team plan or above. Free tier apps are always public.

**Q: How do I delete my app?**
A: App dashboard → Settings → "Delete app" (bottom of page).

**Q: Can I use a different port?**
A: No, Streamlit Cloud always uses port 8501. This is handled automatically.

---

## Conclusion

**You're now ready to deploy!** 🚀

**Quick checklist**:
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed with correct file path
- [ ] ANTHROPIC_API_KEY secret configured
- [ ] All features tested
- [ ] Link shared with users

**Estimated time to first deployment**: 5-10 minutes

**Enjoy your publicly accessible South China Sea maritime negotiation simulator!**

---

**Last Updated**: 2025-01-09
**Version**: 1.0
**Deployment Method**: Streamlit Cloud (Free Tier)
