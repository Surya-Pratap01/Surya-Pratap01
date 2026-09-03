# Setup

1. Push this folder to the public special repository `Surya-Pratap01/Surya-Pratap01`.
2. GitHub → Settings → Actions → General → Workflow permissions → **Read and write permissions**.
3. Create a GitHub personal access token with the minimum access needed for profile metrics and save it as repository secret **METRICS_TOKEN**. Never share the token.
4. Open Actions and manually run:
   - `Refresh profile charts and cards`
   - `Refresh profile metrics`
   - `Generate contribution snake`
5. The snake workflow creates the `output` branch. Its README image can therefore be unavailable until that first run succeeds.
6. Check the profile in both dark/light mode and on mobile.

The package includes local SVG fallbacks, so the stat areas are not empty before Actions are configured.
