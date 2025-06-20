# pytest-plugins
An advanced pytest plugin designed for Python projects, offering robust features and utilities to enhance the testing workflow. <br>
It includes improved `conftest.py` fixtures, automated test result reporting, detailed logging, and seamless integration with external tools for a streamlined and efficient testing experience.

---

## Features
- ✅ **`pytest-better-report`**: Enhanced test result tracking and structured JSON reporting.
- ✅ **`pytest-maxfail-streak`**: Stop test execution after a configurable number of consecutive failures.

---

### 🔧 Usage
- pytest-better-report
  - pytest --better-report-enable
  - pytest --better-report-enable --pr-number=123
- pytest-maxfail-streak
  - pytest --maxfail-streak-enable --maxfail-streak=3

or use the `pytest.ini` configuration file to set default values for these plugins.

```ini
[pytest]
addopts = --better-report-enable --maxfail-streak-enable --maxfail-streak=3
```

or 

```ini
[pytest]
addopts = --better-report-enable --pr-number=123 --maxfail-streak-enable --maxfail-streak=3
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
