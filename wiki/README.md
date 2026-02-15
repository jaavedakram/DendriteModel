# Wiki Content for GitHub

This directory contains markdown files for the GitHub Wiki.

## How to Use

### Option 1: GitHub Wiki (Recommended)

1. Go to your repository: https://github.com/jaavedakram/DendriteModel
2. Click the **Wiki** tab
3. Create/edit pages and copy content from these files:

   - `Home.md` → Wiki Home page
   - `Theory.md` → Create "Theory" page
   - `Configuration.md` → Create "Configuration" page
   - `Examples.md` → Create "Examples" page
   - `Troubleshooting.md` → Create "Troubleshooting" page

### Option 2: Clone Wiki Repository

GitHub wikis are separate git repositories:

```bash
git clone https://github.com/jaavedakram/DendriteModel.wiki.git
cd DendriteModel.wiki

# Copy files
cp ../wiki/*.md .

# Commit and push
git add .
git commit -m "Add comprehensive documentation"
git push origin master
```

## Wiki Files

| File | Purpose |
|------|---------|
| `Home.md` | Wiki landing page with navigation |
| `Theory.md` | Governing equations and physics |
| `Configuration.md` | Parameter reference and examples |
| `Examples.md` | Tutorials and use cases |
| `Troubleshooting.md` | Common issues and solutions |

## Updating Wiki

When you make changes to documentation:

1. Edit files in this `wiki/` directory
2. Commit to main repository
3. Copy updated content to GitHub Wiki (manual or via git)

## Note

These files are kept in the main repository for version control and easy editing. The GitHub Wiki is the public-facing documentation.
