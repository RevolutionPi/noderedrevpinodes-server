SHELL        := bash
MAKEFLAGS     = --no-print-directory --no-builtin-rules
.DEFAULT_GOAL = all

# Variables
PACKAGE       = noderedrevpinodes_server
APP_NAME      = noderedrevpinodes-server
APP_IDENT     = com.revolutionpi.noderedrevpinodes_server

# Python interpreter to use for venv creation
SYSTEM_PYTHON = python3

# Set path to create the virtual environment with package name
ifdef PYTHON3_VENV
VENV_PATH = $(PYTHON3_VENV)/$(PACKAGE)
else
VENV_PATH = venv
endif

# Set targets for "all"-target
all: test build
.PHONY: all

## Virtual environment creation with SYSTEM_PYTHON
venv:
	# Start with empty environment
	"$(SYSTEM_PYTHON)" -m venv "$(VENV_PATH)"
	"$(VENV_PATH)/bin/pip" install --upgrade pip
	"$(VENV_PATH)/bin/pip" install --upgrade -r requirements.txt

venv-ssp:
	# Include system installed site-packages and add just missing modules
	"$(SYSTEM_PYTHON)" -m venv --system-site-packages "$(VENV_PATH)"
	"$(VENV_PATH)/bin/pip" install --upgrade pip
	"$(VENV_PATH)/bin/pip" install --upgrade -r requirements.txt

.PHONY: venv venv-ssp

# Choose python interpreter from venv or system
PYTHON = $(or $(wildcard $(VENV_PATH)/bin/python), $(SYSTEM_PYTHON))

# Read app version from program
APP_VERSION = $(shell "$(PYTHON)" src/$(PACKAGE) --version | cut -d ' ' -f 2)

# Environment info
venv-info:
	@echo Environment for $(APP_NAME) $(APP_VERSION)
	@echo Using path: "$(VENV_PATH)"

.PHONY: venv-info

## Build steps
test:
	PYTHONPATH=src "$(PYTHON)" -m pytest

build:
	"$(PYTHON)" -m setup sdist
	"$(PYTHON)" -m setup bdist_wheel

install: build
	"$(PYTHON)" -m pip install dist/$(PACKAGE)-$(APP_VERSION)-*.whl

uninstall:
	"$(PYTHON)" -m pip uninstall --yes $(PACKAGE)

.PHONY: test build install uninstall

## PyInstaller
app-licenses:
	mkdir -p dist
	# Create a list of all installed libraries, their versions and licenses
	"$(PYTHON)" -m piplicenses \
		--format=markdown \
		--output-file dist/bundled-libraries.md
	# Create a list of installed libraries with complete project information
	"$(PYTHON)" -m piplicenses \
		--with-authors \
		--with-urls \
		--with-description \
		--with-license-file \
		--no-license-path \
		--format=json \
		--output-file dist/open-source-licenses.json
	"$(PYTHON)" -m piplicenses \
		--with-authors \
		--with-urls \
		--with-description \
		--with-license-file \
		--no-license-path \
		--format=plain-vertical \
		--output-file dist/open-source-licenses.txt

app: app-licenses
	"$(PYTHON)" -m PyInstaller -n $(APP_NAME) \
		--add-data="dist/bundled-libraries.md:$(PACKAGE)/open-source-licenses" \
		--add-data="dist/open-source-licenses.*:$(PACKAGE)/open-source-licenses" \
		--noconfirm \
		--clean \
		--onefile \
		src/$(PACKAGE)/__main__.py

.PHONY: app-licenses app

## Clean
clean:
	# PyTest caches
	rm -rf .pytest_cache
	# Build artifacts
	rm -rf build dist src/*.egg-info
	# PyInstaller created files
	rm -rf *.spec
	# Pycaches
	find . -type d -name '__pycache__' -exec rm -r {} \+

distclean: clean
	# Virtual environment
	rm -rf "$(VENV_PATH)"

.PHONY: clean distclean
