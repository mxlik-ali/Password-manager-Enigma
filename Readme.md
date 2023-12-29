
# Password Manager CLI


- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
  - [Linux](#linux)
    - [Install Python Requirements](#install-python-requirements)
    - [MariaDB Installation](#mariadb-installation)
    - [Pyperclip](#pyperclip)
  - [Windows](#windows)
    - [Install Python Requirements](#install-python-requirements-1)
    - [MariaDB Installation](#mariadb-installation-1)
- [Configuration](#configuration)
- [Usage](#usage)
- [Further Information](#further-information)

A secure command-line password manager that encrypts and manages passwords using AES-256 encryption. This tool provides functionalities to add, retrieve, and manage passwords securely.

## Overview

Password Manager CLI is designed to offer a secure environment for storing and managing passwords. It utilizes strong encryption techniques to safeguard sensitive data while providing an easy-to-use command-line interface for interaction.

## Features

- **Secure Storage:** Utilizes AES-256 encryption for password encryption.
- **Command-Line Interface:** User-friendly CLI for managing passwords.
- **Password Generation:** Generates strong, random passwords combining alphabets, numbers, and special characters.
- **Clipboard Support:** Allows automatic copying of passwords to the clipboard for convenience.

## Installation

### Linux

#### Install Python Requirements

```bash
sudo apt install python3-pip
pip install -r requirements.txt
```

#### MariaDB Installation

Follow these steps to install MariaDB on Linux:

1. Import the key:

    ```bash
    sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
    ```

2. Add repository:

    ```bash
    sudo add-apt-repository 'deb http://ftp.osuosl.org/pub/mariadb/repo/5.5/ubuntuprecise main'
    ```

3. Update and install:

    ```bash
    sudo apt-get update
    sudo apt-get install mariadb-server
    ```

#### Pyperclip

If encountering a "not implemented error" with Pyperclip, refer to the [fix](https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error) provided.

### Windows

#### Install Python Requirements

```bash
pip install -r requirements.txt
```

#### MariaDB Installation

Follow the instructions [here](https://www.mariadbtutorial.com/getting-started/install-mariadb/) to install MariaDB on Windows.
#### Create user and grant privileges
- Navigate to MariaDB bin directory
```
C:\Program Files\MariaDB\bin
```
- Login as root with the password you chose while installation
```
mysql.exe -u root -p
```
- Create user
```
CREATE USER 'pm'@localhost IDENTIFIED BY 'password';
```
- Grant privileges
```
GRANT ALL PRIVILEGES ON *.* TO 'pm'@localhost IDENTIFIED BY 'password';
```

## Configuration

Run the configuration script to set up the password manager:

- **Create Configuration:**

    ```bash
    python config.py make
    ```

    This command creates a new configuration, prompts for choosing a MASTER PASSWORD, generating the DEVICE SECRET, and creates the necessary database and tables.

- **Delete Configuration:**

    ```bash
    python config.py delete
    ```

    This command deletes the existing configuration, including the device secret and all entries, irreversibly losing all passwords. Be cautious!

- **Remake Configuration:**

    ```bash
    python config.py remake
    ```

    This command deletes the existing configuration and recreates it, prompting for a new MASTER PASSWORD, generating a new DEVICE SECRET, and setting up the database and tables.

## Usage

```bash
# Add new entry
password-cli add -n "example.com" -u "https://example.com" -e "user@example.com" -p "mysecretpassword"

# Get entry
password-cli get -n "example.com" --with-password
```

## Further Information

- [Pyperclip](https://pypi.org/project/pyperclip/): Python module for copying data to the clipboard.
- [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2): Key derivation function used for creating a 256-bit key.
- [AES-256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard): Encryption standard used for secure storage and retrieval of passwords.

This README file consolidates all the provided information about the Password Manager CLI, including installation steps, configuration details, usage examples, and additional resources for further reference. Feel free to modify or enhance it according to your specific project needs.