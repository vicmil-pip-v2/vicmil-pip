# 🚀 Welcome to **vizpip**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)
![Status](https://img.shields.io/badge/status-active-success)
![Made with ❤️ for C++](https://img.shields.io/badge/made%20with-%E2%9D%A4-red)

> **vizpip** is your lightweight, cross-platform package manager for **C++ libraries** — designed to feel as simple and familiar as Python’s `pip`, but built for modern C++ developers.

---

## ✨ Features

- 📦 **Local-only installs** → no clutter, no root access needed
- ⚡ **Wide library support** across Windows, Linux, and macOS
- 🛠 Comes with **utility helpers** for easy integration
- 🔒 **Self-contained**: lives entirely inside `vizpip_venv/`
- 🎯 Perfect for **rapid prototyping** _and_ production builds

---

## 🏁 Getting Started

Setting up **vizpip** takes just a minute!

### 1️⃣ Create the entry file

```bash
touch vizpip.py
```

### 2️⃣ Install the latest version

Paste this into `vizpip.py` and run it:

```python
# Bootstrap installer for vizpip
import urllib.request

with urllib.request.urlopen(
    'https://raw.githubusercontent.com/vizpip/vizpip/refs/heads/main/vizpip.py'
) as f:
    code = f.read().decode('utf-8')
    with open(__file__, "w") as this_file:
        this_file.write(code)
```

### 3️⃣ Explore commands

```bash
python3 vizpip.py help
```

That’s it! 🎉 You now have `vizpip` ready to go.

---

## 📚 Usage Examples

✅ **Install a package**

```bash
python3 vizpip.py install some_packagename
```

📦 **List all available packages**

```bash
python3 vizpip.py packages
```

🔍 **Search for a package**

```bash
python3 vizpip.py search regex_pattern
```

🗑 **Uninstall a package**

```bash
python3 vizpip.py uninstall some_packagename
```

---

## 🗂 How it Works (Under the Hood)

- Packages are installed inside a local **`vizpip_venv/`** folder
- Libraries live in `vizpip_venv/lib/` → totally isolated
- Safe by design: nothing global is modified
- Works the same way across **Windows, Linux, macOS**
- All packages use **permissive licenses** → friendly for commercial use

---

## 🔧 Manual Installation (Optional)

Prefer doing things by hand? You can:

1. Navigate to your desired package inside `vizpip`

2. Extract it into:

   ```
   vizpip_venv/lib/<package-name>
   ```

3. If present, run `setup.py` or check `vizpip_requirements.txt` for dependencies

---

## 💡 Tips & Notes

- 💾 Works great in **git repos** → commit `vizpip.py` + `vizpip_venv/`
- 🌍 Share your `vizpip_requirements.txt` with teammates for reproducible builds
- 🛡 No `sudo` / root required — keep your system clean
- 🔧 Extendable: you can even publish your own C++ packages for others to use!

---

## 🚀 Quickstart Command

🔥 When in doubt, just run:

```bash
python3 vizpip.py help
```

And let **vizpip** guide you from there.
