# 🔄 Render Service Update Guide

## **Updating Existing Render Service with MCP Tools**

### **Pre-Update Checklist**
- [ ] All changes committed to GitHub
- [ ] `requirements.txt` includes new dependencies
- [ ] `app_production.py` uses MCP tools
- [ ] Deployment tests passed locally

### **Update Steps**

#### **Option A: Auto-Deploy (Easiest)**
1. **Push changes to GitHub:**
   ```bash
   git add .
   git commit -m "Add MCP tools integration"
   git push origin main
   ```

2. **Wait for automatic deployment:**
   - Render detects changes
   - Rebuilds with new dependencies
   - Deploys updated app
   - Same URL, enhanced features!

#### **Option B: Manual Deploy**
1. **Go to Render Dashboard**
2. **Select your Wildlife Insight Agent service**
3. **Click "Manual Deploy"**
4. **Select "Deploy latest commit"**
5. **Wait for build and deployment**

### **Verify Update Success**

#### **Check Build Logs:**
Look for these in your Render build logs:
```
Installing collected packages: ... mcp, streamlit, plotly, pandas, python-dotenv
Successfully installed ...
```

#### **Check Runtime Logs:**
Look for successful startup:
```
You can now view your Streamlit app in your browser.
Network URL: http://0.0.0.0:$PORT
```

#### **Test Your App:**
Visit your existing URL and verify:
- [ ] App loads successfully
- [ ] Species search works
- [ ] New climate data section appears (if API key set)
- [ ] Technical details show MCP tools
- [ ] No error messages

### **Environment Variables (Optional)**

To enable full AI functionality:

1. **In Render Dashboard:**
   - Go to your service
   - Click "Environment" tab
   - Click "Add Environment Variable"

2. **Add API Key:**
   - **Key:** `GEMINI_API_KEY`
   - **Value:** Your actual Gemini API key
   - Click "Save Changes"

3. **Service will restart automatically**

### **Troubleshooting Update Issues**

#### **Build Fails:**
- Check build logs for dependency errors
- Verify `requirements.txt` syntax
- Ensure all files are committed

#### **Import Errors:**
- Check that `tools/` directory is in repository
- Verify MCP tool files are present
- Check Python import paths

#### **Runtime Errors:**
- Check service logs in Render dashboard
- Verify environment variables if using full mode
- Test locally first: `streamlit run app_production.py`

### **Rollback if Needed**

If something goes wrong:

1. **Quick Rollback:**
   - In Render dashboard
   - Go to "Deploys" tab
   - Click "Redeploy" on previous working version

2. **Fix and Redeploy:**
   - Fix issues locally
   - Test with `python final_deployment_test.py`
   - Push fixes and redeploy

### **Expected Results After Update**

#### **Demo Mode (No API Key):**
- Species data via MCP tools
- Enhanced visualizations
- Better error handling
- Technical details showing MCP usage

#### **Full Mode (With API Key):**
- Complete AI analysis pipeline
- Species + climate data correlation
- CrewAI multi-agent processing
- Comprehensive reports

### **Update Benefits**

✅ **Same URL** - No need to change bookmarks or links
✅ **Enhanced Features** - MCP tools integration
✅ **Better Performance** - Improved error handling
✅ **Climate Data** - New environmental insights
✅ **Production Ready** - Robust deployment configuration

### **Post-Update Verification**

Test these features on your updated service:

1. **Basic Functionality:**
   - [ ] App loads without errors
   - [ ] Species selection works
   - [ ] Search returns results

2. **New MCP Features:**
   - [ ] Species data fetched via MCP tools
   - [ ] Technical details show MCP tool usage
   - [ ] Error handling works gracefully

3. **Enhanced UI:**
   - [ ] Climate data section (if API key set)
   - [ ] Improved visualizations
   - [ ] Better technical details

### **Success Indicators**

Your update is successful when:
- ✅ App loads at existing URL
- ✅ All features work as before
- ✅ New MCP integration active
- ✅ No error messages in logs
- ✅ Enhanced functionality available

## 🎉 **Update Complete!**

Your existing Render service now has:
- MCP tools integration
- Enhanced functionality
- Better error handling
- Climate data support
- Same reliable URL

**Your users will automatically get the enhanced experience!** 🌟