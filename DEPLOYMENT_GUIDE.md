# Deployment Guide - A/B Testing Setup

This guide explains how to deploy both versions of the SCS Mediator SDK to Streamlit Cloud for A/B testing.

## Two Versions Available

### Version 1: Production (Stable)
- **Entry point**: `src/scs_mediator_sdk/ui/enhanced_multi_view.py`
- **Features**: Full mediation simulation, bargaining engine, strategic levers
- **Status**: Stable, production-ready
- **Current deployment**: https://galatea-coder-m-srcscs-mediator-sdkuienhanced-multi-view-wenbd2.streamlit.app/

### Version 2: Validation (Experimental)
- **Entry point**: `streamlit_app_validation.py`
- **Features**: Everything from Version 1 PLUS model validation tools
- **Status**: Experimental, for research and A/B testing
- **New features**:
  - Model Validation tab
  - Quick validation check (10 simulations)
  - Interactive sensitivity analysis
  - Historical validation comparison
  - Model documentation and references

## Deploying to Streamlit Cloud

### Option A: Deploy BOTH Versions (Recommended for A/B Testing)

#### Deploy Production Version:
1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select repository: `Galatea-coder/Mediation_Tool_SCS`
4. Branch: `master`
5. **Main file path**: `src/scs_mediator_sdk/ui/enhanced_multi_view.py`
6. App URL (custom): `scs-mediator-stable` (or your choice)
7. Click "Deploy"

#### Deploy Validation Version:
1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select repository: `Galatea-coder/Mediation_Tool_SCS`
4. Branch: `master`
5. **Main file path**: `streamlit_app_validation.py`
6. App URL (custom): `scs-mediator-validation` (or your choice)
7. Click "Deploy"

Now you have TWO separate apps for A/B testing!

### Option B: Update Existing App to Validation Version

If you want to replace your current app with the validation version:

1. Go to your app dashboard: https://share.streamlit.io/
2. Find your existing app
3. Click "⋮" → "Settings"
4. Under "Main file path", change to: `streamlit_app_validation.py`
5. Click "Save"
6. App will automatically redeploy

## Testing Locally

### Test Production Version:
```bash
streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py
```

### Test Validation Version:
```bash
streamlit run streamlit_app_validation.py
```

Or directly:
```bash
streamlit run src/scs_mediator_sdk/ui/validation_multi_view.py
```

## Environment Variables

Both versions require the same environment variables:

- `ANTHROPIC_API_KEY`: Your Anthropic API key for AI features

Configure in Streamlit Cloud:
1. Go to app settings
2. Click "Secrets"
3. Add:
```toml
ANTHROPIC_API_KEY = "your-key-here"
```

## A/B Testing Strategy

### Scenario 1: Internal Testing
- **Stable version**: Share with all users
- **Validation version**: Share only with instructors/researchers
- Collect feedback on validation features

### Scenario 2: Gradual Rollout
- **Week 1-2**: Validation version to 20% of users
- **Week 3-4**: Expand to 50% if positive feedback
- **Week 5+**: Full rollout if validated

### Scenario 3: Parallel Deployment
- **Stable**: Default for all training sessions
- **Validation**: Optional "Advanced Features" version
- Users choose which version to use

## Monitoring & Comparison

Track these metrics for each version:

1. **Usage**: Number of sessions, time per session
2. **Features**: Which tabs are used most
3. **Feedback**: User satisfaction scores
4. **Performance**: Load times, simulation times
5. **Errors**: Any crashes or issues

## Key Differences Between Versions

| Feature | Production | Validation |
|---------|-----------|------------|
| Mediation Simulation | ✅ | ✅ |
| Bargaining Engine | ✅ | ✅ |
| Strategic Levers | ✅ | ✅ |
| Peace Context | ✅ | ✅ |
| AI Guide | ✅ | ✅ |
| **Model Validation Tab** | ❌ | ✅ |
| **Historical Comparison** | ❌ | ✅ |
| **Sensitivity Analysis** | ❌ | ✅ |
| **Model Documentation** | ❌ | ✅ |

## Rollback Plan

If validation version has issues:

1. Revert app to production version:
   - Change main file path back to `src/scs_mediator_sdk/ui/enhanced_multi_view.py`

2. Or create hotfix:
   ```bash
   git revert <commit-hash>
   git push origin master
   ```

## Support & Documentation

- **Production docs**: `docs/USER_GUIDE.md`
- **Validation docs**: `docs/MODEL_ASSUMPTIONS_AND_VALIDATION.md`
- **API docs**: `docs/API_DOCUMENTATION.md`

## Questions?

Review the documentation in `docs/` or check the code comments in:
- `src/scs_mediator_sdk/ui/enhanced_multi_view.py` (production)
- `src/scs_mediator_sdk/ui/validation_multi_view.py` (validation)

---

**Last Updated**: January 2025
**Version**: 9.0.0
