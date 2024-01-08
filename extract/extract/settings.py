from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=[".secrets.yaml", "settings.yaml"],
)
