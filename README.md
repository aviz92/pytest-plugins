# pytest-plugins
An advanced pytest plugin designed for Python projects, offering robust features and utilities to enhance the testing workflow. <br>
It includes improved `conftest.py` fixtures, automated test result reporting, detailed logging, and seamless integration with external tools for a streamlined and efficient testing experience.

---

## 🚀 Features
- ✅ **`better-report`**: Enhanced test result tracking and structured JSON reporting.
- ✅ **`maxfail-streak`**: Stop test execution after a configurable number of consecutive failures.
- ✅ **`fail2skip`**: Change failing tests to skipped, allowing for better test management and reporting.

---

## 📦 Installation
```bash
pip install pytest-plugins
```

---

### 🔧 Usage
- pytest-better-report
  - pytest --better-report
  - pytest --better-report --pr-number=123
- pytest-maxfail-streak
  - pytest --maxfail-streak=3
    - for using without a streak, use the built-in `--maxfail` option
- pytest-fail2skip
  - pytest --fail2skip # must add `@pytest.mark.fail2skip` decorator to the test function

or use the `pytest.ini` configuration file to set default values for these plugins.

```ini
[pytest]
addopts = --better-report --pr-number=123 --maxfail-streak=3 --fail2skip
```

---

## 🤝 Contributing
If you have a helpful tool, pattern, or improvement to suggest:
Fork the repo <br>
Create a new branch <br>
Submit a pull request <br>
I welcome additions that promote clean, productive, and maintainable development. <br>

---

## 🙏 Thanks
Thanks for exploring this repository! <br>
Happy coding! <br>
