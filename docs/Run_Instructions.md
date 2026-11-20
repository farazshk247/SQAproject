# Running the Front End and Back End

## 1. Requirements

The following are required to run the project:

- Git
- Python 3
- C++17 compiler (g++ or clang++)
- Visual Studio Code (recommended)
- Windows: WSL 2 with Ubuntu
- Linux: Ubuntu or another compatible Linux distribution
- macOS: Apple Command Line Tools

Repository: https://github.com/farazshk247/SQAproject.git

## 2. Windows (WSL + Ubuntu)

### Step 1: Install WSL and Ubuntu

Open PowerShell:

```powershell
wsl --install -d Ubuntu
```

Follow the instructions to set up Ubuntu.

Launch Ubuntu:

```powershell
wsl -d Ubuntu
```

### Step 2: Install dependencies

Run inside Ubuntu:

```bash
sudo apt update
sudo apt install -y git g++ python3
```

### Step 3: Open the repository

Clone the repository:

```bash
git clone https://github.com/farazshk247/SQAproject.git
cd SQAproject
```


### Step 4: Compile

```bash
g++ -std=c++17 front_end/*.cpp -o frontend_phase4_linux
```

Verify compilation:

```bash
echo $?
ls -l frontend_phase4_linux
```

If the result is 0 it compiled successfully.

Continue to section 5.

## 3. Linux (Ubuntu)

### Step 1: Install dependencies

```bash
sudo apt update
sudo apt install -y git g++ python3
```

### Step 2: Clone the repository

```bash
git clone https://github.com/farazshk247/SQAproject.git
cd SQAproject
```

### Step 3: Compile

```bash
g++ -std=c++17 front_end/*.cpp -o frontend_phase4_linux
```

Verify compilation:

```bash
echo $?
ls -l frontend_phase4_linux
```

If the result is 0 it compiled successfully.

Continue to section 5.

## 4. macOS

### Step 1: Install dependencies

Install Apple Command Line Tools:

```bash
xcode-select --install
```

Ensure Python 3 and Git are installed:

```bash
python3 --version
git --version
clang++ --version
```

### Step 2: Clone the repository

```bash
git clone https://github.com/farazshk247/SQAproject.git
cd SQAproject
```

### Step 3: Compile

```bash
clang++ -std=c++17 front_end/*.cpp -o frontend_phase4_linux
```

Verify compilation:

```bash
echo $?
ls -l frontend_phase4_linux
```

If the result is 0 it compiled successfully.

Continue to section 5.

## 5. Running the Programs

The following commands work on Linux, Windows WSL/Ubuntu, and macOS.

Run all commands from the root of SQAproject.

### Step 1: Create sample input files

```bash
mkdir -p /tmp/sqa_phase4_test
```

Create an account file:

```bash
printf 'admin           AA 000100.00\nmanager         AM 000000.00\nEND\n' > /tmp/sqa_phase4_test/accounts.txt
```

Create the games file:

```bash
printf 'END\n' > /tmp/sqa_phase4_test/games.txt
```

Create the collection file:

```bash
printf 'END\n' > /tmp/sqa_phase4_test/collection.txt
```

### Step 2: Run the Front End

```bash
./frontend_phase4_linux \
/tmp/sqa_phase4_test/accounts.txt \
/tmp/sqa_phase4_test/games.txt \
/tmp/sqa_phase4_test/collection.txt \
/tmp/sqa_phase4_test/daily.txt
```

The Front End reads commands from standard input.

For example, enter these commands one at a time:

```text
login
manager
create
testuser
FS
logout
```

### Step 3: Check the Daily Transaction File

```bash
cat /tmp/sqa_phase4_test/daily.txt
```

Expected output:

```text
01 testuser        FS 000000.00
00                    000000000
```

### Step 4: Run the Back End

```bash
python3 back_end/main.py \
/tmp/sqa_phase4_test/accounts.txt \
/tmp/sqa_phase4_test/games.txt \
/tmp/sqa_phase4_test/collection.txt \
/tmp/sqa_phase4_test/daily.txt \
/tmp/sqa_phase4_test/new_accounts.txt \
/tmp/sqa_phase4_test/new_games.txt \
/tmp/sqa_phase4_test/new_collection.txt
```

### Step 5: Check the Back End Output

View the updated accounts:

```bash
cat /tmp/sqa_phase4_test/new_accounts.txt
```

Expected output:

```text
admin           AA 000100.00
manager         AM 000000.00
testuser        FS 000000.00
END
```

View the updated games:

```bash
cat /tmp/sqa_phase4_test/new_games.txt
```

View the updated collection:

```bash
cat /tmp/sqa_phase4_test/new_collection.txt
```

Both files should contain their respective END records for the empty sample inputs.

## 6. Running Again

To compile the Front End again:

**Linux / Windows WSL:**

```bash
g++ -std=c++17 front_end/*.cpp -o frontend_phase4_linux
```

**macOS:**

```bash
clang++ -std=c++17 front_end/*.cpp -o frontend_phase4_linux
```

To start another Front End session:

```bash
./frontend_phase4_linux \
/tmp/sqa_phase4_test/accounts.txt \
/tmp/sqa_phase4_test/games.txt \
/tmp/sqa_phase4_test/collection.txt \
/tmp/sqa_phase4_test/daily.txt
```

To run the Back End again:

```bash
python3 back_end/main.py \
/tmp/sqa_phase4_test/accounts.txt \
/tmp/sqa_phase4_test/games.txt \
/tmp/sqa_phase4_test/collection.txt \
/tmp/sqa_phase4_test/daily.txt \
/tmp/sqa_phase4_test/new_accounts.txt \
/tmp/sqa_phase4_test/new_games.txt \
/tmp/sqa_phase4_test/new_collection.txt
```
