# Page build scripts

`fees.html`, `team.html` and `services.html` are generated. Edit the content in these scripts, not in the HTML, then rebuild:

```
python3 tools/build_fees.py
python3 tools/build_team.py
python3 tools/build_services.py
```

- `build_page.py` wraps each page in the shared site chrome (emergency banner, header, mobile menu and bottom bar, footer) taken from `request-appointment.html`. Change the chrome there and rebuild to update all three pages.
- `build_services.py` reuses the service icons from the homepage tiles in `index.html`.
- `build_team.py` holds the staff list. Bios are empty until SWIFT supplies them; fill in the last field of each entry. Photos live in `brand_assets/team/`.
