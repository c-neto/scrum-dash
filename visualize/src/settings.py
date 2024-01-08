from dynaconf import Dynaconf

COLOR_CONTINUOUS_SCALE = [
    (0, "red"),
    (0.4, "red"),
    (0.6, "yellow"),
    (0.7, "yellow"),
    (0.9, "green"),
    (1, "green"),
]

settings = Dynaconf(settings_files=["settings.yaml", ".secrets.yaml"])
