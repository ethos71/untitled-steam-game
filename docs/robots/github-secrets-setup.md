# GitHub Secrets Setup for Steam Deployment

## Required Secrets

To enable automated Steam deployment, configure these secrets in your GitHub repository.

### Navigation
1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

### Secrets to Add

#### `STEAM_USERNAME`
- Your Steamworks build account username
- **NOT your personal Steam account**
- Create a dedicated build account in Steamworks

#### `STEAM_PASSWORD`
- Password for your Steamworks build account
- Consider using Steam Guard with shared secret for automation

#### `STEAM_APP_ID`
- Your game's App ID from Steamworks
- Found in your Steamworks dashboard
- Example: `480` (Spacewar, the test app)

#### `STEAM_DEPOT_ID`
- Your depot ID for the base game
- Found in Steamworks under App Admin → Depots
- You may have multiple depots (one per platform)

#### `STEAM_CONFIG_VDF` (Optional)
- Pre-configured Steam config file
- Used for authentication with Steam Guard
- Base64-encoded content of config.vdf

## Creating a Build Account

1. **Create New Steamworks Account**
   - Go to your Steamworks partner page
   - Users & Permissions → Manage Users
   - Add new user with build permissions only

2. **Grant Permissions**
   - Edit App Metadata
   - Publish App Changes To Steam
   - Edit Steamworks Settings

3. **Setup Steam Guard**
   - Enable Steam Guard on build account
   - For automation, use shared secret method
   - Store shared secret securely

## Security Best Practices

- ✅ Use a dedicated build account (not your personal account)
- ✅ Grant minimum required permissions
- ✅ Rotate passwords periodically
- ✅ Monitor build account activity
- ✅ Use encrypted secrets (GitHub handles this automatically)
- ❌ Never commit credentials to repository
- ❌ Never share secrets in logs or output

## Testing Secrets

After adding secrets, trigger the workflow:
```bash
git tag v0.0.1-test
git push --tags
```

Check the Actions tab to verify the deployment workflow runs successfully.

---
*Created: 2025-12-18*
