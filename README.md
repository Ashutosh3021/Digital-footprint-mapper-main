# 🔍 Digital Footprint Mapper

> **Making the invisible visible** — See your digital shadow before others do.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OSINT](https://img.shields.io/badge/OSINT-Ethical-green.svg)](https://en.wikipedia.org/wiki/Open-source_intelligence)

## 🌐 What Is This?

**Digital Footprint Mapper (DFM)** is an OSINT-powered intelligence system that reveals how much of your digital identity is publicly exposed across the internet. Like holding up a mirror to your online presence, DFM collects scattered public data from GitHub (and potentially Twitter, LinkedIn, Reddit) and weaves it into a visual intelligence graph that shows exactly what investigators, recruiters, or attackers could learn about you.

Think of it as your personal privacy audit tool — because **you can't protect what you can't see**.

---

## ✨ Key Features

### 🎯 **GitHub Intelligence Gathering**
- Extracts public profile data: name, bio, location, company, followers
- Maps repository ownership and collaboration patterns
- Analyzes commit messages and code for accidentally exposed secrets
- Identifies API keys, tokens, passwords, and credentials hiding in plain sight

### 🕸️ **Intelligence Graph Engine**
- Builds a NetworkX-powered relationship graph of all discovered entities
- Connects usernames, emails, organizations, repositories, and risk nodes
- Labels relationships with semantic edges: "has_email", "works_for", "contains_sensitive_data"
- Transforms fragmented data into a coherent identity picture

### 📊 **Interactive Visualization**
- Generates beautiful, color-coded network graphs
- Highlights high-risk elements (suspected secrets) in bold red
- Uses intuitive icons and sizing to differentiate entity types
- Exports to image formats or interactive HTML views

### 🛡️ **Ethical OSINT Approach**
- Operates exclusively on publicly accessible information
- Educates users about their digital exposure
- Designed as a defensive tool, not an exploitation engine
- Emphasizes privacy awareness and responsible disclosure

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/digital-footprint-mapper.git
cd digital-footprint-mapper

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run the prototype
python main_prototype.py

# Enter a GitHub username when prompted
# Sit back and watch your digital footprint unfold
```

### Example Output

```
🔍 Analyzing GitHub footprint for: octocat
✓ Profile retrieved: 50 followers, 12 repositories
✓ Scanning repositories for sensitive data...
⚠️ Found 3 potential secrets in commit history
✓ Building intelligence graph with 28 nodes
✓ Visualization saved: octocat_footprint.png
```

---

## 🏗️ Architecture

```
┌─────────────────┐
│  GitHub Scraper │ ──> Collects public profile & repo data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Secret Scanner  │ ──> Detects exposed credentials & keys
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Intelligence    │ ──> Models entities & relationships
│     Graph       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Visualization  │ ──> Interactive risk map
└─────────────────┘
```

---

## 🎨 Visual Intelligence

DFM transforms raw data into intuitive visual insights:

- **🔵 Blue nodes**: User profiles and identities
- **🟢 Green nodes**: Repositories and projects
- **🟡 Yellow nodes**: Organizations and affiliations
- **🔴 Red nodes**: Suspected sensitive data (HIGH RISK)
- **Edges**: Labeled relationships showing how everything connects

The result? A map that shows what you thought was private scattered across the internet, now connected and visible.

---

## 🧩 Modules

### `github_scraper.py`
Queries GitHub's API to extract profile data, repository metadata, and commit history. Scans code and messages for regex patterns matching API keys, tokens, and other secrets.

### `intelligence_graph.py`
Implements the NetworkX graph structure. Adds nodes for users, emails, locations, organizations, and repositories. Creates edges with semantic labels to represent relationships.

### `main_prototype.py`
Orchestrates the full pipeline: prompts for input, retrieves data, builds the graph, generates visualizations, and narrates each step in plain language.

---

## 🔐 Security & Ethics

**Important**: This tool is designed for:
- ✅ Personal privacy audits
- ✅ Security awareness education
- ✅ OSINT training and research
- ✅ Helping developers find and fix exposed secrets

**Not intended for**:
- ❌ Unauthorized surveillance
- ❌ Stalking or harassment
- ❌ Credential theft or exploitation
- ❌ Any malicious activity

**Remember**: With great power comes great responsibility. Use this tool ethically and legally.

---

## 🛣️ Roadmap

- [ ] Multi-platform support (Twitter, LinkedIn, Reddit)
- [ ] Real-time monitoring and alerts
- [ ] Machine learning for risk scoring
- [ ] Browser extension for on-the-fly analysis
- [ ] Collaborative team privacy audits
- [ ] Integration with security scanning tools

---

## 🤝 Contributing

We welcome contributions! Whether it's:
- 🐛 Bug reports and fixes
- 💡 Feature suggestions
- 📝 Documentation improvements
- 🎨 Visualization enhancements

Please open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:
- NetworkX for graph modeling
- Matplotlib for visualizations
- GitHub API for data collection
- The OSINT community for inspiration

---

## 💬 Support

Have questions? Found a bug? Want to discuss OSINT techniques?

- 📧 Email: ashutoshpatraybl@gmail.com
- 💬 Issues: [GitHub Issues](https://github.com/Ashutosh3021/digital-footprint-mapper/issues)

---

<div align="center">

**Remember**: Your digital footprint is bigger than you think.  
**Know it. Own it. Protect it.**

⭐ Star this repo if DFM helped you discover something about your online presence!

</div>
