import sys

from pymetheus.ui.app import PymetheusApp

app = PymetheusApp()

if __name__ == "__main__":
    app.run()
    sys.exit(app.return_code or 0)
