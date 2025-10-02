# 🚀 Welcome to **vicmil-pip**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)
![Status](https://img.shields.io/badge/status-active-success)
![Made with ❤️ for C++](https://img.shields.io/badge/made%20with-%E2%9D%A4-red)

> **vicmil-pip** is your lightweight, cross-platform package manager for **C++ libraries** — designed to feel as simple and familiar as Python’s `pip`, but built for modern C++ developers.

---

## ✨ Features

- 📦 **Local-only installs** → no clutter, no root access needed
- ⚡ **Wide library support** across Windows, Linux, and macOS
- 🛠 Comes with **utility helpers** for easy integration
- 🔒 **Self-contained**: lives entirely inside `vicmil_pip/`
- 🎯 Perfect for **rapid prototyping** _and_ production builds

---

## 🏁 Getting Started

Setting up **vicmil-pip** takes just a minute!

### 1️⃣ Create the entry file

```bash
touch vicmil-pip.py
```

### 2️⃣ Install the latest version

Paste this into `vimcil-pip.py` and run it:

```python
# Bootstrap installer for vicmil-pip
import urllib.request

with urllib.request.urlopen(
    'https://raw.githubusercontent.com/vicmil-pip-v2/vicmil-pip/refs/heads/main/vicmil-pip.py'
) as f:
    code = f.read().decode('utf-8')
    with open(__file__, "w") as this_file:
        this_file.write(code)
```

### 3️⃣ Explore commands

```bash
python3 vicmil-pip.py help
```

That’s it! 🎉 You now have `vicmil-pip` ready to go.

---

## 📚 Usage Examples

✅ **Install a package**

```bash
python3 vicmil-pip.py install some_packagename
```

📦 **List all available packages**

```bash
python3 vicmil-pip.py packages
```

🗑 **Uninstall a package**

```bash
python3 vicmil-pip.py remove some_packagename
```

---

## 🗂 How it Works (Under the Hood)

- Packages are installed inside a local **`vicmil_pip/`** folder
- Libraries live in `vicmil_venv/lib/` → totally isolated
- Safe by design: nothing global is modified
- Works the same way across **Windows, Linux, macOS**
- All packages use **permissive licenses** → friendly for commercial use

---

## 🔧 Manual Installation (Optional)

Prefer doing things by hand? You can:

1. Navigate to your desired package inside [vicmil-pip-v2](https://github.com/orgs/vicmil-pip-v2/repositories)

2. Extract it into:

   ```
   vicmil_pip/lib/<package-name>
   ```

3. If present, run `setup.py` or check `vicmil_requirements.txt` for dependencies

---

## 💡 Tips & Notes

- 💾 Works great in **git repos** → commit `vicmil-pip.py` + `vicmil_pip/`
- 🌍 Share your `vicmil-pip_requirements.txt` with teammates for reproducible builds
- 🛡 No `sudo` / root required — keep your system clean
- 🔧 Extendable: you can even publish your own C++ packages for others to use!

---

## 🚀 Quickstart Command

🔥 When in doubt, just run:

```bash
python3 vicmil-pip.py help
```

And let **vicmil-pip** guide you from there.
